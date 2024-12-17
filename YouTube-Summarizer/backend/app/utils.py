import logging
import logging.config
import os

def setup_logging(service_name: str, log_file: str = "service.log", log_level=logging.INFO):
    """Sets up logging configuration for the current microservice."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": f"%(asctime)s - {service_name} - %(levelname)s - %(message)s"
            },
            "detailed": {
                "format": f"%(asctime)s - {service_name} - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",  # For development, switch to INFO or WARNING in production
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": log_file,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "": {  # Root logger configuration
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True,
            },
        },
    }

    logging.config.dictConfig(logging_config)


def save_prompt_data(full_text:str, transcription:dict) -> bool:
    try:
        os.makedirs("/code/app/results", exist_ok=True)
        with open("/code/app/results/result.txt", 'w') as file:
            file.write(full_text)
        segments = transcription['segments']
        with open("/code/app/results/result_transcription.txt", 'w') as file:
            for segment in segments:
                start = segment['start']
                end = segment['end']
                text = segment['text']
                full_str = f"{start} - {end} | Text: {text}\n"
                file.write(full_str)
        return True
    except FileNotFoundError:
        print("ERROR")
        return False