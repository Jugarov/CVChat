from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str):
        return self.model.encode(text).tolist()
