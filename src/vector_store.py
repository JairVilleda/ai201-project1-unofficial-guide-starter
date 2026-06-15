"""Store chunk embeddings, text, and metadata in a persistent ChromaDB collection."""

from pathlib import Path

import chromadb

from src.embed import load_chunks, load_model, embed_chunks

PERSIST_DIR = "chroma_db"
COLLECTION_NAME = "gsu_cs_chunks"


def build_chunk_id(chunk):
    """Stable per-chunk id like 'henry_0' so re-runs overwrite instead of duplicate."""
    stem = Path(chunk["source"]).stem
    return f"{stem}_{chunk['chunk_index']}"


def main():
    print("Building chunks from the pipeline...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.")

    print("Loading embedding model and generating embeddings...")
    model = load_model()
    embeddings = embed_chunks(chunks, model)
    print(f"Generated embeddings of shape {embeddings.shape}.\n")

    # PersistentClient writes to disk so the index survives between runs.
    print(f"Opening persistent ChromaDB at ./{PERSIST_DIR} ...")
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    # Chroma takes ids, embeddings, documents, and metadatas as aligned lists.
    ids = [build_chunk_id(c) for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {"source": c["source"], "chunk_index": c["chunk_index"]}
        for c in chunks
    ]
    embedding_list = embeddings.tolist()

    # upsert + stable ids makes this safe to re-run.
    print("Storing chunks in ChromaDB...")
    collection.upsert(
        ids=ids,
        embeddings=embedding_list,
        documents=documents,
        metadatas=metadatas,
    )

    print("\n" + "=" * 50)
    print("VECTOR STORE RESULTS")
    print("=" * 50)
    print(f"Chunks inserted : {len(ids)}")
    print(f"Collection count: {collection.count()}")

    # Read one back to confirm text + metadata round-tripped.
    example = collection.get(ids=[ids[0]])
    print(f"\nExample ID       : {example['ids'][0]}")
    print(f"Example metadata : {example['metadatas'][0]}")
    print(f"Example document : {example['documents'][0][:200]}...")


if __name__ == "__main__":
    main()
