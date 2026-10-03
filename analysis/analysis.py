"""Reference analysis of the Career Anxiety in the Age of AI dataset (Islam et al., 2026, Data in Brief).
Produces the 'possible results' shown on the Prompt Lab website."""
import json, os, re, shutil
import numpy as np, pandas as pd
from scipy import stats
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

UP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = f"{OUT}/results/figures"; TAB = f"{OUT}/results/tables"
os.makedirs(FIG, exist_ok=True); os.makedirs(TAB, exist_ok=True)
R = {}

raw = pd.read_excel(f"{UP}/dataset.xlsx")
enc = pd.read_excel(f"{UP}/dataset_variable_encoded.xlsx")
R["n"] = len(raw); R["cols"] = list(raw.columns)

# ---------- 1. data quality audit ----------
q = {}
q["missing"] = {k: int(v) for k, v in raw.isna().sum().items() if v}
q["dup_rows"] = int(raw.duplicated().sum()); q["dup_ids"] = int(raw.participant_id.duplicated().sum())
q["consent"] = raw.consent.value_counts().to_dict()
q["age"] = {"min": int(raw.age.min()), "max": int(raw.age.max()), "mean": round(raw.age.mean(), 2), "sd": round(raw.age.std(), 2)}
small_ages = raw.age.value_counts()
q["rare_ages"] = {int(k): int(v) for k, v in small_ages[small_ages < 10].items()}
none_like = raw.ai_tool_perception.dropna()
none_like = none_like[none_like.str.strip().str.lower().isin(["none", "nothing", "none of them", "i don't know for now", "no", "n/a", "na"])]
q["perception_none_variants"] = none_like.value_counts().to_dict()
q["perception_levels"] = int(raw.ai_tool_perception.nunique())
q["career_levels"] = int(raw.career_path.nunique())
q["encoded_bad_values"] = {c: sorted(map(str, set(enc[c].dropna()) - set(range(0, 10)))) for c in enc.columns
                           if c in ["gender", "ai_knowledge", "ai_future_perspective", "ai_replace_jobs", "ai_takeover_time", "career_anxiety"]}
q["encoded_bad_values"] = {k: v for k, v in q["encoded_bad_values"].items() if v}
bad_row = enc[enc.ai_takeover_time.astype(str) == "h"]
q["encoded_bad_row"] = {"participant_id": bad_row.participant_id.iloc[0], "raw_value": raw.loc[raw.participant_id == bad_row.participant_id.iloc[0], "ai_takeover_time"].iloc[0]} if len(bad_row) else None
tools_split = raw.ai_tools_used.str.split(",").explode().str.strip()
q["tool_spellings"] = sorted([t for t in tools_split.unique() if t and t.lower() in ("quiltbot", "quillbot", "deepseek", "deep seek")])
R["quality"] = q

# ---------- 2. cleaning & encoding ----------
df = raw.copy()
ORD = {
    "career_anxiety": ["No Anxiety", "Low", "Medium", "High"],
    "ai_knowledge": ["Low", "Medium", "High"],
    "ai_replace_jobs": ["No", "Partially", "Fully"],
    "ai_takeover_time": ["Never", "50+ years", "21–50 years", "11–20 years", "6–10 years", "1–5 years"],
    "academic_year": ["1st Year", "2nd Year", "3rd Year", "4th Year"],
}
PERSP = {
    "I strongly believe AI cannot take over human activities and will be a helpful tool for humans.": (0, "Helpful tool only"),
    "I believe AI will mostly assist humans, with limited job replacement.": (1, "Mostly assist"),
    "I think AI will replace some human jobs but also create new opportunities.": (2, "Replace some, create new"),
    "I believe AI will significantly replace human jobs and create major challenges.": (3, "Significantly replace"),
    "I strongly believe AI will completely take over human jobs and pose serious threat to humanity.": (4, "Complete takeover"),
}
for c, lv in ORD.items():
    df[c + "_code"] = df[c].map({v: i for i, v in enumerate(lv)})
df["perspective_code"] = df.ai_future_perspective.map(lambda s: PERSP[s][0])
df["perspective_short"] = df.ai_future_perspective.map(lambda s: PERSP[s][1])
df["female"] = (df.gender == "Female").astype(int)
norm = lambda s: s.strip().replace("Quiltbot", "QuillBot") if isinstance(s, str) else s
df["ai_tool_perception_clean"] = df.ai_tool_perception.map(norm).replace({"none": "None", "Nothing": "None", "None of them": "None", "I don't know for now": "Don't know"})
tools = raw.ai_tools_used.str.split(",").apply(lambda L: [norm(t) for t in L if t.strip()])
df["n_tools"] = tools.apply(len)
tool_counts = pd.Series([t for L in tools for t in L]).value_counts()
top_tools = tool_counts.head(8).index.tolist()
for t in top_tools:
    df["uses_" + re.sub(r"\W+", "_", t).strip("_").lower()] = tools.apply(lambda L: int(t in L))
R["tools"] = {k: int(v) for k, v in tool_counts.head(12).items()}
R["tools_pct"] = {k: round(v / len(df) * 100, 1) for k, v in tool_counts.head(12).items()}
R["n_tools"] = {"mean": round(df.n_tools.mean(), 2), "median": int(df.n_tools.median()), "max": int(df.n_tools.max())}
df.to_csv(f"{OUT}/results/tables/dataset_clean_encoded.csv", index=False)

# ---------- 3. descriptives ----------
def freq(col, order=None):
    vc = df[col].value_counts(dropna=False)
    if order: vc = vc.reindex(order + [x for x in vc.index if x not in order])
    t = pd.DataFrame({"n": vc, "pct": (vc / vc.sum() * 100).round(1)})
    t.index = t.index.map(lambda x: "Missing" if pd.isna(x) else x)
    return t
D = {}
for c, order in [("career_anxiety", ORD["career_anxiety"]), ("gender", None), ("academic_year", ORD["academic_year"]),
                 ("ai_knowledge", ORD["ai_knowledge"]), ("ai_replace_jobs", ORD["ai_replace_jobs"]),
                 ("ai_takeover_time", ORD["ai_takeover_time"]), ("perspective_short", [v[1] for v in PERSP.values()])]:
    t = freq(c, order); t.to_csv(f"{TAB}/freq_{c}.csv"); D[c] = {str(k): [int(r.n), float(r.pct)] for k, r in t.iterrows()}
R["freq"] = D
R["career_top"] = {k: int(v) for k, v in raw.career_path.value_counts().head(8).items()}

ct = pd.crosstab(df.ai_knowledge, df.career_anxiety, normalize="index").reindex(index=ORD["ai_knowledge"], columns=ORD["career_anxiety"]) * 100
R["ct_knowledge_anx_pct"] = ct.round(1).to_dict(orient="index")
ct2 = pd.crosstab(df.ai_replace_jobs, df.career_anxiety, normalize="index").reindex(index=ORD["ai_replace_jobs"], columns=ORD["career_anxiety"]) * 100
R["ct_replace_anx_pct"] = ct2.round(1).to_dict(orient="index")
ct3 = pd.crosstab(df.gender, df.career_anxiety, normalize="index").reindex(columns=ORD["career_anxiety"]) * 100
R["ct_gender_anx_pct"] = ct3.round(1).to_dict(orient="index")
ct4 = pd.crosstab(df.perspective_short, df.career_anxiety, normalize="index").reindex(index=[v[1] for v in PERSP.values()], columns=ORD["career_anxiety"]) * 100
R["ct_persp_anx_pct"] = ct4.round(1).to_dict(orient="index")
R["high_med_by_persp"] = (ct4["High"] + ct4["Medium"]).round(1).to_dict()

# ---------- 4. inferential ----------
def chi(a, b):
    t = pd.crosstab(df[a], df[b]); c = stats.chi2_contingency(t)
    k = min(t.shape) - 1; v = np.sqrt(c.statistic / (t.values.sum() * k))
    return {"chi2": round(c.statistic, 2), "df": int(c.dof), "p": float(c.pvalue), "cramers_v": round(v, 3), "n": int(t.values.sum()),
            "min_expected": round(float(c.expected_freq.min()), 1)}
I = {"chi_gender": chi("gender", "career_anxiety"), "chi_knowledge": chi("ai_knowledge", "career_anxiety"),
     "chi_replace": chi("ai_replace_jobs", "career_anxiety"), "chi_year": chi("academic_year", "career_anxiety"),
     "chi_perspective": chi("perspective_short", "career_anxiety")}
sp = {}
for c in ["ai_knowledge_code", "ai_replace_jobs_code", "perspective_code", "ai_takeover_time_code", "academic_year_code", "age", "n_tools"]:
    x = df[[c, "career_anxiety_code"]].dropna(); r = stats.spearmanr(x[c], x.career_anxiety_code)
    sp[c] = {"rho": round(r.statistic, 3), "p": float(r.pvalue), "n": len(x)}
I["spearman"] = sp
groups = [g.career_anxiety_code.values for _, g in df.groupby("academic_year")]
kw = stats.kruskal(*groups); n = len(df); eps2 = (kw.statistic - len(groups) + 1) / (n - len(groups))
I["kruskal_year"] = {"H": round(kw.statistic, 2), "df": len(groups) - 1, "p": float(kw.pvalue), "epsilon2": round(eps2, 4)}
mw = stats.mannwhitneyu(df.loc[df.female == 1, "career_anxiety_code"], df.loc[df.female == 0, "career_anxiety_code"])
I["mw_gender"] = {"U": float(mw.statistic), "p": float(mw.pvalue),
                  "mean_female": round(df.loc[df.female == 1, "career_anxiety_code"].mean(), 2),
                  "mean_male": round(df.loc[df.female == 0, "career_anxiety_code"].mean(), 2)}

from statsmodels.miscmodels.ordinal_model import OrderedModel
m = df[["career_anxiety_code", "ai_knowledge_code", "ai_replace_jobs_code", "perspective_code", "female", "academic_year_code"]].dropna()
mod = OrderedModel(m.career_anxiety_code, m[["ai_knowledge_code", "ai_replace_jobs_code", "perspective_code", "female", "academic_year_code"]], distr="logit")
res = mod.fit(method="bfgs", disp=False)
ors = []
for v in ["ai_knowledge_code", "ai_replace_jobs_code", "perspective_code", "female", "academic_year_code"]:
    b, se, p = res.params[v], res.bse[v], res.pvalues[v]
    ors.append({"predictor": v, "OR": round(np.exp(b), 2), "ci_low": round(np.exp(b - 1.96 * se), 2), "ci_high": round(np.exp(b + 1.96 * se), 2), "p": float(p)})
I["ordinal_logit"] = {"n": len(m), "ors": ors, "pseudo_r2": round(1 - res.llf / OrderedModel(m.career_anxiety_code, m[["female"]] * 0 + 0, distr="logit").fit(method="bfgs", disp=False).llf, 3) if False else None}
# McFadden pseudo R2 vs thresholds-only model
null_ll = np.sum(np.log(m.career_anxiety_code.value_counts(normalize=True).reindex(m.career_anxiety_code).values))
I["ordinal_logit"]["mcfadden_r2"] = round(1 - res.llf / null_ll, 3)
pd.DataFrame(ors).to_csv(f"{TAB}/ordinal_logit_odds_ratios.csv", index=False)
R["inferential"] = I

# ---------- 5. figures ----------
BLUE, ORANGE, INK, GREY = "#25668C", "#C8621A", "#14213D", "#8A94A6"
SEQ = ["#D6E4EE", "#93BCD6", "#4B8DB8", "#1F4E79"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titleweight": "bold", "axes.titlesize": 12, "axes.titlelocation": "left", "figure.dpi": 150})

def save(fig, name):
    fig.savefig(f"{FIG}/{name}.png", bbox_inches="tight", dpi=170, facecolor="white"); plt.close(fig)

# F1 anxiety distribution
f = D["career_anxiety"]; labs = ORD["career_anxiety"]
fig, ax = plt.subplots(figsize=(6.4, 3.6))
bars = ax.bar(labs, [f[l][0] for l in labs], color=[SEQ[0], SEQ[1], SEQ[2], ORANGE])
for b_, l in zip(bars, labs): ax.text(b_.get_x() + b_.get_width() / 2, b_.get_height() + 25, f"{f[l][0]}\n({f[l][1]}%)", ha="center", fontsize=9.5)
ax.set_ylabel("Students"); ax.set_ylim(0, max(f[l][0] for l in labs) * 1.22)
ax.set_title(f"Career anxiety (n = {len(df):,})"); save(fig, "fig1_anxiety_distribution")

# F2 stacked anxiety by knowledge
def stacked(ctab, title, name, ylab):
    fig, ax = plt.subplots(figsize=(7.2, 0.7 * len(ctab) + 1.6)); left = np.zeros(len(ctab))
    for j, col in enumerate(ORD["career_anxiety"]):
        v = ctab[col].values; ax.barh(ctab.index, v, left=left, color=(SEQ + [ORANGE])[j] if j < 3 else ORANGE, label=col, edgecolor="white")
        for i, (l, w) in enumerate(zip(left, v)):
            if w >= 6: ax.text(l + w / 2, i, f"{w:.0f}%", ha="center", va="center", fontsize=8.5, color="white" if j >= 2 else INK)
        left += v
    ax.set_xlim(0, 100); ax.set_xlabel("% of students in each group"); ax.set_ylabel(ylab); ax.invert_yaxis()
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(.5, -.28), frameon=False, fontsize=9, title="Career anxiety", title_fontsize=9)
    ax.set_title(title); save(fig, name)
stacked(ct, "Career anxiety by self-rated AI knowledge", "fig2_anxiety_by_knowledge", "AI knowledge")
stacked(ct2, "Career anxiety by belief that AI will replace jobs", "fig3_anxiety_by_replace", "Will AI replace jobs?")
ct4b = ct4.copy(); stacked(ct4b, "Career anxiety by view of AI's future", "fig4_anxiety_by_perspective", "View of AI's future")

# F5 tools
tc = pd.Series(R["tools_pct"]).head(10)[::-1]
fig, ax = plt.subplots(figsize=(6.6, 4))
ax.barh(tc.index, tc.values, color=[ORANGE if i == len(tc) - 1 else BLUE for i in range(len(tc))])
for i, v in enumerate(tc.values): ax.text(v + 1, i, f"{v:.0f}%", va="center", fontsize=9)
ax.set_xlabel("% of students who use the tool (multi-select)"); ax.set_xlim(0, 105)
ax.set_title("AI tools students use"); save(fig, "fig5_tools_used")

# F6 odds ratio forest
lab_map = {"ai_knowledge_code": "AI knowledge (per level)", "ai_replace_jobs_code": "Belief AI replaces jobs (per level)",
           "perspective_code": "Threat view of AI's future (per level)", "female": "Female (vs male)", "academic_year_code": "Academic year (per year)"}
fig, ax = plt.subplots(figsize=(6.8, 3.4))
for i, o in enumerate(ors[::-1]):
    c = ORANGE if o["p"] < .05 else GREY
    ax.plot([o["ci_low"], o["ci_high"]], [i, i], color=c, lw=2); ax.plot(o["OR"], i, "o", color=c, ms=7)
    ax.text(max(o["ci_high"], 1) + .04, i, f"OR {o['OR']:.2f} [{o['ci_low']:.2f}, {o['ci_high']:.2f}]", va="center", fontsize=8.5)
ax.axvline(1, color=INK, lw=1, ls="--"); ax.set_yticks(range(len(ors)), [lab_map[o["predictor"]] for o in ors[::-1]])
ax.set_xlabel("Odds ratio for higher career anxiety (95% CI, log scale)"); ax.set_xscale("log")
ax.set_xlim(min(o["ci_low"] for o in ors) * .85, max(o["ci_high"] for o in ors) * 1.9)
from matplotlib.ticker import FixedLocator, FuncFormatter
ax.xaxis.set_major_locator(FixedLocator([0.7, 0.8, 0.9, 1, 1.2, 1.5, 2, 2.5]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}")); ax.xaxis.set_minor_locator(FixedLocator([]))
ax.set_title(f"Ordinal logistic regression (n = {len(m):,})"); save(fig, "fig6_ordinal_odds_ratios")

json.dump(R, open(f"{OUT}/results/reference_results.json", "w"), indent=1, default=str)
print(json.dumps({k: R[k] for k in ["quality", "tools", "n_tools", "inferential"]}, indent=1, default=str)[:6000])
