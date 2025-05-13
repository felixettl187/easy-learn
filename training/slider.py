import fitz  # PyMuPDF


def extract_slides_from_pdf_bytes(file_bytes):

    slides = []
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page in doc:
        page_text = ""
        blocks = page.get_text("blocks")
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            if y0 > 50 and y1 < (page.rect.height - 50):
                page_text += text.strip() + " "

        cleaned_text = page_text.strip()
        if not cleaned_text:
            cleaned_text = "KEIN TEXT GEFUNDEN"
        slides.append(cleaned_text)

    doc.close()
    return slides

import os
import csv

def save_slides_to_csv(slides, pdf_filename, output_folder="uncompleted_data"):
    os.makedirs(output_folder, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(pdf_filename))[0]
    csv_path = os.path.join(output_folder, f"{base_filename}.csv")

    with open(csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Page", "Content", "Importance"])
        for i, slide in enumerate(slides, start=1):
            writer.writerow([i, slide, ""])

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