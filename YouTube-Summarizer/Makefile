
MODEL_PATH="./llm/models/llama-2-7b-chat.Q5_K_M.gguf"

prepare:
	./utils/dir_setup.sh


download:
	@if [ ! -f MODEL_PATH ]; then \
		poetry run huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q5_K_M.gguf --local-dir ./llm/models/; \
	fi;

clean-cache:
	@echo "Cleaning hugging face cache"
	rm -rf ./llm/models/.cache/huggingface
	rm -rf ./llm/models/.cache


get-model: prepare download clean-cache