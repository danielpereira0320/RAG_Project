#!/bin/bash

# Exit on any error
set -e

echo "Updating and Upgrading System..."
sudo apt update && sudo apt upgrade -y

echo "Installing necessary dependencies..."
sudo apt install -y curl wget git python3 python3-pip python3-venv python3-dev unzip software-properties-common

echo "Checking and installing NVIDIA CUDA toolkit if not installed..."
if ! dpkg -l | grep -q nvidia-cuda-toolkit; then
    sudo apt install -y nvidia-cuda-toolkit
else
    echo "CUDA toolkit is already installed."
fi

echo "Checking and installing NVIDIA container toolkit if not installed..."
if ! dpkg -l | grep -q nvidia-container-toolkit; then
    sudo apt install -y nvidia-container-toolkit
else
    echo "NVIDIA container toolkit is already installed."
fi

echo "Checking and installing Docker if not installed..."
if ! dpkg -l | grep -q docker.io; then
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
else
    echo "Docker is already installed."
fi

echo "Checking and installing NVIDIA Docker support..."
if ! dpkg -l | grep -q nvidia-docker2; then
    distribution=$(. /etc/os-release; echo ${ID}${VERSION_ID//./})
    sudo curl -fsSL https://nvidia.github.io/nvidia-docker/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-docker-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/nvidia-docker-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu$distribution/$(uname -m)/" | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    sudo apt update && sudo apt install -y nvidia-docker2
    sudo systemctl restart docker
else
    echo "NVIDIA Docker is already installed."
fi

echo "Setup complete!"

echo "Pulling required Docker images..."
docker pull ollama/ollama
docker pull chromadb/chroma

echo "Creating necessary directories..."
mkdir -p ollama_models

echo "Starting Ollama container..."
docker run -d --gpus all \
  --name ollama_temp \
  -v "$(pwd)/ollama_models:/root/.ollama/models" \
  ollama/ollama serve

echo "Waiting for Ollama to be ready..."
sleep 5  # Give it time to start

echo "Pulling models into the running container..."
docker exec -it ollama_temp ollama pull mxbai-embed-large || echo "Failed to pull mxbai-embed-large"
docker exec -it ollama_temp ollama pull llama3.1 || echo "Failed to pull llama3.1"

echo "Stopping and removing temporary Ollama container..."
docker stop ollama_temp
docker rm ollama_temp

echo "Model download complete!"


echo "Setting up and starting the chatbot application..."
APP_DIR=$(pwd)
echo "APP_PATH=$APP_DIR" > .env
sudo apt install -y docker-compose-plugin
docker-compose --env-file .env up -d --build

