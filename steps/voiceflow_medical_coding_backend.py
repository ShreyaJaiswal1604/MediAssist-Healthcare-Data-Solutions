from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel, pipeline
import torch

# Define input schema
class TextInput(BaseModel):
    text: str  # Input clinical text

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained ICD-10 prediction model
ICD_MODEL_NAME = "AkshatSurolia/ICD-10-Code-Prediction"
icd_tokenizer = AutoTokenizer.from_pretrained(ICD_MODEL_NAME)
icd_model = AutoModel.from_pretrained(ICD_MODEL_NAME)

# Load the pre-trained BIOMed_NER model
NER_MODEL_NAME = "venkatd/BIOMed_NER"
ner_pipeline = pipeline("token-classification", model=NER_MODEL_NAME, tokenizer=NER_MODEL_NAME, aggregation_strategy="simple")

def extract_entities_with_biomed_ner(text):
    """
    Extract biomedical entities using BIOMed_NER.
    """
    ner_results = ner_pipeline(text)
    entities = {
        "patient_info": [],
        "disease_disorder": [],
        "treatment": [],
        "medication": []
    }

    for entity in ner_results:
        entity_type = entity["entity_group"].lower().replace(" ", "_")  # Normalize entity group names
        if entity_type in entities:
            entities[entity_type].append(entity["word"])

    # Convert lists to readable strings
    for key in entities:
        entities[key] = ", ".join(entities[key]) if entities[key] else None

    return entities

@app.post("/process_text")
async def process_text(data: TextInput):
    """
    Process the clinical text input, categorize the details using BIOMed_NER, 
    and return predicted ICD-10 codes categorized based on the model's output.
    """
    input_text = data.text  # Extract clinical input text

    # Extract entities using BIOMed_NER
    categorized_details = extract_entities_with_biomed_ner(input_text)

    # Tokenize the input text for the ICD prediction model
    icd_inputs = icd_tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)

    # Perform inference with the ICD prediction model
    with torch.no_grad():
        outputs = icd_model(**icd_inputs)
        logits = outputs.last_hidden_state.mean(dim=1)  # Average logits across tokens

        # Convert logits to probabilities
        probabilities = torch.softmax(logits, dim=-1)
        predicted_indices = torch.topk(probabilities, k=3).indices.squeeze(0).tolist()  # Get top 3 predictions

    # Map indices to ICD-10 codes and categories (assuming the model outputs include categories)
    predicted_icd_codes = []
    predicted_categories = []

    for index in predicted_indices:
        # Example: Assuming the model provides a method `get_icd_code_and_category` to fetch ICD codes and their categories
        icd_code = f"ICD-{index}"  # Replace with the actual method to fetch the ICD code
        category = "Example_Category"  # Replace with the actual category predicted by the model
        predicted_icd_codes.append(icd_code)
        predicted_categories.append(category)

    # Organize ICD codes by category
    categorized_icd_codes = {cat: [] for cat in set(predicted_categories)}
    for icd_code, category in zip(predicted_icd_codes, predicted_categories):
        categorized_icd_codes[category].append(icd_code)

    # Convert lists to readable strings
    for key in categorized_icd_codes:
        categorized_icd_codes[key] = ", ".join(categorized_icd_codes[key])

    return {
        "transcription": input_text,
        "categorized_details": categorized_details,
        "icd_codes": predicted_icd_codes,
        "categorized_icd_codes": categorized_icd_codes
    }
