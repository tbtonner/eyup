import string
from . import positions
from . import errors

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# TOKENS
# list of tokens
#######################################

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_SCRIPT = 'SCRIPT'
TT_LETTER = 'LETTER'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'
TT_LBRACK = 'LBRACK'
TT_RBRACK = 'RBRACK'
TT_LEFT_SQUARE_BRACK = 'LEFT_SQUARE_BRACK'
TT_RIGHT_SQUARE_BRACK = 'RIGHT_SQUARE_BRACK'
TT_KEYWORD = 'KEYWORD'
TT_IDENTIFIER = 'IDENTIFIER'
TT_CONCAT_APPEND = 'CONCAT_APPEND'

# make different later for EYUP grammar
TT_VAR_COMPLETE = 'VAR_COMPLETE'
TT_VAR_DECLARE = 'VAR_DECLARE'

TT_EQUALS = 'EQUALS'
TT_NOT_EQUALS = 'NOT_EQUALS'
TT_LESS_THAN = 'LESS_THAN'
TT_GREATER_THAN = 'GREATER_THAN'
TT_LESS_THAN_EQUALS = 'LESS_THAN_EQUALS'
TT_GREATER_THAN_EQUALS = 'GREATER_THAN_EQUALS'
TT_ANSWER = 'ANSWER'
TT_CALL = 'CALL'
TT_COMMA = 'COMMA'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'

KEYWORDS = [
    'bodger',
    'eyup',
    'summat',
    'sithee',
    'sithi',
    'forget',
    'oer',
    'if',
    'when',
    'then',
    'else',
    'elif',
    'fettle',
    'giz',
    'gioer',
    'allus',
    ':',
    'while',
    'gowon',
    '!',
    'and',
    'or',
    'not',
    'gander',
    'wang',
    'missen',
    'Answer',
    'Number',
    'Letter',
    'List',
    'Script',
    'Bodger'
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.value}'
        return f'{self.type}'

#######################################
# TOKENISER
# takes string and creates a token stream in the language of eyup
#######################################


class Tokenise:
    def __init__(self, text):
        self.text = text
        self.pos = positions.Position(-1, 0, -1, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(
            self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_script())
            elif self.current_char == '.':
                tokens.append(Token(TT_CALL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LBRACK, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RBRACK, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LEFT_SQUARE_BRACK, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RIGHT_SQUARE_BRACK, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TT_EQUALS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '$':
                tokens.append(Token(TT_CONCAT_APPEND, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ':':
                pos_start = self.pos.copy()
                self.advance()
                if (self.current_char == '='):
                    tokens.append(
                        Token(TT_VAR_COMPLETE, pos_start=pos_start, pos_end=self.pos))
                    self.advance()
                else:
                    tokens.append(Token(TT_VAR_DECLARE, pos_start=self.pos))
            else:
                return self.return_error()

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_script = '' 
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_script += self.current_char
            self.advance()

        if id_script == 'aye' or id_script == 'nay':
            token_type = TT_ANSWER
        elif id_script in KEYWORDS:
            token_type = TT_KEYWORD
        else:
            token_type = TT_IDENTIFIER

        return Token(token_type, id_script, pos_start, self.pos)

    def make_script(self):
        script = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                script += escape_characters.get(self.current_char,
                                                self.current_char)
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    script += self.current_char
            self.advance()
            escape_character = False

        self.advance()
        if len(script) == 1:
            return Token(TT_LETTER, script, pos_start, self.pos)
        return Token(TT_SCRIPT, script, pos_start, self.pos)

    def return_error(self):
        pos_start = self.pos.copy()
        char = self.current_char
        self.advance()
        return [], errors.VexedError(pos_start, self.pos, "'" + char + "'")

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            return Token(TT_NOT_EQUALS, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, errors.VexedError(pos_start, self.pos, "'=' (after '!')")

    def make_less_than(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_LESS_THAN_EQUALS, pos_start=pos_start, pos_end=self.pos)

        return Token(TT_LESS_THAN, '<', self.pos)

    def make_greater_than(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_GREATER_THAN_EQUALS, '>=', pos_start=pos_start, pos_end=self.pos)

        return Token(TT_GREATER_THAN, '>', self.pos)
