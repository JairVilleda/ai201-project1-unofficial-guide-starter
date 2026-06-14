"""Vector storage for the Unofficial Guide RAG pipeline.

STEP 5 of the pipeline: persist every chunk's embedding (plus its text and
metadata) into a local ChromaDB database. Once stored, vectors survive between
runs, so later stages can search by meaning without re-embedding everything.

This step does NOT query, retrieve, or generate. It only writes to ChromaDB.

It reuses the existing pipeline functions instead of re-implementing them:
    load_chunks()  -> load + clean + chunk all docs   (from src.embed)
    load_model()   -> SentenceTransformer model        (from src.embed)
    embed_chunks() -> embeddings for the chunks         (from src.embed)
"""

from pathlib import Path

import chromadb

from src.embed import load_chunks, load_model, embed_chunks

# Where ChromaDB keeps its files on disk. Using a fixed folder makes the
# database "persistent": it is written once and reused on later runs.
PERSIST_DIR = "chroma_db"

# Name of the collection (think: a table) that holds our chunks.
COLLECTION_NAME = "gsu_cs_chunks"


def build_chunk_id(chunk):
    """Build a deterministic ID for a chunk: '<source-stem>_<chunk_index>'.

    Example: source "henry.txt", chunk_index 0  ->  "henry_0".

    Deterministic IDs matter because they let us re-run this script and have
    each chunk overwrite its own previous entry (via upsert) instead of
    creating duplicates. The ID is unique because filenames are unique and
    chunk_index is unique within a file.
    """
    stem = Path(chunk["source"]).stem  # "henry.txt" -> "henry"
    return f"{stem}_{chunk['chunk_index']}"


def main():
    # --- 1. Rebuild chunks and embeddings from the existing pipeline ---
    # We do NOT re-implement loading/cleaning/chunking/embedding here; we call
    # the functions we already verified so behavior stays consistent.
    print("Building chunks from the pipeline...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.")

    print("Loading embedding model and generating embeddings...")
    model = load_model()
    embeddings = embed_chunks(chunks, model)
    print(f"Generated embeddings of shape {embeddings.shape}.\n")

    # --- 2. Open a persistent ChromaDB client ---
    # PersistentClient writes the database to PERSIST_DIR on disk. (An
    # in-memory Client() would lose everything when the script exits.)
    print(f"Opening persistent ChromaDB at ./{PERSIST_DIR} ...")
    client = chromadb.PersistentClient(path=PERSIST_DIR)

    # --- 3. Get (or create) the collection ---
    # get_or_create_collection is idempotent: it creates the collection the
    # first time and reuses it afterward, so re-running doesn't error out.
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # --- 4. Prepare the four parallel lists ChromaDB's API expects ---
    # ChromaDB.add/upsert takes ids, embeddings, documents, and metadatas as
    # separate lists where index i of each describes the same chunk.
    ids = [build_chunk_id(c) for c in chunks]
    documents = [c["text"] for c in chunks]                # the chunk text
    metadatas = [                                          # citation metadata
        {"source": c["source"], "chunk_index": c["chunk_index"]}
        for c in chunks
    ]
    # model.encode returns a numpy array; ChromaDB wants plain Python lists.
    embedding_list = embeddings.tolist()

    # --- 5. Write the chunks into the collection ---
    # upsert (rather than add) means: insert new IDs, overwrite existing ones.
    # Combined with deterministic IDs, this makes the script safe to re-run.
    print("Storing chunks in ChromaDB...")
    collection.upsert(
        ids=ids,
        embeddings=embedding_list,
        documents=documents,
        metadatas=metadatas,
    )

    # --- 6. Verification output ---
    print("\n" + "=" * 50)
    print("VECTOR STORE RESULTS")
    print("=" * 50)
    print(f"Chunks inserted : {len(ids)}")
    # collection.count() asks ChromaDB how many items it actually holds.
    print(f"Collection count: {collection.count()}")

    # Fetch one stored item back to confirm text + metadata round-tripped.
    example = collection.get(ids=[ids[0]])
    print(f"\nExample ID       : {example['ids'][0]}")
    print(f"Example metadata : {example['metadatas'][0]}")
    preview = example["documents"][0][:200]
    print(f"Example document : {preview}...")


if __name__ == "__main__":
    main()
