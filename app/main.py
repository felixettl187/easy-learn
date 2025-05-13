from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from training.model import ImportanceClassifier

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    predictions = process_pdf_for_prediction(file_bytes)
    return JSONResponse(content={"message": "Upload erfolgreich!", "filename": file.filename, "predictions": predictions})


import os
import fitz
import joblib
import torch
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def process_pdf_for_prediction(file_bytes: bytes):
    model_path = os.path.join("models", "importance_model.pth")
    vectorizer_path = os.path.join("models", "vectorizer.pkl")
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        raise FileNotFoundError("Modelldateien nicht gefunden.")


    vectorizer = joblib.load(vectorizer_path)
    model = ImportanceClassifier(
        input_dim=len(vectorizer.vocabulary_),
        output_dim=1
    )
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        texts = [page.get_text().strip() for page in doc]

    vectors = vectorizer.transform(texts)

    with torch.no_grad():
        inputs = torch.tensor(vectors.toarray(), dtype=torch.float32)
        outputs = model(inputs)
        predictions = (outputs.squeeze() > 0.5).int().tolist()

    return list(enumerate(predictions, start=1))



