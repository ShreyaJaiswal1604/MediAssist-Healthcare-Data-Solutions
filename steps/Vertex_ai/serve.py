from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

app = FastAPI()

# Define GCS bucket and model paths
GCS_BUCKET = "medical_llm_models"
MODEL_PATH = "/app/model"
MODEL_NAME = "Asclepius-Llama3-8B"

# Download model from GCS
try:
    print("[INFO] Downloading model from GCS...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs(prefix=MODEL_NAME)

    # Ensure local model directory exists
    os.makedirs(MODEL_PATH, exist_ok=True)

    for blob in blobs:
        local_file_path = os.path.join(MODEL_PATH, os.path.basename(blob.name))
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        blob.download_to_filename(local_file_path)
        print(f"[INFO] Downloaded: {blob.name}")

    print("[INFO] Loading the model...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
    print("[INFO] Model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Failed to initialize the model: {e}")
    raise e

# Input and output schemas
class ClinicalNoteRequest(BaseModel):
    note: str

class MedicalCodeResponse(BaseModel):
    icd_codes: list[str]

@app.post("/predict", response_model=MedicalCodeResponse)
def predict(request: ClinicalNoteRequest):
    try:
        prompt = f"""
        You are an intelligent clinical language model.
        Below is a patient's clinical note. Generate only the 5 most relevant ICD-10 codes.

        Clinical Note:
        {request.note}

        Return the output in the following format:
        ["ICD10_CODE_1", "ICD10_CODE_2", "ICD10_CODE_3", "ICD10_CODE_4", "ICD10_CODE_5"]
        """
        # Tokenize with the updated max_length
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=8192)
        
        # Generate predictions with adjusted token limits
        output = model.generate(**inputs, pad_token_id=tokenizer.eos_token_id, max_new_tokens=300)

        # Decode the model output
        response_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # Parse and validate the output
        icd_codes = eval(response_text)  # Expecting the output to match the specified JSON format
        if isinstance(icd_codes, list) and all(isinstance(code, str) for code in icd_codes):
            return {"icd_codes": icd_codes}
        else:
            print(f"[ERROR] Unexpected model output: {response_text}")
            raise HTTPException(status_code=500, detail="Invalid model response format")
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}
