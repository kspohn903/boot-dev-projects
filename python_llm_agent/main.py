import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    # --- 1. Load Environment Variables and API Key ---
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
       print("Error: GEMINI_API_KEY not found. Please check your .env file.")
       sys.exit(1)

    # --- 2. Parse Command Line Arguments ---

    # Check for the --verbose flag anywhere in the arguments list 
    # (excluding script name)
    IS_VERBOSE = "--verbose" in sys.argv

    # Filter out the script name and the --verbose flag to isolate potential 
    # prompt arguments
    filtered_args = [arg for arg in sys.argv[1:] if arg != "--verbose"]

    if not filtered_args:
       print("Error: Please provide a prompt as a command line argument.")
       print("Usage example: python main.py \"Your prompt here\" [--verbose]")
       sys.exit(1)

    # The prompt is treated as the first positional argument remaining
    PROMPT = filtered_args[0]

    # --- 3. Create Gemini Client Instance ---
    try:
       client = genai.Client(api_key=api_key)
    except Exception as e:
       print(f"Error creating Gemini client: {e}")
       sys.exit(1)

    # --- 4. Define Model and Generate Content ---
    MODEL_NAME = "gemini-2.0-flash-001"
    try:
       if IS_VERBOSE:
          print(f"User prompt: {PROMPT}")
          print(f"Sending prompt to model: {MODEL_NAME}")
        
       response = client.models.generate_content(
        model=MODEL_NAME,
        contents=PROMPT
       )
       # --- 5. Print Response Text ---
       print(response.text)

       # --- 6. Print Token Usage (Conditionally) ---
       usage = response.usage_metadata

       if IS_VERBOSE and usage:
          prompt_tokens = usage.prompt_token_count
          response_tokens = usage.candidates_token_count
          # Note: The assignment only requires printing these in verbose mode, 
        # but the prompt output format example implies printing X and Y.
        # Following the assignment text: "If the --verbose flag is included, 
        # the console output should include..."
        
        # The assignment specifically asks for "Prompt tokens: X" and 
        # "Response tokens: Y" to be printed *only* when the --verbose flag 
        # is set.
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
     
    except Exception as e:
        # If a verbose flag is present, you might print more context, 
        # but for simplicity, we keep the error handling clean.
        print(f"An error occurred during API call: {e}")
        sys.exit(1)

if __name__ == "__main__":
   main()
