# AI for Research: Prompt-Based Analysis

Training materials for CSE faculty at East West University (EWU). Participants analyse a real, published survey dataset using **standard prompts in Claude or ChatGPT**, with no code to write, and with ethics built into each step.

**Live site:** `https://rifat963.github.io/ewu-ai-training/` (once GitHub Pages is enabled)

## What is inside

| Folder | Contents |
|---|---|
| `index.html` | **EWU Prompt Lab**, an interactive site where you browse the 13 prompts, see each prompt's anatomy, copy it, and compare with the reference result. It also has the ethics checklist, prompt types, the prompt-to-agent ladder and the research ecosystem. |
| `slides/` | Slide deck (PDF, 27 slides) and speaker notes |
| `data/` | Demo dataset (Excel), data dictionary, citation and licence |
| `prompts/` | `prompts.md` (all prompts), `research-context.md` (example context file), `survey-analysis-workflow/SKILL.md` and its upload-ready `.zip` |
| `results/` | Reference figures, tables and `reference_results.json`, used to check your AI's answers |
| `analysis/` | Python scripts that produce the reference results and build the site (for reproducibility) |

## How participants use it

1. **Ethics first.** Read the ethics section of the site and tick the checklist.
2. **Download** `data/dataset.xlsx`.
3. **Open Claude or ChatGPT** and make sure code execution or analysis is on. Optionally, create a Project and add `prompts/research-context.md`.
4. **Run the prompts in order** (P0 to P10) from the site or `prompts/prompts.md`. The AI writes and runs Python, then returns tables and charts.
5. **Compare** with the "Possible result" panel on the site or the `results/` folder. Small differences are normal; large ones are a reason to ask the AI to show its code.

The workflow follows a standard sequence: ethics gate, understand, audit quality, clean and encode, describe, visualise, test hypotheses, model, verify, interpret critically, then report and disclose.

## Using the skill (Claude)

Enable code execution, then go to **Customize › Skills** and upload `prompts/survey-analysis-workflow.zip`. In ChatGPT, the nearest equivalent is to paste `SKILL.md` into a custom GPT's instructions.

## Reproduce the reference results

```bash
pip install -r analysis/requirements.txt
python analysis/analysis.py      # writes results/figures, results/tables, results/reference_results.json
```

Run from the repository root; the scripts read the Excel files from `data/`.

## Publish with GitHub Pages

In **Settings › Pages**, choose *Deploy from a branch*, branch `main`, folder `/ (root)`. The `.nojekyll` file is already included.

## Ethics

All research at EWU that has significant ethical implications must be submitted to the **EWU Research Ethical Committee (EWUREC)** for independent review ([EWUREC](https://www.ewubd.edu/members-east-west-university-research-ethical-committee)). The demo dataset is anonymised, consented, CC BY 4.0 secondary data. For your own data, follow EWU's *Policy and Procedure for Research Ethics Approval and Plagiarism Policy*: get approval, anonymise, never upload identifiable data to AI tools, verify every number, and disclose AI use.

## Credits and licences

- Materials prepared by Dr. Mohammad Rifat Ahmmad Rashid, Associate Professor, Department of CSE, East West University. Code and training materials are under the MIT licence (see `LICENSE`).
- Dataset: Islam et al. (2026), *Data in Brief* 67, 112924, https://doi.org/10.1016/j.dib.2026.112924, under the **CC BY 4.0** licence. See `data/README.md`.
