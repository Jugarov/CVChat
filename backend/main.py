from fastapi import FastAPI
from rag_pipeline import RagPipeline
from pydantic import BaseModel

app = FastAPI()
rag = RagPipeline()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    context: list[str]

@app.post("/api/ask", response_model=QueryResponse)
def ask_question(req: QueryRequest):
    answer, context = rag.run(req.query)
    return QueryResponse(answer=answer, context=context)
