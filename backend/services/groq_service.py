from groq import Groq
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    def __clean_answer(self, text: str) -> str:
        return text.strip()

    def ask(self, query, context):
        context_text = "\n\n".join(context)

        prompt = f"""
Eres un chatbot especializado en hablar sobre el CV proporcionado.
Usa solo la siguiente información del CV para responder.

Contexto:
{context_text}

Pregunta del usuario:
{query}

Respuesta:
"""

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        response_text = response.choices[0].message.content
        response_text = self.__clean_answer(response_text)

        return response_text
