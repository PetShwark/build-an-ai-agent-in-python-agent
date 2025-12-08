import os
from functions.is_subpath import is_subpath

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    print(f"Result for {f"'{directory}'" if directory != '.' else 'current'} directory:")
    if not is_subpath(working_directory, full_path):
        return f'\tError: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'\tError: The directory "{directory}" does not exist.'
    if not os.path.isdir(full_path):
        return f'\tError: "{directory}" is not a directory.'
    files_info = []
    items = os.listdir(full_path)
    if items:
        for item in os.listdir(full_path):
            item_info = f"\t- {item}: file_size={os.path.getsize(os.path.join(full_path, item))} bytes, is_dir={os.path.isdir(os.path.join(full_path, item))}"
            files_info.append(item_info)
    return "\n".join(files_info)

def main():
    pass

if __name__ == "__main__":
    main()