# YouTube Summarizer

YouTube Summarizer is python web app for summarizing and creating highlights of videos uploaded on YouTube platform. Based on audio of video and by using models: (Whisper, Pyannote.audio - speaker diarization model and LLama 2 7B) application performs translation, speaker diarization and summarization. 

## Installation

Start by creating environment with required dependancies:

```bash
poetry install
```
```bash
poetry shell
```

Then run:
```bash
make get-model
```
to download llama-2_7b.gguf model file (around 5gb).


After that export your Hugging Face Token by running command:
```bash
export HUGGING_FACE_TOKEN=<your_token>
```
This is needed to properly run application in docker containers (needed for pyannote model).
and do not forget to accept all user conditions required here (https://huggingface.co/pyannote/speaker-diarization-3.1)



## Usage





## DEMO

https://github.com/user-attachments/assets/bf843078-491f-4c6c-92e7-31394ca49a96

#### Transcription:
**The Joker**:*"Well, you look nervous. Is it the scars? You want to know how I got 'em? Come here. Hey! Look at me. So I had a wife, beautiful, like you, who tells me I worry too much. Who tells me I ought to smile more. Who gambles and gets in deep with the sharks. One day, they carve her face. And we have no money for surgeries. She can't take it. I just want to see her smile again, hm? I just want her to know that I don't care about the scars. So I stick a razor in my mouth and do this to myself. And you know what? She can't stand the sight of me! She leaves. Now I see the funny side.""*


#### Summary:
```
" The speaker describes how they got a scar on their mouth from their father's drunken attack. The father attacked the speaker's mother with a knife, and when the speaker tried to defend themselves, the father turned to them and stuck a knife in their mouth, telling them to put a smile on their face."
```




## CITATIONS

@inproceedings{bert-score,
  title={BERTScore: Evaluating Text Generation with BERT},
  author={Tianyi Zhang* and Varsha Kishore* and Felix Wu* and Kilian Q. Weinberger and Yoav Artzi},
  booktitle={International Conference on Learning Representations},
  year={2020},
  url={https://openreview.net/forum?id=SkeHuCVFDr}
}


## License


[MIT](https://choosealicense.com/licenses/mit/)
