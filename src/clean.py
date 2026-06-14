"""Document cleaning for the Unofficial Guide RAG pipeline.

STEP 2 of the pipeline: take the raw text produced by STEP 1 (load.py) and
remove only mechanical noise -- HTML entities and messy whitespace -- while
keeping every piece of substantive content (professor names, course numbers,
reviews, requirements, etc.) exactly as written.

This step does NOT summarize, rewrite, chunk, or embed. It only tidies.
Standard library only (html + re).
"""

import html
import re


def clean_text(text: str) -> str:
    """Clean raw document text without removing meaningful content.

    The cleaning is intentionally conservative. It performs four passes:

      1. Decode HTML entities ("&amp;" -> "&", "&nbsp;" -> " ", etc.) so the
         text reads naturally. Catalog and review pages copied from the web
         often leave these behind.
      2. Normalize whitespace *within* each line: collapse runs of spaces/tabs
         into a single space and strip leading/trailing spaces from the line.
         This fixes ragged spacing from copy-paste without merging separate
         lines together.
      3. Collapse 3+ consecutive blank lines down to a single blank line, so
         paragraph breaks are preserved but large empty gaps are removed.
      4. Strip leading/trailing whitespace from the whole document.

    Args:
        text: Raw text as returned by load_file().

    Returns:
        Cleaned text with the same words and meaning, just tidier spacing.
    """
    # Pass 1: decode HTML entities (e.g. &amp;, &nbsp;, &#39;).
    text = html.unescape(text)

    # Normalize line endings so Windows/Mac files behave the same.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Pass 2: tidy each line individually.
    cleaned_lines = []
    for line in text.split("\n"):
        # Collapse any run of spaces/tabs into one space.
        line = re.sub(r"[ \t]+", " ", line)
        # Remove leading/trailing spaces on the line.
        line = line.strip()
        cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)

    # Pass 3: collapse 3+ newlines (i.e. 2+ blank lines) into one blank line.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Pass 4: trim the whole document.
    return text.strip()
