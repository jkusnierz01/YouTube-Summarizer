import os
import tempfile
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import uuid
from diarization import perform_diarization, calculate_iou, get_text_for_llm_prepared, create_speaker_sentences, match_diarization_to_transcript
from transcription import make_transcription, make_whisperx_transcription, trans_audio_alignment
from models import load_whisper, load_diarization, load_whisperx, load_alignment_model
from llm import request_llm
from typing import List, Tuple
from pyannote.core.segment import Segment
from utils import setup_logging
import logging
import whisperx
import torch

ml_models = {}
summarization = {}

setup_logging("backend-service",log_file = 'backend.log')
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app:FastAPI):
    if torch.cuda.is_available():
        ml_models['whisper'] = load_whisperx()
        ml_models['alignment_model'], ml_models['alignment_tokenizer'] = load_alignment_model()
    else:
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
    

@app.get("/get_transcription")
async def get_transc(request_id:str):
    print(f"Received request_id: {request_id}")
    if request_id in summarization:
        result = summarization[request_id]
        return {"transcription": result}
    else:
        raise HTTPException(status_code=404, detail="RequestID is not found!")

@app.post("/process")
async def pipeline(url: str):
    request_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as fd:
        os.system(f"yt-dlp -x --audio-format wav -P {fd} -o audio.wav {url}")
        path = os.path.join(fd,"audio.wav")
        if torch.cuda.is_available():
            audio = whisperx.load_audio(path)
            transcription = make_whisperx_transcription(audio, ml_models["whisper"])
            alignment = trans_audio_alignment(ml_models['alignment_model'], ml_models['alignment_tokenizer'], audio, transcription)
            diarization = perform_diarization(path, ml_models["speaker_diarization"])
            data_to_prompt = match_diarization_to_transcript(diarization, alignment)
        else:
            transcription_list, transcription = make_transcription(path, ml_models["whisper"])
            diarization_list = perform_diarization(path, ml_models["speaker_diarization"])
            data_to_prompt = match_diarization_and_transcription(transcription_list, diarization_list, transcription)
        summary = request_llm(data_to_prompt)
        summarization[request_id] = summary
        return {"request_id": request_id}

