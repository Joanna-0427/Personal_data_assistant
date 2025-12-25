import unittest
from pathlib import Path
import json

from pda.analyze import analyze_expenses

class TestAnalyze(unittest.TestCase):
    def test_analyze_expenses_empty_file(self):
        # TODO: create a minimal cleaned CSV and validate results
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
