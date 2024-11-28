import requests
import os
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from pydub.utils import mediainfo
import time
import pandas as pd
from requests import HTTPError

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
    
def calulate_bert_metric(generated_summ, reference_summ, test_case_numm, data_list):
    precision, recall, f1 = bert_score([generated_summ], [reference_summ], lang='en', verbose=True)
    data_list.append([test_case_numm, generated_summ, reference_summ, f1[0]])
    print(f"TEST CASE: {test_case_numm}")
    print(f"F1-score: {f1[0]}")
    
def test():
    try:
        data_list = []
        audio_files = sorted(os.listdir(AUDIO_DIR))
        summary_files = sorted(os.listdir(SUMMARY_DIR))
    except Exception as e:
        print(f"Exception: {e}")
    for idx, (audio_filename, summ_filename) in enumerate(zip(audio_files, summary_files)):
        try:
            audio_full_path = os.path.join(AUDIO_DIR, audio_filename)
            summ_full_path = os.path.join(SUMMARY_DIR, summ_filename)
            audio_metadata = mediainfo(audio_full_path)
            duration = float(audio_metadata["duration"])
            if duration > 20 * 60:
                continue
            with open(audio_full_path, "rb") as audio:
                files = {"file": (audio_full_path, audio, "audio/mpeg")}
                start = time.time()
                response_redirect = requests.post(
                        url=f"http://localhost:8080/test-endpoint/",
                        files=files
                        )
                end = time.time()
                if response_redirect.status_code == 200:
                    resonse = response_redirect.json()
                    g_summary = resonse['summary']
                    with open(summ_full_path, 'r') as file:
                        ref_summ = file.read()
                    print(f"Audio duration: {duration:.2f} | Calculated time: {(end-start):.2f}")
                    # calulate_bert_metric(g_summary, ref_summ, idx, data_list)
                    data_list.append([idx, g_summary, ref_summ])
                elif response_redirect.status_code == 500:
                    raise HTTPError("error in response")
                else:
                    continue
        except Exception as e:
            print(f"Exception: {e}")
            continue
    df=pd.DataFrame(data=data_list, columns=['IDX', 'Generated Summary', 'Ground Truth Summary'])
    df.to_csv("bert-test-result.csv")
    

if __name__ == "__main__":
    test()