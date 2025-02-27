from tokens import Token, TokenType

LETRAS = 'abcdefghijklmnopqrstuvwxyz01234567890.'


class Reader:
    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))
        self.input = set()
        self.Siguiente()

    def Siguiente(self):
        try:
            self.caracter_act = next(self.string)
        except StopIteration:
            self.caracter_act = None

    def CrearTokens(self):
        while self.caracter_act != None:

            if self.caracter_act in LETRAS:
                self.input.add(self.caracter_act)
                yield Token(TokenType.LPAR, '(')
                yield Token(TokenType.LETTER, self.caracter_act)

                self.Siguiente()
                parentesis_añadidos = False

                while self.caracter_act != None and \
                        (self.caracter_act in LETRAS or self.caracter_act in '*+?'):

                    if self.caracter_act == '*':
                        yield Token(TokenType.KLEENE, '*')
                        yield Token(TokenType.RPAR, ')')
                        parentesis_añadidos = True

                    elif self.caracter_act == '+':
                        yield Token(TokenType.PLUS, '+')
                        yield Token(TokenType.RPAR, ')')
                        parentesis_añadidos = True

                    elif self.caracter_act == '?':
                        yield Token(TokenType.QUESTION, '?')
                        yield Token(TokenType.RPAR, ')')
                        parentesis_añadidos = True

                    elif self.caracter_act in LETRAS:
                        self.input.add(self.caracter_act)
                        yield Token(TokenType.APPEND)
                        yield Token(TokenType.LETTER, self.caracter_act)

                    self.Siguiente()

                    if self.caracter_act != None and self.caracter_act == '(' and parentesis_añadidos:
                        yield Token(TokenType.APPEND)

                if self.caracter_act != None and self.caracter_act == '(' and not parentesis_añadidos:
                    yield Token(TokenType.RPAR, ')')
                    yield Token(TokenType.APPEND)

                elif not parentesis_añadidos:
                    yield Token(TokenType.RPAR, ')')

            elif self.caracter_act == '|':
                self.Siguiente()
                yield Token(TokenType.OR, '|')

            elif self.caracter_act == '(':
                self.Siguiente()
                yield Token(TokenType.LPAR)

            elif self.caracter_act in (')*+?'):

                if self.caracter_act == ')':
                    self.Siguiente()
                    yield Token(TokenType.RPAR)

                elif self.caracter_act == '*':
                    self.Siguiente()
                    yield Token(TokenType.KLEENE)

                elif self.caracter_act == '+':
                    self.Siguiente()
                    yield Token(TokenType.PLUS)

                elif self.caracter_act == '?':
                    self.Siguiente()
                    yield Token(TokenType.QUESTION)

                # Finally, check if we need to add an append token
                if self.caracter_act != None and \
                        (self.caracter_act in LETRAS or self.caracter_act == '('):
                    yield Token(TokenType.APPEND, '.')

            else:
                raise Exception(f'Invalid entry: {self.caracter_act}')

    def GetSimbolos(self):
        return self.input