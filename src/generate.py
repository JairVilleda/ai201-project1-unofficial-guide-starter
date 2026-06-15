"""Generate a grounded answer from retrieved chunks using Groq."""

from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # read GROQ_API_KEY from .env

MODEL = "llama-3.3-70b-versatile"

# Grounding rules live in the system prompt so they're harder to override.
SYSTEM_PROMPT = (
    "You are the GSU CS Advisor, a question-answering assistant about Georgia "
    "State University's Computer Science program, courses, and professors.\n"
    "Follow these rules strictly:\n"
    "1. Use ONLY the information in the provided context. \n"
    "2. Do NOT use any outside knowledge or make assumptions.\n"
    "3. If the context does not contain enough information to answer, respond "
    "with EXACTLY this sentence and nothing else: "
    "\"I don't have enough information on that.\"\n"
    "4. Answer clearly and concisely."
)


def build_context(retrieved_chunks):
    """Join chunk texts into one context block, divided so sources stay distinct."""
    return "\n\n---\n\n".join(chunk["text"] for chunk in retrieved_chunks)


def build_user_prompt(question, context):
    return (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above."
    )


def generate_answer(question, retrieved_chunks):
    """Return a grounded answer string for the question (no source attribution)."""
    client = Groq()  # reads GROQ_API_KEY from the environment

    context = build_context(retrieved_chunks)
    user_prompt = build_user_prompt(question, context)

    # temperature=0 keeps answers deterministic and close to the context.
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return completion.choices[0].message.content.strip()
