from jack.compilation_engine import CompilationEngine
from jack.jack_analyzer import create_xml_file
from jack.jack_tokenizer import JackTokenizer


def test_square() -> None:

    input = '''class Square {

   field int x, y; 
   field int size; 

   constructor Square new(int Ax, int Ay, int Asize) {
      let x = Ax;
      let y = Ay;
      let size = Asize;
      do draw();
      return x;
   }
   method void dispose() {
      do Memory.deAlloc(this);
      return;
   }
   method void draw() {
      do Screen.setColor(x);
      do Screen.drawRectangle(x, y, x, y);
      return;
   }
   method void erase() {
      do Screen.setColor(x);
      do Screen.drawRectangle(x, y, x, y);
      return;
   }
   method void incSize() {
      if (x) {
         do erase();
         let size = size;
         do draw();
      }
      return;
   }
   method void decSize() {
      if (size) {
         do erase();
         let size = size;
         do draw();
      }
      return;
   }
   method void moveUp() {
      if (y) {
         do Screen.setColor(x);
         do Screen.drawRectangle(x, y, x, y);
         let y = y;
         do Screen.setColor(x);
         do Screen.drawRectangle(x, y, x, y);
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
    element_tree = compiler.xml

    xml = create_xml_file(element_tree)

    expected = '''<class>
  <keyword> class </keyword>
  <identifier> Square </identifier>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> x </identifier>
    <symbol> , </symbol>
    <identifier> y </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <classVarDec>
    <keyword> field </keyword>
    <keyword> int </keyword>
    <identifier> size </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <subroutineDec>
    <keyword> constructor </keyword>
    <identifier> Square </identifier>
    <identifier> new </identifier>
    <symbol> ( </symbol>
    <parameterList>
      <keyword> int </keyword>
      <identifier> Ax </identifier>
      <symbol> , </symbol>
      <keyword> int </keyword>
      <identifier> Ay </identifier>
      <symbol> , </symbol>
      <keyword> int </keyword>
      <identifier> Asize </identifier>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <letStatement>
          <keyword> let </keyword>
          <identifier> x </identifier>
          <symbol> = </symbol>
          <expression>
            <term>
              <identifier> Ax </identifier>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
        <letStatement>
          <keyword> let </keyword>
          <identifier> y </identifier>
          <symbol> = </symbol>
          <expression>
            <term>
              <identifier> Ay </identifier>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
        <letStatement>
          <keyword> let </keyword>
          <identifier> size </identifier>
          <symbol> = </symbol>
          <expression>
            <term>
              <identifier> Asize </identifier>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> draw </identifier>
          <symbol> ( </symbol>
          <expressionList>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <expression>
            <term>
              <identifier> x </identifier>
            </term>
          </expression>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> dispose </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <doStatement>
          <keyword> do </keyword>
          <identifier> Memory </identifier>
          <symbol> . </symbol>
          <identifier> deAlloc </identifier>
          <symbol> ( </symbol>
          <expressionList>
            <expression>
              <term>
                <keyword> this </keyword>
              </term>
            </expression>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> draw </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <doStatement>
          <keyword> do </keyword>
          <identifier> Screen </identifier>
          <symbol> . </symbol>
          <identifier> setColor </identifier>
          <symbol> ( </symbol>
          <expressionList>
            <expression>
              <term>
                <identifier> x </identifier>
              </term>
            </expression>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> Screen </identifier>
          <symbol> . </symbol>
          <identifier> drawRectangle </identifier>
          <symbol> ( </symbol>
          <expressionList>
            <expression>
              <term>
                <identifier> x </identifier>
              </term>
            </expression>
            <symbol> , </symbol>
            <expression>
              <term>
                <identifier> y </identifier>
              </term>
            </expression>
            <symbol> , </symbol>
            <expression>
              <term>
                <identifier> x </identifier>
              </term>
            </expression>
            <symbol> , </symbol>
            <expression>
              <term>
                <identifier> y </identifier>
              </term>
            </expression>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> erase </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <doStatement>
          <keyword> do </keyword>
          <identifier> Screen </identifier>
          <symbol> . </symbol>
          <identifier> setColor </identifier>
          <symbol> ( </symbol>
          <expressionList>
            <expression>
              <term>
                <identifier> x </identifier>
              </term>
            </expression>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> Screen </identifier>
          <symbol> . </symbol>
          <identifier> drawRectangle </identifier>
          <symbol> ( </symbol>
          <expressionList>
            <expression>
              <term>
                <identifier> x </identifier>
              </term>
            </expression>
            <symbol> , </symbol>
            <expression>
              <term>
                <identifier> y </identifier>
              </term>
            </expression>
            <symbol> , </symbol>
            <expression>
              <term>
                <identifier> x </identifier>
              </term>
            </expression>
            <symbol> , </symbol>
            <expression>
              <term>
                <identifier> y </identifier>
              </term>
            </expression>
          </expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> incSize </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <identifier> x </identifier>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
            <doStatement>
              <keyword> do </keyword>
              <identifier> erase </identifier>
              <symbol> ( </symbol>
              <expressionList>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> size </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> size </identifier>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <doStatement>
              <keyword> do </keyword>
              <identifier> draw </identifier>
              <symbol> ( </symbol>
              <expressionList>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
          </statements>
          <symbol> } </symbol>
        </ifStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> decSize </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <identifier> size </identifier>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
            <doStatement>
              <keyword> do </keyword>
              <identifier> erase </identifier>
              <symbol> ( </symbol>
              <expressionList>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> size </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> size </identifier>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <doStatement>
              <keyword> do </keyword>
              <identifier> draw </identifier>
              <symbol> ( </symbol>
              <expressionList>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
          </statements>
          <symbol> } </symbol>
        </ifStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> method </keyword>
    <keyword> void </keyword>
    <identifier> moveUp </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <statements>
        <ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <identifier> y </identifier>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
            <doStatement>
              <keyword> do </keyword>
              <identifier> Screen </identifier>
              <symbol> . </symbol>
              <identifier> setColor </identifier>
              <symbol> ( </symbol>
              <expressionList>
                <expression>
                  <term>
                    <identifier> x </identifier>
                  </term>
                </expression>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
            <doStatement>
              <keyword> do </keyword>
              <identifier> Screen </identifier>
              <symbol> . </symbol>
              <identifier> drawRectangle </identifier>
              <symbol> ( </symbol>
              <expressionList>
                <expression>
                  <term>
                    <identifier> x </identifier>
                  </term>
                </expression>
                <symbol> , </symbol>
                <expression>
                  <term>
                    <identifier> y </identifier>
                  </term>
                </expression>
                <symbol> , </symbol>
                <expression>
                  <term>
                    <identifier> x </identifier>
                  </term>
                </expression>
                <symbol> , </symbol>
                <expression>
                  <term>
                    <identifier> y </identifier>
                  </term>
                </expression>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> y </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> y </identifier>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <doStatement>
              <keyword> do </keyword>
              <identifier> Screen </identifier>
              <symbol> . </symbol>
              <identifier> setColor </identifier>
              <symbol> ( </symbol>
              <expressionList>
                <expression>
                  <term>
                    <identifier> x </identifier>
                  </term>
                </expression>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
            <doStatement>
              <keyword> do </keyword>
              <identifier> Screen </identifier>
              <symbol> . </symbol>
              <identifier> drawRectangle </identifier>
              <symbol> ( </symbol>
              <expressionList>
                <expression>
                  <term>
                    <identifier> x </identifier>
                  </term>
                </expression>
                <symbol> , </symbol>
                <expression>
                  <term>
                    <identifier> y </identifier>
                  </term>
                </expression>
                <symbol> , </symbol>
                <expression>
                  <term>
                    <identifier> x </identifier>
                  </term>
                </expression>
                <symbol> , </symbol>
                <expression>
                  <term>
                    <identifier> y </identifier>
                  </term>
                </expression>
              </expressionList>
              <symbol> ) </symbol>
              <symbol> ; </symbol>
            </doStatement>
          </statements>
          <symbol> } </symbol>
        </ifStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>'''

    assert xml == expected
