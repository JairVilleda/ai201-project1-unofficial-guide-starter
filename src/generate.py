"""Answer generation for the Unofficial Guide RAG pipeline.

STEP 7 (final core step): given a question and the chunks retrieved from
ChromaDB, ask a Groq-hosted LLM to write an answer that is GROUNDED ONLY in
those chunks. This is the "G" in RAG.

Grounding is the whole point: the model must answer from the retrieved context
and refuse when the context is insufficient, instead of inventing facts from
its own training data.

This module does NOT do retrieval (that's src/retrieve.py) and does NOT build a
UI. It only turns (question + chunks) into an answer string.

Model: llama-3.3-70b-versatile (from planning.md), served by Groq.
"""

import os

from dotenv import load_dotenv
from groq import Groq

# Load variables from the local .env file into the process environment so
# os.environ can see GROQ_API_KEY. Keeping the key in .env (which is
# gitignored) avoids hard-coding secrets in source.
load_dotenv()

MODEL = "llama-3.3-70b-versatile"

# The system prompt sets the rules the model must follow for EVERY answer.
# We put the grounding rules here (not in the user turn) because system
# instructions carry the most weight and are harder for a question to override.
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
    """Join the retrieved chunk texts into a single context block.

    retrieved_chunks is the output of retrieve(): a list of dicts that each
    contain a "text" field. We separate chunks with a divider so the model can
    tell where one piece of source material ends and the next begins.
    """
    return "\n\n---\n\n".join(chunk["text"] for chunk in retrieved_chunks)


def build_user_prompt(question, context):
    """Assemble the user turn: the context followed by the question.

    The model is told (via the system prompt) to answer only from this context.
    """
    return (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer using only the context above."
    )


def generate_answer(question, retrieved_chunks):
    """Generate a grounded answer from the retrieved chunks.

    Args:
        question: The user's natural-language question (str).
        retrieved_chunks: Output of the retrieval pipeline -- a list of dicts
            with a "text" field.

    Returns:
        The model's answer as a string (no source attribution yet).
    """
    # Groq() reads GROQ_API_KEY from the environment automatically. We create
    # the client here so importing this module doesn't require a key to be set.
    client = Groq()

    context = build_context(retrieved_chunks)
    user_prompt = build_user_prompt(question, context)

    # chat.completions.create is Groq's main call. A few non-obvious params:
    #   messages   -> the conversation; "system" sets rules, "user" asks.
    #   temperature=0 -> make output as deterministic/factual as possible,
    #                    which suits a grounded Q&A assistant (less creativity).
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    # The reply text lives at choices[0].message.content. We strip surrounding
    # whitespace so the caller gets a clean string.
    return completion.choices[0].message.content.strip()
