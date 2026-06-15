"""End-to-end RAG orchestration for the Unofficial Guide pipeline.

This module ties the existing stages together into one call:

    retrieve(question, k=5)  ->  generate_answer(...)  ->  {answer, sources}

It deliberately does NOT change retrieval or generation. It only:
  - runs them in order, and
  - attaches source attribution built from RETRIEVAL METADATA (never from the
    LLM), so citations are guaranteed to reflect the chunks actually used.

No UI here -- ask() returns a plain dict that a Gradio interface (next step)
can render however it likes.
"""

from src.retrieve import retrieve
from src.generate import generate_answer


def _unique_sources(retrieved_chunks):
    """Return source filenames in retrieval order, with duplicates removed.

    Several of the top-5 chunks often come from the same file (e.g. multiple
    'henry.txt' chunks). We want each file listed once, in the order it first
    appeared in the ranking. A set alone would lose that order, so we track
    'seen' separately and build the list manually.
    """
    seen = set()
    ordered = []
    for chunk in retrieved_chunks:
        source = chunk["source"]          # exactly as stored in metadata
        if source not in seen:
            seen.add(source)
            ordered.append(source)
    return ordered


def ask(question):
    """Answer a question and report which source files backed the answer.

    Steps:
      1. Retrieve the top-5 most relevant chunks.
      2. Generate a grounded answer from exactly those chunks.
      3. Derive the source list from the chunks' metadata (not the LLM).

    Returns:
        {"answer": <str>, "sources": [<filename>, ...]}
    """
    # 1. Retrieval (unchanged logic, k=5 default).
    retrieved_chunks = retrieve(question, k=5)

    # 2. Generation (unchanged logic). It receives the same chunks we attribute,
    #    so the answer and the sources describe the same evidence.
    answer = generate_answer(question, retrieved_chunks)

    # 3. Source attribution, derived programmatically from metadata.
    sources = _unique_sources(retrieved_chunks)

    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    # Small manual test. Uses one evaluation question from planning.md.
    question = (
        "What issues do students report about Tushara Sadasivuni's "
        "Software Development class?"
    )
    result = ask(question)

    print("Question:")
    print(question)
    print()
    print("Answer:")
    print(result["answer"])
    print()
    print("Sources:")
    for source in result["sources"]:
        print(f"- {source}")
