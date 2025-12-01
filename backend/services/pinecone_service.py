from pinecone import Pinecone
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.pc.Index(PINECONE_INDEX)

    def upsert_embeddings(self, embeddings, chunks):
        vectors = []
        for i, emb in enumerate(embeddings):
            vectors.append({
                "id": f"chunk-{i}",
                "values": emb,
                "metadata": {"text": chunks[i]}
            })
        self.index.upsert(vectors=vectors)

    def query(self, vector, top_k=5):
        res = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
        return [m["metadata"]["text"] for m in res["matches"]]
