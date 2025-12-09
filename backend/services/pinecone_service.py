from pinecone import Pinecone, ServerlessSpec
from pinecone.core.openapi.shared.exceptions import NotFoundException
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEXES = ["cv-juan", "cv-rodri", "cv-dani"]


class PineconeService:
    def __init__(self, namespace="default"):
        self.namespace = namespace
        self.pc = Pinecone(api_key=PINECONE_API_KEY)

        # Guardamos todos los índices en un diccionario
        self.indexes = {}

        for index_name in INDEXES:
            try:
                index = self.pc.Index(index_name)
                index.describe_index_stats()
            except NotFoundException:
                print(f"Índice '{index_name}' no existe. Creándolo...")

                self.pc.create_index(
                    name=index_name,
                    dimension=768,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )

                index = self.pc.Index(index_name)

            # Guardar referencia
            self.indexes[index_name] = index

    def _get_index(self):
        # El namespace determina el índice REAL donde insertar/buscar
        if self.namespace not in self.indexes:
            raise ValueError(f"No existe índice para namespace '{self.namespace}'")
        return self.indexes[self.namespace]

    def upsert_vectors(self, texts, embeddings):
        index = self._get_index()

        items = []
        for i, (t, e) in enumerate(zip(texts, embeddings)):
            items.append({
                "id": f"chunk-{i}",
                "values": e.tolist(),
                "metadata": {"text": t}
            })

        index.upsert(vectors=items, namespace=self.namespace)

    def query(self, vector, top_k=5):
        index = self._get_index()

        return index.query(
            namespace=self.namespace,
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
