import requests
import json
import logging

logger = logging.getLogger(__name__)


def create_prompt(transcription:str) -> str:
    prompt = f"""
    ### Instructions:
    1) Write a **summary only** of the following dialogue under ###Input:.
    2) **Do not continue** the conversation or provide any additional dialogue.
    3) **Do not use** speaker names. They are used as an information for better undersanding of the conversation.

    ### Input:
    {transcription}
    
    ### Summary:
    """
    return prompt


def request_llm(speakers_transcription: str):
    logger.info(f"Starting request to LLM Server!")
    PROMPT = create_prompt(speakers_transcription)
    data = {'prompt': PROMPT, "n_predict":128}
    header = {'Content-type': 'application/json'}
    try:
        response = requests.post(
            url = "http://llm:7000/completion",
            headers = header,
            data=json.dumps(data)
        )
    except Exception as e:
        logger.error(f"Error in LLM Server Request: {e}")
    else: 
        if response.status_code == 200:
            return response.json()['content']