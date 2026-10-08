"""Focused checks for the portable companion, using fictional profiles only."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/writing-companion/scripts/profile.py"
spec = importlib.util.spec_from_file_location("companion_profile", SCRIPT)
profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profile)


def fixture():
    return {"format": "writing-companion-profile", "version": 1, "profileId": "fictional-creator",
            "baseRevision": 0,
            "scopes": [{"id": "global", "kind": "global", "name": "My writing", "parent": None},
                       {"id": "series", "kind": "project", "name": "Test series", "parent": "global"},
                       {"id": "spoken", "kind": "content-type", "name": "Spoken script", "parent": "series"}],
            "entries": [
                {"id": "voice", "scope": "global", "role": "voice", "status": "approved",
                 "text": "# My voice\nUse clear explanations. Preserve café and 日本語.", "evidence": ["User confirmed"]},
                {"id": "series-context", "scope": "series", "role": "context", "name": "project.md",
                 "status": "approved", "text": "Show test dates in this series.", "evidence": ["User requested"]},
                {"id": "template", "scope": "spoken", "role": "template", "status": "approved",
                 "text": "# Opening\n[Practical question]\n# Demonstration\n[Task]", "evidence": ["Format approved"]},
                {"id": "format-rules", "scope": "spoken", "role": "format-instructions", "status": "approved",
                 "text": "Keep recording directions separate.", "evidence": ["Format approved"]}],
            "session": {"stage": "try", "nextStep": "Review the opening", "pendingProposals": [], "rejectedProposals": []},
            "changes": ["Initial approved profile"]}


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = fixture()

    def export(self, data=None, name="profile.zip", previous=None):
        path = self.root / name
        profile.export_profile(data or self.data, path, previous)
        return path

    def test_roundtrip_and_hashes(self):
        path = self.export()
        restored, history = profile.read_archive(path)
        self.assertEqual(restored["entries"], self.data["entries"])
        self.assertEqual(restored["session"], self.data["session"])
        self.assertEqual(history, [])
        with zipfile.ZipFile(path) as z:
            index = json.loads(z.read("index.json"))
            self.assertEqual(index["scopes"], self.data["scopes"])
            for entry in index["entries"]:
                self.assertEqual(entry["sha256"], hashlib.sha256(z.read(entry["path"])).hexdigest())
            self.assertIn("日本語", z.read("writing-profile.md").decode())

    def test_initial_interrupted_setup_without_samples(self):
        self.data["entries"] = []
        self.data["session"] = {"stage": "ask", "confirmedAnswers": {"audience": "Teachers"},
                                "memoryAvailable": False, "nextStep": "Choose one of the trial openings"}
        path = self.export()
        current, _ = profile.read_archive(path)
        self.assertEqual(current["session"], self.data["session"])
        with zipfile.ZipFile(path) as z:
            self.assertFalse(any(n.endswith(".json") and n.startswith("integrations/") for n in z.namelist()))

    def test_pending_and_rejected_learning_stay_out_of_active_guidance(self):
        self.data["entries"].append({"id": "pending-rule", "scope": "global", "role": "rules", "status": "draft",
                                      "text": "UNAPPROVED prefer extravagant claims", "evidence": []})
        self.data["session"]["rejectedProposals"] = ["REJECTED use more hashtags"]
        with zipfile.ZipFile(self.export()) as z:
            active = z.read("writing-profile.md").decode().split("## Session checkpoint")[0]
            self.assertNotIn("UNAPPROVED", active)
            self.assertNotIn("REJECTED", active)
            self.assertIn("drafts/global/rules.md", z.namelist())

    def test_revision_preserves_history_and_unrelated_guidance(self):
        first = self.export()
        old_bytes = first.read_bytes()
        updated = copy.deepcopy(self.data)
        updated["baseRevision"] = 1
        updated["entries"][0]["text"] += "\nUse shorter openings."
        updated["changes"] = ["User approved shorter openings"]
        second = self.export(updated, "v2.zip", first)
        current, history = profile.read_archive(second)
        self.assertEqual(current["revision"], 2)
        self.assertEqual(history[0]["entries"], self.data["entries"])
        self.assertEqual(current["entries"][1:], self.data["entries"][1:])
        self.assertEqual(first.read_bytes(), old_bytes)

    def test_entry_level_undo_preserves_newer_unrelated_changes(self):
        first = self.export()
        updated = copy.deepcopy(self.data)
        updated["baseRevision"] = 1
        updated["entries"][0]["text"] = "A changed voice."
        updated["entries"][1]["text"] += "\nUse dates in ISO format."
        updated["changes"] = ["Approved two preferences"]
        second = self.export(updated, "v2.zip", first)
        current, history = profile.read_archive(second)
        current["entries"][0] = history[0]["entries"][0]
        current["baseRevision"] = 2
        current["changes"] = ["User approved restoring earlier voice"]
        third = self.export(current, "v3.zip", second)
        restored, history = profile.read_archive(third)
        self.assertEqual(restored["entries"][0], self.data["entries"][0])
        self.assertEqual(restored["entries"][1], updated["entries"][1])
        self.assertEqual(len(history), 2)

    def test_scoped_exception_and_templates_stay_separate(self):
        with zipfile.ZipFile(self.export()) as z:
            self.assertEqual(z.read("global/soul.md").decode(), self.data["entries"][0]["text"])
            self.assertEqual(z.read("projects/series/project.md").decode(), "Show test dates in this series.")
            self.assertIn("content-types/spoken/template.md", z.namelist())
            self.assertFalse(any(n.startswith("integrations/") for n in z.namelist()))

    def test_stale_revision_rejected(self):
        first = self.export()
        with self.assertRaisesRegex(ValueError, "latest profile"):
            self.export(self.data, "v2.zip", first)

    def test_missing_previous_rejected(self):
        self.data["baseRevision"] = 2
        with self.assertRaisesRegex(ValueError, "previous ZIP"):
            self.export()

    def test_different_creator_rejected(self):
        first = self.export()
        self.data["profileId"] = "someone-else"
        self.data["baseRevision"] = 1
        with self.assertRaisesRegex(ValueError, "different writing profiles"):
            self.export(self.data, "v2.zip", first)

    def test_no_overwrite(self):
        first = self.export()
        original = first.read_bytes()
        with self.assertRaises(FileExistsError):
            self.export()
        self.assertEqual(first.read_bytes(), original)

    def test_safe_paths_and_duplicate_detection(self):
        for name in ("../../outside.md", "soul.md", "/tmp/escape.md"):
            data = copy.deepcopy(self.data)
            data["entries"][1]["name"] = name
            with self.assertRaises(ValueError):
                profile.validate(data)
        self.data["entries"].append(dict(self.data["entries"][0], id="another-voice"))
        with self.assertRaisesRegex(ValueError, "overwrite"):
            profile.validate(self.data)

    def test_invalid_parent_and_cycles_rejected(self):
        self.data["scopes"][1]["parent"] = "spoken"
        with self.assertRaisesRegex(ValueError, "relationship"):
            profile.validate(self.data)

    def test_approval_evidence_required(self):
        self.data["entries"][0]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "approval/evidence"):
            profile.validate(self.data)

    def test_utf16_limit(self):
        self.data["entries"][0]["text"] = "😀" * 10000
        profile.validate(self.data)
        self.data["entries"][0]["text"] += "a"
        with self.assertRaisesRegex(ValueError, "20,000"):
            profile.validate(self.data)

    def test_format_pair_required(self):
        self.data["entries"].pop()
        with self.assertRaisesRegex(ValueError, "both a template"):
            profile.validate(self.data)

    def test_archive_reader_does_not_extract_untrusted_members(self):
        path = self.export()
        with zipfile.ZipFile(path, "a") as z:
            z.writestr("../../escape.txt", "Untrusted extra member")
        current, _ = profile.read_archive(path)
        current["baseRevision"] = 1
        current["changes"] = ["Checkpoint updated"]
        with zipfile.ZipFile(self.export(current, "clean.zip", path)) as z:
            self.assertNotIn("../../escape.txt", z.namelist())
        self.assertFalse((self.root / "escape.txt").exists())

    def test_manually_edited_guidance_requires_reconciliation(self):
        first = self.export()
        altered = self.root / "edited.zip"
        with zipfile.ZipFile(first) as src, zipfile.ZipFile(altered, "x") as dest:
            for name in src.namelist():
                dest.writestr(name, b"A manually revised voice." if name == "global/soul.md" else src.read(name))
        with self.assertRaisesRegex(ValueError, "differs from its snapshot"):
            profile.read_archive(altered)


if __name__ == "__main__":
    unittest.main()
