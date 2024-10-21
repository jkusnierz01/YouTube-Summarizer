import os
from pyannote.core.segment import Segment
from typing import List
import logging
from ctc_forced_aligner import (
    load_audio,
    generate_emissions,
    preprocess_text,
    get_alignments,
    get_spans,
    postprocess_results,
)
import torch


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
        
        
def make_whisperx_transcription(audio, model):
    logger.info("Starting transcription")
    try:
        transcription = model.transcribe(audio)
        logging.info(f"Transcription successful")
        return transcription
    except Exception as e:
        logger.error(f"Transcription unsuccessfull! {e}")
        
        
def trans_audio_alignment(alignment_model, alignment_tokenizer, audio, transcription):
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