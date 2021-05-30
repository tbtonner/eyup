# imports
import src.tokens as tok
from src.errors import VexedError

# testing the make_tokens() method
def test_make_tokens_base():
    text = '12 + 12.45 "test" . - * / % () [] = $ , !=,<> := : <= >= and testVar \n aye nay'
    tokeniser = tok.Tokenise(text)
    tokens, error = tokeniser.make_tokens()

    assert tokens[0].type == tok.TT_INT and tokens[0].value == 12
    assert tokens[1].type == tok.TT_PLUS
    assert tokens[2].type == tok.TT_FLOAT and tokens[2].value == 12.45
    assert tokens[3].type == tok.TT_SCRIPT and tokens[3].value == "test"
    assert tokens[4].type == tok.TT_CALL
    assert tokens[5].type == tok.TT_MINUS
    assert tokens[6].type == tok.TT_MUL
    assert tokens[7].type == tok.TT_DIV
    assert tokens[8].type == tok.TT_MOD
    assert tokens[9].type == tok.TT_LBRACK
    assert tokens[10].type == tok.TT_RBRACK
    assert tokens[11].type == tok.TT_LEFT_SQUARE_BRACK
    assert tokens[12].type == tok.TT_RIGHT_SQUARE_BRACK
    assert tokens[13].type == tok.TT_EQUALS
    assert tokens[14].type == tok.TT_CONCAT_APPEND
    assert tokens[15].type == tok.TT_COMMA
    assert tokens[16].type == tok.TT_NOT_EQUALS
    assert tokens[17].type == tok.TT_COMMA
    assert tokens[18].type == tok.TT_LESS_THAN
    assert tokens[19].type == tok.TT_GREATER_THAN
    assert tokens[20].type == tok.TT_VAR_COMPLETE
    assert tokens[21].type == tok.TT_VAR_DECLARE
    assert tokens[22].type == tok.TT_LESS_THAN_EQUALS
    assert tokens[23].type == tok.TT_GREATER_THAN_EQUALS
    assert tokens[24].type == tok.TT_KEYWORD and tokens[24].value == "and"
    assert tokens[25].type == tok.TT_IDENTIFIER and tokens[25].value == "testVar"
    assert tokens[26].type == tok.TT_NEWLINE
    assert tokens[27].type == tok.TT_ANSWER and tokens[27].value == "aye"
    assert tokens[28].type == tok.TT_ANSWER and tokens[28].value == "nay"
    assert tokens[29].type == tok.TT_EOF

    assert error is None

def test_return_error():
    tokeniser = tok.Tokenise("test")
    tokens, error = tokeniser.return_error()

    assert tokens == []
    assert type(error) is VexedError
