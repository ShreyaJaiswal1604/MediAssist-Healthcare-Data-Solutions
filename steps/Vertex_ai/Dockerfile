# Use a lightweight Python image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y git curl && \
    pip install --upgrade pip && \
    pip install torch transformers google-cloud-storage fastapi uvicorn pydantic

# Set the working directory
WORKDIR /app

# Copy the serve script into the container
COPY serve.py /app/serve.py

# Run the FastAPI app
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8080"]
