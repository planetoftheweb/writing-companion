# Verification

## Behavior evals

October 8, 2026, Project edition through OpenRouter, graded by Claude Opus 5.5 (`evals/run.py`, 16 scenarios, 42 criteria):

| Model | First run | After fixes |
|---|---|---|
| Claude Opus 5.5 | 40/42 | 42/42 |
| GPT-6.1 Sol | 39/42 | 42/42 |

The first run found two problems. Both models packed several questions into each of their three numbered items, and GPT asked for details instead of drafting from a thin brief. `SKILL.md` and the Project instructions now count every question mark, and they ask for a draft with marked placeholders whenever one is requested.

Not yet covered: the installed skill through the Anthropic Skills API (`--backend skill`, needs `ANTHROPIC_API_KEY`), ChatGPT's own skill upload, and restoring from a profile ZIP rather than pasted `writing-profile.md`. Each scenario was run once, so treat a single pass as encouraging, not conclusive.

## Local checks

`python3 -m unittest discover -s tests` runs 17 profile-exporter checks and 7 build checks. The profile checks cover export and restart, Unicode, partial setup, approved versus draft guidance, rejected proposals, scope separation, format pairs, revision history, restoring single entries, and archive safety. The build checks cover archive allowlists, the ten prompts, the Project guide's embedded assets and links, the six starter formats, and matching plugin versions.

## Platform installs

Uploading the skill in claude.ai and in ChatGPT has not been tested by hand. Platform labels and availability can change; see the links in the README.
