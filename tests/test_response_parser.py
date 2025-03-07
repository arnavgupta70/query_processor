import unittest
from prompt_selector import QueryCategory
from response_parser import ResponseParser

class TestResponseParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResponseParser()

    def test_empty_response(self):
        result = self.parser.parse_response("", QueryCategory.GENERAL)
        self.assertIn("No response was received", result)

    def test_troubleshooting_note(self):
        raw = "Reinstall the software to fix the issue."
        result = self.parser.parse_response(raw, QueryCategory.TROUBLESHOOTING)
        self.assertIn("Reinstall the software to fix the issue.", result)
        self.assertIn("If the issue persists", result)

    def test_disclaimer_added_in_note(self):
        raw = "Here's how to code TicTacToe in Python."
        result = self.parser.parse_response(raw, QueryCategory.TECHNICAL)
        self.assertIn("Here's how to code TicTacToe in Python.", result)
        self.assertIn("content may not be fully accurate", result)

if __name__ == "__main__":
    unittest.main()
