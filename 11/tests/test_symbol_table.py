from jack.compilation_engine import CompilationEngine
from jack.jack_analyzer import create_xml_file
from jack.jack_tokenizer import JackTokenizer


def test_class_subroutine_empty() -> None:

    input = '''class Main {
   function void main() {
      do Output.printInt(1 + 6);
      return;
   }
   }
    '''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    assert compiler.symbol_table.class_table == []
    assert compiler.symbol_table.subroutine_table == []


def test_constructor() -> None:

    input = '''class Ball {
    field int x, y;
    field int lengthx, lengthy;

    constructor Ball new(int Ax, int Ay,
                         int AleftWall, int ArightWall, int AtopWall, int AbottomWall) {    	
	    let x = Ax;		
	    let y = Ay;
	    let leftWall = AleftWall;
	    let rightWall = ArightWall - 6;
	    let topWall = AtopWall; 
	    let bottomWall = AbottomWall - 6;
	    let wall = 0;
        do show();
        return this;
    }
}'''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    assert len(compiler.symbol_table.class_table) == 4
    assert len(compiler.symbol_table.subroutine_table) == 6


def test_method() -> None:

    input = '''class Ball {
    field int x, y;
    field int lengthx, lengthy;

    method void setDestination(int destx, int desty) {
        var int dx, dy, temp;
    }
}'''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    print(f'test_class_ta   {id(compiler)}')
    compiler.parse()

    print(compiler.symbol_table.class_table)
    print(compiler.symbol_table.subroutine_table)
    print(f"argument: field {compiler.symbol_table.var_count('field')}")
    print(f"argument: count {compiler.symbol_table.var_count('argument')}")
    print(f"argument: var {compiler.symbol_table.var_count('var')}")
    print(f"kind_of: lengthx {compiler.symbol_table.kind_of('lengthx')}")
    print(f"kind_of: destx {compiler.symbol_table.kind_of('destx')}")
    print(f"kind_of: None {compiler.symbol_table.kind_of('test')}")
    print(len(compiler.symbol_table.class_table))
    print(len(compiler.symbol_table.subroutine_table))

    assert len(compiler.symbol_table.class_table) == 4
    assert len(compiler.symbol_table.subroutine_table) == 6
    assert compiler.symbol_table.var_count('field') == 4
    assert compiler.symbol_table.var_count('argument') == 3
    assert compiler.symbol_table.var_count('var') == 3


def test_constractor_and_mehod() -> None:

    input = '''class Ball {
    field int x, y;
    field int lengthx, lengthy;

    constructor Ball new(int Ax, int Ay,
                         int AleftWall, int ArightWall, int AtopWall, int AbottomWall) {    	
	    let x = Ax;		
	    let y = Ay;
	    let leftWall = AleftWall;
	    let rightWall = ArightWall - 6;
	    let topWall = AtopWall; 
	    let bottomWall = AbottomWall - 6;
	    let wall = 0;
        do show();
        return this;
    }

    method void setDestination(int destx, int desty) {
        var int dx, dy, temp;
    }
}'''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    print(f'test_class_ta   {id(compiler)}')
    compiler.parse()

    print(compiler.symbol_table.class_table)
    print(compiler.symbol_table.subroutine_table)
    print(len(compiler.symbol_table.class_table))
    print(len(compiler.symbol_table.subroutine_table))

    assert len(compiler.symbol_table.class_table) == 4
    assert len(compiler.symbol_table.subroutine_table) == 6