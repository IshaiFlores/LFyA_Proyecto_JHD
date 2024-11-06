def ExpressionScanner(expression, transiciones, actions, leaves, root):
    # Define el estado inicial explícitamente como el frozenset correspondiente
    initial_state = frozenset(root.first)
    current_state = initial_state  # Estado actual comienza en el estado inicial
    expression_dictionary = {}  # Diccionario para registrar los estados recorridos por cada símbolo de la expresión

    cadena_acumulada = ""  # Acumula la cadena de caracteres hasta que se identifique un token
    complete = False

    list_expression = list(expression)
    idx = 0

    while idx < len(list_expression):

        char = list_expression[idx]
        quoted_char = f"'{char}'"  # Encierran el símbolo entre comillas para compararlo en transiciones

        if char == " " and complete == True:
            idx += 1
            continue

        elif char != " " and complete == True:

            complete = False

        # Determina el tipo de símbolo actual (LETRA, DIGITO o CHARSET)
        symbol_type = None
        if char.isalpha():
            symbol_type = "LETRA"
        elif char.isdigit():
            symbol_type = "DIGITO"
        elif 32 <= ord(char) <= 254:
            symbol_type = "CHARSET"

        # Verifica si hay una transición para el símbolo actual
        if current_state in transiciones:
            if quoted_char in leaves and quoted_char in transiciones[current_state]:
                # Si el símbolo específico (con comillas) está en leaves y tiene una transición, la tomamos
                next_state = frozenset(transiciones[current_state][quoted_char])
                current_state = next_state
                cadena_acumulada += char
                idx += 1  # Solo avanzamos al siguiente carácter si hay una transición válida
            elif symbol_type in leaves and symbol_type in transiciones[current_state]:
                # Si el tipo de símbolo está en leaves y tiene una transición, la tomamos
                next_state = frozenset(transiciones[current_state][symbol_type])
                current_state = next_state
                cadena_acumulada += char
                idx += 1  # Solo avanzamos al siguiente carácter si hay una transición válida
            else:
                complete = True

        # Cuando no hay más transiciones, intentamos detectar el token
        if complete:
            expression_dictionary = TokenAnalysis(cadena_acumulada, current_state, leaves, expression_dictionary,actions)

            # Usamos TokenAnalysis para registrar el token detectado
            if expression_dictionary is not None:
                # Reinicia la cadena acumulada y vuelve al estado inicial para continuar
                cadena_acumulada = ""
                current_state = initial_state
                complete = True  # Restablece el indicador de completitud
            else:
                # No encontramos transición ni token, marcamos error
                print(f"Error: Simbolo {char} no coincide con ningún Token.")
                return None

    # Realiza un último análisis de token para la cadena acumulada final
    if cadena_acumulada:
        expression_dictionary = TokenAnalysis(cadena_acumulada, current_state, leaves, expression_dictionary,actions)

        if expression_dictionary is None:
            # No encontramos transición ni token, marcamos error
            print(f"Error: Simbolo '{cadena_acumulada[-1]}' no coincide con ningún Token.")
            return None

        # Al final de ExpressionScanner, después de retornar el diccionario
    if expression_dictionary:
        print("TOKENS encontrados:")
        for symbol, token in expression_dictionary.items():
            print(f"{symbol} = {token}")





def TokenAnalysis(token, current_state, leaves, expression_dictionary, actions):
    # Verifica si algún número en el estado actual pertenece a una hoja con un token "#TOKEN"
    token_detectado = False
    for estado in current_state:
        # Busca si el estado actual está en el diccionario de hojas con el símbolo especial "#TOKEN"
        for symbol, numbers in leaves.items():
            if symbol.startswith("#") and estado in numbers:
                # Si el token es una palabra reservada, verifica en el diccionario de acciones
                quoted_token = f"'{token}'"

                if symbol.startswith("#RESERVADAS"):
                    compare_token = quoted_token.upper()
                    for identificador, contenido in actions:
                        if compare_token == contenido:
                            # Guarda el identificador en el diccionario bajo el token como clave
                            expression_dictionary[token] = identificador
                            token_detectado = True
                            break

                    if token_detectado != True:

                        number = Find_Number(symbol)
                        expression_dictionary[token] = f"TOKEN{number}"
                        token_detectado = True



                if token_detectado != True:
                    # Si es un símbolo de otro tipo, lo guarda directamente
                    expression_dictionary[token] = symbol[1:]
                    token_detectado = True
                    break
        if token_detectado:
            break  # Sale del bucle si ya se detectó el token

    # Retorna el diccionario si se detectó un token, de lo contrario None
    return expression_dictionary if token_detectado else None


def Find_Number(symbol):

    for i, char in enumerate(symbol):
        if char.isdigit():
            numero = symbol[i:]
            break

    return numero