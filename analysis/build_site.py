"""Build the Prompt Lab website, prompt files and repo assets from the reference analysis."""
import base64, html, json, os, re, shutil
import pandas as pd
from prompts import STEPS, PROMPT_TYPES, DATASET_CITE

D = os.path.dirname(os.path.abspath(__file__)); UP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
R = json.load(open(f"{D}/results/reference_results.json"))
raw = pd.read_excel(f"{UP}/dataset.xlsx"); enc = pd.read_excel(f"{UP}/dataset_variable_encoded.xlsx")
I = R["inferential"]; Q = R["quality"]; F = R["freq"]
e = html.escape

def p_fmt(p): return "< .001" if p < .001 else f"{p:.3f}".lstrip("0")
def p_apa(p): return "p < .001" if p < .001 else "p = " + f"{p:.3f}".lstrip("0")
def table(head, rows, cls=""):
    h = "".join(f"<th>{e(str(x))}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def fig(name, alt):
    b64 = base64.b64encode(open(f"{D}/results/figures/{name}.png", "rb").read()).decode()
    return f'<figure><img src="data:image/png;base64,{b64}" alt="{e(alt)}" loading="lazy"><figcaption>{e(alt)}</figcaption></figure>'

# ---------- career grouping (P3b result) ----------
RULES = [("Data & AI", r"\bdata\b|dara|\bai\b|\bml\b|machine learning|ai/ml|bioinformatic"),
         ("Cybersecurity", r"cyber|hacker|security"),
         ("Health & Food", r"pharm|nutrition|physician|food|drug"),
         ("Business & Finance", r"business|bank|account|entrepreneur|finance|market|corporate|ceo|director|cfo|\bhr\b|manager|trader"),
         ("Research & Academia", r"research|reseacrher|reasearcher|scientist|teacher|lecturer|faculty|professor|r&d"),
         ("Creative & Media", r"design|anim|graphic|writer|news|journal|content|editor|novel|influ"),
         ("Software & IT", r"software|developer|devloper|programmer|web|app|devops|database|blockchain|computer|network|cloud|sqa|stack|front|backend|java|django|larabel|game|tech|it-based|it industry"),
         ("Engineering", r"engineer|robotic|textile|telecom|production|maintainance"),
         ("Public service", r"government|civil|police|\bmto\b")]
def group(s):
    t = s.lower()
    for g, rx in RULES:
        if re.search(rx, t): return g
    return "Other"
cg = raw.career_path.map(group)
multi = raw.career_path[raw.career_path.str.contains(r",| or |&|/|\band\b", case=False)].nunique()
cgc = cg.value_counts()
R["career_groups"] = {k: int(v) for k, v in cgc.items()}

# ---------- results HTML per prompt ----------
RES = {}
RES["P0"] = table(["Issue", "What the file or paper shows", "Risk", "Action"], [
    ["Licence", "CC BY 4.0 (Data in Brief, 2026)", '<span class="pill ok">Low</span>', "Reuse is allowed; cite the article and DOI in every output"],
    ["Consent", f"consent = Yes for all {R['n']:,} rows; only consenting responses were kept", '<span class="pill ok">Low</span>', "Report the original consent procedure"],
    ["Anonymisation", "Random 6-character IDs (e.g. 77BE5Q); no names, emails or student IDs", '<span class="pill ok">Low</span>', "Never try to link IDs to people"],
    ["Re-identification", f"Ages 26 and 27 have only {Q['rare_ages']['26']} and {Q['rare_ages']['27']} students; adding gender, year and a rare career narrows to 1–2 people", '<span class="pill warn">Medium</span>', "Do not publish small cells (n &lt; 10); group ages, e.g. 18–20, 21–23, 24+"],
    ["Uploading to AI", "Public, anonymised, openly licensed file", '<span class="pill ok">Low</span>', "Acceptable here. Check your account's data-training setting. Never upload identifiable data of your own"],
    ["Original approval", "Paper reports verbal approval from institutional review boards", '<span class="pill warn">Medium</span>', "Mention it as a limitation; your own new data needs written EWUREC review"],
    ["Disclosure", "AI will run code and draft text", '<span class="pill warn">Medium</span>', "Disclose tool, version and steps; you remain responsible for every number"],
])
dic = []
types = {"participant_id": "ID", "age": "Numeric", "gender": "Nominal", "academic_year": "Ordinal", "ai_knowledge": "Ordinal", "ai_tools_used": "Multi-select",
         "career_path": "Free text", "ai_tool_perception": "Nominal (free text)", "ai_future_perspective": "Ordinal (statements)", "ai_replace_jobs": "Ordinal",
         "ai_takeover_time": "Ordinal", "career_anxiety": "Ordinal (outcome)", "consent": "Nominal"}
for c in raw.columns:
    ex = raw[c].dropna().astype(str).unique()[:2]; ex = "; ".join(x if len(x) < 48 else x[:45] + "…" for x in ex)
    dic.append([f"<code>{c}</code>", types[c], f"{raw[c].nunique():,}", str(int(raw[c].isna().sum())), e(ex)])
pd.DataFrame([[re.sub("<[^>]+>", "", r[0]), r[1], r[2], r[3], html.unescape(r[4])] for r in dic],
             columns=["column", "type", "unique_values", "missing", "examples"]).to_csv(f"{D}/results/tables/data_dictionary.csv", index=False)
RES["P1"] = table(["Column", "Type", "Unique", "Missing", "Examples"], dic) + """
<ol class="rq"><li><b>RQ1.</b> Is career anxiety associated with the belief that AI will replace jobs? <i>career_anxiety × ai_replace_jobs · chi-square, Spearman's ρ</i></li>
<li><b>RQ2.</b> Does career anxiety differ by self-rated AI knowledge, gender or academic year? <i>chi-square with Cramér's V, Kruskal–Wallis</i></li>
<li><b>RQ3.</b> Which perceptions predict higher career anxiety when considered together? <i>ordinal logistic regression</i></li></ol>"""
RES["P2"] = table(["Check", "Finding", "Examples"], [
    ["Duplicates", f"{Q['dup_rows']} duplicate rows, {Q['dup_ids']} duplicate IDs", "–"],
    ["Missing values", f"ai_knowledge: {Q['missing']['ai_knowledge']} ({Q['missing']['ai_knowledge']/R['n']*100:.1f}%); ai_tool_perception: {Q['missing']['ai_tool_perception']} ({Q['missing']['ai_tool_perception']/R['n']*100:.1f}%)", "No \"None\" category for ai_knowledge, although the paper lists one"],
    ["Synonyms", f"\"no tool\" written {len(Q['perception_none_variants'])} ways in ai_tool_perception ({sum(Q['perception_none_variants'].values())} answers)", e(", ".join(f'"{k}" ({v})' for k, v in Q['perception_none_variants'].items()))],
    ["Spelling", "Quiltbot and quillbot for QuillBot", "In ai_tools_used and ai_tool_perception"],
    ["Free text", f"career_path has {Q['career_levels']} distinct answers; ai_tool_perception has {Q['perception_levels']}", "\"Reseacrher\", \"Electical Engineer\", \"Dara Scientist\""],
    ["Multi-select", "ai_tools_used holds comma-separated lists", "\"ChatGPT, Quiltbot, Grammarly\""],
    ["Age range", f"{Q['age']['min']}–{Q['age']['max']}, mean {Q['age']['mean']} (SD {Q['age']['sd']})", "Plausible; no out-of-range values"],
    ["Consent", "All rows = Yes", "–"],
    ['<b>Encoded file</b>', '<b>ai_takeover_time contains the invalid code "h"</b>', f"participant {Q['encoded_bad_row']['participant_id']}; the raw file says \"{Q['encoded_bad_row']['raw_value']}\", so the code should be 0"],
]) + '<p class="note">The encoded file also uses different codes from a natural order for ai_future_perspective and ai_takeover_time. Recode from the text labels rather than trusting the provided numbers.</p>'
tp = R["tools_pct"]
RES["P3"] = table(["#", "Step", "Rows affected", "Change"], [
    ["1", "Keep missing ai_knowledge", f"{Q['missing']['ai_knowledge']}", "Left as missing; excluded only from analyses that use it"],
    ["2", "Merge synonyms in ai_tool_perception", f"{sum(Q['perception_none_variants'].values())}", "none / Nothing / None of them / No → None; I don't know for now → Don't know"],
    ["3", "Fix spelling", "QuillBot answers", "Quiltbot, quillbot → QuillBot"],
    ["4", "Split ai_tools_used", f"{R['n']:,}", f"One 0/1 column per tool; students use {R['n_tools']['mean']} tools on average (max {R['n_tools']['max']})"],
    ["5", "Encode ordinal variables", f"{R['n']:,}", "career_anxiety 0–3, ai_knowledge 1–3, ai_replace_jobs 0–2, ai_future_perspective 0–4, ai_takeover_time 0–5"],
    ["6", "Row count", f"{R['n']:,} → {R['n']:,}", "No rows dropped"],
])
RES["P3b"] = table(["Career group", "Students", "%"], [[g, f"{v:,}", f"{v/R['n']*100:.1f}"] for g, v in cgc.items()]) + \
    f'<p class="note">{multi} distinct answers name more than one career (e.g. "Software Engineer, Researcher"); they were assigned to the first match and should be reviewed by hand.</p>'
def ftab(var, title):
    return f"<h4>{title}</h4>" + table(["Category", "n", "%"], [[e(k), f"{v[0]:,}", f"{v[1]:.1f}"] for k, v in F[var].items()])
RES["P4"] = '<div class="grid2">' + ftab("career_anxiety", f"Career anxiety (n = {R['n']:,})") + ftab("ai_knowledge", "Self-rated AI knowledge") + \
    ftab("ai_replace_jobs", "Will AI replace jobs?") + ftab("gender", "Gender") + ftab("academic_year", "Academic year") + \
    "<h4 class='span2'>AI tools used (multi-select, % of students)</h4>" + "</div>" + \
    table(["Tool", "%"], [[k, f"{v:.1f}"] for k, v in list(tp.items())[:8]]) + \
    f'<p class="note">Age: M = {Q["age"]["mean"]}, SD = {Q["age"]["sd"]}, range {Q["age"]["min"]}–{Q["age"]["max"]}. Claude was named by only {tp.get("Claude", 0)}% of students.</p>'
RES["P5"] = fig("fig1_anxiety_distribution", "Figure 1. Distribution of career anxiety") + fig("fig2_anxiety_by_knowledge", "Figure 2. Career anxiety by self-rated AI knowledge") + \
    fig("fig3_anxiety_by_replace", "Figure 3. Career anxiety by belief that AI will replace jobs") + fig("fig5_tools_used", "Figure 4. AI tools students use")
c, s = I, I["spearman"]
RES["P6"] = table(["Hypothesis", "Test", "Result", "Effect size", "Verdict"], [
    ["H1 Gender", "χ² test", f"χ²({c['chi_gender']['df']}) = {c['chi_gender']['chi2']}, p = {p_fmt(c['chi_gender']['p'])}", f"V = {c['chi_gender']['cramers_v']:.2f}", "No evidence of a difference"],
    ["H2 AI knowledge", "χ² test", f"χ²({c['chi_knowledge']['df']}) = {c['chi_knowledge']['chi2']}, p {p_fmt(c['chi_knowledge']['p']) if c['chi_knowledge']['p']<.001 else '= '+p_fmt(c['chi_knowledge']['p'])}", f"V = {c['chi_knowledge']['cramers_v']:.2f}", "Associated, very small"],
    ["H2 AI knowledge (trend)", "Spearman's ρ", f"ρ = {s['ai_knowledge_code']['rho']:.2f}, p = {p_fmt(s['ai_knowledge_code']['p'])}", "–", "No monotonic trend"],
    ["H3 Replace jobs", "χ² test", f"χ²({c['chi_replace']['df']}) = {c['chi_replace']['chi2']}, p {p_fmt(c['chi_replace']['p'])}", f"V = {c['chi_replace']['cramers_v']:.2f}", "Associated, small"],
    ["H3 Replace jobs (trend)", "Spearman's ρ", f"ρ = {s['ai_replace_jobs_code']['rho']:.2f}, p {p_fmt(s['ai_replace_jobs_code']['p'])}", "–", "Weak positive trend"],
    ["H4 Academic year", "Kruskal–Wallis", f"H({I['kruskal_year']['df']}) = {I['kruskal_year']['H']:.2f}, p = {p_fmt(I['kruskal_year']['p'])}", f"ε² = {I['kruskal_year']['epsilon2']:.3f}", "No evidence of a difference"],
]) + f'<p class="note"><b>Why H2 matters:</b> the chi-square is significant but Spearman\'s ρ is not. Students with high AI knowledge are the most likely to report <i>no</i> anxiety ({R["ct_knowledge_anx_pct"]["High"]["No Anxiety"]}%) and also the most likely to report <i>high</i> anxiety ({R["ct_knowledge_anx_pct"]["High"]["High"]}%). Ask the AI to explain such patterns rather than reporting only "p &lt; .05". All expected cell counts were ≥ {min(c[k]["min_expected"] for k in ["chi_gender","chi_knowledge","chi_replace","chi_year"]):.0f}.</p>'
RES["PV"] = table(["Statistic", "Reported", "Recomputed", "Match"], [
    ["χ² (anxiety × replace jobs)", f"{c['chi_replace']['chi2']}", f"{c['chi_replace']['chi2']}", '<span class="pill ok">yes</span>'],
    ["Cramér's V", f"{c['chi_replace']['cramers_v']:.3f}", f"{c['chi_replace']['cramers_v']:.3f}", '<span class="pill ok">yes</span>'],
    ["Spearman's ρ (knowledge)", f"{s['ai_knowledge_code']['rho']:.3f}", f"{s['ai_knowledge_code']['rho']:.3f}", '<span class="pill ok">yes</span>'],
    ["n used for knowledge tests", f"{c['chi_knowledge']['n']:,}", f"{c['chi_knowledge']['n']:,}", '<span class="pill ok">yes</span>'],
]) + '<p class="note">A mismatch usually means the AI used a different cleaning step or silently dropped rows. Find out which value is right before you write anything.</p>'
L = {"ai_knowledge_code": "AI knowledge (per level)", "ai_replace_jobs_code": "Belief AI replaces jobs (per level)", "perspective_code": "Threat view of AI's future (per level)", "female": "Female vs male", "academic_year_code": "Academic year (per year)"}
ors = I["ordinal_logit"]["ors"]
RES["P7"] = table(["Predictor", "Odds ratio", "95% CI", "p"], [[L[o["predictor"]], f"{o['OR']:.2f}", f"[{o['ci_low']:.2f}, {o['ci_high']:.2f}]", p_fmt(o["p"])] for o in ors]) + \
    fig("fig6_ordinal_odds_ratios", "Figure 5. Odds ratios for higher career anxiety") + f"""
<ul class="plain"><li>Each step up in believing AI will replace jobs (No → Partially → Fully) goes with 1.48 times the odds of a higher anxiety level, holding the other predictors constant.</li>
<li>Each step towards a more threatening view of AI's future goes with 1.17 times the odds.</li>
<li>Each additional academic year goes with slightly higher odds (1.09; the CI almost touches 1).</li>
<li>AI knowledge and gender show no clear association once the others are included.</li>
<li>McFadden's pseudo-R² = {I['ordinal_logit']['mcfadden_r2']:.3f}: these perceptions explain very little of the variation in anxiety. {R['n'] - I['ordinal_logit']['n']} rows were dropped for missing ai_knowledge.</li></ul>"""
RES["P8"] = f"""<blockquote>In a sample of {R['n']:,} university students in Bangladesh, believing that AI will replace jobs was associated with higher self-reported career anxiety (χ²({c['chi_replace']['df']}) = {c['chi_replace']['chi2']}, {p_apa(c['chi_replace']['p'])}, Cramér's V = {c['chi_replace']['cramers_v']:.2f}); in an ordinal model, each step in that belief went with 1.48 times the odds of a higher anxiety level (95% CI 1.30–1.70). Anxiety did not differ meaningfully by gender or academic year, and self-rated AI knowledge showed no monotonic trend. All effects were small, and together the predictors explained about 1% of the variation (McFadden R² = {I['ordinal_logit']['mcfadden_r2']:.3f}), so other factors not measured here, such as labour-market conditions or discipline, probably matter more.</blockquote>
<h4>Limitations the reviewer should raise</h4><ul class="plain"><li>Single-item, self-reported anxiety with four levels; no validated scale.</li><li>Cross-sectional: no causal direction.</li><li>Convenience sample from five universities, mostly technical disciplines (Software Engineer, Researcher and Data Scientist are the top careers).</li>
<li>An introductory AI seminar before the survey may have primed answers.</li><li>Gender recorded as binary.</li><li>Ethics approval reported as verbal.</li><li>The encoded file contains at least one invalid code; results depend on recoding from labels.</li></ul>"""
RES["P9"] = f"""<blockquote><b>Methods.</b> We analysed the openly available dataset of {DATASET_CITE} (CC BY 4.0), comprising {R['n']:,} responses from students at five Bangladeshi universities who gave informed consent. We merged synonymous categories, corrected spelling variants, split the multi-select tool variable into binary indicators and encoded ordinal variables from their text labels; no responses were removed, and {Q['missing']['ai_knowledge']} missing AI-knowledge values were left missing. We report frequencies, chi-square tests with Cramér's V, Spearman's rank correlations, a Kruskal–Wallis test and an ordinal (proportional-odds) logistic regression, computed in Python [version] with pandas, SciPy and statsmodels. Tests were two-sided at α = .05.</blockquote>
<blockquote><b>AI-use disclosure.</b> [Tool and version, e.g. Claude or ChatGPT] was used to write and run the analysis code and to draft this paragraph from our prompts. All numbers were verified by the authors by re-running the code on the original file, and the authors take full responsibility for the content.</blockquote>"""

CONTEXT = f"""# Research context: Career anxiety and AI among Bangladeshi students

## Research questions
- RQ1: Is career anxiety associated with the belief that AI will replace jobs?
- RQ2: Does career anxiety differ by AI knowledge, gender or academic year?
- RQ3: Which perceptions predict higher career anxiety together (ordinal regression)?

## Data
- {DATASET_CITE}
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
"""
SKILL = """---
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
"""
for name, txt in [("research-context.md", CONTEXT), ("SKILL.md", SKILL)]:
    open(f"{D}/results/{name}", "w").write(txt)
RES["P10"] = f'<div class="grid2"><div><h4>research-context.md</h4><pre class="file">{e(CONTEXT[:1150])}…</pre></div><div><h4>SKILL.md</h4><pre class="file">{e(SKILL[:1150])}…</pre></div></div><p class="note">Download both complete files from the Resources section. Paste the context file into a Claude or ChatGPT Project; upload the skill (zipped in a folder named survey-analysis-workflow) in Claude under Customize › Skills.</p>'

VERIFY = {"P0": "Read the dataset article's ethics statement yourself; do not rely on the AI's summary.",
          "P1": "Count the columns (13) and rows (3,156) yourself in Excel.",
          "P2": "Open the encoded file and filter ai_takeover_time: you should find the stray \"h\".",
          "P3": "Row count must stay 3,156. Spot-check five rows against the original file.",
          "P3b": "Read the mapping table; misspellings and two-career answers are where AI grouping goes wrong.",
          "P4": "Percentages in each table must add to 100; career anxiety Medium should be 1,634 (51.8%).",
          "P5": "Bars start at zero; n appears in titles; the numbers on charts match step 4.",
          "P6": "Run prompt PV. Check that the AI did not use a t-test on the ordinal outcome.",
          "PV": "Any mismatch: stop and find out why before writing.",
          "P7": "n should be 3,111 (45 rows missing ai_knowledge). ORs above 1 mean higher anxiety.",
          "P8": "Every sentence must be supported by a number from steps 6–7.",
          "P9": "Check the citation against the article page; fill every [bracket] yourself.",
          "P10": "Description of the skill ≤ 200 characters; each rule is testable."}
ETHICS = {"P0": "This is the step EWU's ethics committee would care about first.", "P1": "Uploading is acceptable only because this file is public and anonymised.",
          "P3b": "Free text can identify people; report groups, not rare individual answers.", "P4": "Do not report subgroup tables with cells under 10.",
          "P8": "Overclaiming is an ethical issue: participants and readers deserve accurate conclusions.", "P9": "Undisclosed AI use can count as misconduct under journal and university policies."}

# ---------- assemble data for the page ----------
steps_out = []
for st in STEPS:
    ps = []
    for p in st["prompts"]:
        ps.append({"id": p["id"], "title": p["title"], "types": p["types"], "code": p["runs_code"], "parts": p["parts"],
                   "result": RES[p["id"]], "verify": VERIFY.get(p["id"], ""), "ethics": ETHICS.get(p["id"], "")})
    steps_out.append({"id": st["id"], "n": st["n"], "title": st["title"], "lead": st["lead"], "prompts": ps})
csv_raw = raw.to_csv(index=False); csv_enc = enc.to_csv(index=False)
dict_csv = open(f"{D}/results/tables/data_dictionary.csv").read()

# prompts.md (repo + download)
md = ["# Prompt Lab: prompts for analysing the career-anxiety dataset", "",
      "Use these in order with Claude or ChatGPT after uploading `dataset.xlsx` (and `dataset_variable_encoded.xlsx` for step 2).",
      "Every prompt follows the pattern Role · Context · Task · Format · Check.", "", f"Dataset: {DATASET_CITE} Licence: CC BY 4.0.", ""]
for st in STEPS:
    md += [f"## Step {st['n']} · {st['title']}", "", st["lead"], ""]
    for p in st["prompts"]:
        md += [f"### {p['id']} · {p['title']}", "", f"*Type:* {', '.join(p['types'])}" + (" · *runs code*" if p["runs_code"] else ""), "", "```text", "".join(t for _, t in p["parts"]).strip(), "```", ""]
        if VERIFY.get(p["id"]): md += [f"**Verify:** {VERIFY[p['id']]}", ""]
PROMPTS_MD = "\n".join(md)
open(f"{D}/results/prompts.md", "w").write(PROMPTS_MD)

PAGE = {"steps": steps_out, "types": PROMPT_TYPES, "cite": DATASET_CITE,
        "files": {"dataset.csv": csv_raw, "dataset_variable_encoded.csv": csv_enc, "data_dictionary.csv": dict_csv,
                  "prompts.md": PROMPTS_MD, "research-context.md": CONTEXT, "SKILL.md": SKILL},
        "stats": {"n": R["n"], "medium": F["career_anxiety"]["Medium"][1], "high": F["career_anxiety"]["High"][1], "chatgpt": tp["ChatGPT"]}}
tpl = open(f"{D}/site_template.html").read()
page_json = json.dumps(PAGE, ensure_ascii=False).replace("</", "<\\/")
open(f"{D}/index.html", "w").write(tpl.replace("__PAGE_DATA__", page_json))
json.dump(R, open(f"{D}/results/reference_results.json", "w"), indent=1, default=str)
print("index.html", os.path.getsize(f"{D}/index.html") // 1024, "KB; career groups", R["career_groups"])
