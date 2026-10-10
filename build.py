#!/usr/bin/env python3
"""Build the release downloads from skills/writing-companion/ into dist/ and refresh docs/prompts.md."""
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "skills/writing-companion"
DIST = ROOT / "dist"
# Order sets the reading order of the Project edition guide.
REFERENCES = ["setup.md", "writing.md", "learning.md", "series-example.md", "portability.md", "platforms.md",
              "template-library.md", "prompt-series.md", "visual-narration.md", "connected-writing.md"]
FORMATS = ["script", "article", "blog-post", "newsletter", "linkedin-post", "x-post"]
GUIDANCE = ["writing-foundation", "voice-options", "workspace", "series"]
ASSETS = [f"assets/content-types/{kind}/{name}.md" for kind in FORMATS for name in ("template", "ai-instructions")]
ASSETS += [f"assets/guidance/{name}.md" for name in GUIDANCE]
SKILL_FILES = (["SKILL.md", "agents/openai.yaml", "scripts/profile.py", "assets/prompts.json"]
               + ["references/" + name for name in REFERENCES] + ASSETS)


def prompt_guide(prompts):
    sections = ["# Prompt series", "Use one prompt at a time in Claude or ChatGPT. Start at the beginning or choose the task you need. "
                "Workspace and series setup are optional. Provide your latest approved profile when continuing in a new chat."]
    for prompt in prompts:
        sections.append(f"## {prompt['title']}\n\n{prompt['when']}\n\nExpected result: {prompt['output']}\n\n{prompt['prompt']}")
    return "\n\n".join(sections) + "\n"


def project_guide(payload, prompts):
    sections = [payload["SKILL.md"].decode().split("---", 2)[2].strip()]
    sections += [payload["references/" + name].decode().strip() for name in REFERENCES]
    sections += [f"# Library asset {name}\n\n" + payload[name].decode().strip() for name in ASSETS]
    sections.append(prompt_guide(prompts))
    guide = "\n\n---\n\n".join(sections)
    # All local guide references are embedded below; keep only external links as links.
    def local_link(match):
        label, target = match.groups()
        if target.startswith(("https://", "http://", "#")):
            return match.group(0)
        target = target.removeprefix("../").removeprefix("references/")
        if target.startswith("assets/") and target != "assets/prompts.json":
            return f"{label} (Library asset {target}, included in this guide)"
        return f"{label} (included in this guide)"
    guide = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", local_link, guide)
    return guide.replace("scripts/profile.py", "profile.py").replace("from the installed skill directory", "using the attached profile.py") + "\n"


def zip_files(path, entries):
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data if isinstance(data, bytes) else data.encode())


def load():
    on_disk = {str(p.relative_to(SKILL)) for p in SKILL.rglob("*")
               if p.is_file() and p.name != ".DS_Store" and "__pycache__" not in p.parts}
    if on_disk != set(SKILL_FILES):
        raise ValueError(f"Update the file lists in build.py. Unlisted: {sorted(on_disk - set(SKILL_FILES))}, "
                         f"missing: {sorted(set(SKILL_FILES) - on_disk)}")
    payload = {name: (SKILL / name).read_bytes() for name in SKILL_FILES}
    prompts = json.loads(payload["assets/prompts.json"])
    if len({p["id"] for p in prompts}) != len(prompts):
        raise ValueError("Prompt IDs must be unique.")
    for prompt in prompts:
        if not re.fullmatch(r"\d{2}-[a-z-]+", prompt["id"]) or any(c in prompt["prompt"] for c in "\r\n"):
            raise ValueError("Prompts need safe IDs and a single copyable paragraph.")
    # The skill is reusable; a creator's private profile or local paths must never ship in it.
    for name, raw in payload.items():
        if re.search(r"\[TODO:|/Users/|BEGIN (?:RSA )?PRIVATE KEY", raw.decode("utf-8"), re.I):
            raise ValueError(f"Unexpected personal data or scaffold marker in {name}")
    return payload, prompts


def build():
    payload, prompts = load()
    (ROOT / "docs/prompts.md").write_text(prompt_guide(prompts), encoding="utf-8")
    shutil.rmtree(DIST, ignore_errors=True)
    DIST.mkdir()
    zip_files(DIST / "writing-companion-skill.zip", {"writing-companion/" + n: raw for n, raw in payload.items()})
    plugin = {"writing-companion/skills/writing-companion/" + n: raw for n, raw in payload.items()}
    plugin["writing-companion/.codex-plugin/plugin.json"] = (ROOT / ".codex-plugin/plugin.json").read_bytes()
    zip_files(DIST / "writing-companion-plugin.zip", plugin)
    kit = {
        "Quickstart.md": (ROOT / "docs/quickstart.md").read_bytes(),
        "Project edition/writing-companion-guide.md": project_guide(payload, prompts),
        "Project edition/project-instructions.txt": (ROOT / "docs/project-instructions.txt").read_bytes(),
        "Project edition/profile.py": payload["scripts/profile.py"],
        "Prompts/Prompt series.md": prompt_guide(prompts),
    }
    kit.update({f"Prompts/{p['id']}.txt": p["prompt"] for p in prompts})
    kit.update({f"Templates/{name.removeprefix('assets/content-types/')}": payload[name]
                for name in ASSETS if name.startswith("assets/content-types/")})
    kit.update({f"Guidance starters/{name}.md": payload[f"assets/guidance/{name}.md"] for name in GUIDANCE})
    zip_files(DIST / "writing-companion-kit.zip", {"Writing Companion/" + n: data for n, data in kit.items()})
    return DIST


if __name__ == "__main__":
    print(build())
