# main.py
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from typing import Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str


def configure_gemini(api_key: str):
    """Configure Gemini with the provided API key"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def validate_api_key(api_key: str):
    """Validate the API key by making a test request"""
    try:
        model = configure_gemini(api_key)
        # Make a minimal test request
        response = model.generate_content("Test")
        return True
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.post("/generate")
async def generate_text(
    request: GenerateRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    try:
        # Validate API key and configure Gemini
        model = configure_gemini(x_api_key)
        
        # Generate response
        response = model.generate_content(request.prompt)
        
        # Extract and return the generated text
        generated_text = "\n" + response.text
        
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-key")
async def validate_key(x_api_key: str = Header(..., alias="X-API-Key")):
    try:
        validate_api_key(x_api_key)
        return {"status": "valid"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)