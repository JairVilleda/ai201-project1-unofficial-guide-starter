"""Retrieve the chunks most relevant to a query, plus an evaluation harness."""

import chromadb

from src.embed import load_model

# Must match what vector_store.py wrote.
PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "gsu_cs_chunks"

# Cached at module level so repeated retrieve() calls don't reload the model.
_model = None
_collection = None


def _get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


def _get_collection():
    # get_collection (not get_or_create): the index must already exist.
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        _collection = client.get_collection(name=COLLECTION_NAME)
    return _collection


def retrieve(query: str, k: int = 5):
    """Return the top-k chunks for `query`, closest first.

    Each hit is {"distance", "source", "chunk_index", "text"}.
    """
    model = _get_model()
    collection = _get_collection()

    # The query must use the same model as the stored vectors, or distances
    # are meaningless. tolist() because Chroma wants plain lists, not numpy.
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    # Chroma returns one inner list per query; we sent one, so read index [0].
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


# Evaluation questions from planning.md. Each topic lists keyword variants;
# a topic is "found" if any keyword appears in the retrieved text. This is a
# rough keyword check to speed up review, not a semantic judge.
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
    """Split topics into (found, missing) by keyword presence in the hits."""
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

    for i, h in enumerate(hits, start=1):
        print(f"Result {i}")
        print(f"Distance:    {h['distance']:.4f}")
        print(f"Source:      {h['source']}")
        print(f"Chunk Index: {h['chunk_index']}")
        print("Chunk Text:")
        print(h["text"])
        print("-" * 50)

    if topics:
        found, missing = evaluate_topics(topics, hits)
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
    for item in EVAL:
        run_query(item["query"], topics=item["topics"], k=5)


if __name__ == "__main__":
    main()
