import whisper
import torch
from pyannote.audio import Pipeline
import os

def load_whisper():
    model = whisper.load_model("base")
    return model



def load_diarization():
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