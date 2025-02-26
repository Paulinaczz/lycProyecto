# from tokens import Token, TokenType

# LETRAS = 'abcdefghijklmnopqrstuvwxyz01234567890'  # Se eliminó el punto (.)

# class DirectReader:
#     def __init__(self, string: str):
#         self.string = iter(string.replace(' ', ''))  # Elimina espacios
#         self.input = set()
#         self.rparPending = False
#         self.Next()

#     def Next(self):
#         try:
#             self.curr_char = next(self.string)
#         except StopIteration:
#             self.curr_char = None

#     def CreateTokens(self):
#         while self.curr_char is not None:

#             # Si es una letra válida
#             if self.curr_char in LETRAS:
#                 self.input.add(self.curr_char)
#                 yield Token(TokenType.LETTER, self.curr_char)
#                 self.Next()

#                 # Agregar APPEND solo si es necesario
#                 if self.curr_char is not None and self.curr_char in LETRAS + '(':
#                     yield Token(TokenType.APPEND, '.')

#             # Si encuentra un OR
#             elif self.curr_char == '|':
#                 yield Token(TokenType.OR, '|')
#                 self.Next()

#             # Si encuentra un paréntesis de apertura
#             elif self.curr_char == '(':
#                 yield Token(TokenType.LPAR, '(')  # ✅ Ahora tiene su valor
#                 self.Next()

#             # Si encuentra operadores o paréntesis de cierre
#             elif self.curr_char in (')*+?'):
#                 if self.curr_char == ')':
#                     yield Token(TokenType.RPAR, ')')  # ✅ Ahora tiene su valor
#                 elif self.curr_char == '*':
#                     yield Token(TokenType.KLEENE, '*')  # ✅ Ahora tiene su valor
#                 elif self.curr_char == '+':
#                     yield Token(TokenType.PLUS, '+')  # ✅ Ahora tiene su valor
#                 elif self.curr_char == '?':
#                     yield Token(TokenType.QUESTION, '?')  # ✅ Ahora tiene su valor

#                 self.Next()

#                 # Agregar APPEND solo si la siguiente letra lo requiere
#                 if self.curr_char is not None and self.curr_char in LETRAS + '(':
#                     yield Token(TokenType.APPEND, '.')

#             # Si encuentra un punto (concatenación explícita)
#             elif self.curr_char == '.':  
#                 yield Token(TokenType.APPEND, '.')  
#                 self.Next()

#             else:
#                 raise Exception(f'Entrada inválida: {self.curr_char}')

#     def GetSymbols(self):
#         return self.input

from tokens import Token, TokenType

LETTERS = 'abcdefghijklmnopqrstuvwxyz01234567890.'


class DirectReader:

    def __init__(self, string: str):
        self.string = iter(string.replace(' ', ''))
        self.input = set()
        self.rparPending = False
        self.Next()

    def Next(self):
        try:
            self.curr_char = next(self.string)
        except StopIteration:
            self.curr_char = None

    def CreateTokens(self):
            while self.curr_char is not None:

                # Si es una letra válida
                if self.curr_char in LETTERS:
                    self.input.add(self.curr_char)
                    yield Token(TokenType.LETTER, self.curr_char)
                    self.Next()

                    # Agregar APPEND solo si es necesario
                    if self.curr_char is not None and self.curr_char in LETTERS + '(':
                        yield Token(TokenType.APPEND, '.')

                # Si encuentra un OR
                elif self.curr_char == '|':
                    yield Token(TokenType.OR, '|')
                    self.Next()

                # Si encuentra un paréntesis de apertura
                elif self.curr_char == '(':
                    yield Token(TokenType.LPAR, '(')  # ✅ Ahora tiene su valor
                    self.Next()

                # Si encuentra operadores o paréntesis de cierre
                elif self.curr_char in (')*+?'):
                    if self.curr_char == ')':
                        yield Token(TokenType.RPAR, ')')  # ✅ Ahora tiene su valor
                    elif self.curr_char == '*':
                        yield Token(TokenType.KLEENE, '*')  # ✅ Ahora tiene su valor
                    elif self.curr_char == '+':
                        yield Token(TokenType.PLUS, '+')  # ✅ Ahora tiene su valor
                    elif self.curr_char == '?':
                        yield Token(TokenType.QUESTION, '?')  # ✅ Ahora tiene su valor

                    self.Next()

                    # Agregar APPEND solo si la siguiente letra lo requiere
                    if self.curr_char is not None and self.curr_char in LETTERS + '(':
                        yield Token(TokenType.APPEND, '.')

                # Si encuentra un punto (concatenación explícita)
                elif self.curr_char == '.':  
                    yield Token(TokenType.APPEND, '.')  
                    self.Next()

                else:
                    raise Exception(f'Entrada inválida: {self.curr_char}')

    def GetSymbols(self):
        return self.input
