#!/usr/bin/env python3
"""Run the acceptance scenarios against a live model and grade each reply with Claude.

  project  Runs the Project edition (instructions + guide, no file tools) on any OpenRouter model.
  skill    Uploads skills/writing-companion through the Anthropic Skills API, like an installed skill.

Claude Opus 5.5 grades every reply: directly with ANTHROPIC_API_KEY, otherwise through OPENROUTER_API_KEY.
"""
import argparse
from datetime import datetime
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.request
import zipfile

import anthropic
from anthropic.lib import files_from_dir

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
SKILL = ROOT / "skills/writing-companion"
JUDGE_MODEL = "claude-opus-5-5"
JUDGE_OPENROUTER = "anthropic/claude-opus-5.5"  # the same model, by its OpenRouter name
CODE_EXECUTION = {"type": "code_execution_20250825", "name": "code_execution"}
VERDICT = {
    "type": "object",
    "properties": {"results": {"type": "array", "items": {
        "type": "object",
        "properties": {"criterion": {"type": "string"}, "pass": {"type": "boolean"}, "evidence": {"type": "string"}},
        "required": ["criterion", "pass", "evidence"], "additionalProperties": False}}},
    "required": ["results"], "additionalProperties": False,
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load("build", ROOT / "build.py")
profile = load("profile", SKILL / "scripts/profile.py")


def profile_markdown():
    """The fictional profile as a user would paste it: the exporter's writing-profile.md."""
    with tempfile.TemporaryDirectory() as temp:
        archive = Path(temp) / "profile.zip"
        profile.export_profile(json.loads((EVALS / "fixtures/profile.json").read_text()), archive)
        with zipfile.ZipFile(archive) as z:
            return z.read("writing-profile.md").decode()


def turn_text(turn, prompts, profile_md):
    if isinstance(turn, dict):
        return prompts[turn["prompt"]]
    return turn.replace("{profile}", profile_md)


class ClaudeSkill:
    def __init__(self, client, model):
        self.client, self.model = client, model
        self.skill = client.skills.create(files=files_from_dir(str(SKILL)),
                                          display_name=f"writing-companion-eval-{datetime.now():%Y%m%d%H%M%S}")
        self.usage = [0, 0]

    def converse(self, turns, use_skill):
        messages, replies, container_id = [], [], None
        for text in turns:
            messages.append({"role": "user", "content": text})
            reply = []
            while True:
                kwargs = {}
                if use_skill:
                    container = {"skills": [{"type": "custom", "skill_id": self.skill.id, "version": "latest"}]}
                    if container_id:
                        container["id"] = container_id
                    kwargs = {"container": container, "tools": [CODE_EXECUTION]}
                with self.client.messages.stream(model=self.model, max_tokens=32000,
                                                 messages=messages, **kwargs) as stream:
                    response = stream.get_final_message()
                self.usage[0] += response.usage.input_tokens
                self.usage[1] += response.usage.output_tokens
                if response.container:
                    container_id = response.container.id
                messages.append({"role": "assistant", "content": response.content})
                reply += [b.text for b in response.content if b.type == "text"]
                if response.stop_reason == "refusal":
                    reply.append("[refused]")
                    break
                if response.stop_reason != "pause_turn":
                    break
                messages.append({"role": "user", "content": "Continue."})
            replies.append("\n".join(reply))
        return replies

    def close(self):
        for version in self.client.skills.versions.list(skill_id=self.skill.id):
            self.client.skills.versions.delete(version.version, skill_id=self.skill.id)
        self.client.skills.delete(self.skill.id)


def openrouter(model, messages, **extra):
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({"model": model, "messages": messages, **extra}).encode(),
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        data = json.load(response)
    if "error" in data:
        raise OSError(data["error"])
    return data


class OpenRouterProject:
    def __init__(self, model):
        self.model, self.usage = model, [0, 0]
        payload, prompts = build.load()
        self.system = ((ROOT / "docs/project-instructions.txt").read_text()
                       + "\n\nProject file writing-companion-guide.md:\n\n" + build.project_guide(payload, prompts))

    def converse(self, turns, use_skill):
        messages = [{"role": "system", "content": self.system}] if use_skill else []
        replies = []
        for text in turns:
            messages.append({"role": "user", "content": text})
            data = openrouter(self.model, messages)
            reply = data["choices"][0]["message"]["content"] or ""
            self.usage[0] += data.get("usage", {}).get("prompt_tokens", 0)
            self.usage[1] += data.get("usage", {}).get("completion_tokens", 0)
            messages.append({"role": "assistant", "content": reply})
            replies.append(reply)
        return replies

    def close(self):
        pass


def transcript(turns, replies):
    return "\n\n".join(f"### User\n\n{t}\n\n### Assistant\n\n{r}" for t, r in zip(turns, replies))


JUDGE_SYSTEM = ("You grade an AI writing assistant's conversation against acceptance criteria. Judge only what the "
                "transcript shows. Pass a criterion only when the assistant clearly meets it; quote brief evidence.")


def grade(client, scenario, conversation):
    criteria = "\n".join(f"{i}. {c}" for i, c in enumerate(scenario["criteria"], 1))
    prompt = (f"Scenario: {scenario['title']}\n\nCriteria:\n{criteria}\n\n"
              f"<transcript>\n{conversation}\n</transcript>")
    if client:
        response = client.messages.create(
            model=JUDGE_MODEL, max_tokens=16000, system=JUDGE_SYSTEM,
            output_config={"format": {"type": "json_schema", "schema": VERDICT}},
            messages=[{"role": "user", "content": prompt}])
        text = next(b.text for b in response.content if b.type == "text")
    else:
        data = openrouter(JUDGE_OPENROUTER, [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": prompt}],
                          response_format={"type": "json_schema",
                                           "json_schema": {"name": "verdict", "strict": True, "schema": VERDICT}})
        text = data["choices"][0]["message"]["content"]
    return json.loads(text)["results"]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--backend", choices=["project", "skill"], default="project")
    parser.add_argument("--model", default="anthropic/claude-opus-5.5",
                        help="OpenRouter model for project runs, or an Anthropic model ID for skill runs")
    parser.add_argument("--only", nargs="+", metavar="ID", help="Run only these scenario IDs")
    args = parser.parse_args()
    model = args.model
    if args.backend == "skill" and model == parser.get_default("model"):
        model = JUDGE_MODEL

    scenarios = json.loads((EVALS / "scenarios.json").read_text())
    if args.only:
        unknown = set(args.only) - {s["id"] for s in scenarios}
        if unknown:
            parser.error(f"unknown scenario IDs: {', '.join(sorted(unknown))}")
        scenarios = [s for s in scenarios if s["id"] in args.only]
    prompts = {p["id"]: p["prompt"] for p in json.loads((SKILL / "assets/prompts.json").read_text())}
    profile_md = profile_markdown()
    client = anthropic.Anthropic() if os.environ.get("ANTHROPIC_API_KEY") else None
    if args.backend == "skill" and not client:
        parser.error("skill runs need ANTHROPIC_API_KEY")
    runner = ClaudeSkill(client, model) if args.backend == "skill" else OpenRouterProject(model)
    out = EVALS / "results" / f"{datetime.now():%Y%m%d-%H%M%S}-{args.backend}-{model.replace('/', '_')}"
    out.mkdir(parents=True)

    rows, passed, total = [], 0, 0
    try:
        for scenario in scenarios:
            turns = [turn_text(t, prompts, profile_md) for t in scenario["turns"]]
            print(f"{scenario['id']} ...", end=" ", flush=True)
            try:
                replies = runner.converse(turns, scenario.get("skill", True))
                conversation = transcript(turns, replies)
                results = grade(client, scenario, conversation)
            except (anthropic.APIError, OSError, KeyError) as error:
                print(f"error: {error}")
                rows.append(f"| {scenario['id']} | error | {str(error)[:120]} |")
                continue
            ok = sum(r["pass"] for r in results)
            passed, total = passed + ok, total + len(results)
            print(f"{ok}/{len(results)}")
            failures = "; ".join(f"✗ {r['criterion']}: {r['evidence']}" for r in results if not r["pass"])
            rows.append(f"| {scenario['id']} | {ok}/{len(results)} | {failures.replace('|', '/') or '✓'} |")
            verdicts = "\n".join(f"- {'✓' if r['pass'] else '✗'} {r['criterion']}: {r['evidence']}" for r in results)
            (out / f"{scenario['id']}.md").write_text(
                f"# {scenario['title']}\n\n{verdicts}\n\n## Transcript\n\n{conversation}\n")
    finally:
        runner.close()

    report = (f"# Eval report\n\nBackend: {args.backend} · Model: {model} · Judge: {JUDGE_MODEL}\n\n"
              f"**{passed}/{total} criteria passed.** Tested-model tokens: {runner.usage[0]:,} in, {runner.usage[1]:,} out.\n\n"
              "| Scenario | Score | Failed criteria |\n|---|---|---|\n" + "\n".join(rows) + "\n")
    (out / "report.md").write_text(report)
    print(f"\n{passed}/{total} criteria passed. Report: {out / 'report.md'}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
