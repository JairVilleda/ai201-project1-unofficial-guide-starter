"""Verify loading, cleaning, and chunking across the whole corpus.

Run from the project root:
    python pipeline_test.py
"""

import random
from pathlib import Path

from src.load import load_file
from src.clean import clean_text
from src.chunk import chunk_document

RAW_DIR = Path("data/raw")

# Flag a file if cleaning removes more than this fraction of it (it should
# only strip whitespace and entities, so a big drop is suspicious).
LARGE_REMOVAL_FRACTION = 0.30


def get_txt_files():
    """Return all .txt files in data/raw/, sorted by name."""
    return sorted(RAW_DIR.glob("*.txt"))


def verify_corpus() -> None:
    """Load + clean every document and report per-file stats and warnings."""
    files = get_txt_files()

    if not files:
        print(f"No .txt files found in {RAW_DIR}/")
        print("Add documents there, then run this verification again.")
        return

    print("=" * 70)
    print(f"VERIFYING CORPUS: {len(files)} file(s) in {RAW_DIR}/")
    print("=" * 70)

    warnings = []
    seen_names = {}      # lowercased filename -> count, to catch duplicates
    total_raw = 0
    total_cleaned = 0
    representative = None  # first non-empty file, used for the preview

    print(f"\n{'filename':<32}{'raw':>10}{'cleaned':>10}{'removed':>10}")
    print("-" * 62)

    for path in files:
        raw = load_file(str(path))
        cleaned = clean_text(raw)

        raw_len = len(raw)
        cleaned_len = len(cleaned)
        removed = raw_len - cleaned_len

        total_raw += raw_len
        total_cleaned += cleaned_len

        print(f"{path.name:<32}{raw_len:>10}{cleaned_len:>10}{removed:>10}")

        if raw_len == 0:
            warnings.append(f"EMPTY FILE: {path.name} has 0 characters.")
        elif removed > raw_len * LARGE_REMOVAL_FRACTION:
            pct = removed / raw_len * 100
            warnings.append(
                f"LARGE REMOVAL: {path.name} lost {removed} chars "
                f"({pct:.1f}%) during cleaning -- inspect it."
            )

        key = path.name.lower()
        seen_names[key] = seen_names.get(key, 0) + 1

        if representative is None and cleaned_len > 0:
            representative = (path.name, cleaned)

    for name, count in seen_names.items():
        if count > 1:
            warnings.append(f"DUPLICATE FILENAME: '{name}' appears {count} times.")

    print("-" * 62)
    print(f"{'TOTAL':<32}{total_raw:>10}{total_cleaned:>10}"
          f"{total_raw - total_cleaned:>10}")

    if representative is not None:
        name, cleaned = representative
        print(f"\nFirst 200 characters of '{name}' AFTER cleaning:")
        print("-" * 62)
        print(cleaned[:200])
        print("-" * 62)

    print()
    if warnings:
        print(f"⚠️  {len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("✅ No warnings. All files loaded and cleaned without issues.")


def verify_chunking() -> None:
    """Load + clean + chunk every document and report chunk stats."""
    files = get_txt_files()

    if not files:
        print(f"No .txt files found in {RAW_DIR}/")
        print("Add documents there, then run this verification again.")
        return

    print("=" * 70)
    print(f"CHUNKING CORPUS: {len(files)} file(s) in {RAW_DIR}/")
    print("=" * 70)

    all_chunks = []
    per_file_counts = {}

    for path in files:
        cleaned = clean_text(load_file(str(path)))
        chunks = chunk_document(cleaned, source=path.name)
        all_chunks.extend(chunks)
        per_file_counts[path.name] = len(chunks)

    print(f"\n{'filename':<32}{'chunks':>10}")
    print("-" * 42)
    for name, count in per_file_counts.items():
        print(f"{name:<32}{count:>10}")
    print("-" * 42)
    print(f"{'TOTAL CHUNKS':<32}{len(all_chunks):>10}")

    # Seed so the sampled examples are the same on every run.
    random.seed(42)
    sample_size = min(5, len(all_chunks))
    examples = random.sample(all_chunks, sample_size)

    print(f"\n{sample_size} RANDOM EXAMPLE CHUNKS")
    print("=" * 70)
    for c in examples:
        word_count = len(c["text"].split())
        print(f"\n[{c['source']} | chunk #{c['chunk_index']} | {word_count} words]")
        print("-" * 70)
        print(c["text"])
        print("-" * 70)


if __name__ == "__main__":
    verify_chunking()
