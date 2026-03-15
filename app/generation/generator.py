import ollama


class Generator:

    def __init__(self, model="gpt-oss:20b"):
        self.model = model

    def build_prompt(self, context, question):

        prompt = f"""
You are a Wikipedia assistant.

Answer the question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided Wikipedia context."

Context:
{context}

Question:
{question}

Answer:
"""

        return prompt.strip()

    def generate(self, context, question):

        prompt = self.build_prompt(context, question)

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]