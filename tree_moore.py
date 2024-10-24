from collections import deque, defaultdict
import csv

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.root = False
        self.leaf = False
        self.first = set()
        self.last = set()
        self.Nullable = False
        self.value = ""


leaf_counter = 1


class Tree_Moore():

    # Variable global para numerar las hojas
    global leaf_counter

    def op_order(self,op, T):
        operators = [('|', 1), ('.', 2), ('*', 3), ('?', 3), ('+', 3)]
        op_priority = {op: num for op, num in operators}
        return op_priority.get(op, -1) <= op_priority.get(T, -1)

    def Moore_tree(self,Tokens):
        global leaf_counter
        T = deque()  # Pila de operadores
        S = deque()  # Pila de operandos

        op = ['+', '.', '*', '?', '|']

        for Token in Tokens:
            if Token == '(':
                temp = Node()
                temp.value = Token
                T.append(temp)

            elif Token == ')':
                while T and T[-1].value != '(':
                    if len(S) < 2:
                        return "ERROR: Faltan operandos (1)"
                    temp = T.pop()
                    temp_right = S.pop()
                    temp_left = S.pop()
                    temp.right = temp_right
                    temp.left = temp_left
                    temp_right.parent = temp
                    temp_left.parent = temp

                    # Calcular First, Last y Nullable según las reglas
                    if temp.value == '|':
                        temp.first = temp_left.first | temp_right.first  # F = F(c1) ∪ F(c2)
                        temp.last = temp_left.last | temp_right.last  # L = L(c1) ∪ L(c2)
                        temp.Nullable = temp_left.Nullable or temp_right.Nullable  # N = N(c1) ∨ N(c2)

                    elif temp.value == '.':  # Aquí se ajusta para concatenación únicamente
                        # F = F(c1) ∪ F(c2) si N(c1), si no F = F(c1)
                        if temp_left.Nullable:
                            temp.first = temp_left.first | temp_right.first
                        else:
                            temp.first = temp_left.first

                        # L = L(c1) ∪ L(c2) si N(c2), si no L = L(c2)
                        if temp_right.Nullable:
                            temp.last = temp_left.last | temp_right.last
                        else:
                            temp.last = temp_right.last

                        temp.Nullable = temp_left.Nullable and temp_right.Nullable  # N = N(c1) ∧ N(c2)

                    S.append(temp)

                if not T:
                    return "ERROR: Faltan operandos (2)"
                T.pop()  # Descartar el paréntesis de apertura

            elif Token in op:
                if Token == '*' or Token == '?' or Token == '+':
                    temp = Node()
                    temp.value = Token
                    if len(S) == 0:
                        print("ERROR: Faltan operandos")
                    temp_left = S.pop()
                    temp.left = temp_left
                    temp_left.parent = temp

                    # Calcular First, Last y Nullable
                    temp.first = temp_left.first.copy()  # F = F(c1)
                    temp.last = temp_left.last.copy()    # L = L(c1)

                    if Token == '*':
                        temp.Nullable = True  # N = True (siempre anulable)
                    elif Token == '+':
                        temp.Nullable = temp_left.Nullable  # N = False (no anulable, solo afecta el nodo izquierdo)
                    elif Token == '?':
                        temp.Nullable = True   # N = True (anulable por el ?)

                    S.append(temp)

                else:
                    while T and T[-1].value != '(' and self.op_order(Token, T[-1].value):
                        temp = T.pop()

                        if len(S) < 2:
                            return "ERROR: Faltan operandos (x)"

                        temp_right = S.pop()
                        temp_left = S.pop()
                        temp.right = temp_right
                        temp.left = temp_left
                        temp_left.parent = temp
                        temp_right.parent = temp

                        # Recalcular First, Last y Nullable
                        if temp.value == '.':
                            if temp_left.Nullable:
                                temp.first = temp_left.first | temp_right.first
                            else:
                                temp.first = temp_left.first
                            if temp_right.Nullable:
                                temp.last = temp_left.last | temp_right.last
                            else:
                                temp.last = temp_right.last
                            temp.Nullable = temp_left.Nullable and temp_right.Nullable
                        elif temp.value == '|':
                            temp.first = temp_left.first | temp_right.first
                            temp.last = temp_left.last | temp_right.last
                            temp.Nullable = temp_left.Nullable or temp_right.Nullable

                        S.append(temp)

                    temp = Node()
                    temp.value = Token
                    T.append(temp)

            else:
                temp = Node()
                temp.value = Token
                temp.leaf = True
                temp.first.add(leaf_counter)
                temp.last.add(leaf_counter)
                temp.Nullable = False
                S.append(temp)

                # Numerar la hoja
                print(f"Hoja '{Token}' numerada como {leaf_counter}")
                leaf_counter += 1

        while T:
            temp = T.pop()
            if temp.value == '(':
                return "ERROR: Faltan operandos (3)"
            if len(S) < 2:
                return "ERROR: Faltan operandos (4)"
            temp_right = S.pop()
            temp_left = S.pop()
            temp.right = temp_right
            temp.left = temp_left
            temp_right.parent = temp
            temp_left.parent = temp

            # Recalcular First, Last y Nullable
            if temp.value == '.':
                if temp_left.Nullable:
                    temp.first = temp_left.first | temp_right.first
                else:
                    temp.first = temp_left.first
                if temp_right.Nullable:
                    temp.last = temp_left.last | temp_right.last
                else:
                    temp.last = temp_right.last
                temp.Nullable = temp_left.Nullable and temp_right.Nullable
            elif temp.value == '|':
                temp.first = temp_left.first | temp_right.first
                temp.last = temp_left.last | temp_right.last
                temp.Nullable = temp_left.Nullable or temp_right.Nullable

            S.append(temp)

        if len(S) != 1:
            return "ERROR: Faltan operandos (5)"

        root = Node()

        root = S.pop()

        root.root = True

        return root


        # Calcular los followers
    def calculate_followers(self,node, followers):
        if node is None:
            return

        if node.leaf:
            if node.first:
                for symbol in node.first:
                    if symbol not in followers:
                        followers[symbol] = set()  # Aseguramos que haya una entrada para cada hoja

        # Para concatenación (.)
        if node.value == '.':
            for symbol in node.left.last:
                followers[symbol].update(node.right.first)

        # Para el asterisco (*) y el símbolo más (+)
        if node.value == '*' or node.value == '+':
            for symbol in node.last:
                followers[symbol].update(node.first)

        self.calculate_followers(node.left, followers)
        self.calculate_followers(node.right, followers)

    # Función para imprimir los resultados de FIRST, LAST y NULL en formato CSV
    def print_table_csv(self, root, filename='output.csv'):
        with open(filename, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            # Escribir cabecera
            csv_writer.writerow(['SIMBOLO', 'FIRST', 'LAST', 'NULLABLE'])

            # Recorrer en postorden y escribir en el archivo CSV
            self.postorder_traversal(root, {}, csv_writer)

        print(f"Tabla de FIRST, LAST y NULLABLE exportada a {filename}")

    # Función de recorrido postorden
    def postorder_traversal(self, node, followers, csv_writer):
        if node is not None:
            self.postorder_traversal(node.left, followers, csv_writer)
            self.postorder_traversal(node.right, followers, csv_writer)

            # Asegurarse de que first y last sean listas o conjuntos
            if not isinstance(node.first, (list, set)):
                node.first = [node.first] if node.first else []
            if not isinstance(node.last, (list, set)):
                node.last = [node.last] if node.last else []

            # Escribir directamente las listas first y last en el CSV
            csv_writer.writerow([node.value, list(node.first), list(node.last), str(node.Nullable)])


        # Función para imprimir la tabla de FOLLOWERS
    def print_followers_table(self, followers, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Escribimos el encabezado
            writer.writerow(["SIMBOLO", "FOLLOWERS"])

            # Escribimos las filas de cada símbolo y su conjunto de followers
            for symbol, follower_set in sorted(followers.items()):  # Ordenamos por símbolo
                # Convertimos cada elemento de follower_set a string antes de usar join
                writer.writerow([symbol, ", ".join(map(str, sorted(follower_set)))])




        # Función para imprimir todas las hojas del árbol
    def print_leaves(self, node):
        if node is None:
            return

        # Si el nodo es una hoja, lo imprimimos
        if node.leaf:
            print(f"Hoja: {node.value}")

        # Continuar el recorrido en preorden
        self.print_leaves(node.left)
        self.print_leaves(node.right)



    def Make_Tokens(self,Tokens):

        er = []  # Lista donde se almacenará la expresión regular final con concatenaciones
        op = ['+', '*', '?', '|']  # Operadores comunes de ER

        for Token in Tokens:
            previous_char = ""
            empty = False
            quotes = False
            function = False
            i_quotes = 1
            coin = ""

            for char in Token:

                if empty:

                    if char == ')' or char in op:

                        empty = False

                        er.append(char)

                        previous_char = char

                    elif char == '(':

                        empty = False

                        er.append('.')

                        er.append(char)

                        previous_char = char

                    elif char != ' ':

                        if previous_char == '(' or previous_char == '|':

                            empty = False

                            coin += char

                        elif char == "\'" and previous_char != '(' and previous_char !='|':

                            quotes = True

                            empty = False

                            if previous_char == '(' or previous_char == '|':

                                previous_char = char

                                empty = False

                            else:

                                previous_char = char
                                er.append('.')

                        elif char == '{':

                            function = True

                            er.append('.')

                            coin += char

                            empty = False

                        else:

                            er.append('.')

                            coin += char

                            empty = False

                            previous_char = char

                elif quotes:

                    coin += previous_char

                    if  i_quotes < 2:

                        coin += char

                        i_quotes += 1

                    else:

                        quotes = False

                        er.append(coin)

                        coin = ""

                        i_quotes = 1

                elif function:

                    if char == '}':

                        coin += char

                        er.append(coin)

                        coin = ""

                        function = False

                    else:

                        if char == ' ':

                            continue

                        else:

                            coin += char

                else:

                    if char == '\'':

                        quotes = True

                        if previous_char =='(' or previous_char =='|':

                            previous_char = char

                        else:

                            previous_char = char

                            er.append(".")


                    elif char == ' ':

                        empty = True

                        if coin != "":

                            er.append(coin)

                            coin = ""

                            previous_char = char

                        continue

                    elif char == "(" or char == ")" or char in op:

                        previous_char = char

                        if coin != "":

                            er.append(coin)

                            coin = ""

                        er.append(char)

                    elif previous_char == ')' and char != ')':

                        er.append('.')

                        coin += char

                        previous_char = char

                    elif char == '{':

                        coin += char

                        function = True

                    else:
                        coin += char

        er.pop()

        return er


        # Función para almacenar hojas con símbolos únicos y sus valores de 'first'
    def collect_leaves(self, node, leaf_data):
        if node is None:
            return

        # Si el nodo es una hoja, almacenamos su símbolo y first en el diccionario
        if node.leaf:
            if node.value not in leaf_data:
                # Si el símbolo no está en el diccionario, lo agregamos con su conjunto de 'first'
                leaf_data[node.value] = set(node.first)
            else:
                # Si el símbolo ya existe, agregamos los nuevos 'first' al conjunto existente
                leaf_data[node.value].update(node.first)

        # Continuar el recorrido en preorden
        self.collect_leaves(node.left, leaf_data)
        self.collect_leaves(node.right, leaf_data)

    # Función para iniciar la recolección de símbolos y 'first'
    def collect_leaves_data(self, root):
        leaf_data = {}  # Diccionario para almacenar el símbolo y sus 'first'
        self.collect_leaves(root, leaf_data)
        return leaf_data




 # Función para calcular la tabla de transiciones
def calculate_transitions(followers, root, leaves):
    transitions = {}  # Diccionario para almacenar las transiciones de cada estado
    processed_states = []  # Lista para guardar los estados que ya han sido procesados
    pending_states = [set(root.first)]  # Inicializamos con el first de la raíz como primer estado

    # Procesar cada estado en la lista de pendientes
    while pending_states:
        current_state = pending_states.pop(0)  # Tomamos el primer estado pendiente
        processed_states.append(current_state)  # Lo marcamos como procesado
        state_transitions = {}  # Transiciones de este estado

        # Procesamos cada número/símbolo en el estado actual
        for number in current_state:
            # Buscar el símbolo al que pertenece este número
            for symbol, numbers in leaves.items():
                if number in numbers:
                    if symbol not in state_transitions:
                        state_transitions[symbol] = set()  # Inicializamos un conjunto para este símbolo

                    # Obtenemos los followers asociados a ese número
                    if number in followers:
                        state_transitions[symbol].update(followers[number])  # Actualizamos las transiciones

        # Almacenamos las transiciones del estado actual
        transitions[frozenset(current_state)] = state_transitions

        # Revisamos si los nuevos conjuntos de números (estados) son nuevos
        for next_state in state_transitions.values():
            if next_state not in processed_states and next_state not in pending_states:
                pending_states.append(next_state)  # Añadimos el nuevo estado si no ha sido procesado

    return transitions




# Ejemplo de cómo calcular las transiciones
def print_transitions(root, followers, leaves):
    transitions = calculate_transitions(followers, root, leaves)

    # Imprimir las transiciones en formato legible
    print(f"{'ESTADO':<15} {'SIMBOLO':<10} {'SIGUIENTE ESTADO':<20}")
    print("-" * 45)
    for state, trans in transitions.items():
        for symbol, next_state in trans.items():
            print(f"{str(sorted(state)):<15} {symbol:<10} {str(sorted(next_state)):<20}")



# Función para obtener todos los símbolos únicos
def get_unique_symbols(leaves):
    return sorted(leaves.keys())

import csv

def write_transitions_to_csv(root, followers, leaves, filename):
    transitions = calculate_transitions(followers, root, leaves)
    symbols = get_unique_symbols(leaves)  # Obtener todos los símbolos únicos

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Escribimos la primera fila de encabezados
        writer.writerow(["ESTADO"] + symbols)

        # Escribimos las transiciones por cada estado
        for state, trans in transitions.items():
            # Verificamos si el estado actual no está vacío antes de procesar
            if not state:
                continue  # Omitimos la fila si el estado actual está vacío

            row = [sorted(state)]  # Iniciamos con el estado actual

            for symbol in symbols:
                next_state = sorted(trans.get(symbol, []))  # Obtener siguiente estado o lista vacía
                row.append(next_state)

            # Escribimos la fila incluso si los siguientes estados son vacíos,
            # mientras el estado actual sea válido (no vacío)
            writer.writerow(row)






















