import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from schema import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
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
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file]
    )
    if args.verbose:
        print("Hello from python-agent!")
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    if args.verbose:
        print("User Prompt:", args.prompt)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if response.usage_metadata:
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        if response.function_calls:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        raise RuntimeError("No usage metadata found in the response.")


if __name__ == "__main__":
    main()
