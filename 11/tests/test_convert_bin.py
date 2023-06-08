from jack.compilation_engine import CompilationEngine
from jack.jack_tokenizer import JackTokenizer


def test_single_function() -> None:

    input = '''class Main {
    /**
     * Initializes RAM[8001]..RAM[8016] to -1,
     * and converts the value in RAM[8000] to binary.
     */
    function void main() {
	    var int value;
        do Main.fillMemory(8001, 16, -1); // sets RAM[8001]..RAM[8016] to -1
        let value = Memory.peek(8000);    // reads a value from RAM[8000]
        do Main.convert(value);           // performs the conversion	
        return;
    }
    }
    '''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f'compiler.vm_writer.output {compiler.vm_writer}')
    print(f'compiler.vm_writer.output {compiler.vm_writer.output}')

    result = compiler.vm_writer.output

    expected = '''function Main.main 1
push constant 8001
push constant 16
push constant 1
neg
call Main.fillMemory 3
pop temp 0
push constant 8000
call Memory.peek 1
pop local 0
push local 0
call Main.convert 1
pop temp 0
push constant 0
return
'''

    assert result == expected


def test_function_if() -> None:

    input = '''class Main {
    /** Returns the next mask (the mask that should follow the given mask). */	
    function int nextMask(int mask) {	
    	if (mask = 0) {	
    	    return 1;	
    	}	
    	else {	
	    return mask * 2;	
    	}
    }	
    }
    '''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f'compiler.vm_writer.output {compiler.vm_writer}')
    print(f'compiler.vm_writer.output {compiler.vm_writer.output}')

    result = compiler.vm_writer.output

    expected = '''function Main.nextMask 0
push argument 0
push constant 0
eq
not
if-goto flag_1
push constant 1
return
goto tag_1
label flag_1
push argument 0
push constant 2
call Math.multiply 2
return
label tag_1
'''

    assert result == expected


def test_function_while() -> None:

    input = '''class Main {
    /** Fills 'length' consecutive memory locations with 'value',	
      * starting at 'startAddress'. */	
    function void fillMemory(int startAddress, int length, int value) {	
        while (length > 0) {	
            do Memory.poke(startAddress, value);	
            let length = length - 1;	
            let startAddress = startAddress + 1;	
        }	
        return;	
    }	
    }
    '''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f'compiler.vm_writer.output {compiler.vm_writer}')
    print(f'compiler.vm_writer.output {compiler.vm_writer.output}')

    result = compiler.vm_writer.output

    expected = '''function Main.fillMemory 0
label while 1
push argument 1
push constant 0
gt
not
if-goto while_if_1
push argument 0
push argument 2
call Memory.poke 2
pop temp 0
push argument 1
push constant 1
sub
pop argument 1
push argument 0
push constant 1
add
pop argument 0
goto while 1
label while_if_1
push constant 0
return
'''

    assert result == expected



def test_function_while() -> None:

    input = '''class Main {
    /** Converts the given decimal value to binary, and puts 	
     *  the resulting bits in RAM[8001]..RAM[8016]. */	
    function void convert(int value) {	
    	var int mask, position;	
    	var boolean loop;	
    		
    	let loop = true;	
    	while (loop) {	
    	    let position = position + 1;	
    	    let mask = Main.nextMask(mask);	
    		
    	    if (~(position > 16)) {	
    		
    	        if (~((value & mask) = 0)) {	
    	            do Memory.poke(8000 + position, 1);	
       	        }	
    	        else {	
    	            do Memory.poke(8000 + position, 0);	
      	        }    	
    	    }	
    	    else {	
    	        let loop = false;	
    	    }	
    	}	
    	return;	
    }	
    }
    '''

    tokenizer = JackTokenizer(input)
    tokenizer.advance()
    tokens = tokenizer.output

    compiler = CompilationEngine(tokens)
    compiler.parse()

    print(f'compiler.vm_writer.output {compiler.vm_writer}')
    print(f'compiler.vm_writer.output {compiler.vm_writer.output}')

    result = compiler.vm_writer.output

    expected = '''function Main.convert 3
push constant 1
neg
pop local 2
label while_1
push local 2
not
if-goto while_if_1
push local 1
push constant 1
add
pop local 1
push local 0
call Main.nextMask 1
pop local 0
push local 1
push constant 16
gt
not
not
if-goto flag_2
push argument 0
push local 0
and
push constant 0
eq
not
not
if-goto flag_3
push constant 8000
push local 1
add
push constant 1
call Memory.poke 2
pop temp 0
goto tag_3
label flag_3
push constant 8000
push local 1
add
push constant 0
call Memory.poke 2
pop temp 0
label tag_3
goto tag_2
label flag_2
push constant 0
pop local 2
label tag_2
goto while_1
label while_if_1
push constant 0
return
'''

    assert result == expected

