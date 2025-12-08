import os
import subprocess
from functions.is_subpath import is_subpath
from functions.config import SUBPROCESS_TIMEOUT

def run_python_file(working_directory, file_path, args=[])-> str:
    if not os.path.isabs(file_path):
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        file_abspath = file_path
    if not file_abspath.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    if not is_subpath(working_directory, file_abspath):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abspath):
        return f'Error: File "{file_path}" not found.'
    try:
        print(f"Running Python file: {file_path} with args: {args}")
        result = subprocess.run(
            "python3 " + f'"{file_path}" ' + ' '.join(args), 
            cwd=working_directory,
            timeout=SUBPROCESS_TIMEOUT,
            shell=True, 
            capture_output=True, 
            text=True 
            )
        output:str = ""
        if result.stdout:
            output += f"STDOUT: {result.stdout}\n"
        else:
            output += "No output produced.\n"
        if result.stderr:
            output += f"STDERR: {result.stderr}\n"
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        return output.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"

def main()->None:
    pass

if __name__ == "__main__":
    main()