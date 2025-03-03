from pythomata import SimpleDFA
from utils import WriteToFile

ESTADOS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class AFD:
    def __init__(self, tabla_transicion, simbolos, estado_final_afn, expresion_regular):
        # Inicialización de atributos básicos
        self.estado_inicial = 'A'
        self.estado_final_afn = estado_final_afn
        self.expresion_regular = expresion_regular

        # Propiedades relacionadas con el autómata
        self.tabla_transicion = tabla_transicion
        self.simbolos = simbolos

        # Estructuras para manejar el AFD
        self.funcion_transicion = {}
        self.estados = {}
        self.estados_aceptacion = []
        self.nodos = []
        self.iteraciones = 0

        # Eliminar el símbolo epsilon si existe
        self.EliminarEpsilon()
        

    def EliminarEpsilon(self):
        try:
            self.simbolos.remove('e')
        except:
            pass

    def MoverA(self, id_nodo, simbolo_eval='e', array=None, agregar_inicial=False, mover_una_vez=False):
        if array is None:
            array = []
        nodo = self.nodos[id_nodo]

        # Recorremos el nodo solo si no está visitado
        if not nodo.visitado and simbolo_eval in nodo.siguientes_estados:
            nodo.Marcar() # Marcamos el nodo como visitado
            
            # Obtenemos los siguientes estados
            siguientes_estados = [int(s) for s in nodo.siguientes_estados[simbolo_eval]]
            array.extend(siguientes_estados)

            # ¿Tenemos que agregar el nodo inicial?
            if agregar_inicial:
                array.append(id_nodo)

            # Si tenemos que movernos varias veces, habrá que hacerlo de forma recursiva
            if not mover_una_vez:
                for nuevo_id_nodo in siguientes_estados:
                    self.MoverA(nuevo_id_nodo, simbolo_eval, array, agregar_inicial, mover_una_vez)

        return list(set(array))

    def EvaluarCierre(self, cierre, node,  estado_actual):

        # Verificar si la clausura aún no ha sido calculada
        if not cierre:
            cierre = self.MoverA(0, agregar_inicial=True)
            cierre.append(0) # Asegurarse de incluir el estado inicial (0)
            self.estados[estado_actual] = cierre
            if self.estado_final_afn in cierre:
                self.estados_aceptacion.append(estado_actual)

        # Por cada símbolo dentro del conjunto de símbolos
        for simbolo in self.simbolos:
            cierre_simbolo = []
            nuevo_conjunto = []
            # Clausura con el símbolo y el estado
            for valor in cierre:
                cierre_simbolo += self.MoverA(valor, simbolo, mover_una_vez=True)
                [nodo.Desmarcar() for nodo in self.nodos]
            # Clausura con epsilon y el estado
            if cierre_simbolo:
                cierre_epsilon = []
                for valor_e in cierre_simbolo:
                    cierre_epsilon += self.MoverA(valor_e)
                    [nodo.Desmarcar() for nodo in self.nodos]
                nuevo_conjunto += cierre_simbolo
                nuevo_conjunto += cierre_epsilon
                # Eliminar duplicados usando set()
                nuevo_conjunto = list(set(nuevo_conjunto))

                # Verificar si el nuevo conjunto ya ha sido procesado
                if not nuevo_conjunto in self.estados.values():
                    self.iteraciones += 1
                    nuevo_estado = ESTADOS[self.iteraciones]

                    # Intentamos agregar la transición para el estado actual
                    try:
                        dict_actual = self.funcion_transicion[estado_actual]
                        dict_actual[simbolo] = nuevo_estado
                    except:
                        # Si no existe la transición para el estado actual, la creamos
                        self.funcion_transicion[estado_actual] = {simbolo: nuevo_estado}

                    try:
                        self.funcion_transicion[nuevo_estado]
                    except:
                        # Si el nuevo estado no tiene transiciones, lo inicializamos
                        self.funcion_transicion[nuevo_estado] = {}

                    self.estados[nuevo_estado] = nuevo_conjunto

                    # Si posee el estado final del AFN, entonces lo agregamos aceptación
                    if self.estado_final_afn in nuevo_conjunto:
                        self.estados_aceptacion.append(nuevo_estado)

                    # Llamada recursiva para procesar el nuevo conjunto de estados
                    self.EvaluarCierre(nuevo_conjunto, valor, nuevo_estado)

                # Si el estado ya existe, se agrega la transición.
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
