"""End-to-end evaluation of the GSU CS Advisor RAG pipeline.

Runs a fixed set of questions through the existing ask() function and prints
each answer, its sources, and a few automatic observations. It does NOT modify
retrieval, generation, or attribution -- it only calls ask() and inspects the
returned dict.

Run from the project root:
    python evaluate_rag.py
"""

from src.rag import ask

# The exact sentence the system must return when it cannot answer. We compare
# against this verbatim to check the out-of-scope refusal.
REFUSAL = "I don't have enough information on that."

# Each item: the question, and whether we EXPECT the system to refuse it.
QUESTIONS = [
    {"q": "What do students say about the quality of Georgia State "
          "University's Computer Science program?", "out_of_scope": False},
    {"q": "What issues do students report about Tushara Sadasivuni's "
          "Software Development class?", "out_of_scope": False},
    {"q": "Which CS professor is most consistently praised in student "
          "discussions, and what qualities are mentioned?", "out_of_scope": False},
    {"q": "What are the main requirements students must complete before they "
          "can take upper-level CS courses (CSC 2720 and above)?", "out_of_scope": False},
    {"q": "What are two advanced CS elective topics listed in the catalog?",
     "out_of_scope": False},
    {"q": "Who is the current dean of Georgia State University's College of "
          "Arts and Sciences?", "out_of_scope": True},
]


def run_one(item):
    """Run a single question through ask() and print results + observations."""
    question = item["q"]
    result = ask(question)
    answer = result["answer"]
    sources = result["sources"]

    # --- required output block ---
    print("=" * 50)
    print("Question:")
    print(question)
    print()
    print("Answer:")
    print(answer)
    print()
    print("Sources:")
    for source in sources:
        print(f"- {source}")
    print()

    # --- observations ---
    is_refusal = answer.strip() == REFUSAL
    cited = len(sources) > 0

    print("Observations:")
    if item["out_of_scope"]:
        # For the out-of-scope question, the ONLY correct behavior is the exact
        # refusal sentence. Note: retrieval still returns 5 nearest chunks, so
        # `sources` is non-empty even on a refusal -- those chunks were fetched
        # but NOT used, since the model correctly declined to answer.
        passed = "PASS" if is_refusal else "FAIL"
        print(f"- Correctly returned the exact refusal sentence? {passed}")
        if not is_refusal:
            print("    (Expected exactly: \"" + REFUSAL + "\")")
        print("- Note: sources shown were retrieved but not used (answer refused).")
    else:
        # For in-scope questions: grounded answer + at least one source.
        grounded = not is_refusal  # heuristic: it produced a real answer
        print(f"- Answer appears grounded (not a refusal)? "
              f"{'Yes' if grounded else 'No'}")
        print(f"- Cited at least one source? {'Yes' if cited else 'No'}")

    print("=" * 50)
    print()


def main():
    for item in QUESTIONS:
        run_one(item)


if __name__ == "__main__":
    main()
