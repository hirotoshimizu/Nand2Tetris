from dataclasses import dataclass, field
from enum import Enum


class Kind(Enum):
    STATIC = "static"
    FIELD = "field"
    ARG = "arg"
    VAR = "var"


@dataclass
class SymbolTable:
    class_table: list[dict[str, str]] = field(default_factory=list)
    subroutine_table: list[dict[str, str]] = field(default_factory=list)

    def start_class(self):
        self.class_table = []

    def start_subroutine(self) -> None:
        self.subroutine_table = []

    def find_last_element(self, table: list[dict[str, str]], kind: str) -> int:
        if not table:
            return 0
        last_element = table[-1]
        if kind == last_element["kind"]:
            return int(last_element["index"]) + 1
        return 0

    def find_table(self, kind: str) -> list[dict[str, str]]:
        if kind == "static" or kind == "field":
            return self.class_table
        return self.subroutine_table

    def define(self, name: str, type: str, kind: str) -> None:
        # class scope
        table = self.find_table(kind)
        index = self.find_last_element(table, kind)
        table.append({"name": name, "type": type, "kind": kind, "index": index})

    def define_method(
        self, name: str, type: str, kind: str, class_name: str = ""
    ) -> None:
        table = self.find_table(kind)
        index = self.find_last_element(table, kind)
        if index == 0:
            table.append(
                {"name": "this", "type": class_name, "kind": "argument", "index": 0}
            )
            table.append({"name": name, "type": type, "kind": kind, "index": 1})
        else:
            table.append({"name": name, "type": type, "kind": kind, "index": index})

    def var_count(self, kind: str) -> int:
        table = self.find_table(kind)
        return len([i for i in table if i["kind"] == kind])

    def kind_of(self, name: str) -> str | None:
        subroutine_table = self.lookup_subroutine_table(name, "kind")
        if subroutine_table:
            return subroutine_table

        class_table = self.lookup_class_table(name, "kind")
        if class_table:
            return class_table

        return None

    def index_of(self, name: str):
        subroutine_table = self.lookup_subroutine_table(name, "index")
        if subroutine_table is not None:
            return subroutine_table

        class_table = self.lookup_class_table(name, "index")
        if class_table is not None:
            return class_table

        return None

    def lookup_subroutine_table(self, name: str, search: str):
        for i in self.subroutine_table:
            if i["name"] == name:
                return i[search]
        return None

    def lookup_class_table(self, name: str, search: str):
        for i in self.class_table:
            if i["name"] == name:
                return i[search]
        return None
