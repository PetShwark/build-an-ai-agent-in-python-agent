from functions.write_file import write_file

def test_write_file()->None:
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

def main()->None:
    test_write_file()

if __name__ == "__main__":
    main()