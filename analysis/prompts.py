"""Prompt library for the EWU AI-for-Research training.
Each prompt is a list of (part, text) segments so the website can show its anatomy:
role · context · task · format · check (guardrail / verification)."""

DATASET_CITE = ("Islam, S., Piyas, B. R. C., Tisha, F. J., Nayem, H. K., Rahman, S., Preenon, B. R. C., & Hossen, S. (2026). "
                "Career anxiety in the age of artificial intelligence: Survey data of university students in Bangladesh. "
                "Data in Brief, 67, 112924. https://doi.org/10.1016/j.dib.2026.112924")

STEPS = [
 {"id": "s0", "n": "0", "title": "Ethics gate", "lead": "Before you upload anything, check that you may use the data, that participants are protected, and what you will have to disclose.",
  "prompts": [
   {"id": "P0", "title": "Ethical readiness check", "types": ["Role", "Structured output", "Guardrail"], "runs_code": False,
    "parts": [
     ("role", "Act as a research ethics reviewer at a university in Bangladesh."),
     ("context", " I plan a secondary analysis of a published dataset: \"Career anxiety in the age of artificial intelligence: Survey data of university students in Bangladesh\" (Data in Brief, 2026, CC BY 4.0). It has 3,156 student responses from five universities, a consent column and pseudonymous participant IDs. The file is attached."),
     ("task", " Before any analysis, assess: (1) licence and citation duties; (2) consent and anonymisation; (3) re-identification risk from combinations of age, gender, academic year and career path; (4) whether uploading this file to an AI tool is acceptable; (5) what I must disclose in a paper."),
     ("format", " Answer as a table with columns: issue, what the file or paper shows, risk (low/medium/high), action I should take."),
     ("check", " Do not analyse or summarise the survey answers yet. If you are unsure about a policy, say so instead of guessing.")]},
  ]},
 {"id": "s1", "n": "1", "title": "Understand the data", "lead": "Know every column, its type and its coding before you ask a single research question.",
  "prompts": [
   {"id": "P1", "title": "Data dictionary and research questions", "types": ["Tool use (code)", "Structured output"], "runs_code": True,
    "parts": [
     ("context", "I uploaded dataset.xlsx (one row per student)."),
     ("task", " Read it with Python and build a data dictionary: column name, variable type (ID, numeric, nominal, ordinal, multi-select, free text), number of unique values, number missing, and two example values. Then propose three research questions this dataset can answer, each with the variables involved and a suitable statistical test."),
     ("format", " Give the dictionary as a table, then the questions as a numbered list."),
     ("check", " Show the code you ran. Do not change the data.")]},
  ]},
 {"id": "s2", "n": "2", "title": "Audit data quality", "lead": "Find problems first and fix nothing yet. Every later number depends on this step.",
  "prompts": [
   {"id": "P2", "title": "Quality audit, both files", "types": ["Tool use (code)", "Guardrail"], "runs_code": True,
    "parts": [
     ("task", "Audit data quality without changing anything. Check: duplicate rows and duplicate participant_id; missing values per column; inconsistent spellings or synonyms in categorical columns (especially ai_tool_perception and the comma-separated ai_tools_used); free-text columns with too many categories; out-of-range ages; consent values."),
     ("context", " Also open dataset_variable_encoded.xlsx and check that every encoded value is a valid code for its column."),
     ("format", " Report each problem with its count and up to three example participant_ids."),
     ("check", " Show the code. Do not clean or recode anything in this step.")]},
  ]},
 {"id": "s3", "n": "3", "title": "Clean and encode", "lead": "Plan first, approve, then execute and log. Cleaning decisions are research decisions.",
  "prompts": [
   {"id": "P3", "title": "Cleaning plan, then execution", "types": ["Plan-then-execute", "Guardrail", "Tool use (code)"], "runs_code": True,
    "parts": [
     ("task", "Propose a cleaning plan and wait for my approval before running it. The plan should: keep missing ai_knowledge as missing (no imputation); merge synonyms in ai_tool_perception (none, Nothing, None of them → None); fix the spelling Quiltbot → QuillBot; split ai_tools_used into one 0/1 column per tool; encode ordinal variables in this order: career_anxiety No Anxiety=0, Low=1, Medium=2, High=3; ai_knowledge Low=1, Medium=2, High=3; ai_replace_jobs No=0, Partially=1, Fully=2; ai_future_perspective from \"helpful tool\" (0) to \"complete takeover\" (4)."),
     ("format", " After I approve, run it and return a cleaning log (step, rows affected, change) and the clean file as CSV."),
     ("check", " Never drop rows unless I agree. Report the row count before and after.")]},
   {"id": "P3b", "title": "Group free-text careers (few-shot)", "types": ["Few-shot", "Structured output"], "runs_code": True,
    "parts": [
     ("context", "career_path is free text with about 160 different answers."),
     ("task", " Group every answer into one of: Data & AI, Cybersecurity, Software & IT, Engineering, Research & Academia, Health & Food, Business & Finance, Creative & Media, Public service, Other. Examples: \"Software Engineer\" → Software & IT; \"ML Engineer\" → Data & AI; \"Pharmacist\" → Health & Food; \"Banker\" → Business & Finance; \"Reseacrher\" (misspelt) → Research & Academia."),
     ("format", " Return the full mapping table (original → group) and the count per group."),
     ("check", " Answers naming two careers go to the first one; list them separately so I can review.")]},
  ]},
 {"id": "s4", "n": "4", "title": "Describe", "lead": "Frequencies and percentages first. Readers need to see the sample before any test.",
  "prompts": [
   {"id": "P4", "title": "Descriptive statistics tables", "types": ["Tool use (code)", "Structured output"], "runs_code": True,
    "parts": [
     ("task", "Using the cleaned data, produce descriptive statistics: n and % for every categorical variable (keep Missing as its own row), mean, SD and range of age, and the percentage of students who use each AI tool."),
     ("format", " Present APA-style tables I can paste into a paper, with n in each table title."),
     ("check", " Percentages must add to 100 within each variable; tell me if they do not.")]},
  ]},
 {"id": "s5", "n": "5", "title": "Visualise", "lead": "Claude and ChatGPT can run Python and hand back charts as files. Ask for the code too.",
  "prompts": [
   {"id": "P5", "title": "Publication charts (runs code)", "types": ["Tool use (code)", "Constraint"], "runs_code": True,
    "parts": [
     ("task", "Run Python to create: (1) a bar chart of career_anxiety with n and % on each bar; (2) 100% stacked bars of career_anxiety by ai_knowledge and by ai_replace_jobs; (3) a horizontal bar chart of the percentage of students using each AI tool."),
     ("format", " Save each chart as a 300-dpi PNG I can download, and show the code."),
     ("check", " Use a colour-blind-safe palette, label both axes, start bars at zero, and put the sample size in each title.")]},
  ]},
 {"id": "s6", "n": "6", "title": "Test hypotheses", "lead": "Choose tests that fit an ordinal outcome, check assumptions, and always report effect sizes.",
  "prompts": [
   {"id": "P6", "title": "Hypothesis tests with effect sizes", "types": ["Role", "Tool use (code)", "Structured output"], "runs_code": True,
    "parts": [
     ("role", "Act as a statistician."),
     ("context", " career_anxiety is ordinal with four levels."),
     ("task", " Test: H1 anxiety differs by gender; H2 anxiety is related to ai_knowledge; H3 anxiety is related to the belief that AI will replace jobs; H4 anxiety differs by academic year. Use chi-square tests with Cramér's V, Spearman's rho for ordinal pairs, and Kruskal–Wallis where suitable. Check expected cell counts."),
     ("format", " Report a table: hypothesis, test, statistic, df, p, effect size, plain-language verdict."),
     ("check", " Run the code and show it. Do not use causal words.")]},
   {"id": "PV", "title": "Verify the numbers", "types": ["Self-verification", "Tool use (code)"], "runs_code": True,
    "parts": [
     ("task", "Re-compute every number in your last answer from the raw file in a fresh code cell, without reusing earlier variables."),
     ("format", " Show a table: statistic, value you reported, value recomputed, match (yes/no)."),
     ("check", " If anything differs, explain why and tell me which value is correct.")]},
  ]},
 {"id": "s7", "n": "7", "title": "Model", "lead": "One model that holds the predictors together, with odds ratios a reader can interpret.",
  "prompts": [
   {"id": "P7", "title": "Ordinal logistic regression", "types": ["Tool use (code)", "Structured output", "Explain"], "runs_code": True,
    "parts": [
     ("task", "Fit an ordinal logistic (proportional-odds) regression with career_anxiety as the outcome and ai_knowledge, ai_replace_jobs, ai_future_perspective (0–4), gender and academic year as predictors."),
     ("format", " Report odds ratios with 95% CIs and p-values, McFadden's pseudo-R², and a forest plot. Then explain each odds ratio in one plain sentence."),
     ("check", " Tell me how many rows were dropped for missing values, and whether the proportional-odds assumption looks reasonable.")]},
  ]},
 {"id": "s8", "n": "8", "title": "Interpret critically", "lead": "Let the AI argue against you. Small effects, self-report and sampling limit what you can claim.",
  "prompts": [
   {"id": "P8", "title": "Sceptical-reviewer interpretation", "types": ["Role", "Critique", "Constraint"], "runs_code": False,
    "parts": [
     ("role", "Act as a sceptical journal reviewer."),
     ("context", " Here are my results: [paste the tables from steps 6 and 7]."),
     ("task", " Write a 150-word interpretation that uses associational language and states effect sizes. Then list the main limitations of this dataset: self-report, cross-sectional design, students from five universities, an AI seminar given just before the survey, binary gender categories, and verbal (not written) ethics approval."),
     ("check", " Flag any sentence in my draft that overstates the evidence: [paste your draft].")]},
  ]},
 {"id": "s9", "n": "9", "title": "Report and disclose", "lead": "Cite the data, describe what the AI did, and state who verified it.",
  "prompts": [
   {"id": "P9", "title": "Methods paragraph and AI disclosure", "types": ["Structured output", "Constraint"], "runs_code": False,
    "parts": [
     ("task", "Draft the methods paragraph for this secondary analysis: dataset and citation (" + DATASET_CITE + " Licence: CC BY 4.0), cleaning steps, statistical tests and software, and an AI-use disclosure."),
     ("format", " About 200 words, APA 7 style, followed by a separate two-sentence disclosure statement."),
     ("check", " The disclosure must name the AI tool and version, say which steps it performed, and state that all numbers were verified by re-running the code. Do not invent software versions; leave [brackets] where you do not know.")]},
  ]},
 {"id": "s10", "n": "10", "title": "Make it reusable", "lead": "Turn this conversation into a context file and a skill so the next study starts here.",
  "prompts": [
   {"id": "P10", "title": "Write research-context.md and SKILL.md", "types": ["Meta-prompt", "Structured output"], "runs_code": False,
    "parts": [
     ("task", "From this conversation, write two files. (1) research-context.md, at most 40 lines: research questions, dataset citation and licence, variable coding, analysis conventions, ethics rules, and how I want you to work. (2) SKILL.md for a skill named survey-analysis-workflow that turns steps 2–9 into a reusable procedure."),
     ("format", " SKILL.md must start with front matter: name, and a description of at most 200 characters that says what it does and when to use it."),
     ("check", " Keep every rule concrete enough to check, for example \"report Cramér's V with every chi-square\".")]},
  ]},
]

PROMPT_TYPES = [
 ("Zero-shot instruction", "A clear task with no examples.", "Give me the number of missing values in each column of the attached file.", "Quick facts; first look at the data"),
 ("Role prompt", "Tell the AI whose standards to apply.", "Act as a research ethics reviewer at a university in Bangladesh…", "Ethics checks, reviews, statistics advice"),
 ("Context-rich (RCTFC)", "Role, context, task, format, check in one prompt.", "Every prompt in the Prompt Lab follows this pattern.", "Any analysis step you want to reproduce"),
 ("Few-shot", "Show worked examples, then ask for the rest.", "\"Software Engineer\" → Software & IT; \"Pharmacist\" → Health & Food… now classify all 160 careers.", "Coding free text, categorising"),
 ("Plan-then-execute", "Ask for a plan, approve it, then run.", "Propose a cleaning plan and wait for my approval before running it.", "Cleaning, anything that changes data"),
 ("Structured output", "Fix the shape of the answer: table, JSON, schema.", "Report a table: hypothesis, test, statistic, df, p, effect size, verdict.", "Results you will paste or compare"),
 ("Tool use (code)", "Make the AI run Python and show the code.", "Run Python to create… save each chart as a 300-dpi PNG and show the code.", "Statistics, charts, files"),
 ("Self-verification", "Make the AI recompute and compare.", "Re-compute every number from the raw file in a fresh cell… show reported vs recomputed.", "Before any number leaves the chat"),
 ("Critique / red team", "Ask the AI to argue against you.", "Act as a sceptical reviewer… flag any sentence that overstates the evidence.", "Interpretation, discussion, abstracts"),
 ("Meta-prompt", "Ask the AI to write or improve a prompt or file.", "From this conversation, write research-context.md and a SKILL.md…", "Building context files, skills, templates"),
]
