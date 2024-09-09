import os
import tempfile
from fastapi import FastAPI, HTTPException
import whisper
from contextlib import asynccontextmanager
import uuid

def load_model():
    model = whisper.load_model("base")
    return model

ml_models = {}

@asynccontextmanager
async def lifespan(app:FastAPI):
    ml_models['whisper'] = load_model()
    yield
    ml_models.clear()
    

app = FastAPI(lifespan=lifespan)

transcription = {}

@app.post("/process")
async def pipeline(url: str):
    request_id = str(uuid.uuid4())
    with tempfile.TemporaryDirectory() as fd:
        os.system(f"yt-dlp -x --audio-format wav -P {fd} -o audio.wav {url}")
        path = os.path.join(fd,"audio.wav")
        result = ml_models["whisper"].transcribe(path)
        transcription[request_id] = result['text']
        return {"request_id": request_id}
    
    
@app.get("/get_transcription")
async def get_transc(request_id:str):
    print(f"Received request_id: {request_id}")
    if request_id in transcription:
        result = transcription[request_id]
        return {"transcription": result}
    else:
        raise HTTPException(status_code=404, detail="RequestID is not found!")
        
        
        
    
