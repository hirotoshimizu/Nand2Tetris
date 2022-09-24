from jack_analyzer import get_file_path, get_vm_file


def main():
    file_path = get_file_path()
    print(get_vm_file(file_path))
    print("hello")


if __name__ == "__main__":
    main()
