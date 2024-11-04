from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

MODELS_DIR = "uploaded_models"
os.makedirs(MODELS_DIR, exist_ok = True)

loaded_models = {}

class GenerateRequest(BaseModel):
    model: str
    prompt: str

def load_model(model_path: str):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype = torch.float16,
            device_map = "auto"
        )
        return model, tokenizer
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Error loading model: {str(e)}")
    

@app.post("/upload-model")
async def upload_model(model: UploadFile = File(...)):
    try:
        model_path = os.path.join(MODELS_DIR, model.filename)
        with open(model_path, 'wb') as buffer:
            shutil.copyfileobj(model.file, buffer)
        return {"message": f"Model {model.filename} uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    

@app.post("/generate")
async def generate_text(request: GenerateRequest):
    try:
        model_path = os.path.join(MODELS_DIR, request.model)

        if request.model not in loaded_models:
            model, tokenizer = load_model(model_path)
            loaded_models[request.model] = (model, tokenizer)

        else:
            model, tokenizer = loaded_models[request.model]

        inputs = tokenizer(request.prompt, return_tensors ="pt").to(model.device)

        outputs = model.generate(
            inputs.input_ids,
            max_length = 200,
            num_return_sequences = 1,
            temperature = 0.7,
            do_sample = True,
            pad_token_id = tokenizer.eos_token_id
        )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens = True)

        return {"generated_text": generated_text}
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port = 8000)