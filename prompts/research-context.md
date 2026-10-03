# Research context: Career anxiety and AI among Bangladeshi students

## Research questions
- RQ1: Is career anxiety associated with the belief that AI will replace jobs?
- RQ2: Does career anxiety differ by AI knowledge, gender or academic year?
- RQ3: Which perceptions predict higher career anxiety together (ordinal regression)?

## Data
- Islam, S., Piyas, B. R. C., Tisha, F. J., Nayem, H. K., Rahman, S., Preenon, B. R. C., & Hossen, S. (2026). Career anxiety in the age of artificial intelligence: Survey data of university students in Bangladesh. Data in Brief, 67, 112924. https://doi.org/10.1016/j.dib.2026.112924
- Licence CC BY 4.0: cite the article and DOI in every output
- 3,156 students, five universities, one row per student, consent = Yes for all

## Coding (always recode from text labels, not the provided numbers)
- career_anxiety: No Anxiety=0, Low=1, Medium=2, High=3 (outcome)
- ai_knowledge: Low=1, Medium=2, High=3 (45 missing: keep missing)
- ai_replace_jobs: No=0, Partially=1, Fully=2
- ai_future_perspective: helpful tool=0 … complete takeover=4
- ai_tools_used: comma-separated; split into 0/1 columns

## Analysis conventions
- Run Python for every number and show the code
- Chi-square with Cramér's V; Spearman's rho for ordinal pairs; report effect sizes and 95% CIs
- APA 7; p to three decimals, "p < .001" below that; associational language only

## Ethics (EWU)
- Never attempt to re-identify participants; do not report cells with n < 10
- Follow EWU's research ethics policy; new data I collect needs EWUREC review
- Disclose AI use (tool, version, steps); I verify every number before use

## How to work with me
- Plan before changing data; wait for approval
- Say when you are unsure; never invent citations or results
