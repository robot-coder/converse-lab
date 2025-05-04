# README.md

# Web-based Chat Assistant with FastAPI and LiteLLM

This project implements a web-based Chat Assistant that allows users to interact with large language models (LLMs) via a user-friendly front-end interface. The backend is built with FastAPI and integrates with LiteLLM to facilitate conversation, media uploads, and model comparison features. The application is designed to be deployed on Render.com.

## Features

- Real-time chat with LLMs
- Media upload support
- Model comparison functionality
- Deployment-ready on Render.com

## Technologies Used

- Python 3.11+
- FastAPI
- Uvicorn
- LiteLLM
- Starlette
- Pydantic
- HTTPX

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/chat-assistant.git
cd chat-assistant
```

### 2. Create a virtual environment and activate it

```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server locally

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### 5. Deploy on Render.com

- Push your code to a GitHub repository.
- Create a new Web Service on Render.
- Connect your repository.
- Set the start command to:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

- Ensure `requirements.txt` is included for dependency installation.

## API Endpoints

- `POST /chat/` : Send a message and receive a response.
- `POST /upload/` : Upload media files.
- `GET /models/` : List available models.
- `POST /compare/` : Compare different models.

## Files

### main.py

```python
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import liteLLM
import httpx

app = FastAPI()

# Initialize LiteLLM model (placeholder, replace with actual initialization)
model = liteLLM.load_model("default-model")

class ChatRequest(BaseModel):
    message: str
    model_name: Optional[str] = None

class CompareRequest(BaseModel):
    models: List[str]
    message: str

@app.post("/chat/")
async def chat_endpoint(request: ChatRequest):
    """
    Handle chat messages and return model response.
    """
    try:
        # Select model if specified
        current_model = request.model_name or "default-model"
        response = model.generate(request.message, model_name=current_model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/")
async def upload_media(file: UploadFile = File(...)):
    """
    Handle media uploads.
    """
    try:
        content = await file.read()
        # Save or process the media as needed
        # For demonstration, just return filename and size
        return {"filename": file.filename, "size": len(content)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/")
async def list_models():
    """
    List available models.
    """
    try:
        models = liteLLM.list_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare/")
async def compare_models(request: CompareRequest):
    """
    Compare responses from different models.
    """
    try:
        responses = {}
        for model_name in request.models:
            responses[model_name] = model.generate(request.message, model_name=model_name)
        return {"responses": responses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### requirements.txt

```
fastapi
uvicorn
liteLLM
starlette
pydantic
httpx
```

---

**Note:** Replace placeholder code such as `liteLLM.load_model("default-model")` with actual LiteLLM initialization code as per your setup.