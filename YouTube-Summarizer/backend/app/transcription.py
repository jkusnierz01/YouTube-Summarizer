import os
from pyannote.core.segment import Segment
from typing import List
import logging
import torch
from whisperx.alignment import align


logger = logging.getLogger(__name__)

def make_transcription(path: os.path, model) -> List[Segment]:
    logger.info("Starting transcription")
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
        
        
def make_whisperx_transcription(audio, model, alignment_model, alignment_metadata, device):
    logger.info("Starting transcription with WhisperX")
    try:
        # Transcribe with WhisperX
        result = model.transcribe(audio)
        if result["language"] != 'en':
            logger.error("Non-English audio detected. Only English is supported.")
            return None
        # Since we're only handling English, we don't need to check the language code
        # Perform alignment using the preloaded English alignment model
        aligned_result = align(
            result["segments"], alignment_model, alignment_metadata, audio, device
        )
        logging.info("Transcription and alignment successful")
        return aligned_result
    except Exception as e:
        logger.error(f"Transcription unsuccessfull! {e}")
        
        