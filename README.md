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
 1 | GSU page | List of CS professors | https://csds.gsu.edu/directory/ |
| 2 | GSU page | CS program requirements | https://catalogs.gsu.edu/preview_program.php?catoid=42&poid=12378&utm_source=ppcatalog&utm_medium=cas&utm_content=bs&utm_campaign=program_explorer |
| 3 | GSU page | List of CS programs and courses at GSU| https://catalogs.gsu.edu/preview_entity.php?catoid=42&ent_oid=2867 |
| 4 | Reddit | Comparing GSU's CS program | https://www.reddit.com/r/GaState/comments/17tazvq/how_is_the_computer_science_program/ |
| 5 | Reddit | Worst CS professors at GSU| https://www.reddit.com/r/GaState/comments/1j1jp7q/worst_cs_professor_youve_had_off_the_top_of_your/ |
| 6 | Reditt | Best CS professors at GSU| https://www.reddit.com/r/GaState/comments/1j2qjrw/best_cs_profs_at_gsu/ |
| 7 | Reditt | GSU CS program review| https://www.reddit.com/r/GaState/comments/p02fn2/how_good_is_the_cs_program_at_gastate/ |
| 8 | RateMyProfessors| Rates CS professors at GSU| https://www.ratemyprofessors.com/search/professors/360?q=*&did=11 |
| 9 | Quora| Easy classes for CS program | https://www.quora.com/I-am-doing-my-undergrad-in-Georgia-State-University-currently-in-my-sophomore-year-majoring-in-computer-science-I-need-12-credits-from-any-2000-4000-level-classes-Can-someone-please-recommend-some-easy-general-2000 |
| 10 | RateMyProfessors | Professor Roya Hosseini | https://www.ratemyprofessors.com/professor/2723447 |
| 11 | RateMyProfessors | Professor Tushara Sadasivuni| https://www.ratemyprofessors.com/professor/2317655 |
| 12 | RateMyProfessors | Professor Faris Hawamdeh | https://www.ratemyprofessors.com/professor/2927602 |
| 13 | RateMyProfessors | Professor William Johnson | https://www.ratemyprofessors.com/professor/2329806 |
| 14 | RateMyProfessors | Professor Rajshekhar Sunderraman | https://www.ratemyprofessors.com/professor/2614203 |
| 15 | RateMyProfessors | Professor Micheal Week | https://www.ratemyprofessors.com/professor/418488 |
| 16 | RateMyProfessors | Professor David James | https://www.ratemyprofessors.com/professor/3007536 |
| 17 | RateMyProfessors | Professor Louis Henry | https://www.ratemyprofessors.com/professor/458011 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->


**Chunk size:**  
300 words

**Overlap:**  
50 words

**Why these choices fit your documents:**  
I used 300-word chunks because most of my data consists of short-to-medium length content like Reddit posts, professor reviews, and university catalog text. This size keeps enough context in each chunk so a single idea (like a professor’s teaching style or a course requirement) is fully captured without being cut off too early. The 50-word overlap helps preserve continuity between chunks so that important details near boundaries are not lost during retrieval. This is especially useful for review-style text where opinions and explanations can span multiple sentences.

**Final chunk count:**  
171 chunks across 17 documents


---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**
If I were deploying this system for real users and cost was not a concern, I would consider larger embedding models that provide higher retrieval accuracy, better support for longer documents, and stronger performance on domain-specific or multilingual text, while balancing latency and computational requirements.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**  
The system prompt explicitly tells the model to only use the provided context when answering. It says that if the answer is not in the context, it must respond with “I don't have enough information on that.” It also instructs the model to avoid using any outside knowledge and to keep answers strictly based on the retrieved chunks. The retrieved text is passed in as a formatted context block, separated by dividers so the model can clearly distinguish between documents.

**How source attribution is surfaced in the response:**  
Source attribution is not generated by the model. Instead, the system collects metadata from the retrieved chunks (specifically the `source` field like `reddit4.txt` or `gsu2.txt`) and programmatically deduplicates it in Python. These sources are returned alongside the model’s answer, ensuring the citations always match the exact chunks used during retrieval and cannot be hallucinated or altered by the LLM.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the quality of Georgia State University's Computer Science program? | Students generally describe the CS program more positively than its reputation suggests. Success depends heavily on personal effort, participation, office hours, research, and internships. Upper-level professors tend to be better and the program prepares students for software engineering careers. | The system reported mixed but generally positive opinions. Students said the program is "not as bad as everyone makes it out to be," that professors improve in upper-level courses, and that success depends on effort and taking advantage of opportunities such as research and internships. | Relevant | Accurate |
| 2 | What issues do students report about Tushara Sadasivuni’s Software Development class? | Students report disorganized classes, lectures read directly from slides, difficult labs without prior Java experience, unclear instructions, and inconsistent TA guidance. | The system identified many of the same issues, including poor organization, reading from slides, difficult labs requiring self-study, unrealistic Java expectations, late or unhelpful TAs, poor communication, and confusing assignments. | Relevant | Accurate |
| 3 | Which CS professor is most consistently praised in student discussions, and what qualities are mentioned? | William Johnson is the most consistently praised professor and is described as passionate, caring, fair, and effective at teaching. | The system incorrectly identified Rajshekhar Sunderraman and Dr. Henry as the most praised professors and highlighted qualities such as being caring, helpful, funny, and accessible outside class. | Partially relevant | Inaccurate |
| 4 | What are the main requirements students must complete before they can take upper-level CS courses (CSC 2720 and above)? | Students must earn a C or higher in CSC 1301 and CSC 1301L, complete either CSC 2510 or MATH 2420, complete a required math course, and achieve a 2.5 GPA across these courses. | The system correctly listed all requirements, including the C-or-higher grade requirements, the discrete mathematics requirement, the approved math courses, and the 2.5 GPA requirement. | Relevant | Accurate |
| 5 | What are two advanced CS elective topics listed in the catalog? | Artificial Intelligence (CSC 4810), Machine Learning (CSC 4850), Cloud Computing (CSC 4311), and Big Data Programming (CSC 4760). | The system returned valid advanced electives from the catalog, specifically Fundamentals of Game Design (CSC 4821) and Introduction to Deep Learning (CSC 4851). These were different from the expected examples but were still correct catalog electives. | Partially relevant | Partially accurate |

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
Which CS professor is most consistently praised in student discussions, and what qualities are mentioned?

**What the system returned:**  
The system identified Dr. Henry and Rajshekhar Sunderraman as the most praised professors, describing them as caring, helpful, and effective teachers. It did not correctly identify William Johnson, who was the expected answer.

**Root cause (tied to a specific pipeline stage):**  
This is a retrieval issue. The question asks for a comparison (“most consistently praised”), which requires combining information across many chunks. But embedding search only returns the most similar individual chunks. Henry’s reviews contain lots of positive words, so those chunks ranked higher than William Johnson’s. Since no single chunk explicitly says “Johnson is the most praised,” the system never retrieved him. The generation step worked correctly based on what it was given.

**What you would change to fix it:**  
Use a better approach for comparison questions. For example: increase k further, group chunks by professor before ranking, or add a step that aggregates sentiment per professor instead of relying only on top-k similarity search.


---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

## Spec Reflection

**One way the spec helped you during implementation:**  
The planning.md file gave clear structure for each milestone, which made it easier to build the system step by step instead of trying to implement everything at once. The chunk size and overlap guidance was useful because it directly shaped how I designed and validated the chunking logic. The evaluation questions also helped define what “good retrieval” should look like early on, which made debugging much easier.

**One way your implementation diverged from the spec, and why:**  
I ended up injecting the source/professor name into the chunk text during chunking, which was not explicitly required in the original spec. I added this because retrieval was missing professor names when answering questions, since metadata alone is not used during embedding. This change improved retrieval accuracy for professor-specific queries, even though it slightly modified the original chunking design.

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
  I gave Claude my Milestone 3 instructions, chunking strategy from planning.md, and my goal of building a document loading + chunking pipeline in Python.

- *What it produced:*  
  It generated a step-by-step implementation for loading files, cleaning text, and splitting into fixed-size word chunks with overlap, along with a basic testing script to inspect chunk output.

- *What I changed or overrode:*  
  I simplified the implementation to keep it lightweight (standard library only) and adjusted the chunking to a word-based sliding window instead of a more complex splitter. I also added extra validation prints to manually inspect chunk quality before moving on.

---

**Instance 2**

- *What I gave the AI:*  
  I gave Claude my retrieval and evaluation plan, including the 5 test questions and expected answers, and asked it to help implement embedding, vector storage (ChromaDB), and retrieval.

- *What it produced:*  
  It generated code for embedding chunks with sentence-transformers, storing them in ChromaDB with metadata, and a retrieval function using top-k similarity search, plus an evaluation script to test results against my sample questions.

- *What I changed or overrode:*  
  I adjusted k from 4 to 5 after testing to improve retrieval coverage, and I added source name injection into chunks so professor-specific queries would retrieve correctly. I also refined the evaluation output to better distinguish retrieval vs generation issues.
