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
from joblib import load
import os

class QueryCategory(Enum):
    TECHNICAL = "technical"
    TROUBLESHOOTING = "troubleshooting"
    GENERAL = "general"
    UNKNOWN = "unknown"

class PromptSelector:
    def __init__(self, model_path="query_classifier.joblib"):
        # Load the trained pipeline (TfidfVectorizer + LogisticRegression)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. "
                                    f"Please train the model first.")
        
        self.classifier_pipeline = load(model_path)

        self.label_to_category = {
            "technical": QueryCategory.TECHNICAL,
            "troubleshooting": QueryCategory.TROUBLESHOOTING,
            "general": QueryCategory.GENERAL,
            "unknown": QueryCategory.UNKNOWN
        }

        # Predefined templates for different query categories
        self.templates = {
            QueryCategory.TECHNICAL: (
                "You are an expert software engineer with a strong background in Python. "
                "Provide a step-by-step, thorough solution to the user's query, including:\n"
                "1. Clear explanations of key concepts.\n"
                "2. Practical code samples in Python (include necessary dependencies, imports, and a brief explanation).\n"
                "3. References to relevant documentation (official docs, libraries, etc.) where applicable.\n"
                "4. Best practices for scalability, security, and maintainability.\n"
                "Aim to be detailed and precise. Avoid overly brief summaries—explanations must be comprehensive."
            ),
            QueryCategory.TROUBLESHOOTING: (
                "You are a technical support specialist. Examine the user's issue and:\n"
                "1. Suggest likely causes or reasons for the problem.\n"
                "2. Provide step-by-step troubleshooting tips (e.g., checking logs, verifying configurations).\n"
                "3. Highlight any necessary safety or security measures.\n"
                "4. Offer potential workarounds or known fixes.\n"
                "Try to guide the user in a systematic way, from simplest checks to more advanced diagnostic steps."
            ),
            QueryCategory.GENERAL: (
                "You are a well-informed AI. Provide a clear, concise, and factually accurate summary to the user's query. "
                "Include key points and contextual information as necessary.\n\n"
                "Where applicable, reference credible sources (books, articles, or reputable websites) to support your statements. "
                "Aim for an accessible explanation that a general audience can understand."
            ),
            QueryCategory.UNKNOWN: (
                "You are an AI assistant capable of handling diverse queries. "
                "Read the user's request carefully and respond in a helpful, contextually appropriate manner.\n\n"
                "If the query is ambiguous, ask clarifying questions or offer possible interpretations. "
                "Ensure your answer is as complete and self-contained as possible, given the information provided."
            ),
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
        
        model_label = self.classifier_pipeline.predict([user_query])[0]

        category = self.label_to_category.get(model_label, QueryCategory.UNKNOWN)

        base_template = self.templates[category]
        final_prompt = f"{base_template}\nUser Query: {user_query}"

        return final_prompt, category
