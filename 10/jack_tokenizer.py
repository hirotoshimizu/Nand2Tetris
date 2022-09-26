import re
from dataclasses import dataclass
from typing import Any


@dataclass
class SyntaxError(Exception):
    tokenType: str


keyword = [
    # Whitespace:
    # [" +", None],
    ["^\s+", None],
    # Skip single-line comments:
    ["^\/\/.*", None],
    # # Skip multi-line comments:
    ["^\/\*[\s\S]*?\*\/", None],
    # # Symbols, delimiters:
    ["^;", ";"],
    ["^\{", "{"],
    ["^\}", "}"],
    ["^\(", "("],
    ["^\)", ")"],
    ["^,", ","],
    ["^\.", "."],
    # ["/^\[/", "["],
    # ["/^\]/", "]"],
    # # Keywords:
    ["^let", "let"],
    ["^var", "var"],
    ["^boolean", "boolean"],
    # ["^\blet\b", "let"],
    ["^int", "int"],
    ["^char", "char"],
    ["^if", "if"],
    ["^else", "else"],
    ["^do", "do"],
    ["^true", "true"],
    ["^false", "false"],
    ["^null", "null"],
    ["^while", "while"],
    # ["/^\bfor\b/", "for"],
    ["^function", "function"],
    ["^constructor", "constructor"],
    ["^method", "method"],
    ["^return", "return"],
    ["^static", "static"],
    ["^field", "field"],
    ["^void", "void"],
    ["^type", "type"],
    ["^class", "class"],
    # ["/^\bextends\b/", "extends"],
    # ["/^\bsuper\b/", "super"],
    # ["/^\bnew\b/", "new"],
    ["^this", "this"],
    # int
    # ["/^\d+/", 'int'],
    ["^[0-9]+", "int"],
    # Identifiers:
    ["^\w+", "IDENTIFIER"],
    # Equality operators: ==, !=
    # ["/^[=!]=/", "EQUALITY_OPERATOR"],
    # Assignment operators: =, *=, /=, +=, -=,
    ["^=", "SIMPLE_ASSIGN"],
    # ["/^[\*\/\+\-]=/", "COMPLEX_ASSIGN"],
    # # Math operators: +, -, *, /
    # ["/^[+\-]/", "ADDITIVE_OPERATOR"],
    # ["/^[*\/]/", "MULTIPLICATIVE_OPERATOR"],
    # # Relational operators: >, >=, <, <=
    ["^[><]=?", "RELATIONAL_OPERATOR"],
    # # Logical operators: &&, ||
    # ["/^&&/", "LOGICAL_AND"],
    # ["/^\|\|/", "LOGICAL_OR"],
    # ["/^!/", "LOGICAL_NOT"],
    # char:
    ["^[a-zA-Z]+", "char"],
    ['^"[a-zA-Z]+"', "char"],
    # ['^"[^"]*"', "char"],
    # ["/^'[^']*'/", "char"],
    #    ['/^'[^']*'/', 'STRING'],
]


class JackTokenizer:
    def init(self, string: Any):
        self.string: Any = string
        self.cursor: int = 0

    def has_more_tokens(self) -> bool:
        return self.cursor < len(str(self.string))

    def match(self, pattern: str, string: Any):
        # regexp = re.compile(r"^\blet\b")
        regexp = re.compile(rf"{pattern}")
        matched = re.match(regexp, str(string))

        if matched is None:
            return None
        self.cursor += len(matched.group(0))
        return matched.group(0)

    def advance(self):
        if not self.has_more_tokens():
            return None

        string = str(self.string)[self.cursor :]
        if type(self.string) is int:
            string = int(string)

        for pattern in keyword:
            token_value = self.match(pattern[0], string)

            if token_value is None:
                continue

            if pattern[1] is None:
                return self.advance()

            return {
                "type": pattern[1],
                "value": token_value,
            }

        raise SystemError(string[0])
