import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt, llm_model, MAX_LOOPS
from schema import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.llm_call_function import call_function
import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser.parse_args()


def llm_query_loop(cli_args: argparse.Namespace, client: genai.Client):
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=cli_args.prompt)]
            )
        ]
    available_functions = types.Tool(
        function_declarations = [
            schema_get_files_info, 
            schema_get_file_content, 
            schema_run_python_file, 
            schema_write_file
            ]
    )
    # loop_count = MAX_LOOPS - 1 # Testing one time through the loop
    loop_count = 0
    finished = False
    while loop_count < MAX_LOOPS and not finished:
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
            if response.candidates:
                if cli_args.verbose: print(f"Number of candidates received: {len(response.candidates)}")
                for candidate in response.candidates:
                    if candidate.content.parts[0].text:
                        print(candidate.content.parts[0].text)
                        finished = True
                    messages.append(candidate.content)
                    #
                    # Only one field in a part should be populated at a time.
                    # Looking at a few for debugging.
                    if cli_args.debug:
                        print("AI Content Text:", candidate.content.parts[0].text)
                        print("AI Content Function Calls:", candidate.content.parts[0].function_call)
                        print("AI Content Function Responses:", candidate.content.parts[0].function_response)
                        print("AI Content Thought:", candidate.content.parts[0].thought)
                        print("AI Content Executable Code:", candidate.content.parts[0].executable_code)
                        print("AI Content Inline Data:", candidate.content.parts[0].inline_data)
            if response.function_calls:
                # function_response_list = []
                for function_call_part in response.function_calls:
                    function_response = call_function(function_call_part, verbose=cli_args.verbose)
                    if function_response.parts[0].function_response.response:
                        #
                        # Append the function response to the messages for the next LLM call
                        messages.append(types.Content(
                            role="user",
                            parts=function_response.parts
                            ))
                        # function_response_list.append(function_response.parts[0])
                    else:
                        raise RuntimeError("No response from function call.")
                    if cli_args.verbose: print(f"-> {function_response.parts[0].function_response.response}")
        else:
            raise RuntimeError("No usage metadata found in the response.")
        if cli_args.debug:
            print(f"Number of messages so far ({len(messages)})")
            for msg in messages:
                print(f"- Role: {msg.role}, Parts: {len(msg.parts)}")
                for part in msg.parts:
                    print(f"  - Part Text: {part.text}, Function Call: {part.function_call}, Function Response: {part.function_response}")  
        loop_count += 1
    

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
