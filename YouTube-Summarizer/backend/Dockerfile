# Use the NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get install -y \
    nvidia-cuda-toolkit \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    python3-pip \
    # build-essential \
    # g++ \
    git \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /code

# Copy requirements file and install Python dependencies
COPY ./backend/requirements-backend.txt /code/
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cu118 -r requirements-backend.txt

# Copy the application code
COPY ./backend/app /code/app

# Set the working directory to the app folder
WORKDIR /code/app/

# Expose port 8080
EXPOSE 8080

# Default command to keep the container running
# CMD ["/bin/bash"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
