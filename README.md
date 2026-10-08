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

**Claude:** Customize → Skills → Create skill → Upload a skill. Upload `writing-companion-skill.zip` and enable it, with code execution and file creation turned on if required. Then ask Writing Companion to help set up your voice and work on a real piece.

**ChatGPT:** If your account has Plugins → Skills, choose Create → Upload from your computer and upload `writing-companion-skill.zip`. Skills are currently documented for eligible Business, Enterprise, Healthcare, and Edu accounts. Otherwise, use the Project edition.

**Project edition (Claude or ChatGPT):** Create a private Project, paste `Project edition/project-instructions.txt` from the kit into its instructions, and upload `writing-companion-guide.md`. Also upload `profile.py` where code execution is available, for validated ZIP exports.

**Just prompts:** Paste the [prompt series](docs/prompts.md) into any chat, one at a time. Start with "Start with my writing."

## Keep your progress

The companion exports a profile ZIP and a readable `writing-profile.md`. Add the Markdown file to your Project's sources, replacing the old copy, and keep the ZIP privately for history. In a new chat, ask the companion to resume from your profile.

Your profile is separate from the skill. Share the skill freely; share your profile only when you mean to share its contents.

## Working on the skill

Everything is generated from [`writing-companion/`](writing-companion/), the skill itself. Edit there, then:

```bash
python3 -m unittest discover -s tests
```

```bash
python3 build.py
```

The build writes the three downloads to `dist/` and refreshes `docs/prompts.md`. Commit that file when it changes. To publish a release, bump the version in `packaging/plugin.json`, then tag and push. GitHub Actions runs the tests and attaches the downloads:

```bash
git tag v0.1.0 && git push origin v0.1.0
```

| Path | What it is |
|---|---|
| `writing-companion/` | The skill: `SKILL.md`, references, starter templates, prompts, and the `profile.py` exporter |
| `packaging/` | The plugin manifest and Project edition instructions |
| `docs/` | Quickstart, prompt series, acceptance scenarios, and verification notes |
| `tests/` | Profile exporter and build checks (standard library only) |

Platform setup was last checked September 18, 2026: [Claude skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude) · [ChatGPT skills](https://help.openai.com/en/articles/20001066) · [ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt) · [OpenAI plugins](https://help.openai.com/en/articles/20001256)

MIT licensed.
