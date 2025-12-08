from rag_pipeline import RagPipeline

class CVAgent:
    def __init__(self, cv_id, namespace):
        self.cv_id = cv_id
        self.namespace = namespace
        self.pipeline = RagPipeline(namespace)

    def ask(self, question):
        return self.pipeline.run(question)