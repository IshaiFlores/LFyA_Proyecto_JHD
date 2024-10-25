from collections import deque, defaultdict
import csv

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
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

    def Moore_tree(self, Tokens):
        global leaf_counter
        T = deque()  # Pila de operadores
        S = deque()  # Pila de operandos

        # Lista de operadores
        op = ['+', '.', '*', '?', '|']

        # Recorre los tokens (símbolos de la expresión regular)
        for Token in Tokens:
            # Si el token es un paréntesis de apertura
            if Token == '(':
                temp = Node()
                temp.value = Token
                T.append(temp)  # Añade el paréntesis a la pila de operadores

            # Si el token es un paréntesis de cierre
            elif Token == ')':
                # Procesa hasta encontrar el paréntesis de apertura
                while T and T[-1].value != '(':
                    # Verifica que haya suficientes operandos para los operadores
                    if len(S) < 2:
                        return "ERROR: Faltan operandos (1)"
                    temp = T.pop()  # Extrae operador
                    temp_right = S.pop()  # Extrae operando derecho
                    temp_left = S.pop()  # Extrae operando izquierdo
                    temp.right = temp_right
                    temp.left = temp_left
                    temp_right.parent = temp
                    temp_left.parent = temp

                    # Calcula First, Last y Nullable según las reglas
                    if temp.value == '|':
                        # Para unión: F = F(c1) ∪ F(c2), L = L(c1) ∪ L(c2), N = N(c1) ∨ N(c2)
                        temp.first = temp_left.first | temp_right.first
                        temp.last = temp_left.last | temp_right.last
                        temp.Nullable = temp_left.Nullable or temp_right.Nullable

                    elif temp.value == '.':  # Concatenación
                        # F = F(c1) si no es anulable, si no F = F(c1) ∪ F(c2)
                        if temp_left.Nullable:
                            temp.first = temp_left.first | temp_right.first
                        else:
                            temp.first = temp_left.first

                        # L = L(c2) si no es anulable, si no L = L(c1) ∪ L(c2)
                        if temp_right.Nullable:
                            temp.last = temp_left.last | temp_right.last
                        else:
                            temp.last = temp_right.last

                        # N = N(c1) ∧ N(c2)
                        temp.Nullable = temp_left.Nullable and temp_right.Nullable

                    S.append(temp)  # Añade el resultado a la pila de operandos

                if not T:
                    return "ERROR: Faltan operandos (2)"
                T.pop()  # Elimina el paréntesis de apertura

            # Si el token es un operador
            elif Token in op:

                # Operadores unarios (*, ?, +)
                if Token == '*' or Token == '?' or Token == '+':
                    temp = Node()
                    temp.value = Token
                    if len(S) == 0:
                        print("ERROR: Faltan operandos")
                    temp_left = S.pop()  # Extraer único operando
                    temp.left = temp_left
                    temp_left.parent = temp

                    # Calcula First, Last y Nullable
                    temp.first = temp_left.first.copy()  # F = F(c1)
                    temp.last = temp_left.last.copy()    # L = L(c1)

                    # Ajusta según el operador
                    if Token == '*':
                        temp.Nullable = True  # * Siempre es anulable
                    elif Token == '+':
                        temp.Nullable = temp_left.Nullable  # + No es anulable
                    elif Token == '?':
                        temp.Nullable = True  # ? Es anulable

                    S.append(temp)  # Añade a la pila de operandos

                # Operadores binarios (|, .)
                else:
                    # Mientras haya operadores en la pila de operadores con mayor precedencia
                    while T and T[-1].value != '(' and self.op_order(Token, T[-1].value):
                        temp = T.pop()

                        # Verifica que haya suficientes operandos
                        if len(S) < 2:
                            return "ERROR: Faltan operandos (x)"

                        temp_right = S.pop()  # Extrae operando derecho
                        temp_left = S.pop()  # Extrae operando izquierdo
                        temp.right = temp_right
                        temp.left = temp_left
                        temp_left.parent = temp
                        temp_right.parent = temp

                        # Recalcula First, Last y Nullable
                        if temp.value == '.':  # Concatenación
                            if temp_left.Nullable:
                                temp.first = temp_left.first | temp_right.first
                            else:
                                temp.first = temp_left.first
                            if temp_right.Nullable:
                                temp.last = temp_left.last | temp_right.last
                            else:
                                temp.last = temp_right.last
                            temp.Nullable = temp_left.Nullable and temp_right.Nullable

                        elif temp.value == '|':  # Unión
                            temp.first = temp_left.first | temp_right.first
                            temp.last = temp_left.last | temp_right.last
                            temp.Nullable = temp_left.Nullable or temp_right.Nullable

                        S.append(temp)  # Añade el nodo a la pila de operandos

                    temp = Node()
                    temp.value = Token
                    T.append(temp)  # Añade el operador a la pila de operadores

            # Si el token es un símbolo (hoja)
            else:
                temp = Node()
                temp.value = Token
                temp.leaf = True  # Es una hoja
                temp.first.add(leaf_counter)  # Asigna el número de hoja
                temp.last.add(leaf_counter)
                temp.Nullable = False  # Las hojas no son anulables
                S.append(temp)  # Añade el nodo a la pila de operandos

                # Numera cada hoja
                print(f"Hoja '{Token}' numerada como {leaf_counter}")
                leaf_counter += 1

        # Procesa operadores restantes en la pila
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

            # Recalcula First, Last y Nullable
            if temp.value == '.':  # Concatenación
                if temp_left.Nullable:
                    temp.first = temp_left.first | temp_right.first
                else:
                    temp.first = temp_left.first
                if temp_right.Nullable:
                    temp.last = temp_left.last | temp_right.last
                else:
                    temp.last = temp_right.last
                temp.Nullable = temp_left.Nullable and temp_right.Nullable
            elif temp.value == '|':  # Unión
                temp.first = temp_left.first | temp_right.first
                temp.last = temp_left.last | temp_right.last
                temp.Nullable = temp_left.Nullable or temp_right.Nullable

            S.append(temp)  # Añade el nodo a la pila de operandos

        # Verifica que el árbol sea correcto (debe haber un solo nodo en S)
        if len(S) != 1:
            return "ERROR: Faltan operandos (5)"

        # El nodo restante en S es la raíz del árbol de expresión
        root = S.pop()

        #Se retorna la raíz del árbol de expresión
        return root



    # Calcula los followers
    # Esta función calcula los followers de cada nodo en el árbol
    # con base en las reglas para concatenación
    # (.), repetición (*) y el símbolo más (+).

    def calculate_followers(self, node, followers):

        if node is None:
            return

        # Si es una hoja, se asegura de que haya una entrada en followers para cada símbolo
        if node.leaf:
            if node.first:
                for symbol in node.first:
                    if symbol not in followers:
                        followers[symbol] = set()  # Se asegura que haya una entrada para cada hoja

        # Para concatenación (.). Se añaden los símbolos de first del nodo derecho
        # a los followers de los símbolos de last del nodo izquierdo
        if node.value == '.':
            for symbol in node.left.last:
                followers[symbol].update(node.right.first)

        # Para los operadores unarios '*' (cero o más repeticiones) y '+' (una o más repeticiones)
        # Los símbolos en last se añaden a los followers de los símbolos en first.
        if node.value == '*' or node.value == '+':
            for symbol in node.last:
                followers[symbol].update(node.first)

        # Llamadas recursivas para calcular followers en los subárboles izquierdo y derecho
        self.calculate_followers(node.left, followers)
        self.calculate_followers(node.right, followers)




    # Función para imprimir los resultados de FIRST, LAST y NULLABLE en formato CSV
    # Exporta los conjuntos first, last y la propiedad nullable de cada nodo en un archivo CSV,
    # presentando la información de forma más agrdable sobre cada símbolo dentro de la expresión regular.
    def print_table_csv(self, root, filename='output.csv'):
        with open(filename, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            # Escribir cabecera de la tabla CSV (columnas: símbolo, first, last, nullable)
            csv_writer.writerow(['SIMBOLO', 'FIRST', 'LAST', 'NULLABLE'])

            # Llama a la función de recorrido postorden para escribir cada nodo
            # en el archivo CSV
            self.postorder_traversal(root, {}, csv_writer)

        print(f"Tabla de FIRST, LAST y NULLABLE exportada a {filename}")



    # Función de recorrido postorden
    # Esta función realiza un recorrido postorden del árbol de expresión regular,
    # evaluando primero los subárboles y luego el nodo actual. A medida que recorre los nodos,
    # escribe los valores first, last y nullable en el archivo CSV.
    def postorder_traversal(self, node, followers, csv_writer):
        if node is not None:
            # Recorrer primero el subárbol izquierdo
            self.postorder_traversal(node.left, followers, csv_writer)
            # Luego el subárbol derecho
            self.postorder_traversal(node.right, followers, csv_writer)

            # Asegurarse de que las propiedades first y last sean listas o conjuntos,
            # para evitar errores al escribir en el CSV
            if not isinstance(node.first, (list, set)):
                node.first = [node.first] if node.first else []
            if not isinstance(node.last, (list, set)):
                node.last = [node.last] if node.last else []

            # Escribir directamente las listas first y last en el archivo CSV junto con
            # el símbolo del nodo y si es anulable o no
            csv_writer.writerow([node.value, list(node.first), list(node.last), str(node.Nullable)])



    # Función para imprimir la tabla de FOLLOWERS
    # Esta función exporta la tabla de followers a un archivo CSV.
    def print_followers_table(self, followers, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Se escribe el encabezado de la tabla CSV (columnas: símbolo, followers)
            writer.writerow(["SIMBOLO", "FOLLOWERS"])

            # Se itera sobre los elementos del diccionario followers, ordenando por símbolo.
            # Para cada símbolo, se escribe el conjunto de followers asociado.
            for symbol, follower_set in sorted(followers.items()):  # Ordena por símbolo

                # Se convierte cada elemento del conjunto de followers en string, y luego
                # se unen utilizando comas para almacenarlos en el archivo CSV
                writer.writerow([symbol, ", ".join(map(str, sorted(follower_set)))])




    # Función para imprimir todas las hojas del árbol
    # Esta función recorre el árbol de expresión regular e imprime todos los nodos que son hojas,
    # es decir, los símbolos terminales de la expresión regular.
    def print_leaves(self, node):
        if node is None:
            return

        # Si el nodo actual es una hoja, imprimimos su valor (el símbolo que representa)
        if node.leaf:
            print(f"Hoja: {node.value}")

        # Llamadas recursivas para continuar el recorrido en preorden (primero el nodo actual,
        # luego el subárbol izquierdo y finalmente el subárbol derecho)
        self.print_leaves(node.left)
        self.print_leaves(node.right)



    # Función para procesar la entrada de tokens y agregar concatenaciones implícitas
    # Esta función toma una lista de tokens y genera una expresión regular final con los
    # operadores de concatenación explícitamente añadidos donde sea necesario.
    def Make_Tokens(self, Tokens):

        er = []  # Lista donde se almacenará la expresión regular final con concatenaciones
        op = ['+', '*', '?', '|']  # Operadores comunes de expresiones regulares (ER)

        for Token in Tokens:
            previous_char = ""  # Variable para almacenar el último carácter procesado
            empty = False  # Bandera para manejar los espacios
            quotes = False  # Bandera para manejar símbolos dentro de comillas
            function = False  # Bandera para manejar funciones o bloques delimitados por llaves
            i_quotes = 1  # Contador para controlar los símbolos dentro de comillas
            coin = ""  # Variable temporal para construir tokens compuestos

            # Recorrido por cada caracter del token actual
            for char in Token:

                # Si se encontró un espacio vacío
                if empty:
                    if char == ')' or char in op:  # Si el caracter es un operador o paréntesis
                        empty = False
                        er.append(char)  # Se agrega el caracter actual a la ER final
                        previous_char = char  # Se actualiza el caracter previo

                    elif char == '(':  # Si se encuentra un paréntesis de apertura
                        empty = False
                        er.append('.')  # Se añade la concatenación implícita antes del paréntesis
                        er.append(char)
                        previous_char = char

                    elif char != ' ':  # Si no es espacio
                        if previous_char == '(' or previous_char == '|':  # Dependiendo del contexto previo
                            empty = False
                            coin += char  # Se añade el caracter al token temporal

                        elif char == "\'" and previous_char != '(' and previous_char != '|':  # Si es una comilla
                            quotes = True  # Se activa la bandera de comillas
                            empty = False  # Se desactiva la bandera de vacío

                            if previous_char == '(' or previous_char == '|': #Depende del contexto previo
                                previous_char = char    #Se continua con el siguiente caracter y se actualiza el caracter anterior
                                empty = False
                            else:
                                previous_char = char
                                er.append('.')  # Se añade la concatenación antes de comillas

                        elif char == '{':  # Si se encuentra una llave de apertura (inicio de una función)
                            function = True  # Se activa la bandera de función
                            er.append('.')  # Se añade concatenación antes de la función
                            coin += char    #Se concatena el caracter al token compuesto
                            empty = False

                        else:
                            er.append('.')  # Se añade la concatenación antes de cualquier carácter
                            coin += char  # Se construye el token temporal
                            empty = False
                            previous_char = char

                # Si estamos dentro de comillas
                elif quotes:
                    coin += previous_char  # Se añade el caracter previo a la moneda (token temporal)

                    if i_quotes < 2:  # Se verifica la longitud de la secuencia de comillas
                        coin += char
                        i_quotes += 1
                    else:
                        quotes = False  # Se sale del contexto de comillas
                        er.append(coin)  # Se añade el token formado a la ER final
                        coin = ""
                        i_quotes = 1

                # Si estamos procesando una función
                elif function:
                    if char == '}':  # Si se encuentra el cierre de la función
                        coin += char
                        er.append(coin)  # Se añade la función a la ER final
                        coin = ""
                        function = False
                    else:
                        if char == ' ':  # Se ignoran los espacios dentro de funciones
                            continue
                        else:
                            coin += char  # Se añaden los caracteres a la función

                # Si no estamos en contexto de espacios, comillas o funciones
                else:
                    if char == '\'':  # Si encontramos una comilla, entramos en modo "quotes"
                        quotes = True
                        if previous_char == '(' or previous_char == '|':
                            previous_char = char
                        else:
                            previous_char = char
                            er.append(".")

                    elif char == ' ':  # Si se encuentra un espacio
                        empty = True  # Se activa la bandera de espacio
                        if coin != "":  # Si el token temporal no está vacío
                            er.append(coin)  # Se añade el token a la ER final
                            coin = ""
                            previous_char = char

                        continue  # Continuamos con el siguiente carácter

                    elif char == "(" or char == ")" or char in op:  # Si se encuentra un operador o paréntesis
                        previous_char = char
                        if coin != "":  # Si el token temporal no está vacío
                            er.append(coin)  # Se añade el token a la ER final
                            coin = ""
                        er.append(char)  # Se añade el operador o paréntesis a la ER final

                    elif previous_char == ')' and char != ')':  # Si hay concatenación después de un paréntesis
                        er.append('.')  # Se añade la concatenación
                        coin += char
                        previous_char = char

                    elif char == '{':  # Si encontramos una llave de apertura
                        coin += char
                        function = True  # Se activa la bandera de función

                    else:
                        coin += char  # Se añaden los caracteres al token temporal

        er.pop()  # Se elimina el último elemento que contiene la ultima bifurcación (|)
        return er  # Se retorna la expresión regular final con ;as concatenaciones añadidas



        # Función para recolectar las hojas del árbol que tienen símbolos únicos y sus valores 'first'
    # Recorre el árbol en preorden y almacena en un diccionario las hojas con sus conjuntos 'first'
    def collect_leaves(self, node, leaf_data):
        if node is None:
            return

        # Si el nodo es una hoja, almacenamos su símbolo y conjunto 'first'
        if node.leaf:
            if node.value not in leaf_data:
                # Si el símbolo no está en el diccionario, lo agregamos con su conjunto 'first'
                leaf_data[node.value] = set(node.first)
            else:
                # Si el símbolo ya existe, añadimos los nuevos valores 'first' al conjunto existente
                leaf_data[node.value].update(node.first)

        # Continuamos el recorrido en preorden
        self.collect_leaves(node.left, leaf_data)
        self.collect_leaves(node.right, leaf_data)


    # Función para iniciar la recolección de los símbolos y valores 'first'
    # Llama a la función 'collect_leaves' y devuelve un diccionario con los datos recolectados
    def collect_leaves_data(self, root):
        leaf_data = {}  # Diccionario para almacenar el símbolo y sus valores 'first'
        self.collect_leaves(root, leaf_data)
        return leaf_data


    # Función para calcular la tabla de transiciones de estados
    # Usa los conjuntos de followers y las hojas del árbol para determinar las transiciones
    def calculate_transitions(self,followers, root, leaves):
        transitions = {}  # Diccionario para almacenar las transiciones de cada estado
        processed_states = []  # Lista para guardar los estados que ya han sido procesados
        pending_states = [set(root.first)]  # Inicializamos con el conjunto 'first' de la raíz como primer estado

        # Procesamos cada estado en la lista de estados pendientes
        while pending_states:
            current_state = pending_states.pop(0)  # Tomamos el primer estado pendiente
            processed_states.append(current_state)  # Marcamos el estado como procesado
            state_transitions = {}  # Diccionario para almacenar las transiciones del estado actual

            # Procesamos cada número/símbolo dentro del estado actual
            for number in current_state:
                # Buscamos el símbolo al que pertenece el número en las hojas
                for symbol, numbers in leaves.items():
                    if number in numbers:
                        if symbol not in state_transitions:
                            state_transitions[symbol] = set()  # Inicializamos un conjunto para el símbolo

                        # Obtenemos los followers asociados al número y actualizamos las transiciones
                        if number in followers:
                            state_transitions[symbol].update(followers[number])

            # Almacenamos las transiciones del estado actual en el diccionario
            transitions[frozenset(current_state)] = state_transitions

            # Revisamos si los nuevos conjuntos de estados son nuevos
            for next_state in state_transitions.values():
                if next_state not in processed_states and next_state not in pending_states:
                    pending_states.append(next_state)  # Añadimos el nuevo estado a la lista si no ha sido procesado

        return transitions

    # Función para imprimir las transiciones calculadas
    # Muestra la tabla de transiciones entre estados
    def print_transitions(self,root, followers, leaves):
        transitions = self.calculate_transitions(followers, root, leaves)

        # Formato de impresión de la tabla de transiciones
        print(f"{'ESTADO':<15} {'SIMBOLO':<10} {'SIGUIENTE ESTADO':<20}")
        print("-" * 45)
        for state, trans in transitions.items():
            for symbol, next_state in trans.items():
                # Imprime el estado actual, el símbolo y el siguiente estado
                print(f"{str(sorted(state)):<15} {symbol:<10} {str(sorted(next_state)):<20}")

    # Función para obtener todos los símbolos únicos del diccionario de hojas
    # Devuelve una lista de símbolos únicos ordenados alfabéticamente
    def get_unique_symbols(self,leaves):
        return sorted(leaves.keys())


    # Función para escribir las transiciones en un archivo CSV
    # Genera un archivo CSV con las transiciones de estados entre símbolos
    def write_transitions_to_csv(self, root, followers, leaves, filename):
        transitions = self.calculate_transitions(followers, root, leaves)
        symbols = self.get_unique_symbols(leaves)  # Obtenemos los símbolos únicos

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Escribimos la primera fila de encabezados (símbolos)
            writer.writerow(["ESTADO"] + symbols)

            # Escribimos las transiciones por cada estado
            for state, trans in transitions.items():
                if not state:
                    continue  # Omitimos la fila si el estado actual está vacío

                row = [sorted(state)]  # Iniciamos con el estado actual

                # Añadimos el siguiente estado para cada símbolo
                for symbol in symbols:
                    next_state = sorted(trans.get(symbol, []))  # Obtenemos el siguiente estado o lista vacía
                    row.append(next_state)

                # Escribimos la fila en el archivo CSV
                writer.writerow(row)























