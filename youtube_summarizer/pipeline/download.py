import os

def download(url:str):
    audio = os.system(f"yt-dlp -x --audio-format wav {url}")
    return audio







