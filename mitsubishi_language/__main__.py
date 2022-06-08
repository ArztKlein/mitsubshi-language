from sly import Lexer, Parser

from mitsubishi_language.services import *

class MitsubishiLanguage:
    SERVICES = [Printer, KeyboardInput]
    SERVICE_REGEX = '(' + '|'.join([service.name() for service in SERVICES]) + ')'

class CalcLexer(Lexer):

    def __init__(self):
         self.nesting_level = 0

    tokens = {STRING, SERVICE, INSERT, NUMBER, PLUS, MINUS, TIMES, DIVIDE, POWER, ASSIGN, LPAREN, RPAREN, IDENTIFIER}
    ignore = ' \t'

    literals = { '(', ')', '{', '}', '.', '!' }

    # Tokens
    ASSIGN  = r'='
    DIVIDE  = r'/'
    STRING  = r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')'''
    INSERT  = r'->'
    MINUS   = r'-'
    NUMBER  = r'\d+'
    PLUS    = r'\+'
    TIMES   = r'\*'
    POWER   = r'\^'
    LPAREN  = r'\('
    RPAREN  = r'\)'

    # Generate the regex for a service
    SERVICE = MitsubishiLanguage.SERVICE_REGEX

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    
    @_(r'\{')
    def lbrace(self, t):
        t.type = '{'      # Set token type to the expected literal
        self.nesting_level += 1
        return t

    @_(r'\}')
    def rbrace(self, t):
        t.type = '}'      # Set token type to the expected literal
        self.nesting_level -=1
        return t

    @_("string")
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', POWER)
    )

    def __init__(self):
        self.services = {}

        for service in MitsubishiLanguage.SERVICES:
            self.services[service.name()] = service

    @_("value INSERT SERVICE")
    def statement(self, p):
        return self.get_service(p.SERVICE).insert(p.value)
    
    @_("statement INSERT SERVICE")
    def statement(self, p):
        return self.get_service(p.SERVICE).insert(p.statement)

    @_("value POWER value")
    def value(self, p):
        return p.value0 ** p.value1

    @_("value TIMES value")
    def value(self, p):
        return p.value0 * p.value1
    
    @_("value PLUS value")
    def value(self, p):
        return p.value0 + p.value1

    @_("NUMBER")
    def value(self, p):
        return int(p.NUMBER)

    @_("STRING")
    def value(self, p):
        return p.STRING

    def get_service(self, name):
        return self.services[name]

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    while True:
        try:
            text = input('>>> ')
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))