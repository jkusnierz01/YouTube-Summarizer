import os
import tempfile
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uuid
from diarization import perform_diarization
from transcription import make_transcription
from models import load_whisper, load_diarization
from diarization import calculate_iou, get_text_for_llm_prepared, create_speaker_sentences
from llm import request_llm
from typing import List
from pyannote.core.segment import Segment


ml_models = {}

@asynccontextmanager
async def lifespan(app:FastAPI):
    ml_models['whisper'] = load_whisper()
    ml_models['speaker_diarization'] = load_diarization()
    yield
    ml_models.clear()
    

app = FastAPI(lifespan=lifespan)
transcription = {}



def match_diarization_and_transcription(transcription_list: List[Segment], diariazation_list: List[Segment,str], transcription:dict)-> str:
    full_output = []
    for trans_id, transcription_segment in enumerate(transcription_list):
        for diar_id, diarization_element in enumerate(diariazation_list):
            diarization_segment, speaker = diarization_element
            iou = calculate_iou(transcription_segment, diarization_segment)
            if iou > 0.1:
                sentence = create_speaker_sentences(transcription['segments'][trans_id], diarization_segment)
                full_output.append([sentence, speaker])

    return get_text_for_llm_prepared(full_output)
    

@app.get("/get_transcription")
async def get_transc(request_id:str):
    print(f"Received request_id: {request_id}")
    if request_id in transcription:
        result = transcription[request_id]
        return {"transcription": result}
    else:
        raise HTTPException(status_code=404, detail="RequestID is not found!")

@app.post("/process")
async def pipeline(url: str):
    request_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as fd:
        os.system(f"yt-dlp -x --audio-format wav -P {fd} -o audio.wav {url}")
        path = os.path.join(fd,"audio.wav")
        transcription_list, transcription = await make_transcription(path)
        diarization_list = await perform_diarization(path)
        data_to_prompt = match_diarization_and_transcription(transcription_list, diarization_list, transcription)
        llm_response = request_llm(data_to_prompt)
        # transcription[request_id] = transcript['text']
        # return {"request_id": request_id}
    
        
        
        
    
