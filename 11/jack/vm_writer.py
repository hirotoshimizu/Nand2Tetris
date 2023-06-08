from dataclasses import dataclass
from enum import Enum

from jack.symbol_table import SymbolTable


class Segment(Enum):
    CONST = "const"
    ARG = "arg"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


symbols = {
    "add": "+",
    "sub": "-",
    "neg": "-",
    "multiply": "*",
    "eq": "=",
    "gt": "<",
    "lt": ">",
    "and": "&",
    "or": "|",
    "not": "!",
}

# symbols = ["+", "-", "-", "=", "<", ">", "&", "|", "!"]
# symbols = {"+", "-", "*", "=", "<", ">", "&", "|", "!"}

NEW_LINE = "\n"


@dataclass
class VmWriter:
    output: str = ""
    symbol_table = SymbolTable()

    def start(self):
        self.output = ""

    def write_push(self, segment: str, index: int) -> None:
        self.output += f"push {segment} {index}{NEW_LINE}"

    def write_pop(self, segment: str, index: int):
        self.output += f"pop {segment} {index}{NEW_LINE}"

    def write_arithmatic(self, command: str) -> None:
        self.output += f"{command}{NEW_LINE}"

    def write_lable(self, label: str):
        self.output += f"label {label}{NEW_LINE}"

    def write_goto(self, label: str):
        self.output += f"goto {label}{NEW_LINE}"

    def write_if(self, label: str):
        self.output += f"if-goto {label}{NEW_LINE}"

    def write_call(self, name: str, n_args: int):
        self.output += f"call {name} {n_args}{NEW_LINE}"

    def write_function(self, name: str, n_locals: int = 0) -> None:
        self.output += f"function {name} {n_locals}{NEW_LINE}"

    def write_return(self):
        self.output += f"return{NEW_LINE}"
