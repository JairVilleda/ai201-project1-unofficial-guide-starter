"""Split cleaned text into overlapping word-based chunks.

Chunks are ~300 words with a 50-word overlap so ideas that fall near a
boundary stay intact in at least one chunk.
"""

import re

CHUNK_SIZE = 300
OVERLAP = 50


def source_to_label(source):
    """Derive a readable label from a filename, e.g. 'henry.txt' -> 'Henry'."""
    stem = source.rsplit(".", 1)[0]
    stem = re.sub(r"\d+$", "", stem)  # reddit4 -> reddit
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem.title()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split text into overlapping word windows.

    Returns a list of {"chunk_index", "text"}; empty chunks are dropped.
    """
    words = text.split()
    if not words:
        return []

    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    index = 0
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size]).strip()
        if chunk:
            chunks.append({"chunk_index": index, "text": chunk})
            index += 1
        # Stop once a window reaches the end so we don't emit a leftover
        # chunk made only of the overlap tail.
        if start + chunk_size >= len(words):
            break

    return chunks


def chunk_document(text, source, chunk_size=CHUNK_SIZE, overlap=OVERLAP, label=None):
    """Chunk a document, attach source metadata, and prepend the label.

    The label is added to the chunk text (not just metadata) because
    embeddings only see the text. Many reviews never repeat the professor's
    name, so prepending it lets name queries match those chunks.
    """
    if label is None:
        label = source_to_label(source)

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    for c in chunks:
        c["source"] = source
        c["label"] = label
        c["text"] = f"Source: {label}\n\n{c['text']}"
    return chunks
