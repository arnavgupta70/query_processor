"""
response_parser.py

Performs post-processing or formatting of raw AI outputs
to produce a user-friendly final answer. For instance:
- Stripping disclaimers
- Adding category-specific clarifications
- Organizing multi-point answers into bullet points
"""

from prompt_selector import QueryCategory

class ResponseParser:
    def __init__(self):
        """
        Store disclaimers to filter response.
        """
        self.default_end_note = (
            "\n\nNote: This is a simulated AI response; content may not be fully accurate.\n"
        )

    def parse_response(self, raw_response: str, query_category: QueryCategory) -> str:
        """
        Clean and format the AI’s raw response.

        Args:
            raw_response (str): The unprocessed text from the AI system.
            query_category (QueryCategory): Category of the user query.

        Returns:
            str: The cleaned and formatted response.
        """
        if not raw_response:
            return "No response was received. Please try again or revise your question."

        # Customize the final message based on category
        if query_category == QueryCategory.TROUBLESHOOTING:
            raw_response += "\n\nIf the issue persists, consider contacting technical support or an expert."

        # Add a default note at the end
        final_output = raw_response.strip() + self.default_end_note

        return final_output
