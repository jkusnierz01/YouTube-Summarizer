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
export HUGGING_FACE_TOKEN="your_token"
```
This is needed to properly run application in docker containers (needed for pyannote model).
and do not forget to accept (THIS HAS TO BE CHANGED - THINK ABOUT GETTING MODEL LOCALLY OR BY GITHUB REPO)

```bash
export DOCKER_BUILDKIT=1
```
## Usage

```bash
curl --request POST \    --url http://0.0.0.0:8000/completion \     
    --header "Content-Type: application/json" \
    --data '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}' 2>/dev/null | jq -C | less
```

```bash
docker run -v absolute_path:/models -p 8000:8000 llm -m /models/llama-2-7b-chat.Q5_K_M.gguf --port 8000 --host 0.0.0.0 -n 512
```


## Licensing
This project uses code from multiple open-source projects with different licenses:

- **Whisper Model** is licensed under the MIT License. See [LICENSE-MIT]for details.
- **Pyannote.audio Speaker-diarization 3.1 model** is licensed under the MIT License. See [LICENSE-MIT](./LICENSE-MIT) for details.
- **CTC Forced Aligner** is licensed under the BSD License. See [LICENSE-BSD](./LICENSE-BSD) for details.

You must comply with the terms of both licenses when using this project.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)