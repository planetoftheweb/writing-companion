# Writing Companion

Help your AI understand your voice, your work, and what good writing looks like to you.

Install it in Claude or a supported ChatGPT account. Bring a piece you want to write, plus a couple of samples if you have them. The companion asks a few questions, tries a short draft, and builds your profile from what you confirm.

## Start without installing anything

Open `Quickstart.md`, or its Word or PDF copy. The `Prompts` folder contains ten numbered prompts you can use in an ordinary Claude or ChatGPT conversation. Start with `01-start-with-my-writing.txt`, or jump to the task you need.

The `Templates` folder contains a template and custom instructions for script, article, blog post, newsletter, LinkedIn post, and X post. Upload only the pair you want to adapt. The `Guidance starters` folder has optional voice choices and workspace or series guidance. Everything is a starting suggestion until you approve your own version.

## Claude

1. Open Customize → Skills → Create skill → Upload a skill.
2. Upload `Install/writing-companion-skill.zip` and enable it. Enable code execution and file creation if required.
3. Start a chat and ask Writing Companion to help set up your voice and work on a real piece.

You can skip samples and start with a short interview. You can also start writing immediately.

## ChatGPT

If your account has Plugins → Skills, choose Create → Upload from your computer and upload `Install/writing-companion-skill.zip`. Start a chat and ask it to use Writing Companion.

Skills are currently documented for eligible Business, Enterprise, Healthcare, and Edu accounts, subject to workspace controls. If your account lacks that option, use the Project edition below. The optional `writing-companion-plugin.zip` is a skills-only OpenAI plugin package for surfaces supporting plugin import; it is not a published directory listing and may not be accepted by every ChatGPT surface.

## Project edition

This also stays entirely inside ChatGPT or Claude:

1. Create a private Project called Writing Companion.
2. Put the contents of `Project edition/project-instructions.txt` in its project instructions.
3. Upload `Project edition/writing-companion-guide.md`. For validated ZIP exports, also upload `Project edition/profile.py` where code execution is available.
4. Start a chat about the next thing you want to publish.

The guide contains the same workflow as the skill. The companion can help even without code execution; it must tell you when it cannot create downloadable files.

## Keep your progress

The companion exports a profile ZIP and a readable `writing-profile.md`. Add the Markdown file to your Project's knowledge or sources, replacing the old active copy. Retain the ZIP privately for previous versions. In a new chat, ask the companion to resume from your profile.

Your private profile is separate from the installed skill. Share the install ZIP when sharing the companion. Share your profile only when you intend to share its contents.

## What you can ask it to do

- Set up or refine your voice.
- Write using your approved profile.
- Create a reusable content format.
- Learn from edits you choose to keep.
- Export your profile or resume an unfinished setup.

Learning happens through short review checkpoints. It proposes lasting improvements; you choose what to keep. It does not train the underlying model or promise background updates.

## Included

`Install` contains the skill and optional plugin. `Project edition` contains the in-platform alternative. `Source` contains the editable skill. `Prompts` and `Templates` work without installation. `Quickstart` is provided as Markdown, Word, and PDF. `Verification.md` records what has actually been tested.

Your profile stays readable and portable. Its index connects your voice, rules, projects, and content formats without requiring a connection to another app.

## Platform references

Setup checked September 18, 2026. Availability and labels can change.

- [Claude skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [ChatGPT skills](https://help.openai.com/en/articles/20001066)
- [ChatGPT Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt)
- [OpenAI plugins](https://help.openai.com/en/articles/20001256)
