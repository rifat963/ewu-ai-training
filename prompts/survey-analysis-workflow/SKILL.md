---
name: survey-analysis-workflow
description: Runs a verified survey analysis from quality audit to APA write-up with code, effect sizes and an AI-use disclosure. Use when asked to analyse, test or report survey data.
---

# Survey analysis workflow

## When to use
- A survey file (CSV or Excel) needs analysing for a paper or report
- Someone asks for descriptive statistics, hypothesis tests, charts or a methods paragraph

## Steps
1. Ethics gate: check licence, consent, anonymisation and small-cell risk. Stop if the data are identifiable.
2. Build a data dictionary: type, unique values, missing values per column.
3. Audit quality (duplicates, missing, synonyms, spelling, invalid codes). Change nothing.
4. Propose a cleaning plan; wait for approval; execute and log every change; report rows before and after.
5. Describe: n and % for categorical variables; mean, SD and range for numeric ones.
6. Visualise: colour-blind-safe charts, labelled axes, n in titles, bars from zero; save 300-dpi PNGs.
7. Test: choose tests that fit the measurement level; check assumptions; report statistic, df, p and effect size.
8. Model when asked: ordinal or logistic regression with odds ratios and 95% CIs.
9. Verify: recompute every reported number from the raw file in a fresh cell; show a match table.
10. Report: APA methods and results, limitations, and an AI-use disclosure.

## Rules
- Show the code for every number
- Never drop rows or impute without approval
- Use associational language; never claim causation from survey data
- Never report cells smaller than 10 participants

## Output
- Clean data file and cleaning log
- Tables and figures ready for a paper
- Methods paragraph, results paragraph and AI-use disclosure
