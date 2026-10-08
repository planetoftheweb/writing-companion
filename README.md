# Writing Companion

Help your AI understand your voice, your work, and what good writing looks like to you.

Bring a piece you want to write, plus a couple of samples if you have them. The companion asks a few questions, tries a short draft, and builds your profile from what you confirm. It learns through short review checkpoints: it proposes lasting improvements, and you choose what to keep. It does not train the underlying model.

## Get started

Download from the [latest release](https://github.com/planetoftheweb/writing-companion/releases/latest):

| Download | Use it for |
|---|---|
| `writing-companion-skill.zip` | Installing the skill in Claude or ChatGPT |
| `writing-companion-kit.zip` | No install: prompts, templates, the Project edition, and the [quickstart](docs/quickstart.md) |
| `writing-companion-plugin.zip` | Optional skills-only OpenAI plugin package, for surfaces that support plugin import |

**Claude Code:** Run these two commands inside Claude Code:

```
/plugin marketplace add planetoftheweb/writing-companion
/plugin install writing-companion@writing-companion
```

**Claude:** Customize → Skills → Create skill → Upload a skill. Upload `writing-companion-skill.zip` and enable it, with code execution and file creation turned on if required. Then ask Writing Companion to help set up your voice and work on a real piece.

**ChatGPT:** If your account has Plugins → Skills, choose Create → Upload from your computer and upload `writing-companion-skill.zip`. Skills are currently documented for eligible Business, Enterprise, Healthcare, and Edu accounts. Otherwise, use the Project edition.

**Project edition (Claude or ChatGPT):** Create a private Project, paste `Project edition/project-instructions.txt` from the kit into its instructions, and upload `writing-companion-guide.md`. Also upload `profile.py` where code execution is available, for validated ZIP exports.

**Just prompts:** Paste the [prompt series](docs/prompts.md) into any chat, one at a time. Start with "Start with my writing."

**Making video?** The [video playbooks](docs/playbooks/) cover writing and editing with AI, and link to the starter templates in this skill.

## Keep your progress

The companion exports a profile ZIP and a readable `writing-profile.md`. Add the Markdown file to your Project's sources, replacing the old copy, and keep the ZIP privately for history. In a new chat, ask the companion to resume from your profile.

Your profile is separate from the skill. Share the skill freely; share your profile only when you mean to share its contents.

## Working on the skill

Everything is generated from [`skills/writing-companion/`](skills/writing-companion/), the skill itself. Edit there, then:

```bash
python3 -m unittest discover -s tests
```

```bash
python3 build.py
```

The build writes the three downloads to `dist/` and refreshes `docs/prompts.md`. Commit that file when it changes. To publish a release, bump the version in `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and `.codex-plugin/plugin.json` (a test checks they agree), then:

```bash
gh release create v0.3.0 dist/*.zip --generate-notes
```

### Test how it behaves

The unit tests check files. The evals check behavior: [`evals/run.py`](evals/run.py) plays each conversation in [`evals/scenarios.json`](evals/scenarios.json) against a live model, then Claude Opus 5.5 grades every reply against the scenario's criteria. Transcripts and a report land in `evals/results/`. Every profile in the scenarios is fictional.

```bash
python3 -m venv .venv && .venv/bin/pip install -r evals/requirements.txt
```

```bash
.venv/bin/python evals/run.py --model anthropic/claude-opus-5.5
```

```bash
.venv/bin/python evals/run.py --model openai/gpt-6.1-sol
```

The default `project` backend runs the Project edition on any [OpenRouter](https://openrouter.ai/models) model and needs `OPENROUTER_API_KEY`. `--backend skill` uploads the skill through the Anthropic Skills API, which is closest to an installed skill in Claude, and needs `ANTHROPIC_API_KEY`. Use `--only <id>` to rerun single scenarios. Each full run costs a few dollars.

| Path | What it is |
|---|---|
| `skills/writing-companion/` | The skill: `SKILL.md`, references, starter templates, prompts, and the `profile.py` exporter |
| `.claude-plugin/`, `.codex-plugin/` | Plugin manifests for Claude Code and OpenAI |
| `docs/` | Quickstart, prompt series, Project edition instructions, verification notes, and the [video playbooks](docs/playbooks/) |
| `tests/` | Profile exporter and build checks (standard library only) |
| `evals/` | Behavior scenarios, the fictional test profile, and the eval runner |

Platform setup was last checked September 18, 2026: [Claude skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude) · [ChatGPT skills](https://help.openai.com/en/articles/20001066) · [ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) · [OpenAI plugins](https://help.openai.com/en/articles/20001256)

MIT licensed.
