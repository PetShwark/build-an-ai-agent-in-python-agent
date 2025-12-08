import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
import argparse

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.prompt`
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")
    if args.verbose:
        print("Hello from python-agent!")
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    if args.verbose:
        print("User Prompt:", messages[0].parts[0].text)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
        )
    if response.usage_metadata:
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response from Gemini API:")
        print(response.text)
    else:
        raise RuntimeError("No usage metadata found in the response.")


if __name__ == "__main__":
    main()
