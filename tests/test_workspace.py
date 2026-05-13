from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gsd_ai.schema import ContextContract, Signal, SignalType
from gsd_ai.workspace import DEFAULT_DIRS, create_project, init_workspace


class WorkspaceTests(unittest.TestCase):
    def test_init_workspace_creates_expected_layout(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            created = init_workspace(tmp_path)

            for dirname in DEFAULT_DIRS:
                self.assertTrue((tmp_path / dirname).is_dir())

            self.assertTrue((tmp_path / "AGENTS.md").exists())
            self.assertTrue((tmp_path / ".gsd-ai" / "index.json").exists())
            self.assertTrue((tmp_path / ".gsd-ai" / "audit.jsonl").exists())
            self.assertTrue(created)

    def test_create_project_writes_context_and_updates_index(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            init_workspace(tmp_path)

            context_path = create_project(tmp_path, "Launch GSD-AI", purpose="Create a useful execution substrate.")

            self.assertTrue(context_path.exists())
            text = context_path.read_text()
            self.assertIn("# Launch GSD-AI", text)
            self.assertIn("Create a useful execution substrate.", text)

            index = json.loads((tmp_path / ".gsd-ai" / "index.json").read_text())
            self.assertEqual(index["projects"][0]["slug"], "launch-gsd-ai")

    def test_context_contract_markdown_has_core_sections(self):
        md = ContextContract(name="Example", active_goals=["Ship skeleton"]).to_markdown()

        self.assertIn("# Example", md)
        self.assertIn("## Active goals", md)
        self.assertIn("- Ship skeleton", md)
        self.assertIn("## Risks", md)

    def test_signal_fingerprint_is_stable_shape(self):
        signal = Signal(
            signal_type=SignalType.ACTION,
            summary="Draft the initial workspace generator",
            project="GSD-AI",
            source="manual-test",
        )

        self.assertEqual(signal.fingerprint, "action:gsd-ai:draft-the-initial-workspace-generator")


if __name__ == "__main__":
    unittest.main()
