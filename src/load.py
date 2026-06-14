"""Document loading for the Unofficial Guide RAG pipeline.

STEP 1 of the pipeline: load raw documents from disk.
Cleaning, chunking, embeddings, and retrieval come later.
"""


def load_file(path: str) -> str:
    """Read a UTF-8 text file from disk and return its raw contents.

    Args:
        path: Path to a .txt file.

    Returns:
        The file's full contents as a string, unmodified.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
