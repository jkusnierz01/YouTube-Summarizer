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
The Joker:"Want know how I got these scars? My father was a drinker and a fiend. And one night he goes off crazier than usual. Mommy gets the kitchen knife to defend herself. He doesn't like that. Not one bit. So, me watching, he takes the knife to her, laughing while he does it. He turns to me, and he says, 'why so serious?' He comes at me with the knife. 'Why so serious?!'. He sticks the blade in my mouth. 'Let's put a smile on that face!' And why so serious?"








## CITATIONS

@inproceedings{bert-score,
  title={BERTScore: Evaluating Text Generation with BERT},
  author={Tianyi Zhang* and Varsha Kishore* and Felix Wu* and Kilian Q. Weinberger and Yoav Artzi},
  booktitle={International Conference on Learning Representations},
  year={2020},
  url={https://openreview.net/forum?id=SkeHuCVFDr}
}


## License


https://github.com/user-attachments/assets/053c8140-1730-40a4-b23d-0478e5d1ef04



https://github.com/user-attachments/assets/e5ccd336-368c-43d9-893a-7b0574478bb1


[MIT](https://choosealicense.com/licenses/mit/)
