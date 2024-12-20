import os
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile
from contextlib import asynccontextmanager
import uuid
from diarization import perform_diarization, calculate_iou, get_text_for_llm_prepared, create_speaker_sentences, match_diarization_to_transcript
from transcription import make_transcription, make_whisperx_transcription
from models import load_whisper, load_diarization, load_whisperx, load_aligner
from llm import request_llm
from typing import List, Tuple
from pyannote.core.segment import Segment
from utils import setup_logging, save_prompt_data
import logging
import whisperx
import torch
import tempfile
import shutil
from pydantic import BaseModel

ml_models = {}
summarization = {}

setup_logging("backend-service",log_file = 'backend.log')
logger = logging.getLogger(__name__)

class ProcessRequest(BaseModel):
    url: str


@asynccontextmanager
async def lifespan(app:FastAPI):
    
    logger.info(f"torch.cuda.is_available(): {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info("GPU AVAILABLE")
        ml_models['whisper'] = load_whisperx()
        ml_models['align_model'], ml_models['align_metadata'] = load_aligner()
    else:
        logger.info("CPU AVAILABLE")
        ml_models['whisper'] = load_whisper()
    ml_models['speaker_diarization'] = load_diarization()
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


def match_diarization_and_transcription(transcription_list: List[Segment], diariazation_list: List[Tuple[Segment,str]], transcription:dict)-> str:
    full_output = []
    for trans_id, transcription_segment in enumerate(transcription_list):
        for diar_id, diarization_element in enumerate(diariazation_list):
            diarization_segment, speaker = diarization_element
            iou = calculate_iou(transcription_segment, diarization_segment)
            if iou > 0.1:
                sentence = create_speaker_sentences(transcription['segments'][trans_id], diarization_segment)
                full_output.append([sentence, speaker])

    return get_text_for_llm_prepared(full_output)
    

@app.get("/get_summary")
async def get_summary(request_id:str):
    print(f"Received request_id: {request_id}")
    if request_id in summarization:
        result = summarization[request_id]
        return {"transcription": result}
    else:
        raise HTTPException(status_code=404, detail="RequestID is not found!")

@app.post("/process")
async def pipeline(request: ProcessRequest):
    url = request.url
    request_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as fd:
        os.system(f"yt-dlp -x --audio-format wav -P {fd} -o audio.wav {url}")
        path = os.path.join(fd,"audio.wav")
        if torch.cuda.is_available():
            device = "cuda"
            audio = whisperx.load_audio(path)
            
            transcription = make_whisperx_transcription(
                audio, 
                ml_models["whisper"], 
                ml_models['align_model'], 
                ml_models['align_metadata'], 
                device
            )
            
            if not transcription:
                raise HTTPException(
                    status_code=400, 
                    detail="Transcription failed. Ensure the video language matches the model's supported languages."
                )
            
            diarization = perform_diarization(path, ml_models["speaker_diarization"])
            
            data_to_prompt = match_diarization_to_transcript(diarization, transcription)
            if not data_to_prompt:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to match diarization to transcription."
                )
        else:
            transcription_list, transcription = make_transcription(path, ml_models["whisper"])
            diarization_list = perform_diarization(path, ml_models["speaker_diarization"])
            data_to_prompt = match_diarization_and_transcription(transcription_list, diarization_list, transcription)
        if save_prompt_data(data_to_prompt, transcription):
            logger.info("Saved prompt to results directory!")
        summary = request_llm(data_to_prompt)
        summarization[request_id] = summary
        return {"request_id": request_id}


@app.post("/test-endpoint")
async def test_endpoint(file: UploadFile):
        device = "cuda"
        
        fd, tmp_file = tempfile.mkstemp(".wav")
        os.close(fd)
        with open(tmp_file, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        audio = whisperx.load_audio(tmp_file)
        
        transcription = make_whisperx_transcription(
            audio, 
            ml_models["whisper"], 
            ml_models['align_model'], 
            ml_models['align_metadata'], 
            device
        )
        
        if not transcription:
            raise HTTPException(
                status_code=400, 
                detail="Transcription failed. Ensure the video language matches the model's supported languages."
            )
        
        diarization = perform_diarization(tmp_file, ml_models["speaker_diarization"])
        
        data_to_prompt = match_diarization_to_transcript(diarization, transcription)
        if not data_to_prompt:
            raise HTTPException(
                status_code=500, 
                detail="Failed to match diarization to transcription."
            )
        summary = request_llm(data_to_prompt)
        return {"summary": summary, 'data_to_prompt':data_to_prompt, 'transcription':transcription}