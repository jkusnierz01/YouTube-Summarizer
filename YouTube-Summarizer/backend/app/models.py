import whisper
import whisperx
import torch
from pyannote.audio import Pipeline
import os
import logging

logger = logging.getLogger(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_whisper():
    try:
        model = whisper.load_model("base")
        return model
    except Exception as e:
        print(e)
        raise

def load_whisperx():
    try:
        model_name = "medium.en"
        model = whisperx.load_model(model_name, device)
        return model
    except Exception as e:
        print(e)
        raise


def load_aligner():
    logger.info("Loading English alignment model")
    try:
        align_model, align_metadata = whisperx.load_align_model(language_code="en", device=device)
        return align_model, align_metadata
    except Exception as e:
        print(e)
        raise


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
    
    
