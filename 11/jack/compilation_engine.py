from __future__ import annotations
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any
from jack.symbol_table import SymbolTable
from jack.vm_writer import VmWriter

OP = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

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


@dataclass
class CompilationEngine:
    token: list[dict[str, Any]]
    cur_token: int = 0
    next_token: int = 1
    len_token: int = field(init=False)
    return_num: int = 0
    class_name: str = ''
    subroutine_name: str = ''
    subroutine_nam: int = 0
    count: int = 0
    xml = ET.Element
    symbol_table = SymbolTable()
    vm_writer = VmWriter()

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
        self.vm_writer.start()
        self.symbol_table.start_class()
        self.eat("class")
        class_xml = self.xml = ET.Element('class')
        ET.SubElement(class_xml, 'keyword').text = 'class'

        if self.token[self.cur_token].get('Type') != 'IDENTIFIER':
            print('somethin went wront')

        class_name = self.class_name = self.token[self.cur_token].get('Value')
        ET.SubElement(class_xml, 'identifier').text = class_name

        self.advance()

        self.eat("{")
        ET.SubElement(class_xml, 'symbol').text = '{'

        while self.token[self.cur_token].get('Value') in ['static', 'field']:
            class_var_dec_xml = ET.SubElement(class_xml, 'classVarDec')
            self.compile_class_var_dec(class_var_dec_xml)

        while self.token[self.cur_token].get('Value') in ['constructor', 'function', 'method']:
            self.compile_subroutine(class_xml)

        self.eat("}")
        ET.SubElement(class_xml, 'symbol').text = '}'

        print(f'class_table{self.symbol_table.class_table}')
        print(f'subroutine_table{self.symbol_table.subroutine_table}')

    # class_var_dec
    #   : ('static' | 'field') type var_name ( ','var_name) * ';'
    #   ;
    def compile_class_var_dec(self, xml: ET.Element) -> None:
        static_field = self.token[self.cur_token].get("Value")
        ET.SubElement(xml, 'keyword').text = static_field
        self.advance()

        type = self.token[self.cur_token].get("Value")
        print(f'typeeee {type}')

        self.compile_type(xml)
        self.advance()

        # self.var_name_list(xml, static_field, type)
        self.var_name_list(xml, type, static_field)

        self.eat(';')
        ET.SubElement(xml, 'symbol').text = ';'

    # subrouine_dec
    #   : ('constructor' | 'function' | 'method')  ('void' | type) subroutine_name '(' parameter_list ')' subroutine_body
    #   ;
    def compile_subroutine(self, xml: ET.Element) -> None:
        self.subroutine_nam += 1
        subroutine_dec_xml = ET.SubElement(xml, 'subroutineDec')
        self.symbol_table.start_subroutine()

        subroutine_type = self.token[self.cur_token].get("Value")
        ET.SubElement(subroutine_dec_xml, 'keyword').text = subroutine_type
        self.advance()

        void_type = self.token[self.cur_token].get("Value")
        if void_type == 'void':
            ET.SubElement(subroutine_dec_xml, 'keyword').text = void_type
        else:
            self.compile_type(subroutine_dec_xml)

        self.advance()

        self.subroutine_name = self.token[self.cur_token].get("Value")
        ET.SubElement(subroutine_dec_xml, 'identifier').text = self.subroutine_name
        
        self.advance()

        self.eat('(')

        ET.SubElement(subroutine_dec_xml, 'symbol').text = '('
        # self.compile_parameter_list(subroutine_dec_xml)
        self.compile_parameter_list(subroutine_dec_xml, subroutine_type)

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
    def compile_parameter_list(self, xml: ET.Element, subroutine_type: str) -> None:
        parameter_list_xml = ET.SubElement(xml, 'parameterList')
        while (self.token[self.cur_token].get("Value") != ')' and
               self.token[self.next_token].get("Type") == 'IDENTIFIER'):
            type = self.token[self.cur_token].get("Value")
            self.compile_type(parameter_list_xml)
            self.advance()

            name = self.token[self.cur_token].get("Value")
            if subroutine_type == 'method':
                self.symbol_table.define_method(name, type, 'argument', self.class_name)
            else:
                self.symbol_table.define(name, type, 'argument')
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
        

        var_num = self.symbol_table.var_count('var')

        function_name = f'{self.class_name}.{self.subroutine_name}'
        self.vm_writer.write_function(function_name,var_num)

        # constructorの処理
        constructor_var_num = self.symbol_table.var_count('field')
        xmlstr = ET.tostring(self.xml, encoding='utf8', method='xml')
        root = ET.fromstring(xmlstr)
        location = f'./subroutineDec[{self.subroutine_nam}]/keyword'
        for i in root.findall(location):
            if i.text == 'constructor':
                self.vm_writer.write_push('constant', constructor_var_num)
                self.vm_writer.write_call('Memory.alloc', 1)
                self.vm_writer.write_pop('pointer', 0)

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

        print('^^^^^^^^^^^^^^')
        # self.var_name_list(var_dec)
        self.var_name_list(var_dec, type, 'var')

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
        # self.vm_writer.write_call()
        ET.SubElement(do_xml, 'keyword').text = 'do'
        
        self.compile_subroutine_call(do_xml)


        xmlstr = ET.tostring(self.xml, encoding='utf8', method='xml')
        root = ET.fromstring(xmlstr)
        location = f'.//subroutineDec[last()]/keyword'
        for i in root.findall(location):
            if i.text == 'void':
                self.vm_writer.write_pop('temp', 0)

        
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

        # self.compile_expression(let_xml)
        print('compile_expressionnnnnnnnnn_before')
        print(f'var_name {var_name}')
        print(self.symbol_table.class_table)
        print(self.symbol_table.subroutine_table)
        self.compile_expression(let_xml)
        print('let_expression_enddddddddddddddddd')

        # symboltable から変数探す
        kind_of = self.symbol_table.kind_of(var_name)
        index = self.symbol_table.index_of(var_name)
        if kind_of == 'var':
            kind_of = 'local'
        elif kind_of == 'field':
            kind_of = 'this'
        
        self.vm_writer.write_pop(kind_of, index)

        # self.vm_writer.write_pop()

        self.eat(';')
        ET.SubElement(let_xml, 'symbol').text = ';'

    # while_statement
    #    : 'while'  '(' expression ')' '{' statements '}'
    #    ;
    def compile_while(self, xml: ET.Element) -> None:
        self.count_increment()
        print('while startttttttttttttttttttttttttt')
        while_xml = ET.SubElement(xml, 'whileStatement')
        self.eat('while')
        ET.SubElement(while_xml, 'keyword').text = 'while'

        label_count = self.count
        self.vm_writer.write_lable(f'while_{label_count}')
        
        self.eat('(')
        ET.SubElement(while_xml, 'symbol').text = '('

        print(f'compile_expression$$$$ {self.token[self.cur_token].get("Value")}')
        self.compile_expression(while_xml)

        self.eat(')')
        ET.SubElement(while_xml, 'symbol').text = ')'

        # self.vm_writer.write_lable(f'while {self.count}')
        self.vm_writer.write_arithmatic('not')
        self.vm_writer.write_if(f'while_if_{label_count}')

        self.eat('{')
        ET.SubElement(while_xml, 'symbol').text = '{'

        self.statements(while_xml)

        self.eat('}')
        ET.SubElement(while_xml, 'symbol').text = '}'

        self.vm_writer.write_goto(f'while_{label_count}')
        self.vm_writer.write_lable(f'while_if_{label_count}')

    # return_statement
    #    : 'return' expression? ';'
    #    ;
    def compile_return(self, xml: ET.Element) -> None:
        return_xml = ET.SubElement(xml, 'returnStatement')
        self.return_num += 1
        
        xmlstr = ET.tostring(self.xml, encoding='utf8', method='xml')
        root = ET.fromstring(xmlstr)
        location = f'./subroutineDec[{self.subroutine_nam}]/keyword'
        for i in root.findall(location):
            print(f'iiiii {i.text}')
            if i.text == 'void':
                self.vm_writer.write_push('constant', 0)

        self.eat('return')
        # self.vm_writer.write_return()
        ET.SubElement(return_xml, 'keyword').text = 'return'

        print('returnnnnnnnn')

        if self.token[self.cur_token].get('Value') != ';':
            self.compile_expression(return_xml)
            # self.compile_expression()

        self.vm_writer.write_return()
        self.eat(';')
        ET.SubElement(return_xml, 'symbol').text = ';'

    def depth_iter(self, element, tag=None):
        print('*******************depth_iter************')
        stack = []
        stack.append(iter([element]))
        stack2 = []
        stack2.append(element)
        print(f'depth_iterrrrrrrrrrrrrrrrrr {stack}')
        print(f'stack2 {stack2}')
        while stack:
            e = next(stack[-1], None)
            print(e)
            if e == None:
                stack.pop()
                print(stack)
            else:
                stack.append(iter(e))
                if tag == None or e.tag == tag:
                    # yield (e, len(stack) - 1)
                    yield (e, len(stack) - 1)
        print(f'end_while {stack}')

    # tree = ET.ElementTree(etree.fromstring(rexml)) 
    maxdepth = 1
    def depth(self, elem, level): 
        # global maxdepth
        self.maxdepth
        if (level == self.maxdepth):
            self.maxdepth += 1
    # recursive call to function to get the depth
        for child in elem:
            self.depth(child, level + 1) 


    def count_increment(self):
        self.count += 1


    # if_statement
    #    : 'if' '(' expression ')'  '{' statements '}'
    #    : ( 'else' '{' statements '}')?
    #    ;
    def compile_if(self, xml: ET.Element) -> None:
        self.count_increment()
        label_count = self.count
        if_xml = ET.SubElement(xml, 'ifStatement')
        self.eat('if')
        ET.SubElement(if_xml, 'keyword').text = 'if'

        self.eat('(')
        ET.SubElement(if_xml, 'symbol').text = '('

        self.compile_expression(if_xml)

        self.eat(')')
        ET.SubElement(if_xml, 'symbol').text = ')'

        self.vm_writer.write_arithmatic('not')
        self.vm_writer.write_if(f'flag_{label_count}')

        self.eat('{')
        ET.SubElement(if_xml, 'symbol').text = '{'

        self.statements(if_xml)

        self.eat('}')
        ET.SubElement(if_xml, 'symbol').text = '}'

        if self.token[self.cur_token].get('Value') == 'else':
            self.eat('else')
            ET.SubElement(if_xml, 'keyword').text = 'else'
            self.vm_writer.write_goto(f'tag_{label_count}')
            self.vm_writer.write_lable(f'flag_{label_count}')

            self.eat('{')
            ET.SubElement(if_xml, 'symbol').text = '{'

            self.statements(if_xml)

            self.eat('}')
            ET.SubElement(if_xml, 'symbol').text = '}'
            self.vm_writer.write_lable(f'tag_{label_count}')
        
    
    
    def op_convert(self, op: str):
        if op == '+':
            self.vm_writer.write_arithmatic('add')
        elif op == '-':
            self.vm_writer.write_arithmatic('sub')
        elif op == '=':
            self.vm_writer.write_arithmatic('eq')
        elif op == '>':
            self.vm_writer.write_arithmatic('gt')
        elif op == '<':
            self.vm_writer.write_arithmatic('lt')
        elif op == '~':
            self.vm_writer.write_arithmatic('not')
        elif op == '&':
            self.vm_writer.write_arithmatic('and')
        elif op == '*':
            self.vm_writer.write_call('Math.multiply', 2)
    
    def find_symbol_location(self, str: str) -> int | None:
        if self.is_primary_expression(str):
            return self.find_symbol_location_inside_paren(str)
        return self.get_symbol_location(str)
    
    def is_function(self, str: str) -> bool:
        l_paren_location, _ = self.find_parentheses_location(str)
        function_name = str[:l_paren_location]
        if function_name.isalpha() and 1 <= l_paren_location:
            return True
        return False

    def call_function(self, str: str) -> None:
        print('call_function 一旦パス')
        pass
        # l_paren_location, r_paren_location = self.find_parentheses_location(str)
        # expressions = str[l_paren_location + 1: r_paren_location]
        # expressions = list(expressions.split(','))
        # function_name = str[:l_paren_location]
        # for i in expressions:
        #     self.write_arithmatic(i)
        # self.output += f'call {function_name}{NEW_LINE}'

    def is_primary_expression(self, str: str):
        l_paren_location, r_paren_location = self.find_parentheses_location(str)
        # l_paren_location could be 0
        if l_paren_location is not None and r_paren_location:
            return True
        return False
    
    def find_symbol_location_inside_paren(self, str: str) -> int | None:
        l_paren_location, r_paren_location = self.find_parentheses_location(str)

        # str starts '(' and end with ')'
        if len(str) == r_paren_location+1:
            return self.get_symbol_location(str)
        for i, value in enumerate(str):
            if value in list(symbols.values()) and not l_paren_location < i < r_paren_location:
                print(f'forrrrrrrr i {i}')
                return i

    def get_symbol_location(self, str: str) -> int | None:
        for i, value in enumerate(str):
            if value in list(symbols.values()):
                return i
        return None

    def find_parentheses_location(self, str: str) -> tuple[int, int]:
        l_paren_location = str.find('(')
        r_paren_location = str.find(')')
        return l_paren_location, r_paren_location
    
    def strip_paren(self, str: str) -> str:
        print(f'strip_paren_before*** {str}')
        if str.startswith('('):
            str = str[1:]
        
        if str.endswith(')'):
            str = str[:-1]
        
        print(f'strip_paren_after*** {str}')
        return str

    def convert_notation(self, command: str):
        symbol_location = self.find_symbol_location(command)
        print(f'commnadssss {command}')
        print(f'symbol@@@@@@ {symbol_location}')
        lhs = command[:symbol_location]
        op = command[symbol_location: symbol_location+1]
        rhs = command[symbol_location+1:]
        print(f'lhsssss {lhs}')
        print(f'rhsssss {rhs}')

        self.sprit_arithmatic(self.strip_paren(lhs))
        self.sprit_arithmatic(self.strip_paren(rhs))

        print(f'opppp!!!!!!!!!!!! {op}')
        self.op_convert(op)


    def is_variable(self, str: str) -> bool:
        for i in str:
            if i in list(symbols.values()):
                return False
        return True
    
    def unary_op(self, str: str) -> None:
        self.sprit_arithmatic(str[1:])
        if str[:1] == '-':
            self.vm_writer.write_arithmatic('neg')
        elif str[:1] == '~':
            self.vm_writer.write_arithmatic('not')
    
    def sprit_arithmatic(self, command: str) -> None:
        print(f'vmvmvmvmvm {command}')
        if command.isnumeric():
            self.vm_writer.write_push('constant', int(command))
        elif self.is_variable(command): 
            # self.output += f'push {command}{NEW_LINE}'
            kind_of = self.symbol_table.kind_of(command)
            if kind_of == 'var':
                kind_of = 'local'
            index_of = self.symbol_table.index_of(command)
            print(f'is_variableeeeee {command}')
            self.vm_writer.write_push(kind_of, index_of)
        elif command.startswith('-') or command.startswith('~'):
            self.unary_op(command)
        elif self.is_function(command):
            print(f'func!!! {command}')
            self.call_function(command)
        else:
            self.convert_notation(command)




    # expression
    #    : term (op term)*
    #    ;
    # def compile_expression(self, xml: ET.Element) -> None:
    #     expression_xml = ET.SubElement(xml, 'expression')
    #     self.compile_term(expression_xml)
    #     while self.token[self.cur_token].get('Value') in OP:
    #         ET.SubElement(expression_xml, 'symbol').text = self.token[self.cur_token].get('Value')
    #         self.vm_writer.write_arithmatic(self.token[self.cur_token].get('Value'))
    #         self.advance()
    #         self.compile_term(expression_xml)

    # def compile_expression(self) -> str:
    # def compile_expression(self, xml: ET.Element) -> Any:
    def compile_expression(self, xml: ET.Element, call_myself: bool = False) -> Any:
        expression_xml = ET.SubElement(xml, 'expression')
        print(f'self.token[self.cur_token].get("Value") {self.token[self.cur_token].get("Value")}')
        expression = self.compile_term_test(expression_xml)
        
        while self.token[self.cur_token].get('Value') in OP:
            expression += self.token[self.cur_token].get('Value')
            self.advance()
            expression += self.compile_term_test(expression_xml)
        print(f'expression!!! {expression}')
        if call_myself is not True and expression:
            self.sprit_arithmatic(expression)
            # self.convert_notation(expression)
        return expression

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


    def compile_term_test(self, xml: ET.Element, symbol:str = '') -> Any:
        term_xml = ET.SubElement(xml, 'term')
        if (self.token[self.cur_token].get('Type') == 'IDENTIFIER' and 
           self.token[self.next_token].get('Value') == '.'):
            # self.compile_subroutine_call(term_xml)
            return self.compile_subroutine_call(term_xml)
        if self.token[self.cur_token].get('Type') == 'INT':
            num = self.compile_integer_constant_test()
            # self.vm_writer.write_arithmatic(num)
            print(f'num************ {num}')
            return num
        # elif self.token[self.cur_token].get('Type') == 'STRING_CONSTANT':
        #     self.compile_string_constant(term_xml)
        elif self.token[self.cur_token].get('Type') == 'KEYWORD':
            print(f"aaaaaaaaaaaaa {self.token[self.cur_token].get('Value')}")
            self.compile_keyword_constant(term_xml)
        elif self.token[self.cur_token].get('Value') == '(':
            self.eat('(')
            ET.SubElement(term_xml, 'symbol').text = '('
            
            expression = self.compile_expression(term_xml, True)
            # expression = self.compile_expression(term_xml)

            print(f'&&&expression&&& {expression}')
            print(f"cur_token {self.token[self.cur_token].get('Value')}")
            print(f"next_token {self.token[self.next_token].get('Value')}")
            print(f'&&&expression&&&after {expression}')

            self.eat(')')
            ET.SubElement(term_xml, 'symbol').text = ')'
            return f'({expression})'
        # elif (self.token[self.cur_token].get('Type') == 'IDENTIFIER' and
        #       self.token[self.next_token].get('Value') == '['):
        #     self.compile_var_name(term_xml)

        #     self.eat('[')
        #     ET.SubElement(term_xml, 'symbol').text = '['

        #     self.compile_expression(term_xml)

        #     ET.SubElement(term_xml, 'symbol').text = ']'
        #     self.eat(']')

        elif self.token[self.cur_token].get('Type') == 'IDENTIFIER':
            print('identifierrr$$$$$')
            identifier = self.compile_var_name(term_xml)
            return identifier
        elif self.token[self.cur_token].get('Value') == '-' or '~':
            ET.SubElement(term_xml, 'symbol').text = self.token[self.cur_token].get('Value')
            # self.advance()
            # self.compile_term_test()
            print(f"bbbbbbbbbb {self.token[self.cur_token].get('Value')}")
            symbol = self.token[self.cur_token].get('Value')
            self.advance()
            # num = self.compile_integer_constant_test()
            # unary_op_num = f'{symbol}{num}'
            # self.vm_writer.write_arithmatic(unary_op_num)
            term = self.compile_term_test(term_xml)
            print(f'unarryyyyyyyyyyyy aiu {symbol}{term}')
            return f'{symbol}{term}'
        else:
            print(f'elseeeeee {self.token[self.cur_token]}')

    # integerConstant
    #    : Decimal 0 ～ 32767
    #    ;
    def compile_integer_constant(self, xml: ET.Element) -> None:
        ET.SubElement(xml, 'integerConstant').text = self.token[self.cur_token].get('Value')
        # self.vm_writer.write_push('constant', self.token[self.cur_token].get('Value'))
        print('@@@@@@@@@@@@@@@@@@@@@@@')
        print(self.vm_writer.output)
        self.advance()

    def compile_integer_constant_test(self) -> int | None:
        num = self.token[self.cur_token].get('Value')
        print(f'compile_integer_constant_test {num}')
        self.advance()
        return num

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
        print(f'keyword@@@@@@@@@@@@@@@@@@@@@@@@@{self.token[self.cur_token].get("Value")}')
        if self.token[self.cur_token].get("Value") == 'true':
            self.vm_writer.write_push('constant', 1)
            self.vm_writer.write_arithmatic('neg')
        elif self.token[self.cur_token].get("Value") == 'false':
            self.vm_writer.write_push('constant', 0)
        elif self.token[self.cur_token].get("Value") == 'this':
            self.vm_writer.write_push('pointer', 0)
        ET.SubElement(xml, 'keyword').text = self.token[self.cur_token].get('Value')
        self.advance()

    # varNmae
    #    : varNmae
    #    | Identifier
    #    ;
    # def compile_var_name(self, xml: ET.Element) -> None:
    #     self.compile_identifier(xml)
    def compile_var_name(self, xml: ET.Element) -> str | None:
        return self.compile_identifier(xml)
            
    # Identifier
    #    : varNmae
    #    ;
    # def compile_identifier(self, xml: ET.Element) -> None:
    #     if self.token[self.cur_token].get('Type') == 'IDENTIFIER':
    #         ET.SubElement(xml, 'identifier').text = self.token[self.cur_token].get('Value')
    #         self.advance()
    #     else:
    #         print('something went wrong.')
    def compile_identifier(self, xml: ET.Element) -> str | None:
        if self.token[self.cur_token].get('Type') == 'IDENTIFIER':
            var_name = self.token[self.cur_token].get('Value')
            ET.SubElement(xml, 'identifier').text = var_name
            self.advance()
            return var_name
        else:
            print('something went wrong.')

    # subroutine_call
    #    : subroutine_name '(' expression_list ')'
    #    | (className | varName)  '.' subroutin_name '(' expression_list ')'
    #    ;
    def compile_subroutine_call(self, xml: ET.Element) -> None:
        # ET.SubElement(xml, 'identifier').text = self.token[self.cur_token].get('Value')
        name = self.token[self.cur_token].get('Value')
        self.advance()

        print(f'hereeeeeeeeeeeeeeeee {self.token[self.cur_token].get("Value")}')

        if self.token[self.cur_token].get('Value') == '(':
            ET.SubElement(xml, 'symbol').text = '('
            self.eat('(')

            self.compile_expression_list(xml)

            ET.SubElement(xml, 'symbol').text = ')'
            self.eat(')')
        else:
            ET.SubElement(xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.eat('.')

            # ET.SubElement(xml, 'identifier').text = self.token[self.cur_token].get('Value')
            subroutine_name = self.token[self.cur_token].get('Value')
            print(f'!!!!!subroutine_name {subroutine_name}')
            call_name = f'{name}.{subroutine_name}'
            self.advance()
        
            ET.SubElement(xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.eat('(')
            
            expression_list = self.compile_expression_list(xml)
            print(f'expression_listtttlt {expression_list}')
            self.vm_writer.write_call(call_name, len(expression_list))
            
            ET.SubElement(xml, 'symbol').text = self.token[self.cur_token].get('Value')
            self.eat(')')

    # expression_list
    #    : (expression (',' expression)* )?
    #    ;
    def compile_expression_list(self, xml: ET.Element) -> list[str | None]:
        expressionList_xml = ET.SubElement(xml, 'expressionList')
        expression_list = []

        if self.token[self.next_token].get("Value") == ')':
            # self.compile_expression(expressionList_xml)
            expression = self.compile_expression(expressionList_xml)
            expression_list.append(expression)

        while self.token[self.cur_token].get("Value") != ')':
            expression = self.compile_expression(expressionList_xml)
            # self.vm_writer.write_arithmatic(self.compile_expression())
            # self.vm_writer.write_arithmatic(expression)
            expression_list.append(expression)
            if self.token[self.cur_token].get("Value") != ')':
                self.eat(',')
                ET.SubElement(expressionList_xml, 'symbol').text = ','
        return expression_list

    # var_name_list
    #    : (var_name (',' var_name)* )?
    #    ;
    # def var_name_list(self, xml: ET.Element, var_name: list[str] | None = None) -> CompilationEngine | None:
    def var_name_list(self, xml: ET.Element, type: str, kind: str, name_list: list[str] | None = None) -> CompilationEngine | None:
        if name_list is None:
            name_list = []
        # if self.token[self.cur_token].get('Type') != 'IDENTIFIER':
            # pass
        var_name = self.token[self.cur_token].get("Value")
        print(f'kinddd {kind}')
        self.symbol_table.define(var_name, type, kind)
        print(f'*****self.symbol_table.class_table {self.symbol_table.class_table}')
        print(f'*****self.symbol_table.subroutine_table {self.symbol_table.subroutine_table}')
        name_list.append(var_name)
        self.advance()
        if self.token[self.cur_token].get('Value') == ',':
            self.advance()
            return self.var_name_list(xml, type, kind, name_list)

        for i, val in enumerate(name_list):
            ET.SubElement(xml, 'identifier').text = val
            if len(name_list) - 1 != i:
                ET.SubElement(xml, 'symbol').text = ','
