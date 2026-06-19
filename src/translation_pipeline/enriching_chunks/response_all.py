from src.translation_pipeline.prompts.system_prompt import SYSTEM_PROMPT
from src.translation_pipeline.prompts.user_prompt import build_prompt

import time
from tqdm import tqdm
 
from openai import OpenAI
from getpass import getpass

import re
import json



def parse_json_response(result):

    match = re.search(
        r'```json\s*(.*?)\s*```',
        result,
        flags=re.DOTALL
    )

    if match:
        result = match.group(1)

    return json.loads(result)


def enrich_all_chunks(chunks, save_path="rag_chunks.jsonl"):

    DEEPSEEK_API_KEY = getpass("Enter DeepSeek API Key: ")

    client = OpenAI(
        api_key = DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )

    enriched_chunks = []

    for i, chunk in enumerate(tqdm(chunks)):

        # Skip if already processed (resume support)
        if "question_en" in chunk and chunk["question_en"]:
            enriched_chunks.append(chunk)
            continue

        retries = 3

        for attempt in range(retries):

            try:

                prompt = build_prompt(
                    chunk["question_te"],
                    chunk["answer_te"]
                )

                response = client.chat.completions.create(
                    model="deepseek-chat",
                    temperature=0.1,
                    messages=[
                        {
                            "role": "system",
                            "content": SYSTEM_PROMPT
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = response.choices[0].message.content
                parsed = parse_json_response(result)

                # merge original + model output
                chunk.update(parsed)

                enriched_chunks.append(chunk)

                break  # success → exit retry loop

            except Exception as e:

                print(f"Error in chunk {i}, attempt {attempt+1}: {e}")

                time.sleep(2)

                if attempt == retries - 1:
                    print(f"Skipping chunk {i}")
                    enriched_chunks.append(chunk)

        # checkpoint save every 10 chunks
        if i % 10 == 0:

            with open(save_path, "w", encoding="utf-8") as f:
                for c in enriched_chunks:
                    f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # final save
    with open(save_path, "w", encoding="utf-8") as f:
        for c in enriched_chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    return enriched_chunks