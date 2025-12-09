import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, llm_model
from schema import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.llm_call_function import call_function
import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def llm_query_loop(cli_args: argparse.Namespace, client: genai.Client):
    messages = [types.Content(role="user", parts=[types.Part(text=cli_args.prompt)])]
    available_functions = types.Tool(
        function_declarations = [
            schema_get_files_info, 
            schema_get_file_content, 
            schema_run_python_file, 
            schema_write_file
            ]
    )
    response = client.models.generate_content(
        model=llm_model, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if response.usage_metadata:
        if cli_args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        if response.function_calls:
            function_response_list = []
            for function_call_part in response.function_calls:
                function_response = call_function(function_call_part, verbose=cli_args.verbose)
                if function_response.parts[0].function_response.response:
                    function_response_list.append(function_response.parts[0])
                else:
                    raise RuntimeError("No response from function call.")
                if cli_args.verbose: print(f"-> {function_response.parts[0].function_response.response}")
    else:
        raise RuntimeError("No usage metadata found in the response.")
    

def main():
    args = parse_arguments()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: raise RuntimeError("GEMINI_API_KEY not found in environment variables.")
    if args.verbose: print("Hello from python-agent!")
    if args.verbose: print("User Prompt:", args.prompt)
    client = genai.Client(api_key=api_key)
    llm_query_loop(args, client)


if __name__ == "__main__":
    main()
