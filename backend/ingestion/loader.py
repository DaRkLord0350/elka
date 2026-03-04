import os
from pypdf import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def load_documents(directory):

    documents = []

    for file in os.listdir(directory):

        path = os.path.join(directory, file)

        if file.endswith(".pdf"):
            text = load_pdf(path)

            documents.append({
                "text": text,
                "source": file
            })

    return documents