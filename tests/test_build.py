"""Verify the release downloads and the reusable library."""
import importlib.util
import json
from pathlib import Path
import re
import unittest
import zipfile
import tempfile

from test_profile import profile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("companion_build", ROOT / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


class BuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompts_doc = (ROOT / "docs/prompts.md").read_text()
        cls.dist = build.build()
        cls.kit = zipfile.ZipFile(cls.dist / "writing-companion-kit.zip")
        cls.addClassCleanup(cls.kit.close)

    def read_kit(self, name):
        return self.kit.read("Writing Companion/" + name).decode()

    def test_install_archives_contain_only_allowlisted_reusable_files(self):
        with zipfile.ZipFile(self.dist / "writing-companion-skill.zip") as z:
            self.assertEqual(set(z.namelist()), {"writing-companion/" + n for n in build.SKILL_FILES})
            for name in z.namelist():
                self.assertNotRegex(z.read(name).decode(), r"/Users/")
        with zipfile.ZipFile(self.dist / "writing-companion-plugin.zip") as z:
            self.assertEqual(len(z.namelist()), len(build.SKILL_FILES) + 1)
            manifest = json.loads(z.read("writing-companion/.codex-plugin/plugin.json"))
            self.assertEqual(manifest["skills"], "./skills/")

    def test_prompts_are_complete_identical_single_paragraphs(self):
        prompts = json.loads((build.SKILL / "assets/prompts.json").read_text())
        self.assertEqual(len(prompts), 10)
        for item in prompts:
            self.assertTrue(all(item.get(key) for key in ("id", "title", "when", "output", "prompt")))
            actual = self.read_kit(f"Prompts/{item['id']}.txt")
            self.assertEqual(actual, item["prompt"])
            self.assertNotRegex(actual, r"[\r\n]")

    def test_committed_prompt_doc_is_current(self):
        self.assertEqual(self.prompts_doc, (ROOT / "docs/prompts.md").read_text(),
                         "docs/prompts.md was stale; run build.py and commit it.")

    def test_project_guide_embeds_all_assets_without_broken_local_links(self):
        guide = self.read_kit("Project edition/writing-companion-guide.md")
        for asset in build.ASSETS:
            self.assertIn((build.SKILL / asset).read_text().strip(), guide)
        for prompt in json.loads((build.SKILL / "assets/prompts.json").read_text()):
            self.assertIn(prompt["prompt"], guide)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", guide):
            self.assertTrue(target.startswith(("https://", "http://", "#")), target)

    def test_plugin_versions_agree(self):
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        versions = {claude["version"], market["metadata"]["version"], market["plugins"][0]["version"], codex["version"]}
        self.assertEqual(len(versions), 1, versions)

    def test_skill_reference_links_resolve(self):
        for name in build.SKILL_FILES:
            if not name.endswith(".md"):
                continue
            source = build.SKILL / name
            for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text()):
                if not link.startswith(("https://", "http://", "#")):
                    self.assertTrue((source.parent / link).is_file(), f"{name}: {link}")

    def test_all_six_template_pairs_export_as_drafts_without_adoption(self):
        data = {"format": "writing-companion-profile", "version": 1, "profileId": "starter-test", "baseRevision": 0,
                "scopes": [{"id": "global", "kind": "global", "name": "My writing", "parent": None}],
                "entries": [], "session": {}, "changes": ["Starter formats under review"]}
        for kind in build.FORMATS:
            data["scopes"].append({"id": kind, "kind": "content-type", "name": kind, "parent": "global"})
            for filename, role in (("template", "template"), ("ai-instructions", "format-instructions")):
                content = self.read_kit(f"Templates/{kind}/{filename}.md")
                data["entries"].append({"id": f"{kind}-{filename}", "scope": kind, "role": role,
                                        "status": "draft", "text": content, "evidence": []})
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "drafts.zip"
            profile.export_profile(data, archive)
            restored, _ = profile.read_archive(archive)
            self.assertEqual(restored["entries"], data["entries"])
            with zipfile.ZipFile(archive) as z:
                active = z.read("writing-profile.md").decode().split("## Session checkpoint")[0]
                self.assertNotIn("Spoken script instructions", active)
                self.assertEqual(sum(n.startswith("drafts/content-types/") for n in z.namelist()), 12)


if __name__ == "__main__":
    unittest.main()
