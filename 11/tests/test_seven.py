from jack.compilation_engine import CompilationEngine
from jack.jack_tokenizer import JackTokenizer


def test_additive_expression() -> None:

    input = """class Main {
   function void main() {
      do Output.printInt(1 + 6);
      return;
   }
   }
    """
    #   do Output.printInt(1 + 6);

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Main.main 0
push constant 1
push constant 6
add
call Output.printInt 1
pop temp 0
push constant 0
return
"""

    assert result == expected


def test_multicative_expression() -> None:

    input = """class Main {
   function void main() {
      do Output.printInt(2 * 3);
      return;
   }
   }
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()
    print(compiler)

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Main.main 0
push constant 2
push constant 3
call Math.multiply 2
call Output.printInt 1
pop temp 0
push constant 0
return
"""

    assert result == expected


def test_multicative_primary_expression() -> None:

    input = """class Main {
   function void main() {
      do Output.printInt((2 * 3));
      return;
   }
   }
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()
    print(compiler)

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Main.main 0
push constant 2
push constant 3
call Math.multiply 2
call Output.printInt 1
pop temp 0
push constant 0
return
"""

    assert result == expected


def test_additive_multicative_expression() -> None:

    input = """class Main {
   function void main() {
      do Output.printInt(1 + 2 * 3);
      return;
   }
   }
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()
    print(compiler)

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Main.main 0
push constant 1
push constant 2
push constant 3
call Math.multiply 2
add
call Output.printInt 1
pop temp 0
push constant 0
return
"""

    assert result == expected


def test_multicative_primary_expression_1() -> None:

    input = """class Main {
   function void main() {
      do Output.printInt((2 * 3) + 1);
      return;
   }
   }
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()
    print(compiler)

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Main.main 0
push constant 2
push constant 3
call Math.multiply 2
push constant 1
add
call Output.printInt 1
pop temp 0
push constant 0
return
"""

    assert result == expected


def test_multicative_primary_expression_2() -> None:

    input = """class Main {
   function void main() {
      do Output.printInt(1 + (2 * 3));
      return;
   }
   function void test() {
      do Output.printInt(1 + (2 * 3) );
      return;
   }
   }
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()
    print(compiler)

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Main.main 0
push constant 1
push constant 2
push constant 3
call Math.multiply 2
add
call Output.printInt 1
pop temp 0
push constant 0
return
function Main.test 0
push constant 1
push constant 2
push constant 3
call Math.multiply 2
add
call Output.printInt 1
pop temp 0
push constant 0
return
"""

    assert result == expected
