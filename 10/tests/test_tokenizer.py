from jack.jack_tokenizer import JackTokenizer

input = '''if (x < 153)
{let city="Paris";}
'''

tokenizer = JackTokenizer(input)
tokenizer.advance()
token = tokenizer.output


expected = [
{'Type': 'KEYWORD', 'Value': 'if'},
{'Type': 'SYMBOL', 'Value': '('},
{'Type': 'IDENTIFIER', 'Value': 'x'},
{'Type': 'SYMBOL', 'Value': '<'},
{'Type': 'INT', 'Value': '153'},
{'Type': 'SYMBOL', 'Value': ')'},
{'Type': 'SYMBOL', 'Value': '{'},
{'Type': 'KEYWORD', 'Value': 'let'},
{'Type': 'IDENTIFIER', 'Value': 'city'},
{'Type': 'SYMBOL', 'Value': '='},
{'Type': 'STRING_CONSTANT', 'Value': '"Paris"'},
{'Type': 'SYMBOL', 'Value': ';'},
{'Type': 'SYMBOL', 'Value': '}'}
]

def test_if():
    assert(token==expected)
