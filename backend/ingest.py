import os
import pdfplumber
from sentence_transformers import SentenceTransformer
from services.pinecone_service import PineconeService

DOCUMENTS_DIR = "/app/RAG_documents"

def load_documents():
    docs = []
    for filename in os.listdir(DOCUMENTS_DIR):
        path = os.path.join(DOCUMENTS_DIR, filename)
        if not os.path.isfile(path):
            continue

        ext = filename.lower().split(".")[-1]
        if ext in ["txt", "md"]:
            with open(path, "r", encoding="utf-8") as f:
                docs.append(f.read())
        elif ext == "pdf":
            text = ""
            try:
                with pdfplumber.open(path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                docs.append(text)
            except Exception as e:
                print(f"⚠ Error leyendo PDF {filename}: {e}")

    return docs


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

    docs = load_documents()

    for doc in docs:
        chunks = chunk_text(doc)
        vecs = model.encode(chunks)

        pinecone.upsert_vectors(chunks, vecs)

    print("✔ Ingest completed")

ingest_documents()