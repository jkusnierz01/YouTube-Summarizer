import os
from main import ml_models
from pyannote.core.segment import Segment
from typing import List


async def make_transcription(path: os.path) -> List[Segment]:
    transcription = ml_models["whisper"].transcribe(path, word_timestamps = True)
    transcription_list = []
    for segment in transcription['segments']:
        seg = Segment(segment.start, segment.end)
        transcription_list.append(seg) #might be wrong
    return transcription_list, transcription