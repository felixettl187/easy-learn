import torch
import pickle
import os
from model import ImportanceClassifier
from preprocessing import tokenize_and_clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    slides = []
    for page in doc:
        text = page.get_text()
        if text.strip():
            slides.append(text.strip())
    return slides

def predict_importance(pdf_path):
    slides = extract_text_from_pdf(pdf_path)

    with open("models/vectorizer.pkl", "rb") as f:
        vectorizer: TfidfVectorizer = pickle.load(f)

    processed = [tokenize_and_clean_text(text) for text in slides]
    vectors = vectorizer.transform(processed).toarray()
    inputs = torch.tensor(vectors, dtype=torch.float32)

    input_dim = vectors.shape[1]
    output_dim = 1
    model = ImportanceClassifier(input_dim, output_dim)
    model.load_state_dict(torch.load("models/importance_model.pth"))
    model.eval()

    with torch.no_grad():
        outputs = model(inputs)
        preds = (outputs.squeeze() >= 0.5).int()

    for i, prediction in enumerate(preds):
        print(f"Seite {i+1}: Wichtigkeit {prediction.item()}")

if __name__ == "__main__":
    test_pdf_path = "trainingSlides/test_varianten_slidesv3.pdf"
    predict_importance(test_pdf_path)