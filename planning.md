# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain
I chose the domain of student experiences and reviews about Georgia State University's Computer Science program, courses, and professors. This information is valuable because students often want to know what classes and professors are really like before registering, including workload, difficulty, and teaching style. It can be hard to find because these experiences are usually shared across Reddit posts, review websites, and online discussions instead of official university pages.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | GSU page | List of CS professors | https://csds.gsu.edu/directory/ |
| 2 | GSU page | CS program requirements | https://catalogs.gsu.edu/preview_program.php?catoid=42&poid=12378&utm_source=ppcatalog&utm_medium=cas&utm_content=bs&utm_campaign=program_explorer |
| 3 | GSU page | List of CS programs and courses at GSU| https://catalogs.gsu.edu/preview_entity.php?catoid=42&ent_oid=2867 |
| 4 | Reddit | Comparing GSU's CS program | https://www.reddit.com/r/GaState/comments/17tazvq/how_is_the_computer_science_program/ |
| 5 | Reddit | Worst CS professors at GSU| https://www.reddit.com/r/GaState/comments/1j1jp7q/worst_cs_professor_youve_had_off_the_top_of_your/ |
| 6 | Reditt | Best CS professors at GSU| https://www.reddit.com/r/GaState/comments/1j2qjrw/best_cs_profs_at_gsu/ |
| 7 | Reditt | GSU CS program review| https://www.reddit.com/r/GaState/comments/p02fn2/how_good_is_the_cs_program_at_gastate/ |
| 8 | RateMyProfessors| Rates CS professors at GSU| https://www.ratemyprofessors.com/search/professors/360?q=*&did=11 |
| 9 | Coursicle| CS course reviews|https://www.coursicle.com/gsu/courses/CSC/ |
| 10 | Quora| Easy classes for CS program | https://www.quora.com/I-am-doing-my-undergrad-in-Georgia-State-University-currently-in-my-sophomore-year-majoring-in-computer-science-I-need-12-credits-from-any-2000-4000-level-classes-Can-someone-please-recommend-some-easy-general-2000 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
