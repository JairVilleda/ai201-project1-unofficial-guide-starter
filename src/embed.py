"""Embedding generation for the Unofficial Guide RAG pipeline.

STEP 4 of the pipeline: turn each text chunk into a dense vector (embedding)
using a sentence-transformers model. These vectors are what a vector database
(ChromaDB, next step) will index so we can find chunks by meaning rather than
keywords.

Embedding model (from planning.md): all-MiniLM-L6-v2
  - small, fast, runs on CPU
  - produces 384-dimensional vectors
  - a strong default for semantic search on short English text like reviews

This step does NOT store vectors in ChromaDB, retrieve, or generate. It only
loads chunks and computes their embeddings.
"""

from pathlib import Path

from sentence_transformers import SentenceTransformer

from src.load import load_file
from src.clean import clean_text
from src.chunk import chunk_document

RAW_DIR = Path("data/raw")
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks():
    """Rebuild the full list of chunks from the existing pipeline.

    Runs the same load -> clean -> chunk steps we verified earlier across every
    .txt file in data/raw/. We rebuild here (rather than read from a saved file)
    so embeddings always reflect the current documents and chunking logic.

    Returns:
        A flat list of chunk dicts: {"source", "label", "chunk_index", "text"}.
    """
    chunks = []
    for path in sorted(RAW_DIR.glob("*.txt")):
        cleaned = clean_text(load_file(str(path)))
        chunks.extend(chunk_document(cleaned, source=path.name))
    return chunks


def load_model(model_name=MODEL_NAME):
    """Load the sentence-transformers embedding model.

    SentenceTransformer downloads the model weights the first time it runs and
    caches them locally, so later runs are fast. We isolate this in its own
    function because loading the model is the slow part -- callers can load it
    once and reuse it for many encode() calls.

    Returns:
        A ready-to-use SentenceTransformer model.
    """
    return SentenceTransformer(model_name)


def embed_chunks(chunks, model):
    """Generate an embedding vector for every chunk's text.

    We pass all chunk texts to model.encode() in one call so the library can
    batch them efficiently. The result is a 2D array of shape
    (number_of_chunks, embedding_dimension).

    Args:
        chunks: List of chunk dicts (must contain a "text" field).
        model: A loaded SentenceTransformer.

    Returns:
        A numpy array of embeddings, one row per chunk.
    """
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings


def main():
    print("Loading chunks from the pipeline...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.\n")

    print(f"Loading embedding model: {MODEL_NAME} ...")
    model = load_model()
    print("Model loaded.\n")

    print("Generating embeddings...")
    embeddings = embed_chunks(chunks, model)

    # --- verification output ---
    print("\n" + "=" * 50)
    print("EMBEDDING RESULTS")
    print("=" * 50)
    print(f"Total chunks embedded : {len(embeddings)}")
    print(f"Embedding dimension   : {embeddings.shape[1]}")
    print(f"Example embedding shape: {embeddings[0].shape}")


if __name__ == "__main__":
    main()
