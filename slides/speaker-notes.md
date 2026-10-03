# AI for Research: Prompt-Based Analysis — Speaker Notes

## 1. AI for Research

Welcome. Today is deliberately simple: no installation, no code to write. We use the chat tools most of us already have, Claude or ChatGPT, with a set of standard prompts on a real, openly licensed dataset. The emphasis throughout is on doing it ethically and verifiably. Everything is in the GitHub repository and the Prompt Lab website, so participants can repeat the session on their own.

## 2. Five parts, one real dataset, no code to write

Part 3 is where participants spend most of the session: they download the dataset, open Claude or ChatGPT and run the prompts themselves while comparing with the possible results on the website.

## 3. Claude and ChatGPT now run code on your data

Both tools can execute Python on uploaded files: ChatGPT through its data analysis feature, Claude through code execution and file creation. That means statistics and charts are computed, not guessed, provided you ask for the code and check it. This is the main reason a prompt-based approach is now credible for research analysis.

## 4. Six risks every AI-assisted study must manage

Each of these comes back in the demo. Privacy: we use a public, anonymised dataset precisely so nothing sensitive leaves the room. Fabrication: we ask the AI to show and recompute its numbers. Bias: the sample is five universities, mostly technical students. Reproducibility: we keep the prompts in a file and the code. Authorship: we finish with a disclosure statement.

## 5. What EWU's ethics framework asks of us

The quote is from EWU's public EWUREC page. The right-hand column is good practice consistent with that requirement, not a quotation of the policy document; refer participants to the official Policy and Procedure for Research Ethics Approval for the binding rules and forms. Today's dataset is public, anonymised and CC BY licensed, so no new approval is needed to practise on it. Any new survey or interview study participants run at EWU with significant ethical implications goes to EWUREC first.

## 6. An ethical routine: before, during and after

The same eight-item checklist is interactive on the Prompt Lab website; participants tick it before uploading the dataset. A prompt log is simply the list of prompts you used, saved with the date and tool; prompts.md in the repository is an example.

## 7. Eleven steps, one standard prompt each

This is the standard sequence from data management practice: understand, audit, clean, describe, visualise, infer, model, interpret, report. Step 0 adds the ethics gate and step 10 turns the session into reusable files. The human checkpoints are where AI must not decide alone: whether the data may be used, how data are changed, and what the results mean.

## 8. Role, context, task, format, check

Every prompt on the Prompt Lab website has a Show anatomy button that colours these five parts. Point out that most weak prompts are missing format and check: without a fixed format you cannot compare answers, and without a check you get confident prose instead of verifiable output.

## 9. Ten patterns, and when to use each

Good prompts combine patterns: P6 is role plus context-rich plus structured output plus tool use. On the website, clicking a pattern lists the workflow prompts that use it.

## 10. Career anxiety in the age of AI: 3,156 students

The dataset is openly licensed, anonymised with random six-character IDs, and every respondent consented. It is ideal for training because it is real, relevant to our students, and has genuine data-quality issues to find. Participants download it from the Prompt Lab website or the GitHub repository; the original is on Mendeley Data and Zenodo.

## 11. Ask an ethics reviewer before the first analysis

This is real output from the file. The interesting finding for faculty is the small-cell risk: age 26 or 27 combined with gender, academic year and a rare career path could point to one person, even without names. That is why we never publish small cells. The verbal approval is a good discussion point: when we collect our own data, EWU expects documented ethics review.

## 12. A published dataset still has problems to find

All of these come from running prompt P2 on the two files. No duplicates and no out-of-range ages were found. The stray "h" is a nice moment: a published, peer-reviewed data article still contains a coding error, and an AI that is told to check every encoded value against the codebook finds it in seconds. Ask: would you have found it by eye in 3,156 rows?

## 13. Plan first, approve, then let the AI execute

Plan-then-execute is the single most useful habit: without it, AI tools sometimes drop rows with missing values or impute silently. Few-shot prompting is the right tool for free-text answers: five examples teach the AI your categories. Check the mapping, especially answers that name two careers.

## 14. One prompt, and the AI runs the code for the charts

These charts came from prompt P5, which asks for 300-dpi PNGs, a colour-blind-safe palette, labelled axes, bars from zero and n in titles. Claude and ChatGPT both return the image files and the code. Students also report using 2.99 AI tools on average; ChatGPT 98%, Gemini 80%, DeepSeek 46%, Copilot 37%.

## 15. Significant is not the same as large

This is the slide to slow down on. A typical AI summary would report four tests and say two are significant. The prompt forced effect sizes, so we see that the strongest association has a Cramér's V of .09, which is small. The knowledge result shows why you should ask the AI to explain a pattern: the relationship is U-shaped, which a chi-square detects and a correlation does not. All expected cell counts were at least 28, so the chi-square assumptions hold.

## 16. Belief that AI replaces jobs is the clearest predictor

The prompt asks for an ordinal logistic regression, which respects the four ordered anxiety levels. 45 rows were dropped for missing AI knowledge; the prompt makes the AI report that. The honest headline is two-sided: the belief that AI will replace jobs is the clearest predictor, but the model explains about one percent of the variation. Asking for a pseudo-R² is what keeps the interpretation honest.

## 17. Make the AI check itself, then argue against you

Overclaiming is an ethical issue, not just a statistical one. The sceptical-reviewer prompt lists the limitations a real reviewer would raise; several come straight from the data article itself, such as the seminar before the survey, which may have primed students' answers.

## 18. Cite the data, say what the AI did, own the result

The prompt tells the AI not to invent software versions and to leave brackets where it does not know; participants fill those in themselves. Check the target journal's AI policy too; most allow AI assistance with disclosure and none accept an AI as an author.

## 19. Download, prompt, compare, verify

Participants work in pairs: one drives the AI, the other compares with the possible results on the website and keeps the prompt log. Wording will differ between tools and runs; numbers should not. Where they do differ, that is the verification discussion.

## 20. From a prompt to an agent, in seven levels

Today's session lives at level 2. Level 3: Claude Projects and ChatGPT Projects keep instructions and files for every chat in a study. Level 4: a context file in Markdown holds the facts and rules; in Claude Code it is CLAUDE.md, and many coding agents read AGENTS.md. Level 5: a skill is a packaged procedure loaded only when relevant; in ChatGPT the nearest equivalent is a custom GPT. Level 6: connectors, many built on the open Model Context Protocol, let the AI work with Drive, GitHub and other tools. Level 7: agents such as Claude Code, ChatGPT agent or Codex plan and carry out multi-step tasks.

## 21. Which layer for which job

Features change quickly; this table reflects the products as of this training. The concepts are stable even when names change: persistent context, packaged procedures, access to tools, and autonomy.

## 22. Two plain-text files from today's conversation

Both complete files are in the repository and downloadable from the Prompt Lab. A skill's description must say what it does and when to use it, in at most 200 characters, because that is how Claude decides when to load it.

## 23. An agent runs the whole workflow; you keep the gates

An agent is the same model with tools and a loop: it plans, acts, observes and continues. The research risk is that mistakes compound without a human noticing, so the checkpoints are not optional. Claude Code reads CLAUDE.md and skills in a project folder; ChatGPT agent works in a browser; Codex works in code repositories.

## 24. Seven layers, with you at the top

Build from the bottom up. The foundation is ordinary good research practice: protected raw data, a data management plan and version control. Projects and context files come next because they pay off immediately. Skills come when you notice you repeat a procedure. Agents only make sense once the layers below are in place, and the human layer sits above all of them.

## 25. Build it over four weeks, one layer at a time

The ewu-ai-training repository is itself an example of week 1 and week 2: data with its licence, prompts in a file, a context file and a skill, all versioned. Encourage participants to fork it as the template for their own study.

## 26. AI drafts. You decide.

The one rule of the session. Whatever level of the ladder you work at, these three habits keep AI-assisted research honest.

## 27. Standard prompts, real data, ethical by default

Ask each participant to name one study where they will set up a Project and a context file this month. Point them to the repository for the prompts, dataset, website and the example files.
