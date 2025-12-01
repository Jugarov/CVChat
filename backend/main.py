from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import RagPipeline
from pydantic import BaseModel

app = FastAPI()
rag = RagPipeline()

# === AGREGAR CORS para prevenir errores de POST ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    context: list[str]

@app.post("/api/ask", response_model=QueryResponse)
def ask_question(req: QueryRequest):
    answer, context = rag.run(req.query)
    return QueryResponse(answer=answer, context=context)
