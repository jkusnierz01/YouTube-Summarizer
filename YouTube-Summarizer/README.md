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
and do not forget to accept (THIS HAS TO BE CHANGED - THINK ABOUT GETTING MODEL LOCALLY OR BY GITHUB REPO

```bash
export DOCKER_BUILDKIT=1
```
## Usage


TO BE CONTINUED

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)