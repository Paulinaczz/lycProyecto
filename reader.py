from tokens import Token, TokenType

LETRAS = 'abcdefghijklmnopqrstuvwxyz01234567890.'


class Lector:
    def __init__(self, cadena: str):
        self.cadena = iter(cadena.replace(' ', ''))
        self.entrada = set()
        self.Siguiente()

    def Siguiente(self):
        try:
            self.caracter_actual = next(self.cadena)
        except StopIteration:
            self.caracter_actual = None

    def CrearTokens(self):
        while self.caracter_actual is not None:

            if self.caracter_actual in LETRAS:
                self.entrada.add(self.caracter_actual)
                yield Token(TokenType.LPAR, '(')
                yield Token(TokenType.LETRA, self.caracter_actual)
                
                self.Siguiente()
                parentesis_agregados = False

                while self.caracter_actual is not None and \
                        (self.caracter_actual in LETRAS or self.caracter_actual in '*+?'):

                    if self.caracter_actual == '*':
                        yield Token(TokenType.KLEENE, '*')
                        yield Token(TokenType.RPAR, ')')
                        parentesis_agregados = True

                    elif self.caracter_actual == '+':
                        yield Token(TokenType.MAS, '+')
                        yield Token(TokenType.RPAR, ')')
                        parentesis_agregados = True

                    elif self.caracter_actual == '?':
                        yield Token(TokenType.INTERROGACION, '?')
                        yield Token(TokenType.RPAR, ')')
                        parentesis_agregados = True

                    elif self.caracter_actual in LETRAS:
                        self.entrada.add(self.caracter_actual)
                        yield Token(TokenType.CONCATENAR)
                        yield Token(TokenType.LETRA, self.caracter_actual)

                    self.Siguiente()

                    if self.caracter_actual is not None and self.caracter_actual == '(' and parentesis_agregados:
                        yield Token(TokenType.CONCATENAR)

                if self.caracter_actual is not None and self.caracter_actual == '(' and not parentesis_agregados:
                    yield Token(TokenType.RPAR, ')')
                    yield Token(TokenType.CONCATENAR)

                elif not parentesis_agregados:
                    yield Token(TokenType.RPAR, ')')

            elif self.caracter_actual == '|':
                self.Siguiente()
                yield Token(TokenType.OR, '|')

            elif self.caracter_actual == '(':
                self.Siguiente()
                yield Token(TokenType.LPAR)

            elif self.caracter_actual in (')*+?'):

                if self.caracter_actual == ')':
                    self.Siguiente()
                    yield Token(TokenType.RPAR)

                elif self.caracter_actual == '*':
                    self.Siguiente()
                    yield Token(TokenType.KLEENE)

                elif self.caracter_actual == '+':
                    self.Siguiente()
                    yield Token(TokenType.MAS)

                elif self.caracter_actual == '?':
                    self.Siguiente()
                    yield Token(TokenType.INTERROGACION)

                if self.caracter_actual is not None and \
                        (self.caracter_actual in LETRAS or self.caracter_actual == '('):
                    yield Token(TokenType.CONCATENAR, '.')

            else:
                raise Exception(f'Entrada inválida: {self.caracter_actual}')

    def ObtenerSimbolos(self):
        return self.entrada
