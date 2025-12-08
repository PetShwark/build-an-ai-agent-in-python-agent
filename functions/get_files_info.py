import os
from functions.is_subpath import is_subpath
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory:str, directory:str=".")-> str:
    if working_directory is None:
        working_directory = os.getcwd()
    full_path:str = os.path.join(working_directory, directory)
    print(f"Result for {f"'{directory}'" if directory != '.' else 'current'} directory:")
    if not is_subpath(working_directory, full_path):
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'\tError: The directory "{directory}" does not exist.'
    if not os.path.isdir(full_path):
        return f'\tError: "{directory}" is not a directory.'
    files_info:list[str|None] = []
    items:list[str] = os.listdir(full_path)
    if items:
        for item in items:
            item_info:str = f"\t- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={os.path.isdir(os.path.join(full_path, item))}"
            files_info.append(item_info)
    return "\n".join(files_info)

def main()->None:
    pass

if __name__ == "__main__":
    main()