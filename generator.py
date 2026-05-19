import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("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"))

def generate_answer(query, context):
    try:
        prompt = f"""
You are a customer support assistant.

Context:
{context}

Question:
{query}

Answer clearly:
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ LLM Error:", e)
        return None   # IMPORTANT CHANGE