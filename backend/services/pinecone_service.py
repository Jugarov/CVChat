from pinecone import Pinecone, ServerlessSpec
from pinecone.core.openapi.shared.exceptions import NotFoundException
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

class PineconeService:
    def __init__(self, namespace="default"):
        self.namespace = namespace
        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        try:
            # Intentamos obtener el índice
            self.index = self.pc.Index(PINECONE_INDEX)
            # Esto lanzará NotFoundException si no existe
            self.index.describe_index_stats()

        except NotFoundException:
            print(f"Índice '{PINECONE_INDEX}' no existe. Creándolo...")
            
            self.pc.create_index(
                name=PINECONE_INDEX,
                dimension=768,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

            # Reasignar el índice luego de crearlo
            self.index = self.pc.Index(PINECONE_INDEX)

    def upsert_vectors(self, texts, embeddings):
        items = []
        for i, (t, e) in enumerate(zip(texts, embeddings)):
            items.append({
                "id": f"chunk-{i}",
                "values": e.tolist(),
                "metadata": { "text": t }
            })
        self.index.upsert(vectors=items)

    def query(self, vector, top_k=5):
        result = self.index.query(
            namespace=self.namespace,
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return result
