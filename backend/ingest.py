import os
import pdfplumber
from sentence_transformers import SentenceTransformer
from services.pinecone_service import PineconeService

DOCUMENTS_DIR = "/app/RAG_documents"


def extract_text_from_file(path):
    ext = path.lower().split(".")[-1]

    if ext in ["txt", "md"]:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == "pdf":
        text = ""
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            print(f"Error leyendo PDF {path}: {e}")
        return text

    return ""


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def ingest_documents():
    model = SentenceTransformer("all-mpnet-base-v2")
    pinecone = PineconeService()

    print("Escaneando CVs en:", DOCUMENTS_DIR)

    for filename in os.listdir(DOCUMENTS_DIR):
        path = os.path.join(DOCUMENTS_DIR, filename)
        if not os.path.isfile(path):
            continue

        # obtener nombre base sin extensión
        base = os.path.splitext(filename)[0]
        namespace = f"cv-{base.lower()}"

        print(f"\nProcesando CV: {filename} → namespace={namespace}")

        text = extract_text_from_file(path)
        if not text.strip():
            print(f"No se extrajo texto de {filename}")
            continue

        chunks = chunk_text(text)
        vecs = model.encode(chunks)

        pinecone.namespace = namespace
        pinecone.upsert_vectors(
            texts=chunks,
            embeddings=vecs
        )

        print(f"Ingestado {filename} ({len(chunks)} chunks) en {namespace}")

    print("\nIngestión completa")

if __name__ == "__main__":
    ingest_documents()
