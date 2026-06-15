"""Gradio interface for the GSU CS Advisor RAG system.

This is the THIN UI layer. It contains no retrieval, embedding, generation, or
attribution logic -- it only collects a question, hands it to the existing
ask() function, and displays what comes back.

Run from the project root:
    python app.py
"""

import gradio as gr

from src.rag import ask

DESCRIPTION = (
    "Ask questions about Georgia State University's Computer Science program, "
    "professors, and course requirements."
)

# Three questions from the evaluation plan, shown as clickable examples.
EXAMPLES = [
    "What do students say about the quality of Georgia State University's "
    "Computer Science program?",
    "What issues do students report about Tushara Sadasivuni's Software "
    "Development class?",
    "What are the main requirements students must complete before they can "
    "take upper-level CS courses (CSC 2720 and above)?",
]


def handle_query(question):
    """Bridge between the UI and the RAG pipeline.

    Takes the raw textbox string, calls ask(), and formats the result for the
    two output textboxes. Returns a (answer, sources) tuple matching the
    outputs list wired up below.
    """
    # Friendly guard for an empty / whitespace-only question, so we don't run
    # the pipeline on nothing.
    if not question or not question.strip():
        return "Please enter a question to get started.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


# Blocks gives us explicit control over layout and wiring (vs. a one-liner UI).
with gr.Blocks(title="GSU CS Advisor") as demo:
    gr.Markdown("# GSU CS Advisor")
    gr.Markdown(DESCRIPTION)

    # Input: the user's question.
    question_box = gr.Textbox(
        label="Your question",
        placeholder="Ask about GSU CS professors, courses, or requirements...",
        lines=2,
    )
    ask_button = gr.Button("Ask", variant="primary")

    # Outputs: the grounded answer and the list of source files.
    answer_box = gr.Textbox(label="Answer", lines=8)
    sources_box = gr.Textbox(label="Sources", lines=4)

    # Clickable example questions populate the question box.
    gr.Examples(examples=EXAMPLES, inputs=question_box)

    # Wire BOTH triggers to the same handler:
    #   - clicking the Ask button
    #   - pressing Enter inside the question textbox (.submit)
    # Both read question_box and write to [answer_box, sources_box].
    ask_button.click(
        fn=handle_query, inputs=question_box, outputs=[answer_box, sources_box]
    )
    question_box.submit(
        fn=handle_query, inputs=question_box, outputs=[answer_box, sources_box]
    )


if __name__ == "__main__":
    demo.launch()
