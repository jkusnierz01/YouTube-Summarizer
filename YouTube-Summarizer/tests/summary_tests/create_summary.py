import requests
import os
from pydub.utils import mediainfo
import time
import json


AUDIO_DIR = "/home/jedrzej_engineer/Desktop/audio/"
SUMMARY_DIR = "/home/jedrzej_engineer/Desktop/summary/"
TEXT_DIR = "/home/jedrzej_engineer/Desktop/text/"
OUTPUTFILENAME = "summary_test_results.json"
TEST_ENDPOINT_URL = "http://localhost:8080/test-endpoint/"

    
def create_summaries():
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
            audio_full_path = os.path.join(AUDIO_DIR, audio_filename)
            summ_full_path = os.path.join(SUMMARY_DIR, summ_filename)
            audio_metadata = mediainfo(audio_full_path)
            duration = float(audio_metadata["duration"])
            with open(audio_full_path, "rb") as audio:
                files = {"file": (audio_full_path, audio, "audio/mpeg")}
                start = time.time()
                response_redirect = requests.post(
                        url=TEST_ENDPOINT_URL,
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
                    # stenogram = response['data_to_prompt'] #UNCOMMENT IF YOU NEED THIS DATA ALSO
                    # transcript = response['transcription']
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
                        # 'stenogram': stenogram, #UNCOMMENT HERE TOO
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
    with open(OUTPUTFILENAME, 'w') as file:
        json.dump(data_list, file, indent=4)
    

if __name__ == "__main__":
    create_summaries()