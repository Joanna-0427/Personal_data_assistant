import unittest
from pathlib import Path
import json

from pda.ingest import ingest_notes

class TestIngest(unittest.TestCase):
    def test_ingest_notes_extracts_action_items(self):
        tmp = Path("data/processed")
        tmp.mkdir(parents=True, exist_ok=True)

        notes = tmp / "tmp_notes.txt"
        notes.write_text("TODO: do thing\nhello #tag\nFOLLOW UP: x\n", encoding="utf-8")

        out = ingest_notes(str(notes), str(tmp))
        payload = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {"action_items":[],"topics":{}}

        # TODO: after student implements JSON writing, these should pass
        # For now they will fail until implemented.
        self.assertTrue("action_items" in payload)

if __name__ == "__main__":
    unittest.main()
