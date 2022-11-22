import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path


EXTENTION = '.txml'


def get_file_path() -> Path:
    return Path(sys.argv[1])


def get_vm_file(path: Path):
    if path.is_dir():
        return [file_name for file_name in path.glob("*.jack")]
    return [path]


def get_file_location(jack_file: list[Path]) -> str:
    dir = jack_file[0].parent
    file_stem = jack_file[0].stem
    file_path = dir / file_stem
    return str(file_path) + EXTENTION


def read_jack_file(jack_file: list[Path]) -> str:
    with open(jack_file[0]) as f:
        return f.read()


def create_xml_file(element_tree: ET.Element):
    ET.indent(element_tree, space='  ')
    output = ET.tostring(element_tree, encoding='unicode', short_empty_elements=False)

    # 1.Add spaces between tags
    # 2.Add new line if there is no character between bigining and end of tags
    replacements = [('>(.+?)<\/','> \\1 </'), ('(\s+)(<\w+>)(<\/\w+>)','\\1\\2\\1\\3')]
    for pattern, replacement in replacements:
        output = re.sub(pattern, replacement, output)

    return output