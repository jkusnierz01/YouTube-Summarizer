import requests
import json
import logging
from fastapi import HTTPException
from typing import List

logger = logging.getLogger(__name__)


def create_prompt(stenogram:str) -> str:
    prompt = f"""
    ### Instructions:
    1) Write a **summary only** of the following dialogue under ###Input:.
    2) **Do not continue** the conversation or provide any additional dialogue.
    3) **Do not use** speaker names. They are used as an information for better undersanding of the conversation.

    ### Input:
    {stenogram}
    
    ### Summary:
    """
    return prompt

def create_final_prompt(stenogram:str) -> str:
    prompt = f"""
    ### Instructions:
    1) Based on part summaries under ###Input: **create summary**.
    2) **Do not continue** the conversation or provide any additional dialogue.

    ### Input:
    {stenogram}
    
    ### Summary:
    """
    return prompt

def split_data_into_chunks(stenogram:str) -> List[str]:
    chunk_len = 1400
    chunk_list = []
    start, end = 0, 0
    words = stenogram.split()
    nr_of_words = len(words)
    while start < nr_of_words:
        end += chunk_len
        chunk_list.append(' '.join(words[start:end]))
        start=end
    return chunk_list
        
    

def request_llm(speakers_transcription: str):
    logger.info(f"Starting request to LLM Server!")
    PROMPT = create_prompt(speakers_transcription)
    summarization_data = {'prompt': PROMPT, "n_predict":512, "max_tokens":1024, "temperature": 0.7}
    tokenize_data = {'content': speakers_transcription}
    header = {'Content-type': 'application/json'}
    try:
        tok_response = requests.post(
            url = "http://llm:7000/tokenize",
            headers = header,
            data=json.dumps(tokenize_data)
        )
    except Exception as e:
        logger.error(f"Error in LLM Server Request - Tokenize: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"LLM Server request error- Tokenize: {e}"
        )
    number_of_tokens = len(tok_response.json()['tokens'])
    
    
    #if the context is too long 
    if number_of_tokens > 4000:
        chunk_summaries_list = []
        chunks = split_data_into_chunks(speakers_transcription)
        for chunk in chunks:
            PROMPT = create_prompt(chunk)
            summarization_data = {'prompt': PROMPT, "n_predict":128, "temperature": 0.7}
            try:
                response = requests.post(
                    url = "http://llm:7000/completion",
                    headers = header,
                    data=json.dumps(summarization_data)
                )
            except Exception as e:
                logger.error(f"Error in LLM Server Request - Summarization: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"LLM Server request error- Summarization: {e}"
                )
            if response.status_code == 200:
                summ = response.json()['content']
                chunk_summaries_list.append(summ)
        chunk_summaries_concatinated = ''.join(chunk_summaries_list)
        PROMPT = create_final_prompt(chunk_summaries_concatinated)
        summarization_data = {'prompt': PROMPT, "n_predict":512, "max_tokens":1024, "temperature": 0.7}
    try:
        response = requests.post(
            url = "http://llm:7000/completion",
            headers = header,
            data=json.dumps(summarization_data)
        )
    except Exception as e:
        logger.error(f"Error in LLM Server Request - Summarization: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"LLM Server request error- Summarization: {e}"
        )
    else: 
        if response.status_code == 200:
            return response.json()['content']