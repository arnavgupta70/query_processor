"""
ai_client.py

This module manages interactions with an AI model. 
For now, we shall simulate AI responses, but can be 
extended to use external service.
"""

import random
import time

class AIClientError(Exception):
    """
    Custom exception for AI client errors (e.g., unresponsive service).
    """
    pass

class AIClient:
    def __init__(self):
        """
        Initialize the AIClient. In a real-world scenario,
        we would store API credentials and endpoints here.
        """
        pass

    def get_ai_response(self, prompt: str, max_retries=3, retry_delay=1) -> str:
        """
        Simulates response from AI system.

        Args:
            prompt (str): The constructed prompt (including user query).
            max_retries (int): Number of times to retry if there's a failure.
            retry_delay (float): Delay in seconds between retries.

        Returns:
            str: The AI’s response (simulated as of now)

        Raises:
            AIClientError: If the AI system fails after all retries.
        """
        if not prompt.strip():
            raise AIClientError("Prompt cannot be empty.")

        # Simulate transient failures 25% of the time
        for attempt in range(1, max_retries + 1):
            if random.random() < 0.75:
                # 75% chance it “succeeds” on each attempt
                return self._simulate_response(prompt)
            else:
                # Simulate an error
                if attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    raise AIClientError("AI service is unresponsive after multiple attempts.")

        # Should never get here if the logic above is correct,
        # but in case we do, raise an error.
        raise AIClientError("Unknown error occurred in AIClient.")

    def _simulate_response(self, prompt: str) -> str:
        """
        Produces a MOCK response based on the prompt content.
        """
        # For now, randomly picks any of the "responses" and returns it.
        # Can be extended further (eg. add logic to parse prompt and then
        # provide a tailored response specific to query)
        simulated_responses = [
            "Certainly! Here’s a detailed breakdown...",
            "Here’s a concise explanation of the topic...",
            "Apologies, I need more information. Could you clarify?",
            "Below are some steps you can follow to resolve the issue...",
            "Here’s a high-level overview..."
        ]
        chosen_response = random.choice(simulated_responses)
        return chosen_response
