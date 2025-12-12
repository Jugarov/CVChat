from pinecone import Pinecone, ServerlessSpec
from pinecone.core.openapi.shared.exceptions import NotFoundException
import os

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_DEFAULT_INDEX = os.getenv("PINECONE_DEFAULT_INDEX")
INDEXES = ["cv-juan", "cv-rodri", "cv-dani"]

class PineconeService:
    def __init__(self, namespace=PINECONE_DEFAULT_INDEX):
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

    def _get_index(self, namespace):
        # El namespace determina el índice REAL donde insertar/buscar
        if namespace not in self.indexes:
            raise ValueError(f"No existe índice '{namespace}' para namespace '{namespace}'")

        return self.indexes[namespace]

    def upsert_vectors(self, namespace, items):
        index = self._get_index(namespace)
        return index.upsert(
            vectors=items,
            namespace=namespace
        )

    def query(self, vector, namespace=None, top_k=5):
        # usar SIEMPRE el namespace del CVAgent
        ns = namespace if namespace else self.namespace
        index = self._get_index(ns)

        result = index.query(
            vector=vector,
            top_k=top_k,
            namespace=ns,
            include_metadata=True
        )

        return result
