from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.agent_registry import AgentRegistry
from agents.router_agent import RouterAgent
from agents.fusion_agent import FusionAgent

app = FastAPI()
registry = AgentRegistry()


registry.register(
    cv_id="Juan",
    aliases= ["juan ignacio garcia", "juan garcia", "juan"],
    summary="Data Scientist con experiencia en NLP, RAG y LLMs.",
    namespace="cv-juan",
    is_default=True
)

registry.register(
    cv_id="Rodrigo",
    aliases= ["rodrigo mesa", "rodrigo mesa marchi", "rodrigo", "rodri"],
    summary="Data Engineer con experiencia en Databricks.",
    namespace="cv-rodri"
)

registry.register(
    cv_id="Danilo",
    aliases= ["danilo reitano", "danilo", "dani"],
    summary="Software Engineer con experiencia en desarrollo fullstack.",
    namespace="cv-dani"
)

router = RouterAgent(registry)
fusion = FusionAgent()

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

    routing = router.route(req.query)
    mode = routing["mode"]
    targets = routing["targets"]

    if mode == "single":
        cv_id = targets[0]
        agent = registry.get(cv_id)
        answer, context = agent.ask(req.query)
        return QueryResponse(answer=answer, context=context)

    # mode == "multi"
    results = {}
    for cv_id in targets:
        agent = registry.get(cv_id)
        answer, context = agent.ask(req.query)
        results[cv_id] = {"answer": answer, "context": context}

    fused = fusion.fuse(req.query, results)

    merged_ctx = []
    for r in results.values():
        merged_ctx.extend(r["context"])

    return QueryResponse(answer=fused, context=merged_ctx)
