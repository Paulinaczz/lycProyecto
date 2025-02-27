from tokens import TokenType
from nodes.letter import Letter
from nodes.kleene import Kleene
from nodes.question import Question
from nodes.plus import Plus
from nodes.orNode import Or
from nodes.append import Append


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.Siguiente()

    def Siguiente(self):
        try:
            self.token_act = next(self.tokens)
        except StopIteration:
            self.token_act = None

    def NuevoSimbolo(self):
        token = self.token_act

        if token.tipo == TokenType.LPAR:
            self.Siguiente()
            res = self.Expresion()

            if self.token_act.tipo != TokenType.RPAR:
                raise Exception('No right parenthesis for expression!')

            self.Siguiente()
            return res

        elif token.tipo == TokenType.LETTER:
            self.Siguiente()
            return Letter(token.value)

    def NuevoOperador(self):
        res = self.NuevoSimbolo()

        while self.token_act != None and \
                (
                    self.token_act.tipo == TokenType.KLEENE or
                    self.token_act.tipo == TokenType.PLUS or
                    self.token_act.tipo == TokenType.QUESTION
                ):
            if self.token_act.tipo == TokenType.KLEENE:
                self.Siguiente()
                res = Kleene(res)
            elif self.token_act.tipo == TokenType.QUESTION:
                self.Siguiente()
                res = Question(res)
            else:
                self.Siguiente()
                res = Plus(res)

        return res

    def Expresion(self):
        res = self.NuevoOperador()

        while self.token_act != None and \
                (
                    self.token_act.tipo == TokenType.APPEND or
                    self.token_act.tipo == TokenType.OR
                ):
            if self.token_act.tipo == TokenType.OR:
                self.Siguiente()
                res = Or(res, self.NuevoOperador())

            elif self.token_act.tipo == TokenType.APPEND:
                self.Siguiente()
                res = Append(res, self.NuevoOperador())

        return res

    def Parse(self):
        if self.token_act == None:
            return None

        res = self.Expresion()

        return res
