from src.pdf_parser import extract_pdf
from src.extraction_pipeline.chunk_creation import create_chunk, final_chunks

    
import re              
import json            
import openai          
import tqdm

from getpass import getpass
from openai import OpenAI

from src.translation_pipeline.prompts.system_prompt import SYSTEM_PROMPT
from src.translation_pipeline.prompts.user_prompt import build_prompt

from src.translation_pipeline.enriching_chunks.response_all import enrich_all_chunks, parse_json_response
from src.translation_pipeline.enriching_chunks.response_single import enrich_chunk

def main():
    print("Hello from genai-internship-assignment!")

    pdf_path = "./data/ramayana.pdf"

    pages_original = extract_pdf(pdf_path)

    starting_pages = pages_original[:7]
   
    
    all_index_lines = starting_pages[3]["text"].split("\n")[2:-1]  + starting_pages[4]["text"].split("\n")[0:-1]  + starting_pages[5]["text"].split("\n")[0:-1] + starting_pages[6]["text"].split("\n")[0:-1]

    #Preface
    about_text = starting_pages[1]["text"].replace("\n"," ")

    pages = pages_original[7:]
    print(pages[0])

    #Contains all the text
    full_text = ""

    for page in pages:
        full_text += page["text"] + " "

    #All lines is list of lines from the text
    all_lines = full_text.split("\n")


    sarg_idx = []
    for idx,i in enumerate(all_lines):
        if "సర్గలు" in i:
            sarg_idx.append(idx)


    # List of only sargalu
    sarg_list = []
    for i in sarg_idx:
        sarg_list.append(all_lines[i])


    all_text_sarg = []
    for i in range(len(sarg_idx) - 1):
        start_index = sarg_idx[i] + 2
        end_index = sarg_idx[i+1] - 2
        all_text_sarg.append(" ".join(all_lines[start_index:end_index]))

    if sarg_idx and sarg_idx[-1] < len(all_lines):
        all_text_sarg.append(" ".join(all_lines[sarg_idx[-1]:]))


    all_kanda = ["బాల	కాండము"] * 13 + ["అయోధా్	కాండము"] * 19 + ["అరణ్	కాండము"] * 14 + ["కిషకుంధా	కాండము"] * 12  + ["సుందరా	కాండము"] * 15 + ["యుదధి	కాండము"] * 26
    all_sarga = sarg_list
    all_adhyayamu = all_index_lines

    print(all_kanda)

    chunks = final_chunks(all_text_sarg, about_text, all_kanda, all_sarga, all_adhyayamu)
    print(chunks[0])


    enriched_chunks = enrich_all_chunks(chunks, save_path="rag_chunks.jsonl")
    #enriched_chunk = enrich_chunk(chunks[1])
    #print(enriched_chunk)
    #print(chunks[1])


if __name__ == "__main__":
    main()
