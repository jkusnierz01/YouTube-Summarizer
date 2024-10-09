from pydub import AudioSegment
from typing import List
from main import ml_models
import os
from pyannote.core.segment import Segment


def audio_preprocessing(path: os.path) -> None:
    """

    Args:
        path (os.path): _description_
    """    
    audio = AudioSegment.from_wav(path)
    audio = audio.set_channels(1)
    audio.set_sample_rate(16000)
    audio.export(path, format='wav')


async def perform_diarization(path: os.path) -> List[Segment,str]:
    """

    Args:
        path (os.path): _description_

    Returns:
        List[ Segment, str]: _description_
    
        Example:
        [[<Segment(0.0309687, 4.26659)>, 'SPEAKER_00'],...]
    """    
    # audio_preprocessing(path)
    diarization = ml_models["speaker_diarization"].pipeline(path)
    speaker_diar_list = []
    for segment, _, speaker in diarization.itertracks(yield_label=True):
        speaker_diar_list.append([segment, speaker])
    
    return speaker_diar_list


def calculate_iou(transcript_segment: Segment, diarization_segment: Segment) -> float:
    """ 
    This function calculates Intersection Over Union between Segments suggested by Whisper and Pyannote  

    Args:
        whisper_seg (Segment): _description_
        pyannote_seg (Segment): _description_

    Returns:
        float: Value represents how both segments were aligned
    """
    intersect_seg = transcript_segment.__and__(diarization_segment)
    total_seg = transcript_segment.__or__(diarization_segment)

    duration_intersect = intersect_seg.duration
    total_duration = total_seg.duration
    iou = duration_intersect / total_duration

    return iou


def create_speaker_sentences(transcript_segment: Segment, diarization_segment: Segment) -> List[str]:
    """
    We create sentences based on timestamps from speaker diarization pipeline.
    Due to word level timestamping provided by Whisper we can calculate closest "distance"
    from start and end proposed by speaker diarization Segment.
    
    Args:
        transcript_segment (Segment): _description_
        diarization_segment (Segment): _description_

    Returns:
        List[str]: 
        
        Example:
        ['Hello','world',...]
    """
    #just big numbers so we can find value closest to 0
    start_dist = 100
    end_dist = 100
    
    #we iterate over words in transcription segment
    for word in transcript_segment['words']:
        word_start = word['start']
        word_end = word['end']
        
        #calulating distance and finding min ones
        start_distance = abs(diarization_segment.start - word_start)
        end_distance = abs(diarization_segment.end - word_end)
        min_distance_start = min(start_dist, start_distance)
        min_distance_end = min(end_dist, end_distance)
        
        if min_distance_start < start_dist:
            start_dist = min_distance_start
            time_start = word_start
        if min_distance_end < end_dist:
            end_dist = min_distance_end
            time_end = word_end

    sentence = []

    #we iterate again to find words in the middle and create sentence related to
    #diarization speaker segment proposed
    for word in transcript_segment['words']:
        if word['start'] >= time_start and word['end'] <= time_end:
            sentence.append(word['word'])

    return sentence


def get_text_for_llm_prepared(sentences_list: List[List[str],str]) -> str:
    """

    Args:
        sentences_list (List[List[str],str]): 
        it looks like: [[['Hello','world'], 'Speaker 0'],...]
        List contains words related to certain speaker

    Returns:
        List[str]: 
        
        Example:
        "
        SPEAKER_00: ' Hello world!'
        SPEAKER_01: '...'
        "
    """    
    sentences = []
    previous_speaker = None
    text = ""
    
    #we iterate over lists containing list of words and speaker
    for index, elem in enumerate(sentences_list):
        speaker = elem[1]
        
        #if speaker changed we save text of previous one    
        if speaker != previous_speaker and previous_speaker is not None:
            out_str = f" {previous_speaker}: '{text}'"
            sentences.append(out_str)
            text = ""
        
        #then we get text of actual sentence
        t = " ".join(elem[0])
        text += t 
        previous_speaker = speaker

        #if last element we save current speaker and text
        #it is needed in cases were at least we have
        #2 the same speakers at the end
        if index == len(sentences_list) - 1:
            out_str = f" {previous_speaker}: '{text}'"
            sentences.append(out_str)
    full_text = "\n".join(sentences)    
    return full_text