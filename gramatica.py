
class Parsed:

    def validar_SET(self, linea, numero_fila, linea_error):

        # Paso 1: Verificar el formato general (identificador seguido de '=')
        linea = linea.strip()  # Eliminar espacios en blanco al final de la línea

        if '=' not in linea:
            columna_error = (linea_error.find('=') if '=' in linea_error else len(linea_error)) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

        # Dividir la cadena en la parte antes y después del '='
        partes = linea.split('=')
        if len(partes) != 2:
            columna_error = linea_error.rfind('=') + 1
            return f"Error de formato en la fila {numero_fila}: se esperaba un solo signo '=' "

        identificador = partes[0].strip()  # Quitar espacios en blanco alrededor del identificador
        contenido = partes[1].strip()      # Quitar espacios en blanco alrededor del contenido

        # Verificación del identificador
        if not all(c.isalnum() or c == '_' for c in identificador):
            columna_error = linea_error.find(identificador) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error + 2}: se esperaba que el identificador solo contuviera letras"

        # Paso 2: Validar el identificador
        if not identificador.isupper():
            columna_error = linea_error.find(identificador)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error + 2}: se esperaba que el identificador solo contuviera letras mayúsculas"

        # Paso 3: Validar el contenido
        contenido = contenido.strip()

        if not contenido:
            columna_error = linea_error.find('=') + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una definición después de '='"

        if len(contenido) < 3:
            columna_error = linea_error.find(contenido) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una definición completa"

        if contenido[-1] == '+':
            columna_error = len(linea_error)
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba otro símbolo terminal para concatenar"

        # Paso 4: Procesar el contenido
        partes = contenido.split('+')

        for parte in partes:
            parte = parte.strip()

            # Validar si es un rango ('A'..'Z') o ('CHR(x)..CHR(y)')
            if '..' in parte:
                limites = parte.split('..')
                inicio, fin = limites[0].strip(), limites[1].strip()

                if not inicio or not fin:
                    columna_error = linea_error.find(parte) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un intervalo cerrado como 'A'..'Z'"

                # Validar que los rangos sean correctos
                if inicio.startswith("'") and inicio.endswith("'"):


                    if len(inicio) != 3 or len(fin) != 3:
                        columna_error = (linea_error.find(inicio if len(inicio) != 3 else fin)) + 1
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un carácter dentro de las comillas"

                 # Verificar si es una llamada a CHR()
                elif inicio.startswith("CHR(") and inicio.endswith(")"):

                    # Validar que ambos contengan paréntesis de apertura y cierre correctamente
                    if fin.startswith("CHR(") and not fin.endswith(")"):
                        columna_error = len(linea_error) + 1
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: falta un paréntesis de cierre en CHR()"

                    elif not fin.startswith("CHR("):
                        columna_error = (linea_error.find(fin if not fin.startswith("CHR(") else fin)) + 1
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba la funcion CHR()"

                    else:
                        try:
                            # Intentar convertir el contenido entre los paréntesis a números
                            int(inicio[4:-1])  # Validar que haya un número dentro de CHR()
                            int(fin[4:-1])
                        except ValueError:
                            columna_error = (linea_error.find(inicio if not inicio[4:-1].isdigit() else fin)) + 1
                            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un número dentro de los parámetros de la función CHR()"

                # En caso de que no tenga el paréntesis de cierre
                elif inicio.startswith("CHR(") and not inicio.endswith(")"):
                    columna_error = linea_error.find(inicio) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: falta un paréntesis de cierre en CHR()"

                else:
                    columna_error = linea_error.find(parte) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un intervalo válido separado por '..'"

            elif '.' in parte:

                if not (parte.startswith("'") and parte.endswith("'")):
                    columna_error = linea_error.find(parte) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba '..' en lugar de '.' para definir un intervalo"

            elif parte.startswith("'") and parte.endswith("'"):
                if len(parte) != 3:
                    columna_error = linea_error.find(parte) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un carácter dentro de las comillas"

            elif parte.startswith("'") and not parte.endswith("'"):

                columna_error = linea_error.find(parte) + 2
                return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de cierre"

            elif  not parte.startswith("'") and parte.endswith("'"):

                if len(parte) != 3:
                    columna_error = linea_error.find(parte) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de apertura"



        return "Formato valido"



    def validar_ERROR(self, linea, numero_fila, linea_error):

        # Paso 1: Verificar el formato general (identificador seguido de '=')
        linea = linea.strip()  # Eliminar espacios en blanco al principio y al final de la línea

        if '=' not in linea:
            columna_error = len(linea_error)  + 1 # Si no hay '=', se asume que el error está al final de la línea original
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

        # Divide la cadena en la parte antes y después del '='
        partes = linea.split('=')
        if len(partes) != 2:
            columna_error = (linea_error.find('=') if '=' in linea_error else len(linea_error)) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo signo '='"

        identificador = partes[0].strip()  # Quitar espacios en blanco alrededor del identificador
        contenido = partes[1].strip()      # Quitar espacios en blanco alrededor del contenido

        # Valida el identificador
        if not identificador.isalpha() or not identificador.endswith('ERROR'): #Si el identificador no tiene letras o no tiene el sufijo ERROR
            columna_error = linea_error.find(identificador) + 1 # Localizar dónde está el identificador
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: El identificador debe contener solo letras y terminar con 'ERROR'"

        # Valida la parte después del '='
        if not contenido.isdigit():
            columna_error = linea_error.find(contenido) + 1  # Localiza dónde está el contenido después del '='
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: La parte después del '=' debe contener solo números"


        return "Formato valido"



    def validar_TOKENS(self, linea, numero_fila, linea_error):

        # Paso 1: Verificar el formato general (identificador seguido de '=')

        # Se recorre la línea para encontrar el primer '=' que no esté entre comillas simples
        dentro_comillas = False
        posicion_igual = -1  # Guardará la posición del primer '=' encontrado fuera de comillas

        for idx, char in enumerate(linea):

            if char == "'":  # Cambiamos el estado si encontramos una comilla simple
                dentro_comillas = not dentro_comillas

            elif char == '=' and not dentro_comillas:#Sino se guarda la posición donde se encontró el primer '=' fuera de comillas
                posicion_igual = idx
                break  # Nos detenemos al encontrar el primer '=' fuera de comillas


        #Se muestra error sino se encontró un '=' que no sea un símbolo terminal
        if posicion_igual == -1:
            columna_error = len(linea_error) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"


        # Divide la cadena en la parte antes y después del '='
        identificador = linea[:posicion_igual].strip()
        contenido = linea[posicion_igual + 1:].strip()


        # Paso 2: Validar el identificador del Token (debe empezar con "TOKEN")
        if not identificador.startswith("TOKEN"):

            columna_error = linea_error.find(identificador) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba que el identificador iniciara con la palabra 'TOKEN'"

        # Valida que el número del token siga a "TOKEN"
        token_num = identificador[5:].strip()  # Toma la parte después de "TOKEN"

        #Valida que después que el TOKEN venga un número
        if not token_num.isdigit():
            columna_error = linea_error.find(token_num) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba un número después de 'TOKEN'"


        # Paso 3: Validar el contenido
        i = 0

        stack = []  # Pila para validar paréntesis y llaves

        while i < len(contenido):

            # Verificar si el caracter actual es una comilla simple
            if contenido[i] == "'":

                # Asegura de que haya un caracter encerrado entre comillas simples
                if i + 2 >= len(contenido):
                    columna_error = len(linea_error) + 1  # El error está al final de la línea
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba un carácter entre comillas"

                #Si después del caracter encerrado no cierra con una comilla simple
                elif contenido[i + 2] != "'":
                    columna_error = linea_error.find(contenido[i]) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba una comilla de cierre"

                # Verifica que haya exactamente un caracter entre las comillas simples
                if len(contenido[i + 1]) != 1:
                    columna_error = linea_error.find(contenido[i + 1]) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Solo se permite un carácter entre comillas simples"

                # Mueve el índice al siguiente posible token

                i += 3  # Salta el grupo "'X'"
            else:

                # Valida caracteres no terminales de expressiones regulares
                j = i

                #Bucle que itera mientras no se haya caracteres en la definición
                # y la definición se encuentre en letras
                while j < len(contenido) and contenido[j].isalpha():

                    j += 1 #Lee cada caracter

                token = contenido[i:j] #Concatena cada caracter que forma parte de la expresión regular

                #Verifica si lo concatenado estaba en mayúsculas o si se encontró un símbolo de la expresión regular
                if token.isupper() or contenido[j] in {'+', '*', '?', '|', '(', ')', '{', '}'}:
                    i = j  # Mueve el índice más allá del identificador
                else:
                    columna_error = linea_error.find(contenido[j]) + 1
                    return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba un símbolo no terminal o un símbolo de expresión regular"

            # Valida los operadores de expresiones regulares o concatenación
            if i < len(contenido) and contenido[i] in {'+', '*', '?', '|', '(', ')', '{', '}'}:

                # Verifica si el operador actual es un paréntesis o llave de apertura
                if contenido[i] in {'(', '{'}:

                    stack.append(contenido[i])  # Agrega paréntesis o llave de apertura a la pila

                 # Verifica si el operador actual es un paréntesis de cierre
                elif contenido[i] == ')':

                    if not stack or stack[-1] != '(':
                        # Si la pila está vacía o el paréntesis en la cima de la pila no es de apertura,
                        # indica un paréntesis de cierre inesperado
                        columna_error = linea_error.find(contenido[i]) + 1

                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Paréntesis de cierre inesperado"

                    stack.pop()  # Quita el paréntesis de apertura correspondiente de la pila

                # Verifica si el operador actual es una llave de cierre
                elif contenido[i] == '}':
                    if not stack or stack[-1] != '{':
                        columna_error = linea_error.find(contenido[i]) + 1
                        return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Llave de cierre inesperada"
                    stack.pop()  # Quita la llave de apertura correspondiente

                i += 1  # Avanza al siguiente carácter, saltando el operador de expresión regular actual

       # Después de procesar todos los operadores, verifica que no queden paréntesis o llaves sin cerrar en la pila
        if stack:
            columna_error = len(linea_error) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Falta cerrar {'paréntesis' if stack[-1] == '(' else 'llave'}"

        return "Formato valido"


    def validar_ACTIONS(self, linea, numero_fila, linea_error):

        # Paso 1: Verificar el formato general (identificador seguido de '=')
        linea = linea.strip()  # Elimina espacios en blanco al principio y al final de la línea

        #Verifica que se encuentre un signo '='
        if '=' not in linea:
            columna_error = len(linea) + 1  # Si no hay '=', se asume que el error está al final de la línea
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: Se esperaba el signo '='"

        # Divide la cadena en la parte antes y después del '='
        partes = linea.split('=')

        # Verifica que solo exista un signo '=' válido
        if len(partes) != 2:
            columna_error = (linea.rfind('=') if '=' in linea else len(linea)) + 1
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo signo '='"

        identificador = partes[0].strip()  # Quita espacios en blanco alrededor del identificador
        contenido = partes[1].strip()      # Quita espacios en blanco alrededor del contenido

        # Paso 2: Verificar que el identificador sea un número
        if not identificador.isdigit():
            columna_error = linea_error.find(identificador) + 1  # Columna exacta donde está el identificador
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba un número"

        # Paso 3: Verificar que la definición esté en un formato correcto
        if contenido.startswith("'") and not contenido.endswith("'"):
            columna_error = len(linea_error) + 1  # Si falta la comilla de cierre, el error está al final de la línea
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de cierre"

        elif not contenido.startswith("'") and contenido.endswith("'"):
            columna_error = linea_error.find('=') + 1  # # Si falta la comilla de cierre, el error justo después del signo '='
            return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba una comilla de apertura"


        if contenido.startswith("'") and contenido.endswith("'"):
            # Extrae el contenido entre las comillas
            contenido_interno = contenido[1:-1]  # Remueve las comillas simples

            # Verifica que el contenido interno sean solo letras mayúsculas
            if not contenido_interno.isalpha() or not contenido_interno.isupper():

                columna_error = linea_error.find(contenido_interno) + 1  # Error dentro del contenido
                return f"Error de formato en la fila {numero_fila}, cerca de la columna {columna_error}: se esperaba solo letras mayúsculas"

        return "Formato valido"










