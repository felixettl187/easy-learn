import fitz  # PyMuPDF


# Funktion zum Extrahieren der Slides aus PDF-Bytes
def extract_slides_from_pdf_bytes(file_bytes):
    """
    Extrahiert saubere Slide-Texte aus einer PDF (Input als Bytes).
    Kopfzeilen/Fußzeilen werden entfernt.

    :param file_bytes: PDF als Bytes (z.B. Upload)
    :return: Liste der Slide-Texte
    """
    slides = []  # Liste zur Speicherung der extrahierten Slides
    doc = fitz.open(stream=file_bytes, filetype="pdf")  # PDF aus Bytes öffnen

    for page in doc:  # Jede Seite der PDF durchgehen
        page_text = ""  # Zwischenspeicher für den Text der aktuellen Seite
        blocks = page.get_text("blocks")  # Textblöcke auf der Seite abrufen (inkl. Koordinaten)
        for block in blocks:  # Jeden Block auf der Seite durchgehen
            x0, y0, x1, y1, text, *_ = block  # Koordinaten und Text extrahieren
            # Nur Text aus der "Mitte" der Seite nehmen (Kopf- und Fußzeile rausfiltern)
            if y0 > 50 and y1 < (page.rect.height - 50):  # Kopf- und Fußzeilen herausfiltern
                page_text += text.strip() + " "  # Text zum Slide-Text hinzufügen

        cleaned_text = page_text.strip()  # Endgültigen Slide-Text aufräumen
        if not cleaned_text:
            cleaned_text = "KEIN TEXT GEFUNDEN"  # Dummy-Text für leere Seiten
        slides.append(cleaned_text)  # Slide-Text zur Liste hinzufügen

    doc.close()  # PDF-Dokument schließen
    return slides  # Alle extrahierten Slides zurückgeben

import os
import csv

def save_slides_to_csv(slides, pdf_filename, output_folder="uncompleted_data"):
    os.makedirs(output_folder, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(pdf_filename))[0]
    csv_path = os.path.join(output_folder, f"{base_filename}.csv")

    with open(csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Page", "Content", "Importance"])  # Header
        for i, slide in enumerate(slides, start=1):
            writer.writerow([i, slide, ""])  # Page-Nummer, Slide-Text, leere Importance-Spalte

def main():
    folder_path = "/Users/felixettl/Desktop/HTWG/Semester04SoSe25/IoX/easy-learn/training/trainingSlides"
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            slides = extract_slides_from_pdf_bytes(pdf_bytes)
            save_slides_to_csv(slides, pdf_path)

if __name__ == "__main__":
    main()