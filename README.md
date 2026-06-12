# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

I chose the domain of student experiences and reviews about Georgia State University's Computer Science program, courses, and professors. This information is valuable because students often want to know what classes and professors are really like before registering, including workload, difficulty, and teaching style. It can be hard to find because these experiences are usually shared across Reddit posts, review websites, and online discussions instead of official university pages.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
