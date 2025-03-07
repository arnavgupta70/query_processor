# tests/test_main.py

import unittest
from unittest.mock import patch
import io
import main

class TestMainIntegration(unittest.TestCase):
    @patch("main.capture_user_input", return_value="How do I implement a binary search?")
    @patch("main.AIClient.get_ai_response", return_value="Mocked AI response about binary search.")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_successful_flow(self, mock_stdout, mock_ai_response, mock_user_input):
        """
        Tests an end-to-end flow with a known user query and a mocked AI response.
        """
        main.main()  # Run the main function
        output = mock_stdout.getvalue()

        self.assertIn("AI Response", output)
        self.assertIn("Mocked AI response about binary search.", output)
        mock_ai_response.assert_called_once()

    @patch("main.capture_user_input", return_value="")
    @patch("main.AppLogger.log_error")
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_empty_query(self, mock_stdout, mock_log_error, mock_user_input):
        """
        If user input is empty, 'prompt_selector' should raise a ValueError 
        and main.py should handle it gracefully without writing to disk.
        """
        main.main()
        output = mock_stdout.getvalue()

        self.assertIn("Failed to generate a valid prompt", output)

        # Verify that log_error was called, but it won't write to application.log
        mock_log_error.assert_called_once_with(
            "PromptSelectorError", 
            "User query is empty or None."
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("main.capture_user_input", return_value="Troubleshoot my Node.js error")
    @patch("main.AIClient.get_ai_response", side_effect=Exception("Simulated Cohere failure"))
    @patch("main.AppLogger.log_error")
    def test_main_ai_exception(self, mock_log_error, mock_ai_response, mock_user_input, mock_stdout):
        """
        If AIClient raises an exception, we verify main.py handles it gracefully
        by printing an error message and logging appropriately without crashing.
        """
        main.main()
        output = mock_stdout.getvalue()

        # Check console output
        self.assertIn("An unexpected error occurred while communicating with the AI", output)

        # Ensure the logger was called with the correct error category and message
        mock_log_error.assert_called_with("UnexpectedAIError", "Simulated Cohere failure")


if __name__ == "__main__":
    unittest.main()
