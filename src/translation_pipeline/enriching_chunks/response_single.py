from src.translation_pipeline.prompts.system_prompt import SYSTEM_PROMPT
from src.translation_pipeline.prompts.user_prompt import build_prompt

from openai import OpenAI
from getpass import getpass

import re
import json

def enrich_chunk(chunk):
    
    DEEPSEEK_API_KEY = getpass("Enter DeepSeek API Key: ")

    prompt = build_prompt(
        chunk["question_te"],
        chunk["answer_te"]
    )

    client = OpenAI(
            api_key = DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
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


    match = re.search(
        r'```json\s*(.*?)\s*```',
        result,
        flags=re.DOTALL
    )

    if match:
        result = match.group(1)


    return json.loads(result)