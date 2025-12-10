# NOTES:

## "Update Code" lesson

This is the prompting (more specific) that I needed in order to get the agent to edit the code.

    (python_agent) ➜  python_agent git:(main) ✗ uv run main.py "fix the bug in the python code in the calculator folder. 3 + 7 * 2 should not be 20"
    - Calling function: get_files_info
    Result for 'calculator' directory:
    - Calling function: get_files_info
    Result for current directory:
    - Calling function: get_file_content
    - Calling function: get_file_content
    - Calling function: write_file
    I've updated the `precedence` of the addition operator in `pkg/calculator.py` to correctly reflect the order of operations. Addition now has a lower precedence than multiplication.
    (python_agent) ➜  python_agent git:(main) uv run calculator/main.py "3 + 7 * 2"
    {
    "expression": "3 + 7 * 2",
    "result": 17
    }
    (python_agent) ➜  python_agent git:(main)