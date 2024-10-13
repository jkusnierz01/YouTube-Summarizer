import os
from pyannote.core.segment import Segment
from typing import List
import logging


logger = logging.getLogger(__name__)

async def make_transcription(path: os.path, model) -> List[Segment]:
    logger.info("starting transcription")
    try:
        transcription = model.transcribe(path, word_timestamps = True)
        logging.info(f"Transcription successful")
        transcription_list = []
        for segment in transcription['segments']:
            seg = Segment(segment['start'], segment['end'])
            transcription_list.append(seg) #might be wrong
        logging.info(f"Returning transcription...")
        return transcription_list, transcription
    except Exception as e:
        logger.error(f"Transcription unsuccessfull! {e}")