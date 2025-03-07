# AI Query Processor

This repository contains a robust reference implementation of an AI-Driven Query Processor. It demonstrates:

1. ML-Based Query Classification:

    - Uses a Logistic Regression model (trained via scikit-learn with TF-IDF features) to classify incoming queries into technical, troubleshooting, general, or unknown.

2. Abstraction & Modular Design:

   - Modules split by responsibility (`prompt_selector`, `ai_client`, `response_parser`, `logger`).
   - Clear layering of logic that simplifies maintenance and potential expansion.

3. Root Cause & "Why" Analysis:

   - Each module is self-documented, explaining the rationale behind its implementation.
   - Testing suite ensures edge cases and error conditions are handled properly.

4. Robustness & Testing:

   - Comprehensive unit tests
   - Demonstrates how to handle transient failures, empty prompts, or unknown categories.

5. Cohere Integration:

- ai_client.py now interacts with Cohere’s Chat API using cohere.ClientV2.
- You must set your Cohere API key as an environment variable COHERE_API_KEY or provide it explicitly.

# Requirements & Installation

- Python 3.8+ recommended.

- Install Poetry
If you haven’t already:

`curl -sSL https://install.python-poetry.org | python3 -`

- Clone the repository

`git clone https://github.com/arnavgupta70/query_processor.git`
`cd query_processor`

- Install Dependencies with Poetry

`poetry install`

This will create/update a virtual environment and install everything declared in `pyproject.toml`.

- Activate the Poetry Shell (optional but convenient):

`poetry shell`

Now you can run commands without prefixing poetry run.

- COHERE_API_KEY

Your Cohere API key.

Set it in your shell or environment 

(e.g., `export COHERE_API_KEY="your_key_here"` on Linux/Mac, `set COHERE_API_KEY=your_key_here` on Windows).

If you don’t want to set an environment variable, you can pass api_key directly to the AIClient constructor in main.py, but using environment variables is generally preferred for secrets.

# Usage

1. (Optional) Train the Model Manually
If you want to train the classifier before running the main app:

        poetry run python train_query_classifier.py

This script uses a small, hardcoded dataset to train a Logistic Regression model, saving it to query_classifier.joblib.

2. Run the Application
If you have the Poetry shell activated

        python main.py

Or, from outside the poetry shell

        poetry run python main.py

If `query_classifier.joblib` is not found, do Step 1 and try again.

3. Flow
- `main.py` starts the process.
- Classification & Prompt: `prompt_selector.py` loads the model, categorizes the query, and builds a tailored prompt.
- Cohere Call: `ai_client.py` calls Cohere’s Chat API using your API key.
- Response Parsing: `response_parser.py` cleans or enriches the AI’s text.
- Display: The user sees the final answer.

# Testing
Run all tests via:

    # If in poetry shell:
    python -m unittest discover -s tests

    # Or with poetry run:
    poetry run python -m unittest discover -s tests

## Mocking Strategy
test_ai_client.py: Mocks out cohere.ClientV2 to avoid actual API calls.

test_main.py: Mocks user input and AI responses to test the main flow in isolation.

Integration vs. Unit Tests: Integration tests patch less (only external calls), while unit tests patch individual modules more thoroughly.

# Key Files

1. main.py

Orchestrates the entire flow:
- Checks/loads the ML model,
- Captures user input,
- Calls Cohere for an AI response,
- Parses the output, and
- Displays the final answer.

2. train_query_classifier.py

Trains a simple text classifier (TF-IDF + Logistic Regression) to categorize user queries. Saves the model as query_classifier.joblib.

3. prompt_selector.py

Loads the trained model, predicts the query category, and composes a specialized prompt string based on that category.

4. ai_client.py

Interacts with Cohere Chat API (via cohere.ClientV2). Replaces the prior random simulation logic.

5. response_parser.py

Cleans the AI response (e.g., removing disclaimers, adding disclaimers of your own, formatting steps for troubleshooting queries, etc.).

6. tests/

Contains unit/integration tests using Python’s unittest, ensuring each component behaves correctly. Mocks are used to avoid hitting real endpoints in tests.

# Design Overview

1. ML Classifier
- train_query_classifier.py trains a simple TF-IDF + LogisticRegression model, saving the result as query_classifier.joblib.
- prompt_selector.py loads and uses this model to predict a category for each new query, instead of relying on manual keyword checks.

2. Cohere Chat API
- ai_client.py uses cohere.ClientV2 to send chat messages to the model specified (e.g., "command-r-plus-08-2024").
- Features basic retry logic for transient failures.

3. Response Parsing
- response_parser.py might remove disclaimers, add disclaimers, or reformat the text (especially for troubleshooting queries).

4. Automatic Training
- If the model is absent, main.py triggers train_query_classifier.py via subprocess. This ensures the app can bootstrap itself.

5. Logging
- logger.py (if present) can record events or errors to a file (application.log).

6. Testing with Mocks
- Ensures you’re not making real calls to Cohere or rewriting model files.
- Keeps tests deterministic and fast.

#

Enjoy using the AI Query Processor with Poetry!
Feel free to raise issues or PRs for enhancements, and happy hacking.
