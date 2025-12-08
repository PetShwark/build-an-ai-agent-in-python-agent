import os

def is_subdir(parent_dir, child_dir):
    parent_dir = os.path.abspath(parent_dir)
    child_dir = os.path.abspath(child_dir)
    return os.path.commonpath([parent_dir]) == os.path.commonpath([parent_dir, child_dir])

def main():
    pass

if __name__ == "__main__":
    main()