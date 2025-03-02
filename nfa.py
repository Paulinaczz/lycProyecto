from graphviz import Digraph
from pprint import pprint
from nodes.letter import Letter
from nodes.kleene import Kleene
from nodes.question import Question
from nodes.plus import Plus
from nodes.orNode import Or
from nodes.append import Append
from tokens import TokenType
from utils import WriteToFile
import os

class AFND:
    def __init__(self, arbol, simbolos, expresion_regular):
        # Propiedades de un autómata finito
        self.estados_aceptacion = []
        self.simbolos = simbolos
        self.func_trans = None
        self.estado_act = 1

        # Árbol de nodos y expresión regular
        self.expresion_regular = expresion_regular
        self.arbol = arbol
        self.regexAccepted = None

        # Propiedades para crear el diagrama
        self.dot = Digraph(comment='Diagrama NFA', strict=True)
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='circle')

        # Se ejecuta el algoritmo
        self.Render(arbol)
        self.func_trans = self.GenerarTablaTransicion()
        self.estados_aceptacion = self.GetEstadoAceptacion()

    def Render(self, nodo):
        self.estado_ant = self.estado_act
        nombre_metodo = nodo.__class__.__name__ + 'Node'
        metodo = getattr(self, nombre_metodo)
        return metodo(nodo)

    def LetterNode(self, nodo):
        return nodo.value

    def AppendNode(self, nodo):
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.a))
        self.estado_act += 1
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.b))

    def OrNode(self, nodo):
        nodo_inicial = self.estado_act - 1
        mid_nodo = None

        # Primera transición epsilon
        self.dot.edge(str(nodo_inicial), str(self.estado_act), 'e')
        self.estado_act += 1

        # Transición a la primera rama
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.a))
        mid_nodo = self.estado_act
        self.estado_act += 1

        # Segunda transición epsilon
        self.dot.edge(str(nodo_inicial), str(self.estado_act), 'e')
        self.estado_act += 1

        # from epsilon to second
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.b))
        self.estado_act += 1

        # Transición a la segunda rama
        self.dot.edge(str(mid_nodo), str(self.estado_act), 'e')

        # Transiciones epsilon finales
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), 'e')

    def KleeneNode(self, nodo):

        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), 'e')

        primer_nodo = self.estado_act - 1
        self.estado_act += 1

        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.a))

        # Conexión final de la cerradura de Kleene
        self.dot.edge(str(self.estado_act), str(primer_nodo + 1), 'e')
        self.estado_act += 1

        # Segundo epsilon
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), 'e'
        )

        # Primer epsilon al último estado
        self.dot.edge(str(primer_nodo), str(self.estado_act), 'e')

    def PlusNode(self, nodo):
        self.KleeneNode(nodo)
        self.estado_act += 1

        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.a))

    def QuestionNode(self, nodo):
        nodo_inicial = self.estado_act - 1
        mid_nodo = None

        # Primera epsilon
        self.dot.edge(str(nodo_inicial), str(self.estado_act), 'e')
        self.estado_act += 1

        # Transición a la opción 1
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), self.Render(nodo.a))
        mid_nodo = self.estado_act
        self.estado_act += 1

        # Segunda epsilon
        self.dot.edge(str(nodo_inicial), str(self.estado_act), 'e')
        self.estado_act += 1

        # Otra transicion epsilon para permitir el paso al estado final
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), 'e')
        self.estado_act += 1

        # Transición final
        self.dot.edge(str(mid_nodo), str(self.estado_act), 'e')
        self.dot.edge(str(self.estado_act - 1), str(self.estado_act), 'e')

    def GenerarTablaTransicion(self):
        """Genera la tabla de transiciones del NFA."""
        estados = [i.replace('\t', '') for i in self.dot.source.split('\n') if '->' in i and '=' in i]

        self.func_trans = dict.fromkeys([str(s) for s in range(self.estado_act + 1)])
        self.func_trans[str(self.estado_act)] = dict()

        for estado in estados:
            splitted = estado.split(' ')
            init = splitted[0]
            final = splitted[2]
            simbolo_index = splitted[3].index('=')
            simbolo = splitted[3][simbolo_index + 1]

            try:
                self.func_trans[init][simbolo].append(final)
            except:
                self.func_trans[init] = {simbolo: [final]}

        return self.func_trans

    def GetEstadoAceptacion(self):
        """Obtiene el estado de aceptación del autómata."""
        self.dot.node(str(self.estado_act), shape='doublecircle')
        self.estados_aceptacion.append(self.estado_act)
        return self.estado_act

    def WriteAFNDiagram(self):
        source = self.dot.source
        debug_string = f'''
NFA:
- Símbolos: {self.simbolos}
- Estado final: {self.estados_aceptacion}
- Tabla de transición:
        '''
        # print(debug_string)
        # pprint(self.trans_func)
        WriteToFile('./output/NFA.gv', source)
        self.dot.render('./output/NFA.gv', view=True)
