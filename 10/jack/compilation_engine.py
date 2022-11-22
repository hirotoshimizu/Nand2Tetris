from __future__ import annotations
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any

OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']


@dataclass
class CompilationEngine:
    token: list[dict[str, Any]]
    output: str = ""
    cur_token: int = 0
    next_token: int = 1
    len_token: int = field(init=False)
    indent: str = ''

    def __post_init__(self) -> None:
        self.len_token = len(self.token)

    def has_more_token(self) -> bool:
        return self.cur_token < self.len_token

    def parse(self) -> None:
        if self.token[self.cur_token].get('Value') == 'class':
            self.compile_class()

    def advance(self) -> None:
        self.cur_token += 1
        self.next_token += 1

    def eat(self, token_type: str) -> str:
        token = self.token[self.cur_token]['Value']

        if token is None:
            print("ERROR")
        
        if token != token_type:
            print('different token type')
            print(f'token, token_type {token}, {token_type}')

        self.advance()
        return token

    # class
    #   : 'class' class_name '{' class_var_dec* subroutine_dec* '}'
    #   ;
    def compile_class(self) -> None:
        self.eat("class")
        class_xml = self.xml = ET.Element('class')
        ET.SubElement(class_xml, 'keyword').text = 'class'

        if self.token[self.cur_token].get('Type') != 'IDENTIFIER':
            print('somethin went wront')

        class_name = self.token[self.cur_token].get('Value')
        ET.SubElement(class_xml, 'identifier').text = class_name

        self.advance()

        self.eat("{")
        ET.SubElement(class_xml, 'symbol').text = '{'

        while self.token[self.cur_token].get('Value') in ['static', 'field']:
            class_var_dec_xml = ET.SubElement(class_xml, 'classVarDec')
            self.compile_class_var_dec(class_var_dec_xml)

        while self.token[self.cur_token].get('Value') in ['constructor', 'function', 'method']:
            self.compile_subroutine()

        self.eat("}")
        ET.SubElement(class_xml, 'symbol').text = '}'

    # class_var_dec
    #   : ('static' | 'field') type var_name ( ','var_name) * ';'
    #   ;
    def compile_class_var_dec(self, xml: ET.Element) -> None:
        static_field = self.token[self.cur_token].get("Value")
        ET.SubElement(xml, 'keyword').text = static_field
        self.advance()

        self.compile_type(xml)
        self.advance()

        self.var_name_list(xml)

        self.eat(';')
        ET.SubElement(xml, 'symbol').text = ';'

    # subrouine_dec
    #   : ('constructor' | 'function' | 'method')  ('void' | type) subroutine_name '(' parameter_list ')' subroutine_body
    #   ;
    def compile_subroutine(self, tag: str = '') -> None:
        subroutine_dec_xml = ET.SubElement(self.xml, 'subroutineDec')

        subroutine = self.token[self.cur_token].get("Value")
        ET.SubElement(subroutine_dec_xml, 'keyword').text = subroutine
        self.advance()

        void_type = self.token[self.cur_token].get("Value")
        if void_type == 'void':
            ET.SubElement(subroutine_dec_xml, 'keyword').text = void_type
        else:
            self.compile_type(subroutine_dec_xml)

        self.advance()

        subroutine_name = self.token[self.cur_token].get("Value")
        ET.SubElement(subroutine_dec_xml, 'identifier').text = subroutine_name
        self.advance()

        self.eat('(')
        ET.SubElement(subroutine_dec_xml, 'symbol').text = '('
        self.compile_parameter_list(subroutine_dec_xml)

        self.eat(')')
        ET.SubElement(subroutine_dec_xml, 'symbol').text = ')'

        self.compile_subroutine_body(xml=subroutine_dec_xml)

    # type
    #   : 'int' | 'char' | 'boolean' | className
    #   ;
    def compile_type(self, xml: ET.Element) -> None:
        type_class_name = self.token[self.cur_token].get("Value")
        if type_class_name == 'int':
            ET.SubElement(xml, 'keyword').text = 'int'
        elif type_class_name == 'char':
            ET.SubElement(xml, 'keyword').text = 'char'
        elif type_class_name == 'boolean':
            ET.SubElement(xml, 'keyword').text = 'boolean'
        else:
            ET.SubElement(xml, 'identifier').text = type_class_name

    # parameter_list
    #   : ((type var_name) (',' type var_name)*)?
    #   ;
    def compile_parameter_list(self, xml: ET.Element) -> None:
        parameter_list_xml = ET.SubElement(xml, 'parameterList')
        while (self.token[self.cur_token].get("Value") != ')' and
               self.token[self.next_token].get("Type") == 'IDENTIFIER'):
            self.compile_type(parameter_list_xml)
            self.advance()

            self.compile_var_name(parameter_list_xml)

            if self.token[self.cur_token].get("Value") == ',':
                ET.SubElement(parameter_list_xml, 'symbol').text = ','
                self.eat(',')

    # subroutineBody
    #   : '{' varDec* statements '}'
    #   ;
    def compile_subroutine_body(self, xml: ET.Element) -> None:
        subroutine_body_xml = ET.SubElement(xml, 'subroutineBody')
        self.eat('{')
        ET.SubElement(subroutine_body_xml, 'symbol').text = '{'

        while self.token[self.cur_token].get('Value') == 'var':
            self.compile_var_dec(subroutine_body_xml)

        if (self.token[self.cur_token].get('Value') != 'var' and 
            self.token[self.cur_token].get('Value') != '}'):
            self.statements(subroutine_body_xml)

        self.eat('}')
        ET.SubElement(subroutine_body_xml, 'symbol').text = '}'

    # var_dec
    #    : 'var' type varName ( ',' varName)* ';'
    #    ;
    def compile_var_dec(self, xml: ET.Element) -> None:
        var_dec = ET.SubElement(xml, 'varDec')
        self.eat('var')
        ET.SubElement(var_dec, 'keyword').text = 'var'

        type = self.token[self.cur_token].get('Value')
        if type in ['int', 'char', 'boolean']:
            ET.SubElement(var_dec, 'keyword').text = type
        else:
            ET.SubElement(var_dec, 'identifier').text = type
        self.advance()

        self.var_name_list(var_dec)

        self.eat(';')
        ET.SubElement(var_dec, 'symbol').text = ';'

    # statements
    #    : statement*
    #    ;
    def statements(self, xml: ET.Element) -> None:
        statements_xml = ET.SubElement(xml, 'statements')
        while self.token[self.cur_token].get('Value') in ['let', 'if', 'while', 'do', 'return']:
            self.compile_statements(statements_xml)

    # statement
    #     : let_statement
    #     | if_statement
    #     | whileStatement
    #     | do_statement
    #     | return_statement
    #     ;
    def compile_statements(self, xml: ET.Element) -> None:
        if self.token[self.cur_token].get('Value') == 'let':
            self.compile_let(xml)
        elif self.token[self.cur_token].get('Value') == 'if':
            self.compile_if(xml)
        elif self.token[self.cur_token].get('Value') == 'while':
            self.compile_while(xml)
        elif self.token[self.cur_token].get('Value') == 'do':
            self.compile_do(xml)
        elif self.token[self.cur_token].get('Value') == 'return':
            self.compile_return(xml)

    # do_statement
    #    : 'do' subroutine_call ';'
    #    ;
    def compile_do(self, xml: ET.Element) -> None:
        do_xml = ET.SubElement(xml, 'doStatement')
        self.eat('do')
        ET.SubElement(do_xml, 'keyword').text = 'do'
        
        self.compile_subroutine_call(do_xml)
        
        self.eat(';')
        ET.SubElement(do_xml, 'symbol').text = ';'

    # let_statement
    #    : 'let' var_name ( '[' expression ']')? '=' expression ';'
    #    ;
    def compile_let(self, xml: ET.Element) -> None:
        let_xml = ET.SubElement(xml, 'letStatement')
        self.eat('let')
        ET.SubElement(let_xml, 'keyword').text = 'let'
        
        var_name = self.token[self.cur_token].get('Value')
        ET.SubElement(let_xml, 'identifier').text = var_name
        self.advance()

        if self.token[self.cur_token].get('Value') == '[':
            self.eat('[')
            ET.SubElement(let_xml, 'symbol').text = '['

            self.compile_expression(let_xml)

            self.eat(']')
            ET.SubElement(let_xml, 'symbol').text = ']'
        
        self.eat('=')
        ET.SubElement(let_xml, 'symbol').text = '='

        self.compile_expression(let_xml)

        self.eat(';')
        ET.SubElement(let_xml, 'symbol').text = ';'

    # while_statement
    #    : 'while'  '(' expression ')' '{' statements '}'
    #    ;
    def compile_while(self, xml: ET.Element) -> None:
        while_xml = ET.SubElement(xml, 'whileStatement')
        self.eat('while')
        ET.SubElement(while_xml, 'keyword').text = 'while'
        
        self.eat('(')
        ET.SubElement(while_xml, 'symbol').text = '('

        self.compile_expression(while_xml)

        self.eat(')')
        ET.SubElement(while_xml, 'symbol').text = ')'

        self.eat('{')
        ET.SubElement(while_xml, 'symbol').text = '{'

        self.statements(while_xml)

        self.eat('}')
        ET.SubElement(while_xml, 'symbol').text = '}'

    # return_statement
    #    : 'return' expression? ';'
    #    ;
    def compile_return(self, xml: ET.Element) -> None:
        return_xml = ET.SubElement(xml, 'returnStatement')
        self.eat('return')
        ET.SubElement(return_xml, 'keyword').text = 'return'

        if self.token[self.cur_token].get('Value') != ';':
            self.compile_expression(return_xml)

        self.eat(';')
        ET.SubElement(return_xml, 'symbol').text = ';'

    # if_statement
    #    : 'if' '(' expression ')'  '{' statements '}'
    #    : ( 'else' '{' statements '}')?
    #    ;
    def compile_if(self, xml: ET.Element) -> None:
        if_xml = ET.SubElement(xml, 'ifStatement')
        self.eat('if')
        ET.SubElement(if_xml, 'keyword').text = 'if'

        self.eat('(')
        ET.SubElement(if_xml, 'symbol').text = '('

        self.compile_expression(if_xml)

        self.eat(')')
        ET.SubElement(if_xml, 'symbol').text = ')'

        self.eat('{')
        ET.SubElement(if_xml, 'symbol').text = '{'

        self.statements(if_xml)

        self.eat('}')
        ET.SubElement(if_xml, 'symbol').text = '}'

        if self.token[self.cur_token].get('Value') == 'else':
            self.eat('else')
            ET.SubElement(if_xml, 'keyword').text = 'else'

            self.eat('{')
            ET.SubElement(if_xml, 'symbol').text = '{'

            self.statements(if_xml)

            self.eat('}')
            ET.SubElement(if_xml, 'symbol').text = '}'

    # expression
    #    : term (op term)*
    #    ;
    def compile_expression(self, xml: ET.Element) -> None:
        expression_xml = ET.SubElement(xml, 'expression')
        self.compile_term(expression_xml)
        if self.token[self.cur_token].get('Value') in OP:
            ET.SubElement(expression_xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.advance()
            self.compile_term(expression_xml)

    # term
    #    : integer_constant
    #    | string_constant
    #    | keyword_constant
    #    | var_name
    #    | var_name '[' expression ']'
    #    | subroutine_calil
    #    | '(' expression ')'
    #    | unary_op term
    #    ;
    def compile_term(self, xml: ET.Element) -> None:
        term_xml = ET.SubElement(xml, 'term')
        if (self.token[self.cur_token].get('Type') == 'IDENTIFIER' and 
           self.token[self.next_token].get('Value') == '.'):
            self.compile_subroutine_call(term_xml)
        elif self.token[self.cur_token].get('Type') == 'INT':
            self.compile_integer_constant(term_xml)
        elif self.token[self.cur_token].get('Type') == 'STRING_CONSTANT':
            self.compile_string_constant(term_xml)
        elif self.token[self.cur_token].get('Type') == 'KEYWORD':
            self.compile_keyword_constant(term_xml)
        elif self.token[self.cur_token].get('Value') == '(':
            self.eat('(')
            ET.SubElement(term_xml, 'symbol').text = '('

            self.compile_expression(term_xml)
            
            self.eat(')')
            ET.SubElement(term_xml, 'symbol').text = ')'
        elif (self.token[self.cur_token].get('Type') == 'IDENTIFIER' and
              self.token[self.next_token].get('Value') == '['):
            self.compile_var_name(term_xml)

            self.eat('[')
            ET.SubElement(term_xml, 'symbol').text = '['

            self.compile_expression(term_xml)

            ET.SubElement(term_xml, 'symbol').text = ']'
            self.eat(']')

        elif self.token[self.cur_token].get('Type') == 'IDENTIFIER':
            self.compile_var_name(term_xml)
        elif self.token[self.cur_token].get('Value') == '-' or '~':
            ET.SubElement(term_xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.advance()
            self.compile_term(term_xml)
        else:
            print(f'elseeeeee {self.token[self.cur_token]}')

    # integerConstant
    #    : Decimal 0 ～ 32767
    #    ;
    def compile_integer_constant(self, xml: ET.Element) -> None:
        ET.SubElement(xml, 'integerConstant').text = self.token[self.cur_token].get('Value')
        self.advance()

    # stringConstant
    #    : " unicord no new line "
    #    ;
    def compile_string_constant(self, xml: ET.Element) -> None:
        ET.SubElement(xml, 'stringConstant').text = self.token[self.cur_token].get('Value')[1:-1]
        self.advance()

    # keywordConstant
    #    : keyword
    #    ;
    def compile_keyword_constant(self, xml: ET.Element) -> None:
        ET.SubElement(xml, 'keyword').text = self.token[self.cur_token].get('Value')
        self.advance()

    # varNmae
    #    : varNmae
    #    | Identifier
    #    ;
    def compile_var_name(self, xml: ET.Element) -> None:
        self.compile_identifier(xml)
            
    # Identifier
    #    : varNmae
    #    ;
    def compile_identifier(self, xml: ET.Element) -> None:
        if self.token[self.cur_token].get('Type') == 'IDENTIFIER':
            ET.SubElement(xml, 'identifier').text = self.token[self.cur_token].get('Value')
            self.advance()
        else:
            print('something went wrong.')

    # subroutine_call
    #    : subroutine_name '(' expression_list ')'
    #    | (className | varName)  '.' subroutin_name '(' expression_list ')'
    #    ;
    def compile_subroutine_call(self, xml: ET.Element) -> None:
        ET.SubElement(xml, 'identifier').text = self.token[self.cur_token].get('Value')
        self.advance()

        if self.token[self.cur_token].get('Value') == '(':
            ET.SubElement(xml, 'symbol').text = '('
            self.eat('(')

            self.compile_expression_list(xml)

            ET.SubElement(xml, 'symbol').text = ')'
            self.eat(')')
        else:
            ET.SubElement(xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.eat('.')

            ET.SubElement(xml, 'identifier').text = self.token[self.cur_token].get('Value')
            self.advance()
        
            ET.SubElement(xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.eat('(')

            self.compile_expression_list(xml)
            
            ET.SubElement(xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.eat(')')

    # expression_list
    #    : (expression (',' expression)* )?
    #    ;
    def compile_expression_list(self, xml: ET.Element) -> None:
        expressionList_xml = ET.SubElement(xml, 'expressionList')

        if self.token[self.next_token].get("Value") == ')':
            self.compile_expression(expressionList_xml)

        while self.token[self.cur_token].get("Value") != ')':
            self.compile_expression(expressionList_xml)
            if self.token[self.cur_token].get("Value") != ')':
                self.eat(',')
                ET.SubElement(expressionList_xml, 'symbol').text = ','

    # var_name_list
    #    : (var_name (',' var_name)* )?
    #    ;
    def var_name_list(self, xml: ET.Element, var_name: list[str] | None = None) -> CompilationEngine | None:
        if var_name is None:
            var_name = []
        # if self.token[self.cur_token].get('Type') != 'IDENTIFIER':
            # pass
        var_name.append(self.token[self.cur_token].get("Value"))
        self.advance()
        if self.token[self.cur_token].get('Value') == ',':
            self.advance()
            return self.var_name_list(xml, var_name)

        for i, val in enumerate(var_name):
            ET.SubElement(xml, 'identifier').text = val
            if len(var_name) - 1 != i:
                ET.SubElement(xml, 'symbol').text = ','
