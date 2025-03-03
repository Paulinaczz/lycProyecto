from pprint import pprint
from pythomata import SimpleDFA
from graphviz import Digraph
from utils import WriteToFile

STATES = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class AFD:
    def __init__(self, tabla_transicion, simbolos, estados, estado_final_afn, expresion_regular):

        # Proveniente del NFA
        self.tabla_transicion = tabla_transicion
        self.estado_final_afn = estado_final_afn

        # Propiedades de un AF
        self.simbolos = simbolos
        self.funcion_transicion = dict()
        self.estados = dict()
        self.estados_aceptacion = list()
        self.estado_inicial = 'A'

        try:
            self.simbolos.remove('e')
        except:
            pass

        self.nodos = []
        self.iteraciones = 0
        self.expresion_regular = expresion_regular

    def MoverA(self, id_nodo, simbolo_eval='e', array=[], agregar_inicial=False, mover_una_vez=False):

        arr = array
        nodo = self.nodos[id_nodo]
        # Recorremos el nodo si no está visitado
        if not nodo.visitado and simbolo_eval in nodo.siguientes_estados:

            # Marcamos el nodo
            nodo.Marcar()
            # Obtenemos los siguientes estados
            siguientes_estados = [int(s) for s in nodo.siguientes_estados[simbolo_eval]]
            if simbolo_eval == 'e':
                arr = [*siguientes_estados]
            else:
                arr = [*siguientes_estados]

            # ¿Tenemos que agregar el nodo inicial?
            if agregar_inicial:
                arr = [*siguientes_estados, id_nodo]

            # Si tenemos que movernos varias veces, habrá que hacerlo de forma recursiva
            if not mover_una_vez:
                for nuevo_id_nodo in nodo.siguientes_estados[simbolo_eval]:
                    arr += [*self.MoverA(int(nuevo_id_nodo), simbolo_eval, arr)]

        return list(set(arr))

    def EvaluarCierre(self, cierre, node,  estado_actual):

        # Estado inicial no creado?
        if not cierre:
            cierre = self.MoverA(0, agregar_inicial=True)
            cierre.append(0)
            self.estados[estado_actual] = cierre
            if self.estado_final_afn in cierre:
                self.estados_aceptacion.append(estado_actual)

        # Por cada símbolo dentro del set...
        for simbolo in self.simbolos:
            cierre_simbolo = list()
            nuevo_conjunto = list()

            # Clausura con el símbolo y el estado
            for valor in cierre:
                cierre_simbolo += self.MoverA(valor, simbolo, mover_una_vez=True)
                [nodo.Desmarcar() for nodo in self.nodos]

            # Clausura con epsilon y el estado
            if cierre_simbolo:
                cierre_epsilon = list()
                for valor_e in cierre_simbolo:
                    cierre_epsilon += self.MoverA(valor_e)
                    [nodo.Desmarcar() for nodo in self.nodos]

                nuevo_conjunto += list(set([*cierre_simbolo, *cierre_epsilon]))

                # Si este nuevo estado no existe es nuevo...
                if not nuevo_conjunto in self.estados.values():
                    self.iteraciones += 1
                    nuevo_estado = STATES[self.iteraciones]

                    # Se crea la entrada en la función de transición
                    try:
                        dict_actual = self.funcion_transicion[estado_actual]
                        dict_actual[simbolo] = nuevo_estado
                    except:
                        self.funcion_transicion[estado_actual] = {simbolo: nuevo_estado}

                    try:
                        self.funcion_transicion[nuevo_estado]
                    except:
                        self.funcion_transicion[nuevo_estado] = {}

                    # Se agrega dicha entrada
                    self.estados[nuevo_estado] = nuevo_conjunto

                    # Si posee el estado final del AFN, entonces agregarlo al set
                    if self.estado_final_afn in nuevo_conjunto:
                        self.estados_aceptacion.append(nuevo_estado)

                    # Repetir con el nuevo set
                    self.EvaluarCierre(nuevo_conjunto, valor, nuevo_estado)

                # Este estado ya existe, se agrega la transición.
                else:
                    for S, V in self.estados.items():
                        if nuevo_conjunto == V:

                            try:
                                dict_actual = self.funcion_transicion[estado_actual]
                            except:
                                self.funcion_transicion[estado_actual] = {}
                                dict_actual = self.funcion_transicion[estado_actual]

                            dict_actual[simbolo] = S
                            self.funcion_transicion[estado_actual] = dict_actual
                            break

    def EvaluarExpresionRegular(self):
        estado_actual = 'A'

        for simbolo in self.expresion_regular:
            # El símbolo no está dentro del set
            if not simbolo in self.simbolos:
                return 'No'
            # Intentamos hacer una transición a un nuevo estado
            try:
                estado_actual = self.funcion_transicion[estado_actual][simbolo]
            except:
                # Volvemos al inicio y verificamos que sea un estado de aceptacion
                if estado_actual in self.estados_aceptacion and simbolo in self.funcion_transicion['A']:
                    estado_actual = self.funcion_transicion['A'][simbolo]
                else:
                    return 'No'

        return 'Yes' if estado_actual in self.estados_aceptacion else 'No'

    def GetEstadosDeterministas(self):
        for estado, valores in self.tabla_transicion.items():
            self.nodos.append(Nodo(int(estado), valores))

    def TransformarAFNaAFD(self):
        self.GetEstadosDeterministas()
        self.EvaluarCierre([], 0, 'A')

    def GraficarAFD(self):
        estados = set(self.funcion_transicion.keys())
        alfabeto = set(self.simbolos)
        estado_inicial = 'A'

        afd = SimpleDFA(estados, alfabeto, estado_inicial,
                        set(self.estados_aceptacion), self.funcion_transicion)

        graph = afd.trim().to_graphviz()
        graph.attr(rankdir='LR')

        source = graph.source
        WriteToFile('./output/DFA.gv', source)
        graph.render('./output/DFA.gv', format='pdf', view=True)

    def EvaluarCadena(self, cadena):
        estado_actual = 'A'

        for simbolo in cadena:
            if simbolo not in self.simbolos:
                return False  # Símbolo no reconocido, cadena inválida

            try:
                estado_actual = self.funcion_transicion[estado_actual][simbolo]
            except KeyError:
                return False  # No hay transición válida

        return estado_actual in self.estados_aceptacion  # Solo retorna True si termina en un estado de aceptación

class Nodo:
    def __init__(self, estado, siguientes_estados):
        self.estado = estado
        self.visitado = False
        self.siguientes_estados = siguientes_estados

    def Marcar(self):
        self.visitado = True

    def Desmarcar(self):
        self.visitado = False

    def __repr__(self):
        return f'{self.estado} - {self.visitado}: {self.siguientes_estados}'
