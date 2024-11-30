import os
from pyannote.core.segment import Segment
from typing import List, Tuple, Dict
import logging
import numpy as np
from ctc_forced_aligner import (
    generate_emissions,
    preprocess_text,
    get_alignments,
    get_spans,
    postprocess_results,
)
import torch


logger = logging.getLogger(__name__)

def make_transcription(path: os.path, model) -> Tuple[List[Segment], Dict]:
    """
    Transcribes an audio file and returns a list of segments with timestamps.

    This function uses a given model to transcribe an audio file from the specified
    path. The model provides word-level timestamps, which are converted into 
    `Segment` objects representing the start and end times of each word.

    Args:
        path (os.path): The path to the audio file to be transcribed.
        model: The transcription model with a `transcribe` method that supports 
               word-level timestamps.

    Returns:
        List[Segment]: A list of `Segment` objects with start and end timestamps.
        dict: The complete transcription result containing additional details.
    """
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
        
        
def make_whisperx_transcription(audio: np.ndarray, model):
    """_summary_
    Transcribes an audio waveform using a WhisperX model.

    This function performs transcription on an audio waveform using a WhisperX 
    model and returns the transcription result, which includes the transcribed 
    text and word timestamps.

    Args:
        audio: The audio waveform to be transcribed.
        model: The WhisperX model with a `transcribe` method.

    Returns:
        dict: The transcription result, including transcribed text and word timestamps.
    """
    logger.info("Starting transcription")
    try:
        transcription = model.transcribe(audio)
        logging.info(f"Transcription successful")
        return transcription
    except Exception as e:
        logger.error(f"Transcription unsuccessfull! {e}")
        
        
def trans_audio_alignment(alignment_model, alignment_tokenizer, audio: np.ndarray, transcription) ->List:
    """_summary_
    Performs forced alignment on an audio waveform to generate word timestamps.

    This function uses a CTC-based alignment model to align transcribed text 
    with the audio waveform. It processes the audio and text, generates emissions, 
    and computes the alignment, returning word timestamps.

    Args:
        alignment_model: The model used to generate emissions for forced alignment.
        alignment_tokenizer: The tokenizer used for text preprocessing and decoding.
        audio: The audio waveform as a numpy array.
        transcription: The transcription result with segments and text.

    Returns:
        list: A list of word timestamps, each containing start and end times.
    """
    batch_size = 16,
    language = "eng"
    
    audio_waveform = (
        torch.from_numpy(audio)
        .to(alignment_model.dtype)
        .to(alignment_model.device)
    )
    segments = transcription['segments']
    text = "".join(segment['text'] for segment in segments).strip()

    emissions, stride = generate_emissions(alignment_model, audio_waveform, batch_size)

    tokens_starred, text_starred = preprocess_text(
        text,
        romanize=True,
        language=language,
    )

    segments, scores, blank_id = get_alignments(
        emissions,
        tokens_starred,
        alignment_tokenizer,
    )
    blank_id = alignment_tokenizer.convert_tokens_to_ids('<blank>')
    spans = get_spans(tokens_starred, segments, alignment_tokenizer.decode(blank_id))

    word_timestamps = postprocess_results(text_starred, spans, stride, scores)
    
    return word_timestamps