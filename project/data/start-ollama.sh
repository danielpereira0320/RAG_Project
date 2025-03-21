#!/bin/sh
set -e  # Stop on error

echo "Pulling required models..."
ollama pull llama3.1:8b
ollama pull quen2.5:3b

echo "Starting Ollama server..."
exec ollama serve

