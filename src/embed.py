"""Generate embeddings for the document chunks."""

from pathlib import Path

from sentence_transformers import SentenceTransformer

from src.load import load_file
from src.clean import clean_text
from src.chunk import chunk_document

RAW_DIR = Path("data/raw")
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks():
    """Load, clean, and chunk every document in data/raw/."""
    chunks = []
    for path in sorted(RAW_DIR.glob("*.txt")):
        cleaned = clean_text(load_file(str(path)))
        chunks.extend(chunk_document(cleaned, source=path.name))
    return chunks


def load_model(model_name=MODEL_NAME):
    """Load the embedding model (kept separate so it can be loaded once and reused)."""
    return SentenceTransformer(model_name)


def embed_chunks(chunks, model):
    """Embed all chunk texts in one batched call. Returns a (n, dim) array."""
    texts = [c["text"] for c in chunks]
    return model.encode(texts, show_progress_bar=True)


def main():
    print("Loading chunks from the pipeline...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks.\n")

    print(f"Loading embedding model: {MODEL_NAME} ...")
    model = load_model()
    print("Model loaded.\n")

    print("Generating embeddings...")
    embeddings = embed_chunks(chunks, model)

    print("\n" + "=" * 50)
    print("EMBEDDING RESULTS")
    print("=" * 50)
    print(f"Total chunks embedded : {len(embeddings)}")
    print(f"Embedding dimension   : {embeddings.shape[1]}")
    print(f"Example embedding shape: {embeddings[0].shape}")


if __name__ == "__main__":
    main()
