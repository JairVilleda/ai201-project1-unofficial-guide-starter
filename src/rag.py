"""Tie retrieval, generation, and source attribution into a single ask() call."""

from src.retrieve import retrieve
from src.generate import generate_answer


def _unique_sources(retrieved_chunks):
    """Source filenames in retrieval order, de-duplicated."""
    seen = set()
    ordered = []
    for chunk in retrieved_chunks:
        source = chunk["source"]
        if source not in seen:
            seen.add(source)
            ordered.append(source)
    return ordered


def ask(question):
    """Answer a question and list the source files behind it.

    Sources come from chunk metadata, not the model, so they always reflect
    the chunks the answer was generated from.

    Returns {"answer": str, "sources": [filename, ...]}.
    """
    retrieved_chunks = retrieve(question, k=5)
    answer = generate_answer(question, retrieved_chunks)
    sources = _unique_sources(retrieved_chunks)
    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
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
