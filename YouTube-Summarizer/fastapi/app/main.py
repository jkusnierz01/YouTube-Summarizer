import os
import tempfile
from fastapi import FastAPI, HTTPException
import whisper
from contextlib import asynccontextmanager
import uuid
import torch
from pyannote.audio import Pipeline
from pydub import AudioSegment
from typing import List

def load_whisper():
    model = whisper.load_model("base")
    return model

def load_diarization_pipeline():
    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token = os.environ['HUGGING_FACE_TOKEN']
        )
        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))
        return pipeline
    except KeyError:
        raise RuntimeError("Hugging Face token is missing!")
        # sys.exit(1)

ml_models = {}

@asynccontextmanager
async def lifespan(app:FastAPI):
    ml_models['whisper'] = load_whisper()
    ml_models['speaker_diarization'] = load_diarization_pipeline()
    yield
    ml_models.clear()
    

app = FastAPI(lifespan=lifespan)

transcription = {}


async def make_transcription(path: os.path) -> str:
    return ml_models["whisper"].transcribe(path)

def audio_preprocessing(path: os.path) -> None:
    audio = AudioSegment.from_wav(path)
    audio = audio.set_channels(1)
    audio.set_sample_rate(16000)
    audio.export(path, format = 'wav')


async def perform_diarization(path: os.path) -> List:
    audio_preprocessing()
    diarization = ml_models["speaker_diarization"].pipeline(path)
    speker_segment_list = []
    for segment,_,speaker in diarization.itertracks(yield_label=True):
        speker_segment_list.append([segment,speaker])
    return speker_segment_list

def match_diarization_transcript(transciption, diarization):
    
    

    

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
        transcript = await make_transcription(path)
        diarization = await perform_diarization(path)
        transcription[request_id] = transcript['text']
        return {"request_id": request_id}
    
        
        
        
    
