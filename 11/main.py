import sys

from jack.compilation_engine import CompilationEngine
from jack.jack_analyzer import (
    create_xml_file,
    get_file_location,
    get_file_path,
    get_vm_file,
    read_jack_file,
)
from jack.jack_tokenizer import JackTokenizer


def main():
    file_path = get_file_path()
    jack_file = get_vm_file(file_path)

    file_path_location = get_file_location(jack_file)
    jack = read_jack_file(jack_file)

    tokenizer = JackTokenizer(jack)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    element_tree = compiler.xml
    output = create_xml_file(element_tree)

    with open(file_path_location, mode="w") as f:
        f.write(output)


if __name__ == "__main__":
    main()
