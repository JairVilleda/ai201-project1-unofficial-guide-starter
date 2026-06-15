"""Gradio interface for the GSU CS Advisor.

Run from the project root:
    python app.py
"""

import gradio as gr

from src.rag import ask

DESCRIPTION = (
    "Ask questions about Georgia State University's Computer Science program, "
    "professors, and course requirements."
)

EXAMPLES = [
    "What do students say about the quality of Georgia State University's "
    "Computer Science program?",
    "What issues do students report about Tushara Sadasivuni's Software "
    "Development class?",
    "What are the main requirements students must complete before they can "
    "take upper-level CS courses (CSC 2720 and above)?",
]


def handle_query(question):
    """Call ask() and format the result for the answer and sources boxes."""
    if not question or not question.strip():
        return "Please enter a question to get started.", ""

    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources


with gr.Blocks(title="GSU CS Advisor") as demo:
    gr.Markdown("# GSU CS Advisor")
    gr.Markdown(DESCRIPTION)

    question_box = gr.Textbox(
        label="Your question",
        placeholder="Ask about GSU CS professors, courses, or requirements...",
        lines=2,
    )
    ask_button = gr.Button("Ask", variant="primary")

    answer_box = gr.Textbox(label="Answer", lines=8)
    sources_box = gr.Textbox(label="Sources", lines=4)

    gr.Examples(examples=EXAMPLES, inputs=question_box)

    # Answer on button click or on Enter in the textbox.
    ask_button.click(
        fn=handle_query, inputs=question_box, outputs=[answer_box, sources_box]
    )
    question_box.submit(
        fn=handle_query, inputs=question_box, outputs=[answer_box, sources_box]
    )


if __name__ == "__main__":
    demo.launch()
