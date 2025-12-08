import os

def is_subpath(test_parent, test_child)-> bool:
    parent_abspath = os.path.abspath(test_parent)
    child_abspath = os.path.abspath(test_child)
    return os.path.commonpath([parent_abspath]) == os.path.commonpath([parent_abspath, child_abspath])

def main()->None:
    pass

if __name__ == "__main__":
    main()