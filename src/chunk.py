"""Document chunking for the Unofficial Guide RAG pipeline.

STEP 3 of the pipeline: split cleaned text into overlapping word-based chunks.

Chunking strategy (from planning.md):
  - ~300 words per chunk
  - 50-word overlap between consecutive chunks

Why overlap? A key idea (e.g. "Prof. Johnson is fair but the labs are hard")
can land right on a chunk boundary. Overlapping the last 50 words of one chunk
into the start of the next keeps such ideas intact in at least one chunk, which
improves retrieval later.

This step does NOT embed, store, or retrieve. It only splits text.
Standard library only.
"""

import re

CHUNK_SIZE = 300   # target words per chunk
OVERLAP = 50       # words shared between consecutive chunks


def source_to_label(source):
    """Turn a source filename into a human-readable label.

    Most professor files are named after the professor's surname
    (e.g. "henry.txt" -> "Henry"). Other sources are named by type with a
    trailing number (e.g. "reddit4.txt" -> "Reddit", "gsu2.txt" -> "Gsu").

    The transformation: drop the extension, drop a trailing run of digits,
    swap separators for spaces, and title-case.

    Args:
        source: A filename like "henry.txt" or "ratemyprofessors8.txt".

    Returns:
        A readable label like "Henry" or "Ratemyprofessors".
    """
    stem = source.rsplit(".", 1)[0]          # drop the ".txt" extension
    stem = re.sub(r"\d+$", "", stem)         # drop trailing digits (reddit4 -> reddit)
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem.title()


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """Split text into overlapping word-based chunks.

    The text is split on whitespace into words, then a window of `chunk_size`
    words slides across them, advancing by `chunk_size - overlap` each time so
    consecutive chunks share `overlap` words.

    Args:
        text: Cleaned document text.
        chunk_size: Target number of words per chunk.
        overlap: Number of words each chunk shares with the previous one.

    Returns:
        A list of dicts, one per chunk:
            {"chunk_index": int, "text": str}
        Empty/whitespace-only chunks are filtered out. The source filename is
        attached later by chunk_document() so this function stays text-only.
    """
    words = text.split()  # splits on any whitespace, drops empty tokens
    if not words:
        return []

    step = chunk_size - overlap  # how far the window advances each iteration
    if step <= 0:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    index = 0
    for start in range(0, len(words), step):
        window = words[start:start + chunk_size]
        chunk = " ".join(window).strip()
        if chunk:  # filter out empty chunks
            chunks.append({"chunk_index": index, "text": chunk})
            index += 1
        # If this window already reached the end, stop (avoids a trailing
        # duplicate chunk made only of the overlap tail).
        if start + chunk_size >= len(words):
            break

    return chunks


def chunk_document(text, source, chunk_size=CHUNK_SIZE, overlap=OVERLAP, label=None):
    """Chunk one document, attach metadata, and inject the source label.

    Two things happen on top of plain chunking:

      1. Metadata: each chunk records its source filename, label, and index --
         the information retrieval needs to cite where an answer came from.

      2. Name injection: the label (e.g. "Henry") is prepended to each chunk's
         TEXT. This matters because embeddings encode the chunk text, not the
         metadata. Many RateMyProfessors reviews never repeat the professor's
         name -- it only lived in the filename -- so a query like "What do
         students say about Professor Henry?" would not match those chunks.
         Prepending "Source: Henry" puts the name into the embeddable text so
         such queries retrieve the right chunks.

    Injection happens AFTER windowing, so it does not affect the 300-word
    chunk boundaries -- it only adds a short prefix line to each finished chunk.

    Args:
        text: Cleaned document text.
        source: Source filename (e.g. "reddit4.txt").
        label: Optional human-readable label to inject. Defaults to one
            derived from the filename via source_to_label().

    Returns:
        A list of dicts:
            {"source": str, "label": str, "chunk_index": int, "text": str}
        where "text" begins with a "Source: <label>" line.
    """
    if label is None:
        label = source_to_label(source)

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    for c in chunks:
        c["source"] = source
        c["label"] = label
        c["text"] = f"Source: {label}\n\n{c['text']}"
    return chunks
