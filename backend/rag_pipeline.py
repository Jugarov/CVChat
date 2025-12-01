from services.embeddings import EmbeddingService
from services.pinecone_service import PineconeService
from services.groq_service import GroqService
import os

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

class RagPipeline:
    def __init__(self):
        self.embedder = EmbeddingService(EMBEDDING_MODEL)
        self.pinecone = PineconeService()
        self.groq = GroqService()

    def run(self, query: str):
        query_vector = self.embedder.embed(query)
        result  = self.pinecone.query(query_vector)
        context = [
            match["metadata"]["text"]
            for match in result.get("matches", [])
            if "metadata" in match and "text" in match["metadata"]
        ]
        
        answer = self.groq.ask(query, context)
        return answer, context
