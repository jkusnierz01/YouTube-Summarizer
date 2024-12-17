import requests
import os
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from pydub.utils import mediainfo
import time
import pandas as pd
from requests import HTTPError
import json
import numpy as np


AUDIO_DIR = "/home/jedrzej_engineer/Desktop/audio/"
SUMMARY_DIR = "/home/jedrzej_engineer/Desktop/summary/"
TEXT_DIR = "/home/jedrzej_engineer/Desktop/text/"


def calculate_rouge_metric(generated_summ, reference_summ, test_case_numm):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(reference_summ, generated_summ)
    
    print(f"TEST CASE: {test_case_numm}")
    print(f"ROUGE-1: {rouge_scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-2: {rouge_scores['rouge2'].fmeasure:.4f}")
    print(f"ROUGE-L: {rouge_scores['rougeL'].fmeasure:.4f}")
    
def calulate_bert_metric(filename:str):
    out_data = []
    with open(filename, 'r') as file:
        data = json.load(file)
    for idx, item in enumerate(data):
        precision, recall, f1 = bert_score([item['generated_summary']], [item['reference_summary']], lang='en', verbose=True)
        print(f1.numpy()[0])
        print(precision.numpy()[0])
        print(recall.numpy()[0])
        bert_score_dict = {
            'index':idx,
            'precision':str(precision.numpy()[0]),
            'recall':str(recall.numpy()[0]),
            'f1':str(f1.numpy()[0])
        }
        out_data.append(bert_score_dict)
    with open("bert_score_result2.json",'w') as file:
        json.dump(out_data, file)
    
def test():
    try:
        number_of_samples = 0
        data_list = []
        audio_files = sorted(os.listdir(AUDIO_DIR))
        summary_files = sorted(os.listdir(SUMMARY_DIR))
    except Exception as e:
        print(f"Exception: {e}")
    print(len(audio_files))
    print(len(summary_files))
    for idx, (audio_filename, summ_filename) in enumerate(zip(audio_files, summary_files)):
        try:
            if idx < 26:
                continue
            audio_full_path = os.path.join(AUDIO_DIR, audio_filename)
            summ_full_path = os.path.join(SUMMARY_DIR, summ_filename)
            audio_metadata = mediainfo(audio_full_path)
            duration = float(audio_metadata["duration"])
            with open(audio_full_path, "rb") as audio:
                files = {"file": (audio_full_path, audio, "audio/mpeg")}
                start = time.time()
                response_redirect = requests.post(
                        url=f"http://localhost:8080/test-endpoint/",
                        files=files
                        )
                end = time.time()
                if response_redirect.status_code == 200:
                    try:
                        response = response_redirect.json()
                    except ValueError:
                        print("Invalid JSON response")
                        continue
                    g_summary = response['summary']
                    stenogram = response['data_to_prompt']
                    transcript = response['transcription']
                    with open(summ_full_path, 'r') as file:
                        ref_summ = file.read()
                    audio_duration = round(duration,2)
                    calc_time = round((end-start),2)
                    print(f"Audio duration: {audio_duration} | Calculated time: {calc_time}")
                    # calulate_bert_metric(g_summary, ref_summ, idx, data_list)
                    iteration_data = {
                        'index': idx,
                        'filename': audio_full_path,
                        'generated_summary':g_summary,
                        'reference_summary':ref_summ,
                        # 'stenogram': stenogram,
                        # 'transcription': transcript,
                        'audio_duration' : audio_duration,
                        'calculation_time':calc_time,
                    }
                    data_list.append(iteration_data)
                    number_of_samples += 1
                else:
                    print(f"{response_redirect.status_code} : {response_redirect.json().get('detail','Other')}")
        except Exception as e:
            print(f"Exception: {e}")
            continue
    with open("addition2_summary_test_results.json", 'w') as file:
        json.dump(data_list, file, indent=4)
    # df=pd.DataFrame(data=data_list, columns=['IDX', 'Generated Summary', 'Ground Truth Summary', 'Audio Duration', 'Exec Time'])
    # df.to_csv("bert-test-result.csv")
    

if __name__ == "__main__":
    calulate_bert_metric("summary_test_results.json")