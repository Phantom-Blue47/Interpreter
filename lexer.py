INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
REM = 'REM'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LCURL = 'LCURL'
RCURL = 'RCURL'
ID = 'ID'
ASSIGN = 'ASSIGN'
LEQUAL = '<='
GEQUAL = '>='
DEQUAL = '=='
LESSTHAN = '<'
GREATHAN = '>'
NOTEQUAL = '!='
SEMI = 'SEMI'
DOT = 'DOT'
OBJECT = 'OBJECT'
VAR = 'VAR'
COLON = 'COLON'
COMMA = 'COMMA'
EOF = 'EOF'
DEF = 'DEF'
IF = 'IF'
ELSE = 'ELSE'
TRUE = 'TRUE'
FALSE = 'FALSE'
OBJECT = 'OBJECT'
DO = 'DO'
WHILE = 'WHILE'
INT = 'INT'
MAIN = 'MAIN'
ARGS = 'ARGS'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
STRING = 'STRING'
ARRAY = 'ARRAY'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'IF': Token('IF', 'IF'),
    'ELSE': Token('ELSE', 'ELSE'),
    'TRUE': Token('TRUE', 'TRUE'),
    'FALSE': Token('FALSE', 'FALSE'),
    'VAR': Token('VAR', 'VAR'),
    'OBJECT': Token('OBJECT', 'OBJECT'),
    'DO': Token('DO', 'DO'),
    'WHILE': Token('WHILE', 'WHILE'),
    'INT': Token('INT','INT'),
    'MAIN': Token('MAIN','MAIN'),
    'DEF' : Token('DEF','DEF'),
    'ARGS': Token('ARGS','ARGS'),
    'STRING': Token('STRING','STRING'),
    'ARRAY': Token('ARRAY','ARRAY')
}


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char != '/' or self.peek() != '*':
            self.advance()
        self.advance()
        self.advance()

    def number(self):
        """Return a (multidigit) integer  consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

            token = Token('INTEGER', int(result))

        return token

    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))
        return token

    # need to implement if ,else methods.

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char == '{':
                self.advance()
                return Token('LCURL', '{')

            elif self.current_char == '*' and self.peek() == '/':
                self.advance()
                self.advance()
                self.skip_comment()
                continue
            elif self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('LEQUAL', '<=')
            elif self.current_char == '<':
                self.advance()
                return Token('LESSTHAN', '<')
            elif self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('GEQUAL', '>=')

            elif self.current_char == '>':
                self.advance()
                return Token('GREATHAN', '<')
            elif self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('DEQUAL', '==')
            elif self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('DEQUAL', '==')
            
            elif self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=')


            # in scala the starting char of the variable should not be a digit.
            elif self.current_char.isalpha():
                return self._id()

            elif self.current_char.isdigit():
                return self.number()

            elif self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')
            elif self.current_char == '\n':
                self.advance()
                return Token('EOL', '\n')

            elif self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')

            elif self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')

            elif self.current_char == '*':
                self.advance()
                return Token('MUL', '*')

            elif self.current_char == '/':
                self.advance()
                return Token('DIV', '/')

            elif self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            elif self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            elif self.current_char == ':':
                self.advance()
                return Token('COLON', ':')

            elif self.current_char == '}':
                self.advance()
                return Token('RCURL', '}')

            elif self.current_char == '[':
                self.advance()
                return Token('LBRACE', '[')
            
            elif self.current_char == ']':
                self.advance()
                return Token('RBRACE', ']')
            
            elif self.current_char == '%':
                self.advance()
                return Token('REM', '%')

            self.error()

        return Token(EOF, None)

    def checking(self):

        currenttoken = None
        while self.current_char is not None:
            currenttoken = self.get_next_token()
            print(currenttoken.type, " ", currenttoken.value)
