# Prompt Lab: prompts for analysing the career-anxiety dataset

Use these in order with Claude or ChatGPT after uploading `dataset.xlsx` (and `dataset_variable_encoded.xlsx` for step 2).
Every prompt follows the pattern Role · Context · Task · Format · Check.

Dataset: Islam, S., Piyas, B. R. C., Tisha, F. J., Nayem, H. K., Rahman, S., Preenon, B. R. C., & Hossen, S. (2026). Career anxiety in the age of artificial intelligence: Survey data of university students in Bangladesh. Data in Brief, 67, 112924. https://doi.org/10.1016/j.dib.2026.112924 Licence: CC BY 4.0.

## Step 0 · Ethics gate

Before you upload anything, check that you may use the data, that participants are protected, and what you will have to disclose.

### P0 · Ethical readiness check

*Type:* Role, Structured output, Guardrail

```text
Act as a research ethics reviewer at a university in Bangladesh. I plan a secondary analysis of a published dataset: "Career anxiety in the age of artificial intelligence: Survey data of university students in Bangladesh" (Data in Brief, 2026, CC BY 4.0). It has 3,156 student responses from five universities, a consent column and pseudonymous participant IDs. The file is attached. Before any analysis, assess: (1) licence and citation duties; (2) consent and anonymisation; (3) re-identification risk from combinations of age, gender, academic year and career path; (4) whether uploading this file to an AI tool is acceptable; (5) what I must disclose in a paper. Answer as a table with columns: issue, what the file or paper shows, risk (low/medium/high), action I should take. Do not analyse or summarise the survey answers yet. If you are unsure about a policy, say so instead of guessing.
```

**Verify:** Read the dataset article's ethics statement yourself; do not rely on the AI's summary.

## Step 1 · Understand the data

Know every column, its type and its coding before you ask a single research question.

### P1 · Data dictionary and research questions

*Type:* Tool use (code), Structured output · *runs code*

```text
I uploaded dataset.xlsx (one row per student). Read it with Python and build a data dictionary: column name, variable type (ID, numeric, nominal, ordinal, multi-select, free text), number of unique values, number missing, and two example values. Then propose three research questions this dataset can answer, each with the variables involved and a suitable statistical test. Give the dictionary as a table, then the questions as a numbered list. Show the code you ran. Do not change the data.
```

**Verify:** Count the columns (13) and rows (3,156) yourself in Excel.

## Step 2 · Audit data quality

Find problems first and fix nothing yet. Every later number depends on this step.

### P2 · Quality audit, both files

*Type:* Tool use (code), Guardrail · *runs code*

```text
Audit data quality without changing anything. Check: duplicate rows and duplicate participant_id; missing values per column; inconsistent spellings or synonyms in categorical columns (especially ai_tool_perception and the comma-separated ai_tools_used); free-text columns with too many categories; out-of-range ages; consent values. Also open dataset_variable_encoded.xlsx and check that every encoded value is a valid code for its column. Report each problem with its count and up to three example participant_ids. Show the code. Do not clean or recode anything in this step.
```

**Verify:** Open the encoded file and filter ai_takeover_time: you should find the stray "h".

## Step 3 · Clean and encode

Plan first, approve, then execute and log. Cleaning decisions are research decisions.

### P3 · Cleaning plan, then execution

*Type:* Plan-then-execute, Guardrail, Tool use (code) · *runs code*

```text
Propose a cleaning plan and wait for my approval before running it. The plan should: keep missing ai_knowledge as missing (no imputation); merge synonyms in ai_tool_perception (none, Nothing, None of them → None); fix the spelling Quiltbot → QuillBot; split ai_tools_used into one 0/1 column per tool; encode ordinal variables in this order: career_anxiety No Anxiety=0, Low=1, Medium=2, High=3; ai_knowledge Low=1, Medium=2, High=3; ai_replace_jobs No=0, Partially=1, Fully=2; ai_future_perspective from "helpful tool" (0) to "complete takeover" (4). After I approve, run it and return a cleaning log (step, rows affected, change) and the clean file as CSV. Never drop rows unless I agree. Report the row count before and after.
```

**Verify:** Row count must stay 3,156. Spot-check five rows against the original file.

### P3b · Group free-text careers (few-shot)

*Type:* Few-shot, Structured output · *runs code*

```text
career_path is free text with about 160 different answers. Group every answer into one of: Data & AI, Cybersecurity, Software & IT, Engineering, Research & Academia, Health & Food, Business & Finance, Creative & Media, Public service, Other. Examples: "Software Engineer" → Software & IT; "ML Engineer" → Data & AI; "Pharmacist" → Health & Food; "Banker" → Business & Finance; "Reseacrher" (misspelt) → Research & Academia. Return the full mapping table (original → group) and the count per group. Answers naming two careers go to the first one; list them separately so I can review.
```

**Verify:** Read the mapping table; misspellings and two-career answers are where AI grouping goes wrong.

## Step 4 · Describe

Frequencies and percentages first. Readers need to see the sample before any test.

### P4 · Descriptive statistics tables

*Type:* Tool use (code), Structured output · *runs code*

```text
Using the cleaned data, produce descriptive statistics: n and % for every categorical variable (keep Missing as its own row), mean, SD and range of age, and the percentage of students who use each AI tool. Present APA-style tables I can paste into a paper, with n in each table title. Percentages must add to 100 within each variable; tell me if they do not.
```

**Verify:** Percentages in each table must add to 100; career anxiety Medium should be 1,634 (51.8%).

## Step 5 · Visualise

Claude and ChatGPT can run Python and hand back charts as files. Ask for the code too.

### P5 · Publication charts (runs code)

*Type:* Tool use (code), Constraint · *runs code*

```text
Run Python to create: (1) a bar chart of career_anxiety with n and % on each bar; (2) 100% stacked bars of career_anxiety by ai_knowledge and by ai_replace_jobs; (3) a horizontal bar chart of the percentage of students using each AI tool. Save each chart as a 300-dpi PNG I can download, and show the code. Use a colour-blind-safe palette, label both axes, start bars at zero, and put the sample size in each title.
```

**Verify:** Bars start at zero; n appears in titles; the numbers on charts match step 4.

## Step 6 · Test hypotheses

Choose tests that fit an ordinal outcome, check assumptions, and always report effect sizes.

### P6 · Hypothesis tests with effect sizes

*Type:* Role, Tool use (code), Structured output · *runs code*

```text
Act as a statistician. career_anxiety is ordinal with four levels. Test: H1 anxiety differs by gender; H2 anxiety is related to ai_knowledge; H3 anxiety is related to the belief that AI will replace jobs; H4 anxiety differs by academic year. Use chi-square tests with Cramér's V, Spearman's rho for ordinal pairs, and Kruskal–Wallis where suitable. Check expected cell counts. Report a table: hypothesis, test, statistic, df, p, effect size, plain-language verdict. Run the code and show it. Do not use causal words.
```

**Verify:** Run prompt PV. Check that the AI did not use a t-test on the ordinal outcome.

### PV · Verify the numbers

*Type:* Self-verification, Tool use (code) · *runs code*

```text
Re-compute every number in your last answer from the raw file in a fresh code cell, without reusing earlier variables. Show a table: statistic, value you reported, value recomputed, match (yes/no). If anything differs, explain why and tell me which value is correct.
```

**Verify:** Any mismatch: stop and find out why before writing.

## Step 7 · Model

One model that holds the predictors together, with odds ratios a reader can interpret.

### P7 · Ordinal logistic regression

*Type:* Tool use (code), Structured output, Explain · *runs code*

```text
Fit an ordinal logistic (proportional-odds) regression with career_anxiety as the outcome and ai_knowledge, ai_replace_jobs, ai_future_perspective (0–4), gender and academic year as predictors. Report odds ratios with 95% CIs and p-values, McFadden's pseudo-R², and a forest plot. Then explain each odds ratio in one plain sentence. Tell me how many rows were dropped for missing values, and whether the proportional-odds assumption looks reasonable.
```

**Verify:** n should be 3,111 (45 rows missing ai_knowledge). ORs above 1 mean higher anxiety.

## Step 8 · Interpret critically

Let the AI argue against you. Small effects, self-report and sampling limit what you can claim.

### P8 · Sceptical-reviewer interpretation

*Type:* Role, Critique, Constraint

```text
Act as a sceptical journal reviewer. Here are my results: [paste the tables from steps 6 and 7]. Write a 150-word interpretation that uses associational language and states effect sizes. Then list the main limitations of this dataset: self-report, cross-sectional design, students from five universities, an AI seminar given just before the survey, binary gender categories, and verbal (not written) ethics approval. Flag any sentence in my draft that overstates the evidence: [paste your draft].
```

**Verify:** Every sentence must be supported by a number from steps 6–7.

## Step 9 · Report and disclose

Cite the data, describe what the AI did, and state who verified it.

### P9 · Methods paragraph and AI disclosure

*Type:* Structured output, Constraint

```text
Draft the methods paragraph for this secondary analysis: dataset and citation (Islam, S., Piyas, B. R. C., Tisha, F. J., Nayem, H. K., Rahman, S., Preenon, B. R. C., & Hossen, S. (2026). Career anxiety in the age of artificial intelligence: Survey data of university students in Bangladesh. Data in Brief, 67, 112924. https://doi.org/10.1016/j.dib.2026.112924 Licence: CC BY 4.0), cleaning steps, statistical tests and software, and an AI-use disclosure. About 200 words, APA 7 style, followed by a separate two-sentence disclosure statement. The disclosure must name the AI tool and version, say which steps it performed, and state that all numbers were verified by re-running the code. Do not invent software versions; leave [brackets] where you do not know.
```

**Verify:** Check the citation against the article page; fill every [bracket] yourself.

## Step 10 · Make it reusable

Turn this conversation into a context file and a skill so the next study starts here.

### P10 · Write research-context.md and SKILL.md

*Type:* Meta-prompt, Structured output

```text
From this conversation, write two files. (1) research-context.md, at most 40 lines: research questions, dataset citation and licence, variable coding, analysis conventions, ethics rules, and how I want you to work. (2) SKILL.md for a skill named survey-analysis-workflow that turns steps 2–9 into a reusable procedure. SKILL.md must start with front matter: name, and a description of at most 200 characters that says what it does and when to use it. Keep every rule concrete enough to check, for example "report Cramér's V with every chi-square".
```

**Verify:** Description of the skill ≤ 200 characters; each rule is testable.
