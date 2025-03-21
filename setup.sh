#!/bin/bash

# Exit on any error
set -e

echo "Updating and Upgrading System..."
sudo apt update && sudo apt upgrade -y

echo "Installing necessary dependencies..."
sudo apt install -y curl wget git python3 python3-pip python3-venv python3-dev unzip software-properties-common

echo "Setting up CUDA tools and packages..."
sudo apt install -y nvidia-cuda-toolkit nvidia-container-toolkit

echo "Setting up Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker

echo "Configuring Docker for NVIDIA support..."
distribution=$(. /etc/os-release; echo ${ID}${VERSION_ID//./})
sudo curl -fsSL https://nvidia.github.io/nvidia-docker/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-docker-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nvidia-docker-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu$distribution/$(uname -m)/" | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update && sudo apt install -y nvidia-docker2
sudo systemctl restart docker

echo "Pulling required Docker images..."
docker pull ollama/ollama
docker pull chromadb/chroma

echo "Creating necessary directories..."
mkdir -p ollama_models

echo "Running a temporary Ollama container to pull models..."
docker run --rm --gpus all -v "$(pwd)/ollama_models:/root/.ollama/models" ollama/ollama ollama pull mxbai-embed-large
docker run --rm --gpus all -v "$(pwd)/ollama_models:/root/.ollama/models" ollama/ollama ollama pull llama3.2

echo "Setting up and starting the chatbot application..."
APP_DIR=$(pwd)
echo "APP_PATH=$APP_DIR" > .env
docker-compose --env-file .env up -d --build

