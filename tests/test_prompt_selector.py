import unittest
from unittest.mock import patch, MagicMock
from prompt_selector import PromptSelector, QueryCategory

class TestPromptSelector(unittest.TestCase):
    @patch("prompt_selector.load")
    def test_generate_prompt_technical(self, mock_load):
        """
        If the classifier predicts 'technical', we check that the prompt is correct.
        """
        # Mock pipeline's predict return value
        mock_pipeline = MagicMock()
        mock_pipeline.predict.return_value = ["technical"]
        mock_load.return_value = mock_pipeline

        selector = PromptSelector(model_path="query_classifier.joblib")
        user_query = "How do I implement a queue in Python?"
        prompt, category = selector.generate_prompt(user_query)

        self.assertEqual(category, QueryCategory.TECHNICAL)
        self.assertIn("expert software engineer", prompt.lower())

    @patch("prompt_selector.load")
    def test_generate_prompt_troubleshooting(self, mock_load):
        """
        If the classifier predicts 'troubleshooting', verify the prompt text.
        """
        mock_pipeline = MagicMock()
        mock_pipeline.predict.return_value = ["troubleshooting"]
        mock_load.return_value = mock_pipeline

        selector = PromptSelector()
        user_query = "I keep getting an error when installing Node.js"
        prompt, category = selector.generate_prompt(user_query)

        self.assertEqual(category, QueryCategory.TROUBLESHOOTING)
        self.assertIn("technical support specialist", prompt.lower())

    @patch("prompt_selector.load")
    def test_empty_query_raises_valueerror(self, mock_load):
        # Ensure no classification attempt if the query is empty
        mock_pipeline = MagicMock()
        mock_load.return_value = mock_pipeline

        selector = PromptSelector()
        with self.assertRaises(ValueError):
            selector.generate_prompt("")

if __name__ == "__main__":
    unittest.main()
