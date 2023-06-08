import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# from .compilation_engine import CompilationEngine

patterns = {
    # Whitespace:
    "^\s+": "SKIP",
    # Skip single-line comment:
    "^\/\/.*": "SKIP",
    # Skip multi-line comment:
    "^\/\*[\s\S]*?\*\/": "SKIP",
    # Symbols: delimiter:
    "^;": "SYMBOL",
    "^~": "SYMBOL",
    "^\{": "SYMBOL",
    "^\}": "SYMBOL",
    "^\[": "SYMBOL",
    "^\]": "SYMBOL",
    "^\(": "SYMBOL",
    "^\)": "SYMBOL",
    "^,": "SYMBOL",
    "^\.": "SYMBOL",
    # Assignment operators: =, *=, /=, +=, -,
    "^=": "SYMBOL",
    "/^[\*\/\+\-]=/": "SYMBOL",
    # Math operators: +, -, *,/
    "^[+\-]": "SYMBOL",
    "^[*\/]": "SYMBOL",
    # Relational operators: >,<
    "^[><]": "SYMBOL",
    # Logical operators: &&: |
    "^&": "SYMBOL",
    "^\|": "SYMBOL",
    "/^!/": "SYMBOL",
    # Keyword:
    "^let": "KEYWORD",
    "^var": "KEYWORD",
    "^boolean": "KEYWORD",
    "^int": "KEYWORD",
    "^char": "KEYWORD",
    "^if": "KEYWORD",
    "^else": "KEYWORD",
    "^do": "KEYWORD",
    "^true": "KEYWORD",
    "^false": "KEYWORD",
    "^null": "KEYWORD",
    "^while": "KEYWORD",
    "^function": "KEYWORD",
    "^constructor": "KEYWORD",
    "^method": "KEYWORD",
    "^return": "KEYWORD",
    "^static": "KEYWORD",
    "^field": "KEYWORD",
    "^void": "KEYWORD",
    "^type": "KEYWORD",
    "^class": "KEYWORD",
    "^this": "KEYWORD",
    # int
    "^[0-9]+": "INT_CONSTANT",
    # Identifier:
    "^\w+": "IDENTIFIER",
    # string:
    "^[a-zA-Z]+": "IDENTIFIER",
    # '^"[\w\W\s][^"]*"': "STRING_CONSTANT",
    '^"[\w\s][^"]*"': "STRING_CONSTANT",
}


@dataclass
class JackTokenizer:
    string: Any
    cursor: int = 0
    output: list[dict[str, Any]] = field(default_factory=list)

    def set_string(self, string: str) -> None:
        self.string = string

    def has_more_token(self) -> bool:
        return self.cursor < len(str(self.string))

    def match(self, pattern: str, string: Any) -> tuple[None, None] | tuple[str, str]:
        regexp = re.compile(rf"{pattern}")
        matched = re.match(regexp, str(string))

        if matched is None:
            return None, None

        matched_string = matched.group(0)
        self.cursor += len(matched_string)

        if matched_string == " ":
            self.advance()

        return patterns[pattern], matched_string

    def advance(self):
        if not self.has_more_token():
            return None

        string = str(self.string)[self.cursor :]
        if type(self.string) is int:
            string = int(string)

        # for key, value in patterns.items():
        for key in patterns.keys():
            matched_string, token_type = self.match(key, string)

            if token_type is None or not token_type:
                continue

            return self.token_type(matched_string, token_type)
            # return dict(type=matched_string, value=token_type)

    # def token_type(self, token_type: str, matched_string: str) -> None:
    def token_type(self, token_type: str, string: str) -> None:
        if token_type == "KEYWORD":
            self.keyword(string)
        elif token_type == "SYMBOL":
            self.symbol(string)
        elif token_type == "IDENTIFIER":
            self.identifier(string)
        elif token_type == "INT_CONSTANT":
            self.int_val(string)
        elif token_type == "STRING_CONSTANT":
            self.string_val(string)
        elif token_type == "SKIP":
            self.advance()

    def keyword(self, matched_string: str) -> None:
        self.output.append({"Type": "KEYWORD", "Value": matched_string})
        self.advance()

    def symbol(self, matched_string: str) -> None:
        self.output.append({"Type": "SYMBOL", "Value": matched_string})
        self.advance()

    def identifier(self, matched_string: str) -> None:
        self.output.append({"Type": "IDENTIFIER", "Value": matched_string})
        self.advance()

    def int_val(self, matched_string: str) -> None:
        self.output.append({"Type": "INT", "Value": matched_string})
        self.advance()

    def string_val(self, matched_string: str) -> None:
        if matched_string.startswith('"'):
            self.output.append({"Type": "STRING_CONSTANT", "Value": matched_string})
        else:
            self.output.append({"Type": "STRING", "Value": matched_string})
        self.advance()
