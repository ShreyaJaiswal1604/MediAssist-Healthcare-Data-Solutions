from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import torch

# Define input schema
class TextInput(BaseModel):
    text: str  # Input clinical text

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained ICD-10 prediction model and tokenizer
MODEL_NAME = "AkshatSurolia/ICD-10-Code-Prediction"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

@app.post("/process_text")
async def process_text(data: TextInput):
    """
    Process the clinical text input and return predicted ICD-10 codes.
    """
    input_text = data.text  # Extract clinical input text

    # Tokenize the input text for the model
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)

    # Perform inference with the pre-trained model
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.last_hidden_state.mean(dim=1)  # Average logits across tokens

        # Convert logits to probabilities (use softmax if necessary)
        probabilities = torch.softmax(logits, dim=-1)
        predicted_indices = torch.topk(probabilities, k=3).indices.squeeze(0).tolist()  # Get top 3 predictions

    # Map indices to ICD-10 codes (use the model's predefined mapping)
    # Assuming the ICD codes are already represented in `predicted_indices`
    predicted_icd_codes = [f"ICD-{index}" for index in predicted_indices]  # Replace with actual ICD mapping if provided

    return {
        "transcription": input_text,
        "icd_codes": predicted_icd_codes
    }
