from jack.compilation_engine import CompilationEngine
from jack.jack_tokenizer import JackTokenizer


def test_constructor() -> None:

    input = """class Point {
        field int x, y;
        static int pointCount;

        constructor Point new(int ax, int ay){
            let x = ax;
            let y = ay;
            let pointCount = pointCount + 1;
            return this;
        }
}
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function Point.new 0
push constant 2
call Memory.alloc 1
pop pointer 0
push argument 0
pop this 0
push argument 1
pop this 1
push static 0
push constant 1
add
pop static 0
push pointer 0
return
"""

    assert result == expected


def test_constructor_2() -> None:

    input = """class SquareGame {
   field Square square; // the square of this game
   field int direction; // the square's current direction: 
                        // 0=none, 1=up, 2=down, 3=left, 4=right

   /** Constructs a new Square Game. */
   constructor SquareGame new() {
      // Creates a 30 by 30 pixels square and positions it at the top-left
      // of the screen.
      let square = Square.new(0, 0, 30);
      let direction = 0;  // initial state is no movement
      return this;
   }

   /** Disposes this game. */
   method void dispose() {
      do square.dispose();
      do Memory.deAlloc(this);
      return;
   }
}
    """

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f"compiler.vm_writer.output {compiler.vm_writer}")
    print(f"compiler.vm_writer.output {compiler.vm_writer.output}")

    result = compiler.vm_writer.output

    expected = """function SquareGame.new 0
push constant 2
call Memory.alloc 1
pop pointer 0
push constant 0
push constant 0
push constant 30
call Square.new 3
pop this 0
push constant 0
pop this 1
push pointer 0
return
function SquareGame.dispose 0
push argument 0
pop pointer 0
push this 0
call Square.dispose 1
pop temp 0
push pointer 0
call Memory.deAlloc 1
pop temp 0
push constant 0
return
"""

    assert result == expected
