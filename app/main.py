from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz
from bertopic import BERTopic

generated_chunks = {}


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
async def upload_files(files: List[UploadFile] = File(...)):
    filenames = []
    for file in files:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        chunks = split_text_into_chunks(text)
        generated_chunks[file.filename] = []
        generated_chunks[file.filename].extend(chunks)
        filenames.append(file.filename)

    for file in generated_chunks:
        for chunk in generated_chunks[file]:
            print(chunk)
            print(len(chunk))
            print("=====================")
        print(len(generated_chunks[file]))

        print("=== TEST: Starte Themen-Generierung ===")

        texts_for_analysis = []
        for filename in filenames:  # die frisch hochgeladenen Dateien
            if filename in generated_chunks:
                texts_for_analysis.extend(generated_chunks[filename])

        if texts_for_analysis:
            topic_model = BERTopic(
                language="german",
                min_topic_size=2,
                n_gram_range=(1, 3),
                calculate_probabilities=True
            )
            topics, probs = topic_model.fit_transform(texts_for_analysis)
            topics_info = topic_model.get_topic_info()

            print("=== THEMEN ERKANNT ===")
            print(topics_info)
        else:
            print("Keine Texte für Analyse gefunden.")

    return JSONResponse(content={"message": "Upload erfolgreich!", "filenames": filenames})

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
        return text

def split_text_into_chunks(text: str, max_words: int = 20) -> list:
    """
    Teilt einen langen Text in kleinere Chunks auf.

    :param text: Der gesamte extrahierte Text als ein String.
    :param max_words: Maximale Wortanzahl pro Chunk.
    :return: Liste von Text-Chunks.
    """
    chunks = []
    words = text.split()

    current_chunk = []
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(' '.join(current_chunk))
            current_chunk = []

    # Falls noch Wörter übrig sind
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

@app.post("/generate_topics")
async def generate_topics(selected_files: List[str]):
    texts_for_analysis = []
    for filename in selected_files:
        if filename in selected_files:
            if filename in generated_chunks:
                texts_for_analysis.extend(generated_chunks[filename])
    if not texts_for_analysis:
        return JSONResponse(content={"error": "Keine Texte Gefunden"}, status_code=400)

    topic_model = BERTopic(language="german")
    topics, probs = topic_model.fit_transform(texts_for_analysis)

    topics_info = topic_model.get_topic_info()

    topic_tree = {}
    for topic_id in topics_info["topics"]:
        if topic_id == -1:
            continue
        name = topics_info[topics_info["topics"] == topic_id]["name"].values[0]
        topic_tree[f"Topic {topic_id}"] = name
    return JSONResponse(content={"topics": topic_tree})