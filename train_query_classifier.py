#!/usr/bin/env python3
"""
train_query_classifier.py

Trains a text classification model to categorize queries into:
- technical
- troubleshooting
- general
- unknown

Uses scikit-learn's TfidfVectorizer + LogisticRegression.
"""

from typing import List
import numpy as np
from joblib import dump

# scikit-learn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

def get_training_data() -> (List[str], List[str]):
    """
    Returns a small, hard-coded dataset of queries and their labels.
    Each label must be one of: 'technical', 'troubleshooting', 'general', 'unknown'.
    """
    train_queries = [
        # TECHNICAL
        "How do I implement a binary search tree in Python?",
        "Please explain the steps to build a Flask application.",
        "How do I develop a REST API in Django?",
        "Can you detail the process of writing unit tests in Java?",
        "Steps to implement concurrency in Go?",

        # TROUBLESHOOTING
        "I'm getting an error when installing Node.js",
        "How do I troubleshoot a 404 not found issue?",
        "My program crashes with a segmentation fault, how do I fix it?",
        "Why am I seeing a 'connection refused' error on my server?",
        "Printer is not working, any troubleshooting steps?",

        # GENERAL
        "What is the capital of France?",
        "Who is the President of the United States?",
        "When did World War II end?",
        "Where is the tallest building in the world?",
        "Could you define photosynthesis?",

        # UNKNOWN / MISC
        "Bananas on Mars - is it feasible?",
        "Explain the meaning of the color purple in dreams?",
        "Random query about cats and dancing cheese.",
        "Hello, are you an AI or a human?",
        "What's your favorite movie?"
    ]

    train_labels = [
        # Match each query's label
        "technical", "technical", "technical", "technical", "technical",
        "troubleshooting", "troubleshooting", "troubleshooting", "troubleshooting", "troubleshooting",
        "general", "general", "general", "general", "general",
        "unknown", "unknown", "unknown", "unknown", "unknown"
    ]

    return train_queries, train_labels


def build_classifier_pipeline():
    """
    Creates a scikit-learn Pipeline that vectorizes text using TF-IDF
    and classifies with LogisticRegression.
    
    Returns:
        Pipeline object ready for training.
    """
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ])
    return pipeline


def main():
    # 1. Get training data
    train_queries, train_labels = get_training_data()

    # 2. Build pipeline: TF-IDF vectorizer + Logistic Regression
    pipeline = build_classifier_pipeline()

    # 3. Evaluate using cross-validation for a quick performance check
    scores = cross_val_score(pipeline, train_queries, train_labels, cv=3)
    print(f"Cross-validation scores: {scores}")
    print(f"Average CV score: {np.mean(scores):.3f}")

    # 4. Train on the entire dataset
    pipeline.fit(train_queries, train_labels)
    print("Model trained on entire dataset.")

    # 5. Make some test predictions
    test_queries = [
        "How do I fix an error when installing Docker?",
        "What is the population of Canada?",
        "I see a bug in my code. Why doesn't it compile?",
        "Are unicorns real or imaginary?",
        "How to code tictactoe game?"
    ]
    predictions = pipeline.predict(test_queries)
    for query, label in zip(test_queries, predictions):
        print(f"\nQuery: {query}\nPredicted Category: {label}")

    # 6. Save the trained pipeline to a file (using joblib) for later use
    dump(pipeline, "query_classifier.joblib")
    print("\nSaved trained model to query_classifier.joblib.")

if __name__ == "__main__":
    main()
