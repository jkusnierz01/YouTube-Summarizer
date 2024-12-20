#!/bin/bash

# Step 1: Build and Start Backend and LLM Containers
echo "Starting backend and LLM containers..."
docker-compose build backend llm
docker-compose up -d backend llm  # Detached mode

echo "Installing packages..."
pip3 install -r tests/summary_tests/requirements.txt

# Wait for services to be ready (adjust time as needed)
echo "Waiting for services to initialize..."
sleep 35

# Step 2: Run Tests
echo "Running tests..."

python3 tests/summary_tests/create_summary.py

# Step 3: Stop Containers After Tests
echo "Stopping containers..."
docker-compose down  # Use full path to docker-compose

echo "BERTScore calculation..."
python3 tests/summary_tessts/summary_test.py

echo "Tests completed."
