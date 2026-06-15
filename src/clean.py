"""Clean raw document text: fix whitespace and decode HTML entities."""

import html
import re


def clean_text(text: str) -> str:
    """Tidy whitespace and decode HTML entities without changing the content."""
    text = html.unescape(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Collapse runs of spaces/tabs and trim each line.
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"[ \t]+", " ", line).strip()
        lines.append(line)
    text = "\n".join(lines)

    # Collapse multiple blank lines into one, then trim the whole document.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
