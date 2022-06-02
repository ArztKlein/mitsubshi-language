from sly import Lexer, Parser

from mitsubishi_language.services import Printer

class MitsubishiLanguage:
    SERVICES = [Printer]
    SERVICE_REGEX = '(' + '|'.join([service.name() for service in SERVICES]) + ')'

class CalcLexer(Lexer):
    tokens = {STRING, SERVICE, INSERT}
    ignore = ' \t'

    # Tokens
    STRING = r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')'''

    # Generate the regex for a service
    SERVICE = MitsubishiLanguage.SERVICE_REGEX
    
    # Special symbols
    INSERT = r'->'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_("string")
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    @_("STRING INSERT SERVICE")
    def statement(self, p):
        self.get_service(p.SERVICE).insert(p.STRING)

    def __init__(self):
        self.services = {}

        for service in MitsubishiLanguage.SERVICES:
            self.services[service.name()] = service

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