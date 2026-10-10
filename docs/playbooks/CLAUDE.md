# Video playbooks: context for Claude Code

Two PDF playbooks live here, built from the HTML in [`source/`](source/). This file hands over everything learned while drafting them, so work can continue here without the original chat.

- [`ai-video-writing-playbook.pdf`](ai-video-writing-playbook.pdf): Writing for Video with AI, 3 pages
- [`ai-video-editing-playbook.pdf`](ai-video-editing-playbook.pdf): Editing Video with AI, 3 pages
- [`README.md`](README.md): the short public description linked from the repo README

## How to edit and rebuild

1. Edit the page HTML in [`source/writing.py`](source/writing.py) or [`source/editing.py`](source/editing.py). Shared styles are in [`source/common.py`](source/common.py).
2. Rebuild both PDFs from `source/`:

```bash
pip install playwright && playwright install chromium
```

```bash
cd docs/playbooks/source && python3 build.py
```

3. Check the printed overflow numbers. Anything over about 2 pixels on a page means text is cut off at the bottom. Fix it by trimming copy, not by shrinking fonts.
4. Look at every page before calling it done. Rasterize and view them, for example with `pdftoppm -png -r 80`.
5. Check for em dashes and en dashes in the PDF text. There must be none.

The build loads Inter from Google Fonts. Without a network connection it falls back to a locally installed Inter, or the system font, and line breaks can shift.

## Who it's for

Video newcomers and professionals alike. The videos might be 30 second feed clips, 10 minute explainers or full courses. Readers use Claude, ChatGPT or another assistant, and Descript or another editor. Every tip has to make sense to someone who has never edited a video.

## Hard rules from Ray's feedback

- **No em dashes or en dashes anywhere.** Ray treats them as a sign of AI writing.
- **Plain language.** No jargon a newcomer wouldn't know. Words like "pass," "pickup," "rough cut" and "B-roll" need a few plain words of explanation, or should be avoided. Ray called an earlier editing page "horrible" because it said things like "find what the passes leave."
- **No project or episode names** that readers don't know, such as specific model names from his episodes, Stanford videos or internal projects. Use plain labels like "a recent video."
- **Don't name Writaible.** Describe what his writing app does without naming it. This is open for Ray to change; see Open items.
- **Tool-agnostic.** Name the tools Ray uses (Descript, Snagit, Claude, ChatGPT, PixTaffy, Publer, Obsidian), but always say other tools have similar features. Publer is "a tool like Publer," never the only option.
- **Positive tone.** No complaints, grievances or "the honest catch" warnings.
- **Ray's voice.** Short sentences, conversational, direct, no hype, no marketing language. Avoid AI-sounding patterns like "not just X but Y."
- **Actionable over clever.** Ray rejected low-value tips and a chart whose takeaway was vague. Each item should tell the reader exactly what to do.

## What each playbook covers

### Writing for Video with AI

- **Page 1:**
  - Stats: 150 courses, 3M+ learners, 3x output, and about 200K learners on AI Trends.
  - "Build your writing files": soul file, rules file, POV statement (one per series) and format files, with links to the matching starters in [`skills/writing-companion/assets/`](../../skills/writing-companion/assets/).
  - "Keep them alive": the files are living documents, improved after every piece.
  - "Put them to work": paste into a chat, a Project with a custom instruction (marked best), or a skill.
  - A copyable custom instruction.
- **Page 2:**
  - Six short prompts adapted from the [prompt series](../prompts.md).
  - "Let AI do the heavy lifting": research, options, rewriting one part, visual ideas, learning from edits, and formatting for recording.
  - "Check every draft against your files": a table of voice, rules, promise, evidence, specific, read aloud, AI demos and performance, plus a copyable check prompt.
- **Page 3:**
  - Ten tips for writing for the ear and the screen.
  - A script example: spoken lines, on-screen visuals and recording notes.
  - "Your script is a draft": write, record, edit, publish.
  - A real before and after of Ray's Gemini Flash closing line.
  - "Organize and improve": skills, Projects, Obsidian, a performance rubric built from Publer or another aggregator, time to relevance, and the human parts.

### Editing Video with AI

- **Page 1:**
  - Stats.
  - "Polish it three times": write, record, edit, publish, like a movie.
  - "Record like you're editing", with 6 tips.
  - "Let AI do the first cleanup": Ray's Descript menu graphic, with the four tools numbered in the order he uses them.
- **Page 2:**
  - "Make it shorter": the editor's real job. AI already clears pauses and retakes.
  - "Ask the AI editor for a to-do list": a report prompt, then an approve-the-cuts prompt, plus jobs to keep for yourself.
  - "Make it look finished".
  - A checklist before you export.
- **Page 3:**
  - A gallery of visuals you can make in minutes, with links to each tool.
  - A copyable motion graphic prompt.
  - "One recording, many videos": vertical, short clips, a companion post, and saving the final transcript.
  - The 9-step workflow strip.

## Ray's ideas that shaped the content

- **Record like you're editing, and write with visuals in mind.** Attention spans are short, so plan what is on screen for each part.
- **The script is a draft until you publish.** Writing is for how people read. Recording reveals what doesn't sound like you. Editing reveals where shorter is better. Improvise and rewrite until it ships.
- **In the edit, AI catches the repeats and pauses.** The person's job is making it shorter and more efficient.
- **The order he runs Descript's AI tools:** Shorten word gaps (over 1 second), Remove retakes, Edit for clarity at medium, then Add chapters. Studio Sound and Remove filler words are worth a click too.
- **Every series has a POV statement:** the promise to the viewer, which writing gets checked against. The AI Trends promise has five parts: respect their time, filter ruthlessly, real demos, no algorithm chasing, and a positive outlook.
- **A companion post** reflects what's in the video, teases it, and gives one useful takeaway that stands on its own.
- **A performance rubric:** use analytics from Publer or another social aggregator to build a rubric that new writing is checked against.
- **Organize the work:** turn your files into skills, use one Project per series, and drive an editor like Obsidian with Claude or ChatGPT.

## Facts and where they came from

| Claim | Source |
|---|---|
| 150 courses, 3M+ learners | Ray |
| 3x output, 2 to 3 short videos a week, rough cut in minutes instead of a full day | Ray's own description of his workflow |
| About 200K learners and close to 10K bookmarks on AI Trends | Ray |
| 41 minutes recorded to about 7 published | Descript project durations for one of Ray's recent model review videos (raw sequences compared with the final composition) |
| Recordings run five to six times longer than the final video | Two Descript projects, at ratios of about 5.7 and 6.4 |
| Before and after closing line | Ray's Gemini Flash script compared with its recorded transcript |
| About 150 words a minute | General speaking rate. Ray's own measured pace is about 160. |

## Visuals in `source/img/`

| File | What it is |
|---|---|
| `descript-passes.png` | Ray's screenshot of Descript's menu, with the four tools he uses numbered |
| `heart-frame.jpg` | One frame of a 20 second motion graphic Claude built. The page links to the live version at https://claude.ai/artifact/4XT7m3ePiNgqQXNgLnfKba |
| `bars.jpg` | A 3D bar chart exported from Ray's writing app, used as a chart overlay example |
| `infographic.jpg` | An infographic Ray supplied, used as the image-tool example |
| `mock-stock.jpg` | A drawn mockup of a stock video thumbnail with a play button. The page footer says it's a mockup. |
| `mock-snagit.jpg` | A drawn mockup of a screenshot with a numbered marker, highlight box and arrow. Also labeled a mockup. |

## Open items

- **Page count.** Each playbook is 3 pages. Ray first asked for up to 2 pages each, then content grew. He hasn't confirmed 3.
- **Naming Writaible.** It's unnamed. Ray may want to name and link it.
- **Real Publer numbers.** Publer needs a sign-in, so no real post performance numbers are in the playbooks yet.
- **A PixTaffy image of "Record like you're editing".** Two generation attempts timed out on Ray's Mac and may have landed in his PixTaffy gallery. One could replace or join the gallery images.
