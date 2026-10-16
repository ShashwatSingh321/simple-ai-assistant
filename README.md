
# Simple AI Assistant

A beginner-friendly Python project that connects to a locally running AI model using Ollama and Qwen3:4b.

## Project Goal

Send a prompt from a Python program to a locally running language model and display its response.

## Technology Stack

- Python
- Ollama
- Qwen3:4b
- OpenAI-compatible Python client

## Current Status

**Working initial version.**

- [x] Create the project directory
- [x] Create a Python virtual environment
- [x] Initialize the Git repository
- [x] Configure Git to ignore local environment files
- [x] Install Ollama and download Qwen3:4b
- [x] Install the Python dependencies
- [x] Connect Python to the local Ollama API
- [x] Run the assistant and receive a model response
- [x] Record Python dependencies in `requirements.txt`

## Prerequisites

- Python 3.10 or compatible version
- Git
- Ollama
- The Qwen3:4b model downloaded through Ollama
- Sufficient system memory and disk space for the model

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd simple-ai-assistant
```

### 2. Create and activate a virtual environment

On Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```cmd
python -m pip install -r requirements.txt
```

### 4. Start Ollama

Make sure Ollama is running and the Qwen3:4b model is available:

```cmd
ollama run qwen3:4b
```

You can exit the interactive chat with `/bye`. If Ollama is configured to use a custom model directory, ensure the server uses that configuration.

### 5. Run the assistant

In the project directory, run:

```cmd
python simple_ai_assistant.py
```

The program sends the prompt `Hello LLM!` to Qwen3:4b and prints the response.

## Project Structure

```text
simple-ai-assistant/
├── .gitignore
├── README.md
├── requirements.txt
└── simple_ai_assistant.py
```

The `.venv` directory is local to your machine and should not be committed.

## Scope

This project follows the basic local AI assistant workflow demonstrated in the learning material. The current version sends one predefined prompt and prints the response. Interactive conversations and additional features may be added later.
