"""Retrieval for the Unofficial Guide RAG pipeline.

STEP 6 of the pipeline: given a natural-language question, find the chunks in
ChromaDB whose meaning is closest to the question. This is the "R" in RAG --
it selects the context that a generator would later use.

This file does NOT generate answers. It only embeds the query, searches the
vector store, and reports/evaluates what comes back.

It reuses existing pipeline pieces:
    load_model()    -> the SAME SentenceTransformer used to build the index
    "gsu_cs_chunks" -> the persistent ChromaDB collection we already populated
"""

import chromadb

from src.embed import load_model

# Must match what src/vector_store.py used, or retrieval would hit the wrong
# database / collection.
PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "gsu_cs_chunks"

# The query must be embedded by the SAME model that produced the stored
# vectors, otherwise the numbers live in different "spaces" and distances are
# meaningless. We cache the model at module level so repeated retrieve() calls
# don't reload it (loading is the slow part).
_model = None
_collection = None


def _get_model():
    """Lazily load and cache the embedding model."""
    global _model
    if _model is None:
        _model = load_model()
    return _model


def _get_collection():
    """Lazily open the persistent ChromaDB collection and cache it.

    We use get_collection (not get_or_create) because the collection must
    already exist -- this stage reads, it never builds the index.
    """
    global _collection
    if _collection is None:
        # PersistentClient points at the on-disk database we wrote earlier.
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        _collection = client.get_collection(name=COLLECTION_NAME)
    return _collection


def retrieve(query: str, k: int = 5):
    """Return the top-k chunks most relevant to `query`.

    Steps:
      1. Embed the query with the same model used for the chunks.
      2. Ask ChromaDB for the k nearest stored vectors.
      3. Repackage the results into a simple list of dicts.

    Returns:
        A list of dicts: {"distance", "source", "chunk_index", "text"},
        ordered from most relevant (smallest distance) to least.
    """
    model = _get_model()
    collection = _get_collection()

    # encode() expects a list and returns a 2D array; we pass [query] and take
    # the resulting single embedding. .tolist() converts numpy -> plain list,
    # which is what ChromaDB's query API accepts.
    query_embedding = model.encode([query]).tolist()

    # collection.query finds the nearest neighbors to our query vector.
    # n_results=k limits how many chunks come back. We ask for documents,
    # metadatas, and distances so we can print and evaluate each hit.
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    # ChromaDB returns results as lists-of-lists (one inner list per query).
    # We sent one query, so we read index [0] of each field and zip them.
    hits = []
    for distance, document, metadata in zip(
        results["distances"][0],
        results["documents"][0],
        results["metadatas"][0],
    ):
        hits.append(
            {
                "distance": distance,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "text": document,
            }
        )
    return hits


# --- Evaluation harness -------------------------------------------------------
#
# Each question lists the expected TOPICS from planning.md. For every topic we
# give a few lowercase keyword variants. A topic counts as "found" if ANY of
# its keywords appears in the combined retrieved text.
#
# IMPORTANT: this is a keyword heuristic to make eyeballing faster -- it is NOT
# a semantic judge. Read the actual chunk text before trusting the Yes/No.

EVAL = [
    {
        "query": "What do students say about the quality of Georgia State "
                 "University's Computer Science program?",
        "topics": {
            "Better than its reputation": ["not as bad", "better than", "reputation", "decent", "not that bad"],
            "Success depends on personal effort": ["effort", "put in", "what you make", "give a", "study"],
            "Office hours / research / internships matter": ["office hours", "research", "internship", "career fair"],
            "Upper-level professors are better": ["get better", "higher level", "upper level", "higher-level"],
            "Good prep for SWE careers": ["swe", "software engineer", "prepared", "job", "good paying"],
        },
    },
    {
        "query": "What issues do students report about Tushara Sadasivuni's "
                 "Software Development class?",
        "topics": {
            "Disorganized class": ["disorganiz", "unorganiz", "all over"],
            "Reads from slides": ["slides", "read", "powerpoint", "zybook"],
            "Hard labs without Java experience": ["lab", "java"],
            "Missing / unclear instructions": ["instruction", "unclear", "vague", "missing", "confusing"],
            "TA issues / inconsistent guidance": [" ta ", "ta's", "tas ", "teaching assistant"],
        },
    },
    {
        "query": "Which CS professor is most consistently praised in student "
                 "discussions, and what qualities are mentioned?",
        "topics": {
            "William Johnson": ["johnson"],
            "Passionate": ["passion"],
            "Caring": ["caring", "cares", "care about"],
            "Fair": ["fair"],
            "Effective teacher": ["effective", "great teacher", "good teacher", "best prof", "great prof"],
        },
    },
    {
        "query": "What are the main requirements students must complete before "
                 "they can take upper-level CS courses (CSC 2720 and above)?",
        "topics": {
            "C or higher in CSC 1301 / 1301L": ["1301"],
            "CSC 2510 or MATH 2420": ["2510", "2420"],
            "A required math course": ["math 1113", "1113", "2211", "2212", "2215"],
            "2.5 GPA across required courses": ["2.5", "gpa"],
        },
    },
    {
        "query": "What are two advanced CS elective topics listed in the catalog?",
        "topics": {
            "Artificial Intelligence (CSC 4810)": ["4810", "artificial intelligence"],
            "Machine Learning (CSC 4850)": ["4850", "machine learning"],
            "Cloud Computing (CSC 4311)": ["4311", "cloud computing"],
            "Big Data Programming (CSC 4760)": ["4760", "big data"],
        },
    },
]


def evaluate_topics(topics, hits):
    """Split expected topics into (found, missing) by keyword presence.

    Combines all retrieved chunk text into one lowercase blob, then checks each
    topic's keyword list against it.
    """
    blob = " ".join(h["text"] for h in hits).lower()
    found, missing = [], []
    for topic, keywords in topics.items():
        if any(kw in blob for kw in keywords):
            found.append(topic)
        else:
            missing.append(topic)
    return found, missing


def run_query(query, topics=None, k=5):
    """Retrieve for one query, print every hit, then print a topic summary."""
    hits = retrieve(query, k=k)

    print("=" * 50)
    print("Query:")
    print(query)
    print()

    # Print each retrieved chunk in the required format.
    for i, h in enumerate(hits, start=1):
        print(f"Result {i}")
        print(f"Distance:    {h['distance']:.4f}")
        print(f"Source:      {h['source']}")
        print(f"Chunk Index: {h['chunk_index']}")
        print("Chunk Text:")
        print(h["text"])
        print("-" * 50)

    # Topic-level relevance summary.
    if topics:
        found, missing = evaluate_topics(topics, hits)
        # "Relevant" = at least one expected topic surfaced in the results.
        relevant = "Yes" if found else "No"
        print("\nSUMMARY")
        print(f"Retrieved chunks appear relevant? {relevant}")
        print(f"Topics FOUND ({len(found)}):")
        for t in found:
            print(f"  + {t}")
        print(f"Topics MISSING ({len(missing)}):")
        for t in missing:
            print(f"  - {t}")
    print("=" * 50 + "\n")


def main():
    # Run all five evaluation questions from planning.md.
    for item in EVAL:
        run_query(item["query"], topics=item["topics"], k=5)


if __name__ == "__main__":
    main()
