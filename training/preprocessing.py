import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import torch
import pickle

def load_and_prepare_data(csv_dir, max_features=1000, test_size=0.2):
    # Alle CSV-Dateien zusammenführen
    all_rows = []
    for file in os.listdir(csv_dir):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(csv_dir, file), sep=";")
            all_rows.append(df)
    data = pd.concat(all_rows, ignore_index=True)

    # Importance von 1-5 auf 0-4 mappen
    data["Importance"] = data["Importance"].astype(int)

    # TF-IDF-Vektorisierung
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(data["Content"]).toarray()
    y = data["Importance"].values

    # Daten splitten
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)

    # In Tensoren umwandeln
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.long)
    y_val_tensor = torch.tensor(y_val, dtype=torch.long)

    # Vektorizer speichern
    with open(os.path.join(csv_dir, "..", "models", "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    return X_train_tensor, X_val_tensor, y_train_tensor, y_val_tensor

def tokenize_and_clean_text(text):
    import re
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-ZäöüÄÖÜß0-9 ]", "", text)
    return text