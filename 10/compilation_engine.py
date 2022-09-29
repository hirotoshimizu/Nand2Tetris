from dataclasses import dataclass
from typing import Any

from jack.jack_tokenizer import JackTokenizer


@dataclass
class SyntaxError(Exception):
    tokenType: str


@dataclass
class CompilationEngine:
    string = ""
    tokenizer = JackTokenizer()
    new_line_char = "\n"

    def list_to_string(self, list: list[str]) -> str:
        return "\n".join(list)

    def parse(self, string: Any) -> str:
        self.string = string
        self.tokenizer.init(string)
        self.lookahead = self.tokenizer.advance()
        return self.program()

    def eat(self, tokenType: str) -> str:
        token = self.lookahead

        if token is None:
            print(f"Unexpected end of input, expected: {token}")
            raise SyntaxError(tokenType)

        if token["type"] != tokenType:
            print(f"Unexpected token: {token}, expected: {tokenType}")
            raise SyntaxError(tokenType)

        self.lookahead = self.tokenizer.advance()

        return token

    # program
    #    : literal
    #    ;
    def program(self) -> str:
        return f"<class>\n" f"{self.class_dec()}\n" f"</class>"

    # class
    #   : 'class' class_name '{' class_var_dec* subroutine_dec* '}'
    #   ;
    def class_dec(self) -> str:
        self.eat("class")
        class_name = self.class_name()
        self.eat("{")
        class_var_dec = self.list_to_string(self.class_var_decs())
        subroutine_dec = self.list_to_string(self.subroutine_decs())
        self.eat("}")
        return (
            f"<keyword> class </keyword>\n"
            f"{class_name}\n"
            f"<symbol> {{ </symbol>\n"
            f"{class_var_dec}\n"
            f"{subroutine_dec}\n"
            f"<symbol> }} </symbol>"
        )

    def class_var_decs(self) -> list[str]:
        class_var_decs = [self.class_var_dec()]
        while self.lookahead["type"] == "static" or self.lookahead["type"] == "field":
            class_var_decs.append(self.class_var_dec())
        return class_var_decs

    def subroutine_decs(self) -> list[str]:
        subroutine_decs = [self.subroutine_dec()]
        while (
            self.lookahead["type"] == "constructor"
            or self.lookahead["type"] == "function"
            or self.lookahead["type"] == "method"
        ):
            subroutine_decs.append(self.subroutine_dec())
        return subroutine_decs

    # class_var_dec
    #   : ('static' | 'field') type var_name ( ','var_name) * ';'
    #   ;
    def class_var_dec(self) -> str:
        if self.lookahead["type"] == "static":
            pre = self.eat("static")
        elif self.lookahead["type"] == "field":
            pre = self.eat("field")
        type = self.type()
        var_name = self.list_to_string(self.var_names())
        self.eat(";")
        return (
            f"<classVarDec>\n"
            f"<keyword> {pre['value']} </keyword>\n"
            f"{type}\n"
            f"{var_name}\n"
            f"<symbol> ; </symbol>\n"
            f"</classVarDec>"
        )

    def var_names(self) -> list[str]:
        var_name_list = [self.var_name()]
        while self.lookahead["type"] == "," and self.eat(","):
            var_name_list.append("<symbol> , </symbol>")
            var_name_list.append(f"{self.var_name()}")
        return var_name_list

    # subrouine_dec
    #   : ('constructor' | 'function' | 'method')  ('void' | type) subroutine_name '(' parameter_list ')' subroutine_body
    #   ;
    def subroutine_dec(self) -> str:
        if (
            self.lookahead["type"] == "constructor"
            or self.lookahead["type"] == "function"
            or self.lookahead["type"] == "method"
        ):
            token = self.eat(self.lookahead["type"])
            declaration = f"<keyword> {token['value']} </keyword>"

        if self.lookahead["type"] == "void":
            token = self.eat(self.lookahead["type"])
            type = f"<keyword> {token['value']} </keyword>"
        else:
            type = self.type()

        subroutine_name = self.subroutine_name()
        self.eat("(")
        parameter_list = self.parameter_list()
        if parameter_list:
            parameter_list = self.list_to_string(parameter_list)
        self.eat(")")

        subroutine_body = self.subroutine_body()

        return (
            f"<subroutineDec>\n"
            f"{declaration}\n"
            f"{type}\n"
            f"{subroutine_name}\n"
            f"<symbol> ( </symbol>\n"
            f"{parameter_list if parameter_list else ''}"
            f"{self.new_line_char if parameter_list else ''}"
            f"<symbol> ) </symbol>\n"
            f"{subroutine_body}"
            f"</subroutineDec>"
        )

    # parameter_list
    #   : ((type var_name) (',' type var_name)*)?
    #   ;
    def parameter_list(self) -> list[str]:
        if self.lookahead["value"] == ")":
            return None

        parameter_list = [self.type(), self.var_name()]

        while self.lookahead["type"] == "," and self.eat(","):
            parameter_list.append("<symbol> , </symbol>")
            parameter_list.append(self.type())
            parameter_list.append(self.var_name())
        return parameter_list

    # subroutine_body
    #    : '{' varDec* statements '}'
    #    ;
    def subroutine_body(self) -> str:
        var_decs = []
        self.eat("{")
        while self.lookahead["type"] == "var":
            var_decs.append(self.var_dec())
        statements = self.list_to_string(self.statements("}"))
        self.eat("}")
        var_decs = self.list_to_string(var_decs)
        if var_decs:
            return (
                f"<symbol> {{ </symbol>\n"
                f"{var_decs}\n"
                f"{statements if statements else ''}"
                f"{self.new_line_char if statements else ''}"
                f"<symbol> }} </symbol>"
            )
        return f"<symbol> {{ </symbol>\n{statements}\n<symbol> }} </symbol>"

    # var_dec
    #    : 'var' type varName ( ',' varName)* ';'
    #    ;
    def var_dec(self) -> str:
        self.eat("var")
        type = self.type()
        var_name = self.list_to_string(self.var_name_list())
        self.eat(";")
        return (
            f"<keyword> var </keyword>\n"
            f"{type}\n"
            f"{var_name}\n"
            f"<symbol> ; </symbol>"
        )

    def var_name_list(self) -> list["str"]:
        var_name_list = [self.var_name()]
        while self.lookahead["type"] == "," and self.eat(","):
            var_name_list.append("<symbol> , </symbol>")
            var_name_list.append(self.var_name())
        return var_name_list

    # statements
    #    : statement
    #    | statements statement
    #    ;
    def statements(self, stop_lookahead: str = None) -> list[str]:
        statements = [self.statement()]
        while self.lookahead is not None and self.lookahead["type"] != stop_lookahead:
            statements.append(self.statement())
        return statements

    # statement
    #     : let_statement
    #     | if_statement
    #     | whileStatement
    #     | do_statement
    #     | return_statement
    #     ;
    def statement(self) -> list[str]:
        if self.lookahead["type"] == "let":
            return self.let_statement()
        elif self.lookahead["type"] == "if":
            return self.if_statement()
        elif self.lookahead["type"] == "while":
            return self.while_statement()
        elif self.lookahead["type"] == "do":
            return self.do_statement()
        elif self.lookahead["type"] == "return":
            return self.return_statement()
        else:
            return None

    # while_statement
    #    : 'while'  '(' expression ')' '{' statements '}'
    #    ;
    def while_statement(self) -> str:
        self.eat("while")
        self.eat("(")
        expression = self.expression()
        self.eat(")")
        self.eat("{")
        statements = self.list_to_string(self.statements("}"))
        self.eat("}")
        return (
            f"<keyword> while </keyword>\n"
            f"<symbol> ( </symbol>\n"
            f"{expression}\n"
            f"<symbol> ) </symbol>\n"
            f"<symbol> {{ </symbol>\n"
            f"{statements}\n"
            f"<symbol> }} </symbol>"
        )

    # do_statement
    #    : 'do' subroutine_call ';'
    #    ;
    def do_statement(self) -> str:
        self.eat("do")
        subroutine_call = self.subroutine_call()
        self.eat(";")
        return f"<keyword> do </keyword>\n{subroutine_call}\n<symbol> ; </symbol>"

    # subroutine_call
    #    : subroutine_name '(' expression_list ')'
    #    | (className | varName)  '.' subroutin_name '(' expression_list ')'
    #    ;
    def subroutine_call(self, name: str | None = None) -> str:
        if name is None:
            name = self.subroutine_name()
        if self.lookahead["type"] == ".":
            self.eat(".")
            subroutine_name = self.subroutine_name()
            self.eat("(")
            expression_list = self.is_end_of_expression()
            self.eat(")")
            return (
                f"{name}\n"
                f"<symbol> . </symbol>\n"
                f"{subroutine_name}\n"
                f"<symbol> ( </symbol>\n"
                f"{expression_list if expression_list else ''}"
                f"{self.new_line_char if expression_list  else ''}"
                f"<symbol> ) </symbol>"
            )
        self.eat("(")
        expression_list = self.is_end_of_expression()
        self.eat(")")
        return (
            f"{name}\n"
            f"<symbol> ( </symbol>\n"
            f"{expression_list if expression_list else ''}"
            f"{self.new_line_char if expression_list  else ''}"
            f"<symbol> ) </symbol>"
        )

    def is_end_of_expression(self) -> str:
        if self.lookahead["type"] != ")":
            expression_list = self.expression_list()
            return self.list_to_string(expression_list)
        return None

    # expression_list
    #    : (expression (',' expression)* )?
    #    ;
    def expression_list(self) -> list[str]:
        expression = [self.expression()]
        while self.lookahead["type"] == "," and self.eat(","):
            expression.append("<symbol> , </symbol>")
            expression.append(self.expression())
        return expression

    # return_statement
    #    : 'return' expression? ';'
    #    ;
    def return_statement(self) -> str:
        self.eat("return")
        expression = self.expression()
        self.eat(";")
        if expression:
            return f"<keyword> return </keyword>\n{expression}\n<symbol> ; </symbol>"
        return """<returnStatement>
<keyword> return </keyword>
<symbol> ; </symbol>
</returnStatement>"""

    # if_statement
    #    : 'if' '(' expression ')'  '{' statements '}'
    #    : ( 'else' '{' statements '}')?
    #    ;
    def if_statement(self) -> str:
        self.eat("if")
        self.eat("(")
        expression = self.expression()
        self.eat(")")
        self.eat("{")
        statements = self.statements("}")
        if statements[0] is not None:
            statements = self.list_to_string(statements)
        else:
            statements = ""
        self.eat("}")
        if self.lookahead != None and self.lookahead["type"] == "else":
            self.eat("else")
            self.eat("{")
            else_statements = self.statements("}")
            if else_statements[0]:
                else_statements = self.list_to_string(else_statements)
            else:
                else_statements = ""
            self.eat("}")
            return (
                f"<keyword> if </keyword>\n"
                f"<symbol> ( </symbol>\n"
                f"{expression}\n"
                f"<symbol> ) </symbol>\n"
                f"<symbol> {{ </symbol>\n"
                f"{statements if statements else ''}"
                f"{self.new_line_char if statements else ''}"
                f"<symbol> }} </symbol>\n"
                f"<keyword> else </keyword>\n"
                f"<symbol> {{ </symbol>\n"
                f"{else_statements if else_statements else ''}"
                f"{self.new_line_char if else_statements else ''}"
                f"<symbol> }} </symbol>"
            )

        return (
            f"<keyword> if </keyword>\n"
            f"<symbol> ( </symbol>\n"
            f"{expression}\n"
            f"<symbol> ) </symbol>\n"
            f"<symbol> {{ </symbol>\n"
            f"{statements}\n"
            f"<symbol> }} </symbol>"
        )

    # let_statement
    #    : 'let' var_name ( '[' expression ']')? '=' expression ';'
    #    ;
    def let_statement(self) -> str:
        self.eat("let")
        var_name = self.var_name()
        lhs_expression = ""
        if self.lookahead["value"] == "[":
            self.eat("[")
            lhs_expression = self.expression()
            self.eat("]")
            lhs_expression = (
                f"<symbol> [ </symbol>\n"
                f"{lhs_expression}\n"
                f"<symbol> ] </symbol>\n"
            )

        self.eat("SIMPLE_ASSIGN")
        expression = self.expression()
        self.eat(";")
        return (
            f"<keyword> let </keyword>\n"
            f"{var_name}\n"
            f"{lhs_expression  if lhs_expression else ''}"
            f"<symbol> = </symbol>\n"
            f"{expression}\n"
            f"<symbol> ; </symbol>"
        )

    # expression
    #     : term (op term)*
    #     ;
    def expression(self) -> str | None:
        term = self.term()

        if (
            self.lookahead["type"] == "ADDITIVE_OPERATOR"
            or self.lookahead["type"] == "MULTIPLICATIVE_OPERATOR"
            or self.lookahead["type"] == "LOGICAL_AND"
            or self.lookahead["type"] == "LOGICAL_OR"
            or self.lookahead["type"] == "RELATIONAL_OPERATOR"
            or self.lookahead["type"] == "SIMPLE_ASSIGN"
        ):
            if term:
                op_term = [term]
            op_term.append(self.list_to_string(self.term_list()))
            op_term = self.list_to_string(op_term)

            return op_term
        return term

    def term_list(self):
        term_list = [self.op()]
        term_list.append(self.expression())
        return term_list

    # op
    #    : '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    #    ;
    def op(self) -> str:
        op = self.lookahead["type"]
        token = self.eat(op)
        if token["value"] == "<":
            token = "&lt;"
        elif token["value"] == ">":
            token = "&gt;"
        elif token["value"] == "&":
            token = "&amp;"
        else:
            token = token["value"]

        return f"<symbol> {token} </symbol>"

    # term
    #    : integer_constant
    #    | string_constant
    #    | keyword_constant
    #    | var_name
    #    | var_name '[' expression ']'
    #    | subroutine_call
    #    | '(' expression ')'
    #    | unary_op term
    #    ;
    def term(self) -> str | None:
        if self.lookahead["type"] == "int":
            return self.integer_constant()
        elif self.lookahead["type"] == "char":
            return self.string_constant()
        elif (
            self.lookahead["type"] == "true"
            or self.lookahead["type"] == "false"
            or self.lookahead["type"] == "null"
            or self.lookahead["type"] == "this"
        ):
            return self.keyword_constant()
        elif self.lookahead["type"] == "let":
            return self.var_name()
        elif self.lookahead["type"] == "IDENTIFIER":
            name = self.subroutine_name()
            if self.lookahead["value"] == ".":
                return self.subroutine_call(name)
            elif self.lookahead["value"] == "[":
                self.eat("[")
                expression = self.expression()
                self.eat("]")
                return (
                    f"{name}\n<symbol> [ </symbol>\n{expression}\n<symbol> ] </symbol>"
                )
            else:
                return f"{name}"
        elif self.lookahead["type"] == "(":
            self.eat("(")
            expression = self.expression()
            self.eat(")")
            return f"<symbol> ( </symbol>\n{expression}\n<symbol> ) </symbol>"
        elif self.lookahead["value"] == "-" or self.lookahead["value"] == "~":
            unary = self.unary_op()
            term = self.term()
            return f"{unary}\n{term}"
        else:
            return None

    # unary_op
    #    : '-' | '~'
    #    ;
    def unary_op(self) -> str:
        token = self.eat(self.lookahead["type"])
        return f"<symbol> {token['value']} </symbol>"

    # keyword_constant
    #    : 'true' | 'false' | 'null' | 'this'
    #    ;
    def keyword_constant(self) -> str:
        token = self.eat(self.lookahead["type"])
        return f"<keyword> {token['value']} </keyword>"

    # integer_constant
    #    : int
    #    ;
    def integer_constant(self) -> str:
        token = self.eat("int")
        return f"<integerConstant> {token['value']} </integerConstant>"

    # string_constant
    #    : char
    #    ;
    def string_constant(self) -> str:
        token = self.eat("char")
        if not token["value"].startswith('"'):
            return f"<stringConstant> {token['value']} </stringConstant>"
        return f"<stringConstant> {token['value'][1: -1]} </stringConstant>"

    # type
    #    : int
    #    | char
    #    | boolean
    #    | class_name
    #    ;
    def type(self) -> str:
        if (
            self.lookahead["type"] == "int"
            or self.lookahead["type"] == "char"
            or self.lookahead["type"] == "boolean"
        ):
            token = self.eat(self.lookahead["type"])
            return f"<keyword> {token['value']} </keyword>"
        return self.class_name()

    # class_name
    #    : Identifier
    #    ;
    def class_name(self) -> str:
        return self.identifier()

    # subroutine_name
    #    : Identifier
    #    ;
    def subroutine_name(self) -> str:
        return self.identifier()

    # var_name
    #    : Identifier
    #    ;
    def var_name(self) -> str:
        return self.identifier()

    # identifier
    #    : アルファベット、数字、アンダースコアの文字列。ただし数字から始まる文字列は除く
    #    ;
    def identifier(self) -> str:
        token = self.eat("IDENTIFIER")
        return f"<identifier> {token['value']} </identifier>"
