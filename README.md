# AI Query Processor

This repository contains a robust reference implementation of an AI-Driven Query Processor. It demonstrates:

1. **Prompt Engineering & AI Integration**:

   - Adaptive prompts based on user query category (technical, troubleshooting, general, unknown).
   - A simulated AI client that could easily be extended to connect to a real service (local or remote).

2. **Abstraction & Modular Design**:

   - Modules split by responsibility (`prompt_selector`, `ai_client`, `response_parser`, `logger`).
   - Clear layering of logic that simplifies maintenance and potential expansion.

3. **Root Cause & "Why" Analysis**:

   - Each module is self-documented, explaining the rationale behind its implementation.
   - Testing suite ensures edge cases and error conditions are handled properly.

4. **Robustness & Testing**:

   - Comprehensive unit tests
   - Demonstrates how to handle transient failures, empty prompts, or unknown categories.