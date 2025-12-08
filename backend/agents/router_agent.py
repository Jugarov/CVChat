from groq import Groq
import os
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

class RouterAgent:
    def __init__(self, registry):
        self.registry = registry
        self.client = Groq(api_key=GROQ_API_KEY)

    def route(self, question: str):
        cv_infos = [
            {
                "id": cv_id,
                "is_default": data["is_default"],
                "summary": data["summary"]
            }
            for cv_id, data in self.registry.agents.items()
        ]

        prompt = f"""
Eres un agente de ruteo que decide qué CV-agent debe ser consultado.
Debes devolver SIEMPRE un JSON válido con esta estructura:

{{
  "mode": "single|multi",
  "targets": ["id1", "id2"]
}}

El usuario hizo esta pregunta:
"{question}"

Los agentes disponibles son:
{json.dumps(cv_infos, indent=2)}

Reglas:
1. Si la pregunta no menciona persona explícita ni tiene intención comparativa:
   → usa el agente con "is_default": true.

2. Si menciona claramente una persona, elige SOLO ese agente.

3. Si es una pregunta comparativa, clasificatoria o que evalúa a múltiples personas:
   → usa TODOS los agentes relevantes.

4. Si menciona habilidades o características que deben buscarse entre varios CVs:
   → usa modo "multi".

Devuelve únicamente el JSON, sin texto adicional.
"""

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.choices[0].message.content.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # fallback seguro
            default = self.registry.get_default()
            return {"mode": "single", "targets": [default]}