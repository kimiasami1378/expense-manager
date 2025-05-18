from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import speech_recognition as sr
import io
import os
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageResponse(BaseModel):
    id: str
    text: str

# In-memory storage for messages (replace with database in production)
conversation_history = []

@app.get("/")
def read_root():
    return {"message": "Voice Chat API is running"}

@app.post("/api/transcribe", response_model=MessageResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Read uploaded file into memory
        contents = await file.read()
        
        # Use SpeechRecognition library to convert speech to text
        recognizer = sr.Recognizer()
        
        with io.BytesIO(contents) as audio_file:
            # Convert to AudioFile format that speech_recognition can process
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                
                # Use Google's Speech Recognition service
                # In production, consider using a more robust service
                text = recognizer.recognize_google(audio_data)
                
                # Generate a unique ID for this message
                message_id = str(uuid.uuid4())
                
                # Add to history (in production, save to database)
                conversation_history.append({"id": message_id, "text": text})
                
                return {"id": message_id, "text": text}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing audio: {str(e)}")

@app.post("/api/chat", response_model=MessageResponse)
async def process_message(message: str):
    try:
        # Process the incoming message and generate a response
        # This is where you would integrate with your NLP or AI backend
        
        # For this example, we're just echoing the message with a prefix
        response_text = f"Echo: {message}"
        
        # Generate a unique ID for this message
        message_id = str(uuid.uuid4())
        
        # Add to history (in production, save to database)
        conversation_history.append({"id": message_id, "text": response_text})
        
        return {"id": message_id, "text": response_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)