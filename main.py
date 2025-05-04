from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os
from liteLLM import LiteLLM

app = FastAPI(title="Web-based Chat Assistant")

# Initialize LiteLLM instance (assuming local or environment-configured)
llm = LiteLLM()

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class Conversation(BaseModel):
    messages: List[Message]
    model_name: Optional[str] = None  # For model comparison if needed

@app.post("/chat/")
async def chat_endpoint(conversation: Conversation):
    """
    Handle chat messages, maintain conversation context, and generate responses.
    """
    try:
        # Prepare the conversation history for the LLM
        messages = [(msg.role, msg.content) for msg in conversation.messages]
        # Select model if specified
        model_name = conversation.model_name or "default"
        # Generate response using LiteLLM
        response_text = llm.chat(messages, model_name=model_name)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_media/")
async def upload_media(file: UploadFile = File(...)):
    """
    Handle media uploads (images, audio, etc.).
    """
    try:
        # Save uploaded file temporarily
        temp_dir = "uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        # Here, you could process the media as needed
        # For now, just acknowledge upload
        return {"filename": file.filename, "message": "Upload successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare_models/")
async def compare_models(conversation: Conversation):
    """
    Generate responses from multiple models for comparison.
    """
    try:
        responses = {}
        models_to_compare = ["modelA", "modelB"]  # Example model names
        for model_name in models_to_compare:
            response_text = llm.chat(
                [(msg.role, msg.content) for msg in conversation.messages],
                model_name=model_name
            )
            responses[model_name] = response_text
        return {"comparisons": responses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Web-based Chat Assistant API"}

# Note: To run the server, use: uvicorn main:app --host 0.0.0.0 --port 8000