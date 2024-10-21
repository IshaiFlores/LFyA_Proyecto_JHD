from collections import deque

class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.root = False
        self.leaf = False
        self.first = []
        self.last = []
        self.Nullable = False
        self.value = ""

def op_order(op, T):
    operators  = [('|', 1), ('.', 2), ('*', 3), ('?', 3), ('+', 3)]
    op_priority = {op: num for op, num in operators}

    test = op_priority.get(op, -1) <= op_priority.get(T, -1)

    return test

def Moore_tree(Tokens):
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
                S.append(temp)

            if not T:
                return "ERROR: Faltan operandos (2)"

            T.pop()  # Descartar el paréntesis de apertura

        elif Token in op:

            if Token == '+' or Token == '*' or Token == '?':

                temp = Node()

                temp.value = Token

                if len(S) == 0:
                    print("ERROR: Faltan operandos")

                temp_left = S.pop()

                temp.left = temp_left

                temp_left.parent = temp

                S.append(temp)

            else:

                while T and T[-1].value != '(' and op_order(Token, T[-1].value):
                    temp = T.pop()

                    if len(S) < 2:
                        return "ERROR: Faltan operandos(x)"
                    temp_right = S.pop()
                    temp_left = S.pop()
                    temp.right = temp_right
                    temp.left = temp_left
                    temp_left.parent = temp
                    temp_right.parent = temp
                    S.append(temp)


                temp = Node()
                temp.value = Token
                T.append(temp)

        else:
            temp = Node()
            temp.value = Token
            S.append(temp)

    while T:
        temp = T.pop()
        if temp.value == '(':
            return "ERROR: Faltan operandos(3)"
        if len(S) < 2:
            return "ERROR: Faltan operandos(4)"
        temp_right = S.pop()
        temp_left = S.pop()
        temp.right = temp_right
        temp.left = temp_left
        temp_right.parent = temp
        temp_left.parent = temp
        S.append(temp)

    if len(S) != 1:
        return "ERROR: Faltan operandos(5)"

    return S.pop()


# Función para mostrar el árbol en preorden
def print_tree(node, level=0):
    if node is not None:
        # Mostrar el nodo actual con indentación dependiendo del nivel
        print("  " * level + f"{node.value}")
        # Recorrer el hijo izquierdo
        print_tree(node.left, level + 1)
        # Recorrer el hijo derecho
        print_tree(node.right, level + 1)


# Prueba con la expresión proporcionada
expresion = "((a|b)*.a.b.b).#"
resultado = Moore_tree(expresion)
# Mostrar el árbol si no hubo errores
if isinstance(resultado, Node):
    print("Árbol de la expresión:")
    print_tree(resultado)
else:
    print(resultado)

#Muestra el recorrido en Preorden