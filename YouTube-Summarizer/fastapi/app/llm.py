import requests
import json




def request_llm(speakers_transcription: str):
    PROMPT = f"Based on provided transcription create short summary: {speakers_transcription}"
    data = {'prompt': PROMPT, "n_predict":128}
    header = {'Content-type': 'application/json'}
    response = requests.post(
        url = "http://0.0.0.0:8000/completion",
        headers = header,
        data=json.dumps(data)
    )
    print(response)
    print(response.json())