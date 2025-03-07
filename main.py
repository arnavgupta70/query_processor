import sys
from prompt_selector import PromptSelector, QueryCategory
from ai_client import AIClient, AIClientError
from ai_response import ResponseParser
from logger import AppLogger

def main():
    """
    Main function to run the AI Query Processor as a command-line tool.
    """
    logger = AppLogger()

    # 1. Capture user input from command line or prompt
    user_query = capture_user_input()

    # 2. Initialize PromptSelector to generate the correct prompt
    prompt_selector = PromptSelector()

    try:
        prompt, query_category = prompt_selector.generate_prompt(user_query)
    except ValueError as e:
        logger.log_error("PromptSelectorError", str(e))
        print("Failed to generate a valid prompt. Please try again.")
        return
    
    # 3. Interact with the AI (simulation for now)
    ai_client = AIClient()
    raw_response = None
    try:
        raw_response = ai_client.get_ai_response(prompt)
    except AIClientError as e:
        logger.log_error("AIClientError", str(e))
        print("The AI service is unavailable or encountered an error. Please try later.")
        return
    except Exception as e:
        logger.log_error("UnexpectedAIError", str(e))
        print("An unexpected error occurred while communicating with the AI.")
        return
    
    # 4. Parse the AI response
    parser = ResponseParser()
    final_answer = parser.parse_response(raw_response, query_category)

    # 5. Display the final answer to the user
    print("\n=== AI Response ===")
    print(final_answer)

def capture_user_input():
    """
    Retrieves user input either from command line arguments or from stdin.

    Returns:
        str: The combined user query string.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:])
    else:
        return input("Enter your query: ")

if __name__ == "__main__":
    main()
