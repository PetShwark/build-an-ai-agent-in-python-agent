import os
from dotenv import load_dotenv
from google import genai
import argparse

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    args = parser.parse_args()
    # Now we can access `args.prompt`
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables.")
    print("Hello from python-agent!")
    user_prompt = args.prompt
    print("User Prompt:", user_prompt)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=user_prompt
        )
    if response.usage_metadata:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response from Gemini API:")
        print(response.text)
    else:
        raise RuntimeError("No usage metadata found in the response.")


if __name__ == "__main__":
    main()
