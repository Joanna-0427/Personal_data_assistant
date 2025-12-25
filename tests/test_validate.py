import unittest
from pda.validate import validate_date, parse_amount, validate_row

class TestValidate(unittest.TestCase):
    def test_validate_date_ok(self):
        self.assertTrue(validate_date("2024-01-01"))

    def test_validate_date_bad(self):
        self.assertFalse(validate_date("01-01-2024"))

    def test_parse_amount_ok(self):
        self.assertEqual(parse_amount("12.34"), 12.34)

    def test_parse_amount_out_of_range(self):
        with self.assertRaises(ValueError):
            parse_amount("999999")

    def test_validate_row_ok(self):
        ok, cleaned, err = validate_row({"date":"2024-01-01","amount":"10","category":"Food","description":"x"})
        self.assertTrue(ok)
        self.assertIsNone(err)
        self.assertEqual(cleaned["category"], "Food")

    def test_validate_row_bad_category(self):
        ok, cleaned, err = validate_row({"date":"2024-01-01","amount":"10","category":" ","description":"x"})
        self.assertFalse(ok)
        self.assertIn("Empty", err)

if __name__ == "__main__":
    unittest.main()
