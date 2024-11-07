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

        if char == " " and complete:
            idx += 1
            continue
        elif char != " " and complete:
            complete = False

        # Determina el tipo de símbolo actual (LETRA, DIGITO o CHARSET)
        symbol_types = []
        if char.isalpha() or char == "_":
            symbol_types.append("LETRA")
        if char.isdigit():
            symbol_types.append("DIGITO")
        if 32 <= ord(char) <= 254:
            symbol_types.append("CHARSET")

        valid_transition = False
        if current_state in transiciones:
            if quoted_char in leaves and quoted_char in transiciones[current_state]:
                # Si el símbolo específico (con comillas) está en leaves y tiene una transición, la tomamos
                next_state = frozenset(transiciones[current_state][quoted_char])
                current_state = next_state
                cadena_acumulada += char
                idx += 1
                valid_transition = True
            else:
                for stype in symbol_types:
                    if stype in leaves and stype in transiciones[current_state]:
                        # Si el tipo de símbolo está en leaves y tiene una transición, la tomamos
                        next_state = frozenset(transiciones[current_state][stype])
                        current_state = next_state
                        cadena_acumulada += char
                        idx += 1
                        valid_transition = True
                        break

        # Si no hay transición válida, marca como completo
        if not valid_transition:
            complete = True

        if complete:
            # Analiza el token acumulado
            result = TokenAnalysis(cadena_acumulada, current_state, leaves, expression_dictionary, actions)
            if result is not None:
                # Reinicia la cadena acumulada y vuelve al estado inicial
                cadena_acumulada = ""
                current_state = initial_state
            else:
                # Si no hay transición ni token válido, guarda el error en el diccionario
                expression_dictionary[cadena_acumulada] = "Error: Token inválido"
                cadena_acumulada = ""
                current_state = initial_state
                idx += 1

    # Procesar la cadena acumulada al final del bucle
    if cadena_acumulada:

        result = TokenAnalysis(cadena_acumulada, current_state, leaves, expression_dictionary, actions)
        if result is None:
            expression_dictionary[cadena_acumulada] = "Error: Token inválido"

    # Imprime cada símbolo con su respectivo token en una línea separada
    print("TOKENS encontrados:")
    for symbol, token in expression_dictionary.items():
        print(f"{symbol} = {token}")

    return expression_dictionary


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

                    if not token_detectado:
                        number = Find_Number(symbol)
                        expression_dictionary[f" {token} "] = f"TOKEN{number}"
                        token_detectado = True

                if not token_detectado:
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
