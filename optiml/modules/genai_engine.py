# # LangChain + LLM integration

# from langchain import PromptTemplate, LLMChain
# # from langchain_openai import ChatOpenAI    # example

# def build_financial_prompt(question: str, context: str) -> str:
#     template = """
#     You are a financial assistant. Use the given data to answer.

#     Context:
#     {context}

#     Question:
#     {question}

#     Answer in simple language, short and clear.
#     """
#     prompt = template.format(context=context, question=question)
#     return prompt

# def get_genai_answer(question: str, context: str) -> str:
#     prompt = build_financial_prompt(question, context)
#     # llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)
#     # response = llm.invoke(prompt)
#     # return response.content
#     return "GenAI response here (connect LLM in real implementation)."


# modules/genai_engine.py

# """
# Simple placeholder for GenAI answer.

# Right now it does NOT call a real LLM.
# You can later integrate LangChain + OpenAI / any LLM here.
# """
# from langchain.prompts import PromptTemplate


# def generate_ai_answer(question: str, context: str) -> str:
#     # Very simple logic just to show something on UI
#     response = (
#         "This is a demo AI explanation.\n\n"
#         f"Your question:\n{question}\n\n"
#         f"Available data/context:\n{context}\n\n"
#         "In a real deployment, this function will send the context and question "
#         "to a Generative AI model (via LangChain) and return a proper financial explanation."
#     )
#     return response

# modules/genai_engine.py

# """
# Temporary simple AI logic — this avoids LangChain entirely.
# No imports from LangChain, OpenAI, or any LLM.
# This is safe and will never cause ImportError.
# """

# def generate_ai_answer(question: str, context: str) -> str:
#     # Simple placeholder logic for demo
#     return (
#         "📘 **AI Financial Insight (Demo Mode)**\n\n"
#         f"**Your Question:** {question}\n\n"
#         f"**Based on Data:** {context}\n\n"
#         "📝 *This is a mock response. In the real project, this function will connect to an AI model "
#         "to generate detailed insights.*"
#     )


# modules/genai_engine.py

import os
from groq import Groq

# Read key from environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Initialise client only if key is set
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


SYSTEM_PROMPT = """You are a financial analysis assistant.
You receive:
- A natural language question from a user.
- Structured context containing metrics (returns, volatility, risk etc.).

Rules:
- Answer in simple, clear English.
- Do NOT give trading tips like 'buy' or 'sell'. Just explain risk/return.
- Keep answers short: 4–7 lines.
"""


def build_context_text(metrics: dict) -> str:
    """
    Convert metrics/context dictionary into a readable text block
    to send to the LLM.
    """
    if not metrics:
        return "No numeric metrics were provided."

    lines = []
    for key, value in metrics.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def generate_ai_answer(question: str, context_dict: dict | None = None) -> str:
    """
    Call Groq LLM (Llama 3.x) to generate an answer based on
    the user question + numeric context.

    If GROQ_API_KEY is not configured, returns a safe fallback message.
    """
    if client is None:
        return (
            "⚠️ AI is not fully configured yet (GROQ_API_KEY missing).\n"
            "Ask your developer to set the GROQ_API_KEY environment variable."
        )

    context_text = build_context_text(context_dict or {})

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # recommended Groq chat model :contentReference[oaicite:1]{index=1}
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"User question:\n{question}\n\n"
                        f"Available financial context:\n{context_text}"
                    ),
                },
            ],
            temperature=0.2,
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Error while calling Groq API: {e}"
