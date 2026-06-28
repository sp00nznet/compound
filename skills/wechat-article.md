# WeChat Public-Account Article: Author-Editor-Reader Three-Agent Collaboration

Conduct in-depth research on $ARGUMENTS and produce a WeChat public-account article ready to publish as-is. Three Agents each have a distinct role: the Author writes a deep first draft, the Editor refines structure and expression, and the Reader reviews it from the target audience's perspective.

**Supported input format**: a topic description, e.g.: `Explaining large-model OPD techniques`, `Walkthrough of the Qwen3 technical report`, `Why Buffett doesn't buy tech stocks`

---

## Design Philosophy

A good public-account article must satisfy three dimensions at once:
1. **Depth** — worthy of someone who spends the time to read it through (the Author's job)
2. **Readability** — clear structure, good pacing, doesn't drive readers away (the Editor's job)
3. **Actually understandable** — the target reader won't give up halfway (the Reader's job)

Solo writing easily turns into self-indulgence — the writer thinks it's clear, the reader can't follow. The essence of three-Agent collaboration is to **force in an outside perspective**.

---

## Phase 1: Research and Material Gathering

### Step 1: Define the article's positioning

Before writing, confirm the following (proactively ask the user if unspecified):

| Dimension | What to confirm | Default |
|------|---------|--------|
| **Target reader** | Level of technical background | Some technical background but not an expert in the field |
| **Article depth** | Popular science / mid-depth / hardcore | Mid-depth (formulas allowed but must be clearly explained) |
| **Article length** | Word-count range | 3,000–4,000 characters |
| **Need to download source papers/materials** | Need PDFs/figures | Yes |
| **Writing style** | Formal / conversational / sharp | Conversational (like writing to a smart friend) |

### Step 2: Deep research

Use the Agent tool to launch 2–3 research Agents **in parallel** and gather enough material:

**Research Agent A: Core content research**
- If it's a paper walkthrough: download the paper PDF, extract the core contributions, key figures, experimental results
- If it's a technical topic: search for the latest progress, key papers, technical details
- If it's a business/investment topic: search for the latest data, industry reports, the competitive landscape

**Research Agent B: Industry background and applications**
- Search how the technology/topic is being deployed in the industry
- Which companies are using it? How well does it work?
- Latest development trends and milestone events

**Research Agent C (optional): Competitor/comparison research**
- Comparison with similar methods/products
- Historical development arc
- Future evolution direction

### Step 3: Organize the material framework

Once all research Agents finish, compile:
1. **Core thesis** (one sentence summarizing the central message of the article)
2. **Key data** (the 3–5 most impactful data points)
3. **Figure list** (which figures are needed and their sources)
4. **Article outline** (titles and core content for 6–8 sections)

---

## Phase 2: Author Agent Writes the First Draft

Use the Agent tool to launch the **Author Agent**, with detailed writing instructions.

### Author Agent Prompt Template

```
You are an in-depth technical writer (Author Agent), tasked with writing a WeChat public-account article.

## Target reader
{the reader persona confirmed in Step 1}

## Writing-style requirements
- Write in pure Chinese; avoid mixing Chinese and English (give the English term the first time a technical term appears, then use Chinese thereafter)
- Like technical popular science written for a smart friend, not a translated academic paper
- Use analogies to aid understanding, but keep them apt and not clichéd
- Include key formulas/data, but explain each one in plain language
- No emoji
- Keep paragraphs under 4 lines (the public-account reading environment)

## Core content
{the compiled material, data, and theses}

## Article-structure requirements
1. **Opening (first 3 paragraphs)**: must have a strong hook — open with the impact of data or a counterintuitive conclusion, not a mild analogy
2. **Background**: why does this matter? what problem does it solve?
3. **Core content (2–3 sections)**: this is where technical depth shows, but every technical point must have a "plain-language translation"
4. **Evidence/cases**: let data and cases speak, no empty talk
5. **Industry impact/outlook**: what this means for the industry
6. **Ending**: close with one shareable judgment, suitable for being screenshotted and forwarded

## Figure requirements
- For paper-walkthrough articles: you must extract the original figures from the paper PDF and insert them directly into the article with `![description](relative_path)`; do not use `[Figure X: description]` placeholders
- Extraction method: use pdftoppm to render PDF pages to high-resolution PNG (at least 900 DPI), then use PIL to crop the target figure region
- Each figure should be at least 500KB to ensure high definition
- Store all images under the `assets/{topic_short_name}/` directory
- For non-paper articles: if figures are needed, search and download suitable images and insert them directly the same way

## Formula requirements
- All math formulas use LaTeX format: inline with `$...$`, standalone formulas with `$$...$$`
- Do not write formulas in plain text (e.g. `> D_KL(P || Q) = ...`); they must use LaTeX rendering format
- Every formula must still be accompanied by a "plain-language translation"

Please write the complete first draft, about {target word count} characters.
```

### After the Author Agent finishes

Check that the draft file was generated, and read the whole thing to confirm completeness.

---

## Phase 3: Editor Agent + Reader Agent Review in Parallel

Once the first draft is done, use the Agent tool to launch the Editor Agent and the Reader Agent in the **same message**.

### Editor Agent Prompt Template

```
You are a senior public-account editor (Editor Agent). Please refine and review the following article.

## Review criteria
1. **Title**: will it attract clicks in a Moments feed? Will it be truncated (over 30 characters)?
2. **Opening**: do the first 3 paragraphs hold the reader? Is the hook strong enough?
3. **Structure**: is the logical chain smooth? Any jumps or breaks?
4. **Balance of depth and readability**: are the formula/technical parts genuinely accessible? Anywhere that "pretends to be accessible but isn't actually explained clearly"?
5. **Pacing**: any overly long paragraphs? Is each section's length appropriate?
6. **Figures**: are images actually inserted (not placeholders)? Do they appear right where the reader most needs visual support?
7. **Ending**: does it have shareability? Will the reader want to forward it after reading?

## Full article
{the complete first draft}

## Output format
1. Overall assessment (3–5 sentences)
2. Title revision suggestions (give 2–3 alternatives)
3. Section-by-section revision suggestions (give concrete "original → suggested revision" comparisons)
4. The 3 most critical improvement points
```

### Reader Agent Prompt Template

```
You are a {target reader persona} (Reader Agent). Please review the following article from a reader's perspective.

## Your background
{a concrete description of the target reader's knowledge level and reading habits}

## Full article
{the complete first draft}

## Please answer the following questions
1. After reading the first 3 paragraphs, would you keep reading? Why?
2. Where did you "not understand" or "need to re-read to grasp"? Which exact sentence?
3. Did you understand the technical/formula parts? Did the "plain-language translation" help you?
4. Is the article's core analogy apt? Is there a better analogy?
5. Too long or too short? Where would you lose patience?
6. After reading, can you summarize the article's core point in one sentence?
7. Would you forward this article? What would you say when forwarding it?
8. Any question you wanted answered that the article didn't cover?
```

---

## Phase 4: Finalize

### Step 1: Synthesize the feedback from both Agents

Focus on these high-frequency issues:

| Issue type | Common editor feedback | Common reader feedback | How to handle |
|---------|------------|------------|---------|
| Weak opening | Hook not strong enough | No motivation to continue past first 3 paragraphs | Rewrite the opening with data/a counterintuitive conclusion |
| Technical section drives readers away | Formulas too dense | A paragraph needed re-reading 3 times | Cut formulas or turn them into figures, add a more intuitive analogy |
| Sluggish pacing | A section too long | Lost patience somewhere | Merge or trim (especially repeated technical explanations in the second half) |
| Weak ending | Lacks shareability | Wouldn't forward | Rewrite into one screenshot-shareable judgment |
| Conceptual jumps | Logic has a break | "Suddenly couldn't follow" somewhere | Add a transition sentence or background explanation |

### Step 2: Make the revisions

Rewrite the article based on the feedback. Core revision principles:

1. **Issues flagged by both editor and reader must be fixed**
2. **Issues flagged only by the editor very likely need fixing** (the editor's professional judgment is usually accurate)
3. **Issues flagged only by the reader are fixed case by case** (reader feedback reflects the real experience, but not every point needs a response)
4. **When the two conflict, lean toward the reader** (the editor chases perfection, but reader experience is the final standard)

### Step 3: Extract the figures

Paper-walkthrough articles must complete figure extraction before finalizing:

1. **Render**: `pdftoppm -png -r 900 -f {page_number} -l {page_number} paper.pdf /tmp/page` (start at 900 DPI; bump to 1200 or 1500 DPI if an image is under 500KB)
2. **Locate**: first render the full page at 150 DPI and visually confirm the pixel coordinates of each figure
3. **Crop**: crop by coordinates with PIL, save with `compress_level=1`, ensuring each is ≥ 500KB
4. **Store**: save to the `assets/{topic_short_name}/` directory, named `fig{number}-{description}.png`
5. **Insert**: reference in the article with `![description](../../assets/{topic_short_name}/fig{number}-{description}.png)`

### Step 4: Produce the final file

Save the final draft as a md file, with links to the original paper/materials appended at the end of the file:

```markdown
**Original paper:**
- arXiv: {link}
```

---

## File Naming and Storage

| Type | Path | Naming format |
|------|------|---------|
| Technical topic | `reports/ai-industry-research/` | `wechat-{topic_keyword}-{YYYYMMDD}.md` |
| Investment topic | `reports/{company_name}/` | `{company_name}-wechat-{YYYYMMDD}.md` |
| General topic | `reports/` | `wechat-{topic_keyword}-{YYYYMMDD}.md` |

---

## Writing Red Lines

1. **No fabricated data**. Cited data must have a source; if you can't find it, label it "estimate"
2. **No AI-speak**. Banned: filler phrases like "let's take a look together", "what's worth noting is", "it has to be said"
3. **No over-promising**. Technical articles don't say "disruptive" or "revolutionary"; let the data speak
4. **Formulas must come with plain language**. Every formula must be followed by a "translated into plain words, this means…"
5. **Formulas must use LaTeX**. `$$...$$` format; plain-text formulas are banned
6. **Figures must actually be inserted**. Paper walkthroughs extract high-definition originals from the PDF (≥500KB); `[Figure X]` placeholders are banned
7. **Parenthetical notes in tables must be precise**. Use accurate definitions when describing a concept, not vague verb-object phrases (e.g. "text comes from the teacher" rather than "learn the teacher's text")
8. **Keep the analogy consistent**. Use one main analogy throughout, don't switch to a new analogy every section
9. **The ending must have shareability**. The last sentence must be worth screenshotting and forwarding on its own
