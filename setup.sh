#!/bin/bash

# Exit immediately if a command exits with a non-zero status
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

echo "Configuring Docker for CUDA support..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
sudo curl -fsSL https://nvidia.github.io/nvidia-docker/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-docker-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nvidia-docker-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu$distribution/$(uname -m)/" | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update && sudo apt install -y nvidia-docker2
sudo systemctl restart docker

echo "Setting up Ollama and ChromaDB on Docker..."
docker pull ollama/ollama
docker pull chromadb/chroma

echo "Building the Chatbot Docker Image"
cd project
docker-compose up -d --build
cd ../

