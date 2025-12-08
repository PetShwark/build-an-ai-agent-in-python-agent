import os
from functions.is_subpath import is_subpath

def write_file(working_directory, file_path, content)-> str:

    if not os.path.isabs(file_path):
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not is_subpath(working_directory, file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        return f'Error: Unable to write to file "{file_path}": {str(e)}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def main()->None:
    pass

if __name__ == "__main__":
    main()