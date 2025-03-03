# from pythomata import SimpleDFA
# from graphviz import Digraph
# from utils import WriteToFile
# from pprint import pprint

# ESTADOS_BRUTO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# class DADF:
#     def __init__(self, arbol, simbolos, expresion_regular):

#         # Useful for syntax tree
#         self.nodos = list()

#         # FA properties
#         self.simbolos = simbolos
#         self.estados = list()
#         self.funcion_transicion = dict()
#         self.estados_aceptacion = set()
#         self.estado_inicial = 'A'

#         # Class properties
#         self.arbol = arbol
#         self.expresion_regular = expresion_regular
#         self.estado_aumentado = None
#         self.iter = 1

#         self.ESTADOS = iter(ESTADOS_BRUTO)
#         try:
#             self.simbolos.remove('e')
#         except:
#             pass

#         # Initialize dfa construction
#         self.ParseArbol(self.arbol)
#         self.CalcSigPos()

#     def CalcSigPos(self):
#         for nodo in self.nodos:
#             if nodo.value == '*':
#                 for i in nodo.ultima_pos:
#                     nodo_hijo = next(filter(lambda x: x._id == i, self.nodos))
#                     nodo_hijo.followpos += nodo.primera_pos
#             elif nodo.value == '.':
#                 for i in nodo.c1.ultima_pos:
#                     nodo_hijo = next(filter(lambda x: x._id == i, self.nodos))
#                     nodo_hijo.followpos += nodo.c2.firstpos

#         # Initiate state generation
#         estado_inicial = self.nodos[-1].firstpos

#         # Filter the nodes that have a symbol
#         self.nodos = list(filter(lambda x: x._id, self.nodos))
#         self.estado_aumentado = self.nodos[-1]._id

#         # Recursion
#         self.CalcularNuevosEstados(estado_inicial, next(self.ESTADOS))

#     def CalcularNuevosEstados(self, estado, estado_actual):

#         if not self.estados:
#             self.estados.append(set(estado))
#             if self.estado_aumentado in estado:
#                 self.estados_aceptacion.update(estado_actual)

#         # Iteramos por cada símbolo
#         for simbolo in self.simbolos:

#             # Get all the nodes with the same symbol in followpos
#             mismos_simbolos = list(
#                 filter(lambda x: x.value == simbolo and x._id in estado, self.nodos))

#             # Create a new state with the nodes
#             nuevo_estado = set()
#             for nodo in mismos_simbolos:
#                 nuevo_estado.update(nodo.followpos)

#             # new state is not in the state list
#             if nuevo_estado not in self.estados and nuevo_estado:

#                 # Get this new state's letter
#                 self.estados.append(nuevo_estado)
#                 nuevo_estado = next(self.ESTADOS)

#                 # Add state to transition function
#                 try:
#                     self.funcion_transicion[nuevo_estado]
#                 except:
#                     self.funcion_transicion[nuevo_estado] = dict()

#                 try:
#                     estados_existentes = self.funcion_transicion[estado_actual]
#                 except:
#                     self.funcion_transicion[estado_actual] = dict()
#                     estados_existentes = self.funcion_transicion[estado_actual]

#                 # Add the reference
#                 estados_existentes[simbolo] = nuevo_estado
#                 self.funcion_transicion[estado_actual] = estados_existentes

#                 # Is it an acceptina_state?
#                 if self.estado_aumentado in nuevo_estado:
#                     self.estados_aceptacion.update(nuevo_estado)

#                 # Repeat with this new state
#                 self.CalcularNuevosEstados(nuevo_estado, nuevo_estado)

#             elif nuevo_estado:
#                 # State already exists... which one is it?
#                 for i in range(0, len(self.estados)):

#                     if self.estados[i] == nuevo_estado:
#                         referencia_estado = ESTADOS_BRUTO[i]
#                         break

#                 # Add the symbol transition
#                 try:
#                     estados_existentes = self.funcion_transicion[estado_actual]
#                 except:
#                     self.funcion_transicion[estado_actual] = {}
#                     estados_existentes = self.funcion_transicion[estado_actual]

#                 estados_existentes[simbolo] = referencia_estado
#                 self.funcion_transicion[estado_actual] = estados_existentes

#     def ParseArbol(self, nodo):
#         nombre_metodo = nodo.__class__.__name__ + 'Node'
#         metodo = getattr(self, nombre_metodo)
#         return metodo(nodo)

#     def LetraNodo(self, nodo):
#         nuevo_nodo = Nodo(self.iter, [self.iter], [
#                         self.iter], valor=nodo.value, anulable=False)
#         self.nodos.append(nuevo_nodo)
#         return nuevo_nodo

#     def OrNodo(self, nodo):
#         nodo_a = self.ParseArbol(nodo.a)
#         self.iter += 1
#         nodo_b = self.ParseArbol(nodo.b)

#         es_anulable = nodo_a.anulable or nodo_b.anulable
#         primera_pos = nodo_a.primera_pos + nodo_b.primera_pos
#         ultima_pos = nodo_a.ultima_pos + nodo_b.ultima_pos

#         self.nodos.append(Nodo(None, primera_pos, ultima_pos,
#                                es_anulable, '|', nodo_a, nodo_b))
#         return Nodo(None, primera_pos, ultima_pos, es_anulable, '|', nodo_a, nodo_b)

#     def AppendNodo(self, nodo):
#         nodo_a = self.ParseArbol(nodo.a)
#         self.iter += 1
#         nodo_b = self.ParseArbol(nodo.b)

#         es_anulable = nodo_a.anulable and nodo_b.anulable
#         if nodo_a.anulable:
#             primera_pos = nodo_a.primera_pos + nodo_b.primera_pos
#         else:
#             primera_pos = nodo_a.primera_pos

#         if nodo_b.anulable:
#             ultima_pos = nodo_b.ultima_pos + nodo_a.ultima_pos
#         else:
#             ultima_pos = nodo_b.ultima_pos

#         self.nodos.append(
#             Nodo(None, primera_pos, ultima_pos, es_anulable, '.', nodo_a, nodo_b))

#         return Nodo(None, primera_pos, ultima_pos, es_anulable, '.', nodo_a, nodo_b)

#     def KleeneNodo(self, nodo):
#         nodo_a = self.ParseArbol(nodo.a)
#         primera_pos = nodo_a.primera_pos
#         ultima_pos = nodo_a.ultima_pos
#         self.nodos.append(Nodo(None, primera_pos, ultima_pos, True, '*', nodo_a))
#         return Nodo(None, primera_pos, ultima_pos, True, '*', nodo_a)

#     def PlusNodo(self, nodo):
#         nodo_a = self.ParseArbol(nodo.a)

#         self.iter += 1

#         nodo_b = self.KleeneNodo(nodo)

#         es_anulable = nodo_a.anulable and nodo_b.anulable
#         if nodo_a.anulable:
#             primera_pos = nodo_a.primera_pos + nodo_b.primera_pos
#         else:
#             primera_pos = nodo_a.primera_pos

#         if nodo_b.anulable:
#             ultima_pos = nodo_b.ultima_pos + nodo_a.ultima_pos
#         else:
#             ultima_pos = nodo_b.ultima_pos

#         self.nodos.append(
#             Nodo(None, primera_pos, ultima_pos, es_anulable, '.', nodo_a, nodo_b))

#         return Nodo(None, primera_pos, ultima_pos, es_anulable, '.', nodo_a, nodo_b)

#     def QuestionNodo(self, nodo):
#         # Node_a is epsilon
#         nodo_a = Nodo(None, list(), list(), True)
#         self.iter += 1
#         nodo_b = self.ParseArbol(nodo.a)

#         es_anulable = nodo_a.anulable or nodo_b.anulable
#         primera_pos = nodo_a.primera_pos + nodo_b.primera_pos
#         ultima_pos = nodo_a.ultima_pos + nodo_b.ultima_pos

#         self.nodos.append(Nodo(None, primera_pos, ultima_pos,
#                                es_anulable, '|', nodo_a, nodo_b))
#         return Nodo(None, primera_pos, ultima_pos, es_anulable, '|', nodo_a, nodo_b)

#     def EvaluarRegex(self):
#         estado_actual = 'A'
#         for simbolo in self.expresion_regular:

#             if not simbolo in self.simbolos:
#                 return 'No'

#             try:
#                 estado_actual = self.funcion_transicion[estado_actual][simbolo]
#             except:
#                 if estado_actual in self.estados_aceptacion and simbolo in self.funcion_transicion['A']:
#                     estado_actual = self.funcion_transicion['A'][simbolo]
#                 else:
#                     return 'No'

#         return 'Yes' if estado_actual in self.estados_aceptacion else 'No'

#     def GraficarDFA(self):
#         estados = set(self.funcion_transicion.keys())
#         alfabeto = set(self.simbolos)

#         afd = SimpleDFA(estados, alfabeto, self.estado_inicial,
#                         self.estados_aceptacion, self.funcion_transicion)

#         graph = afd.trim().to_graphviz()
#         graph.attr(rankdir='LR')

#         source = graph.source
#         WriteToFile('./output/DirectDFA.gv', source)
#         graph.render('./output/DirectDFA.gv', format='pdf', view=True)


# class Nodo:
#     def __init__(self, _id, primera_pos=None, ultima_pos=None, anulable=False, valor=None, c1=None, c2=None):
#         self._id = _id
#         self.primera_pos = primera_pos
#         self.ultima_pos = ultima_pos
#         self.siguientes_pos = list()
#         self.anulable = anulable
#         self.valor = valor
#         self.c1 = c1
#         self.c2 = c2

#     def __repr__(self):
#         return f'''
#     id: {self._id}
#     valor: {self.valor}
#     primera_pos: {self.primera_pos}
#     ultima_pos: {self.ultima_pos}
#     siguientes_pos: {self.siguientes_pos}
#     anulable: {self.anulable}
#     '''
