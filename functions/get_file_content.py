import os
from functions.is_subpath import is_subpath
from functions.config import MAX_FILE_READ_SIZE

def get_file_content(working_directory, file_path)->str:
    result: str = ""
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not is_subpath(working_directory, file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            result = file.read(MAX_FILE_READ_SIZE)
            if len(result) >= MAX_FILE_READ_SIZE:
                result += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f'Error: Unable to read file "{file_path}": {str(e)}'
    return result

def main()->None:
    pass

if __name__ == "__main__":
    main()