"""
ai_client.py

This module interacts with the Cohere Chat API to get answers
based on the prompt (user query). It replaces the prior simulation.

Prerequisites:
1. pip install cohere
2. Set Cohere API key in this file or via an environment variable.
"""

import cohere
from dotenv import load_dotenv
import os
import time

class AIClientError(Exception):
    """
    Custom exception for AI client errors (e.g., unresponsive service).
    """
    pass

class AIClient:
    def __init__(
        self,
        api_key: str = "",
        model_name: str = "command-r-plus-08-2024",
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initializes the AIClient with Cohere's Chat API.

        Args:
            api_key (str): Your Cohere API key (if not provided, tries COHERE_API_KEY env var).
            model_name (str): Cohere model name, e.g. "command-r-plus-08-2024".
            max_retries (int): Number of times to retry if failure.
            retry_delay (float): Time (seconds) to wait between retries.
        """
        # Retrieve API key from argument or environment
        load_dotenv()
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise AIClientError("Cohere API key not found. Provide api_key or set COHERE_API_KEY env var.")

        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Create a Cohere client (ClientV2 for the chat endpoint)
        self.client = cohere.ClientV2(api_key=self.api_key)

    def get_ai_response(self, prompt: str) -> str:
        """
        Retrieves a response from Cohere's Chat API using the provided prompt.

        Args:
            prompt (str): The user's query or system instructions.

        Returns:
            str: The Cohere model's response text.

        Raises:
            AIClientError: If Cohere API fails after max_retries or the response is invalid.
        """
        if not prompt.strip():
            raise AIClientError("Prompt cannot be empty.")

        # Attempt to call Cohere multiple times (up to max_retries) to handle transient issues
        last_err = None
        for attempt in range(1, self.max_retries + 1):
            try:
                # We construct messages for the Chat API
                # The entire prompt is treated as a single user message in this simple example.
                messages = [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]

                # Call Cohere's Chat endpoint
                # (can use chat_stream to get response in real time, without wait)
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                )

                # Extract the text from the response
                if not response.message or not response.message.content:
                    raise AIClientError("Empty response from Cohere.")

                # If message.content is a list or string, handle accordingly.
                # For Command-R style responses, we expect `response.message.content` to be a list of tokens/segments.
                # The below is a generic approach if it's a list:
                content = response.message.content
                if isinstance(content, list):
                    return "".join(segment.text for segment in content)
                else:
                    # If it's a string, just return it directly
                    return content

            except Exception as e:
                last_err = e
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    # Exhausted all retries
                    raise AIClientError(f"Cohere Chat API failed after {self.max_retries} attempts."
                                       f"Last error: {last_err}") from last_err

        # Error handling (unlikely to reach here though).
        raise AIClientError("Unknown error occurred in Cohere AI client.")
