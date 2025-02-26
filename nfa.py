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


class NFA:
    def __init__(self, tree, symbols, regex):
        # Propiedades de un autómata finito
        self.accepting_states = []
        self.symbols = symbols
        self.trans_func = None
        self.curr_state = 1

        # Árbol de nodos y expresión regular
        self.regex = regex
        self.tree = tree
        self.regexAccepted = None

        # Propiedades para crear el diagrama
        self.dot = Digraph(comment='Diagrama NFA', strict=True)
        self.dot.attr(rankdir='LR')
        self.dot.attr('node', shape='circle')

        # Se ejecuta el algoritmo
        self.Render(tree)
        self.trans_func = self.GenerateTransitionTable()
        self.accepting_states = self.GetAcceptingState()

    def Render(self, node):
        self.prev_state = self.curr_state
        method_name = node.__class__.__name__ + 'Node'
        method = getattr(self, method_name)
        return method(node)

    def LetterNode(self, node):
        return node.value

    def AppendNode(self, node):
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.a)
        )

        self.curr_state += 1
        self.dot.edge(
            str(self.curr_state - 1),
            str(self.curr_state),
            self.Render(node.b)
        )

    def OrNode(self, node):
        initial_node = self.curr_state - 1
        mid_node = None

        # Primera transición epsilon
        self.dot.edge(str(initial_node), str(self.curr_state), 'e')
        self.curr_state += 1

        # Transición a la primera rama
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), self.Render(node.a))
        mid_node = self.curr_state
        self.curr_state += 1

        # Segunda transición epsilon
        self.dot.edge(str(initial_node), str(self.curr_state), 'e')
        self.curr_state += 1

        # Transición a la segunda rama
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), self.Render(node.b))
        self.curr_state += 1

        # Transiciones epsilon finales
        self.dot.edge(str(mid_node), str(self.curr_state), 'e')
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), 'e')

    def KleeneNode(self, node):
        first_node = self.curr_state - 1
        self.dot.edge(str(first_node), str(self.curr_state), 'e')

        self.curr_state += 1
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), self.Render(node.a))

        # Conexión final de la cerradura de Kleene
        self.dot.edge(str(self.curr_state), str(first_node + 1), 'e')
        self.curr_state += 1
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), 'e')
        self.dot.edge(str(first_node), str(self.curr_state), 'e')

    def PlusNode(self, node):
        self.KleeneNode(node)
        self.curr_state += 1
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), self.Render(node.a))

    def QuestionNode(self, node):
        initial_node = self.curr_state - 1
        mid_node = None

        # Primera epsilon
        self.dot.edge(str(initial_node), str(self.curr_state), 'e')
        self.curr_state += 1

        # Transición a la opción 1
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), self.Render(node.a))
        mid_node = self.curr_state
        self.curr_state += 1

        # Segunda epsilon
        self.dot.edge(str(initial_node), str(self.curr_state), 'e')
        self.curr_state += 1

        # Transición final
        self.dot.edge(str(self.curr_state - 1), str(self.curr_state), 'e')
        self.dot.edge(str(mid_node), str(self.curr_state), 'e')

    def GenerateTransitionTable(self):
        """Genera la tabla de transiciones del NFA."""
        states = [i.replace('\t', '') for i in self.dot.source.split('\n') if '->' in i and '=' in i]

        self.trans_func = dict.fromkeys([str(s) for s in range(self.curr_state + 1)])
        self.trans_func[str(self.curr_state)] = dict()

        for state in states:
            splitted = state.split(' ')
            init = splitted[0]
            final = splitted[2]
            symbol_index = splitted[3].index('=')
            symbol = splitted[3][symbol_index + 1]

            try:
                self.trans_func[init][symbol].append(final)
            except:
                self.trans_func[init] = {symbol: [final]}

        return self.trans_func

    def GetAcceptingState(self):
        """Obtiene el estado de aceptación del autómata."""
        self.dot.node(str(self.curr_state), shape='doublecircle')
        self.accepting_states.append(self.curr_state)
        return self.curr_state

    def WriteNFADiagram(self):
        if not os.path.exists("./output"):
            os.makedirs("./output")

        # 🔹 Eliminar transiciones con `#` antes de generar el gráfico
        estados_a_remover = []
        for estado, transiciones in list(self.trans_func.items()):  # Convertimos a lista para evitar RuntimeError
            if '#' in transiciones:
                estados_a_remover.append(estado)
                del transiciones['#']  # ✅ Eliminar la transición con `#`

        # 🔹 También eliminamos el estado de aceptación si está vinculado con `#`
        for estado in estados_a_remover:
            if estado in self.accepting_states:
                self.accepting_states.remove(estado)

        # 🔹 Eliminar la transición `#` en el archivo fuente de Graphviz
        dot_lines = self.dot.source.split("\n")
        dot_lines = [line for line in dot_lines if "->" not in line or "#" not in line]

        # Guardar el archivo sin `#`
        source = "\n".join(dot_lines)
        with open("./output/NFA.gv", "w") as f:
            f.write(source)

        print("\n✅ Diagrama del AFND generado sin `#`. Abriendo archivo...")

        self.dot.render("./output/NFA.gv", view=True)
