from groq import Groq
import os

GROQ_MODEL = os.getenv("GROQ_MODEL")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

class FusionAgent:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def fuse(self, question, results):
        formatted = "\n".join(
            f"=== {name.upper()} ===\nRespuesta:\n{val['answer']}"
            for name, val in results.items()
        )

        prompt = f"""
Eres un agente experto que combina información desde múltiples agentes.
La pregunta del usuario es:

{question}

Respuestas obtenidas desde los agentes especializados:
{formatted}

Produce un análisis comparativo claro, corto y basado SOLO en estos datos.
"""

        resp = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        return resp.choices[0].message.content.strip()
