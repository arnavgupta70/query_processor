"""
prompt_selector.py

This module determines what kind of query a user is 
asking and builds the right prompt accordingly.

Includes:
- QueryCategory Enum to categorize different types of queries.
- PromptSelector class which analyzes user input and generate 
                the best possible prompt, with built-in error handling.
"""

from enum import Enum

class QueryCategory(Enum):
    TECHNICAL = "technical"
    TROUBLESHOOTING = "troubleshooting"
    GENERAL = "general"
    UNKNOWN = "unknown"

class PromptSelector:
    def __init__(self):
        """
        Initializes the PromptSelector with pre-defined prompt
        templates for each supported category.
        """
        # Predefined templates for different query categories
        self.templates = {
            QueryCategory.TECHNICAL: (
                "You are an expert software engineer. Please provide a step-by-step, thorough solution "
                "with relevant examples or references where applicable."
            ),
            QueryCategory.TROUBLESHOOTING: (
                "You are a technical support assistant. Suggest potential reasons for the issue and "
                "step-by-step troubleshooting tips, including any necessary safety measures."
            ),
            QueryCategory.GENERAL: (
                "You are a well-informed AI. Provide a clear, concise, and factually accurate summary."
            ),
            QueryCategory.UNKNOWN: (
                "You are an AI assistant capable of handling diverse queries. "
                "Try to interpret the query and respond helpfully."
            ),
        }

        self.classification_rules = {
            QueryCategory.TECHNICAL: [
                "how do i",
                "please explain",
                "implement",
                "build",
                "develop",
                "step-by-step"
            ],
            QueryCategory.TROUBLESHOOTING: [
                "troubleshoot",
                "error",
                "issue",
                "bug",
                "fix",
                "cannot open",
            ],
            QueryCategory.GENERAL: [
                "what is",
                "who is",
                "when did",
                "where is",
                "can you define",
            ],
        }

    def generate_prompt(self, user_query: str):
        """
        Determines template to use based on user_query
        content, then appends the user's query to the template.

        Args:
            user_query (str): The input string from the user.

        Returns:
            tuple: (str, QueryCategory)
                - str is the full prompt, 
                - QueryCategory is the assigned category.

        Raises:
            ValueError: If the input query is None or empty.
        """
        if not user_query or not user_query.strip():
            raise ValueError("User query is empty or None.")

        query_lower = user_query.lower()
        category = QueryCategory.UNKNOWN

        # Check whether the user input query matches any of the strings in
        # the classification rules above.
        for cat, keywords in self.classification_rules.items():
            if any(keyword in query_lower for keyword in keywords):
                category = cat
                break

        # Build the final prompt
        base_template = self.templates.get(category, self.templates[QueryCategory.UNKNOWN])
        final_prompt = f"{base_template}\n\nUser Query:\n{user_query.strip()}\n"

        return final_prompt, category
