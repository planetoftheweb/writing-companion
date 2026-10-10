"""Packaging contract for portable rules and optional connected guidance."""
import unittest
import zipfile
import tempfile
from pathlib import Path
from unittest.mock import patch
from test_build import build, ROOT

class SharedGuidanceTests(unittest.TestCase):
    def test_every_edition_carries_the_same_method_and_optional_connection(self):
        guide = (build.SKILL / "references/visual-narration.md").read_text()
        with tempfile.TemporaryDirectory() as tmp, patch.object(build, "DIST", Path(tmp)):
            build.build()
            for archive, prefix in [("writing-companion-skill.zip", "writing-companion/"),
                                    ("writing-companion-plugin.zip", "writing-companion/skills/writing-companion/")]:
                with zipfile.ZipFile(Path(tmp) / archive) as z:
                    self.assertEqual(z.read(prefix + "references/visual-narration.md").decode(), guide)
                    bridge = z.read(prefix + "references/connected-writing.md").decode()
                    self.assertIn("import_guidance without ifRevision to preview", bridge)
                    self.assertIn("cannot modify raw personal account voice", bridge)
                    self.assertIn("Grok Bot", bridge)
            with zipfile.ZipFile(Path(tmp) / "writing-companion-kit.zip") as z:
                project = z.read("Writing Companion/Project edition/writing-companion-guide.md").decode()
                self.assertIn(guide.strip(), project)
                self.assertIn("get_writing_context", project)
                self.assertIn("no background", project.lower())

    def test_guidance_recommendations_are_routed_and_scoped(self):
        entry = (build.SKILL / "SKILL.md").read_text()
        writing = (build.SKILL / "references/writing.md").read_text()
        learning = (build.SKILL / "references/learning.md").read_text()
        self.assertIn("During regular writing", entry)
        self.assertIn("recommendation workflow", writing)
        for expected in ["soul.md", "rules.md", "workspace guidance", "project guidance", "format instructions", "Read what already exists first", "Create or revise only approved guidance"]:
            self.assertIn(expected, learning)
