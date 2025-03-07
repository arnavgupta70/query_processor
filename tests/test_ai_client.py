import unittest
from unittest.mock import patch, MagicMock
from ai_client import AIClient, AIClientError

class TestAIClient(unittest.TestCase):
    @patch("ai_client.cohere.ClientV2")
    def test_successful_cohere_call(self, mock_client_class):
        """
        Checks that a valid prompt returns a correct message from the Cohere mock.
        """
        mock_client_instance = mock_client_class.return_value
        mock_chat_return = MagicMock()
        
        # Simulate .message.content returning a string
        mock_chat_return.message.content = "Mocked Cohere content"
        
        mock_client_instance.chat.return_value = mock_chat_return

        ai_client = AIClient(api_key="fake_key", model_name="command-r-plus-08-2024")
        result = ai_client.get_ai_response("A valid prompt")

        self.assertEqual(result, "Mocked Cohere content")
        mock_client_instance.chat.assert_called_once()

    @patch("ai_client.cohere.ClientV2")
    def test_empty_prompt_raises_error(self, mock_client_class):
        """
        If the prompt is empty, AIClient raises an AIClientError.
        """
        ai_client = AIClient(api_key="fake_key")
        with self.assertRaises(AIClientError):
            ai_client.get_ai_response("")

    @patch("ai_client.cohere.ClientV2")
    def test_cohere_empty_content(self, mock_client_class):
        """
        If Cohere returns an empty .message.content, AIClient raises AIClientError.
        """
        mock_instance = mock_client_class.return_value
        mock_chat_return = MagicMock()
        mock_chat_return.message.content = ""
        mock_instance.chat.return_value = mock_chat_return

        ai_client = AIClient(api_key="fake_key")
        with self.assertRaises(AIClientError):
            ai_client.get_ai_response("Non-empty prompt")

    @patch("ai_client.cohere.ClientV2")
    def test_retry_logic(self, mock_client_class):
        """
        If cohere.ClientV2.chat fails on the first attempt but succeeds later,
        AIClient should retry and eventually succeed.
        """
        mock_instance = mock_client_class.return_value

        # We'll make the first call to chat() raise an exception,
        # the second call returns a valid response.
        side_effects = [
            Exception("Temporary Cohere error"),
            MagicMock(message=MagicMock(content="Recovered content"))
        ]
        mock_instance.chat.side_effect = side_effects

        ai_client = AIClient(api_key="fake_key", max_retries=2)

        response = ai_client.get_ai_response("Prompt that eventually succeeds")
        self.assertEqual(response, "Recovered content")
        self.assertEqual(mock_instance.chat.call_count, 2)

if __name__ == "__main__":
    unittest.main()
