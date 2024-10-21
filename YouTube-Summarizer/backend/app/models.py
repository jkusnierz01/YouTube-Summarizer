import whisper
import whisperx
import torch
from pyannote.audio import Pipeline
import os
from ctc_forced_aligner import load_alignment_model

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
        model_name = "medium"
        model = whisperx.load_model(model_name, device)
        return model
    except Exception as e:
        print(e)
        raise


def load_aligner():
    try:
        alignment_model, alignment_tokenizer = load_alignment_model(
            device,
            dtype=torch.float16 if device == "cuda" else torch.float32,
        )
        return alignment_model, alignment_tokenizer
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
    
    
