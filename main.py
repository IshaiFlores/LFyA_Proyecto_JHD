from gramatica import Parsed
import os

def eliminar_espacios(linea):
    # Reemplaza todos los espacios en blanco en una línea
    linea = linea.replace(' ', '')

    return linea

# Inicializa la instancia de la clase que manejará la validación de las secciones
parseo = Parsed()

def main ():

    while(True):

        #Lista de secciones para llevar un control de qué secciones deben haber ocurrido
        secciones= ["S","T","A","E"]
        secciones[0] = False
        secciones[1] = False
        secciones[2] = False
        secciones[3] = False


        # Variables de control para cada sección del archivo
        seccion_SETS = False
        seccion_TOKENS = False
        seccion_ACTIONS = False
        seccion_ERROR = False
        validacion = "" # Variable que almacena el resultado de las validaciones
        i = 1  # Contador de líneas, usado para identificar la primera línea, si existen lineas vacías

        #Flags para manejo de llaves, funciones activas y el control de RESERVADAS
        llave_abierta = False  #Verifica si la llave de apertura { ya fue encontrada
        f_reservadas = False  #Verificar si RESERVADAS() ya fue encontrada
        f_activa = False #Verifica si se encuentra una funcion activa para

        filepath = input("Ingrese la ruta del archivo a leer: ")

        try:

            # Abre el archivo y lo lee línea por línea
            with open(filepath, 'r') as archivo:

                for numero_fila, linea in enumerate(archivo, start=1): # `start=1` para contar las líneas desde 1

                    #Variable que guarda la linea "cruda" del archivo .txt
                    linea_error = linea

                    #Elimina los saltos de línea al final de la línea
                    linea = linea.replace('\n','')
                    linea_error = linea_error.replace('\n','')

                    #Elimina los espacios al final de la línea que ayudará a identificar los errores
                    linea_error = linea_error.rstrip()
                    linea = linea.rstrip()

                    #Si la línea esta vacía, salta a la siguiente
                    if not linea:
                        i += 1
                        continue


                    if numero_fila ==  i:  # Si estamos en la primera línea

                        if linea == 'SETS':# Si la cadena concuerda con la palabra 'SETS'
                            seccion_SETS = True  # Activa seccion de SETS
                            continue

                        elif linea == 'TOKENS':#Si la cadena concuerda con la palabra 'SETS'
                            seccion_TOKENS = True # Activa seccion de TOKENS
                            secciones[1] = True # Valida que si hubo una seccion de TOKENS
                            continue # Pasa a la siguiente línea

                        else: #Si no concuerda
                            if linea.startswith('S') | linea.startswith('s'): #Si la cadena iniciaba con la letra 's' o 'S'
                                #Se asume que el error se encuentra al final de la cadena
                                columna_error = len(linea_error) + 1
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'SETS'")
                                break #Interrumpe la lectura del archivo .txt

                            else: #Si no, se asume que la palabra que venía era 'TOKENS'
                                columna_error = len(linea_error) + 1
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'TOKENS'")
                                break

                    #Verifica si existen espacios vacíos antes de la cadena
                    if linea == linea.lstrip():

                        #Si no hay espacios vacíos
                        if linea == 'TOKENS':#Si la cadena concuerda con la palabra 'TOKENS'
                            seccion_SETS = False #Desactiva la sección de SETS
                            seccion_TOKENS = True #Activa la sección de SETS
                            secciones[1] = True #Valida si hubo una sección de TOKENS
                            continue

                        elif linea.startswith('t') or linea.startswith('T'): # Si la cadena empezaba con la letra T
                            columna_error = len(linea_error) + 1
                            print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'TOKENS'")
                            break


                        elif linea == 'ACTIONS':#Si la cadena concuerda con la palabra 'ACTIONS

                            if secciones[1] == False: #Si antes no estuvo la seccion 'TOKENS'
                                #Se asume que el error viene en la primera columna de la línea
                                columna_error = 1
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'TOKENS'")
                                break

                            seccion_TOKENS = False #Desactiva la seccion de TOKENS
                            seccion_ACTIONS = True #Activa la sección de ACTIONS
                            secciones[2] = True # Valida si la sección de ACTIONS estuvo presente
                            continue

                        elif linea.startswith('a') or linea.startswith('A'): #Si la cadena iniciaba con la letra 'a'
                            columna_error = len(linea_error) + 1
                            print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'ACTIONS'")
                            break

                        elif 'ERROR' in linea: #Si la cadena concuerda con la palabra 'ERROR'

                            if secciones[2] == False: #Si no hubo una sección de ACTIONS
                                columna_error = 1
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'ACTIONS'")
                                break

                            elif f_reservadas == False: #Si no estuvo la función RESERVADAS() en la sección de ACTIONS
                                columna_error = 1
                                print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la funcion 'RESERVADAS()' en ACTIONS")
                                break

                            seccion_ACTIONS = False #Desactiva la seccion de ACTIONS
                            seccion_ERROR = True #Activa la seccion de ERROR
                            secciones[3] = True #Valida si la seccion de ERROR estuvo presente

                        elif linea.startswith('e') or linea.startswith('E'): #Si la cadena iniciaba con la letra 'e'
                            columna_error = len(linea_error) + 1
                            print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba la palabra 'ERROR'")
                            break

                        else:#Si la cadena no concuerda con una sección

                            if seccion_ACTIONS == True:#Si la sección ACTIONS se encuentre activa

                                if linea == 'RESERVADAS()': #Si la línea concuerda con la función 'RESERVADAS()'
                                    f_reservadas = True #Valida si estuvo presente la función 'RESERVADAS()'
                                    f_activa = True #Valida si está activa una función
                                    continue

                                # Verifica apertura de llave
                                elif '{' in linea:

                                    if llave_abierta:#Si ya habia una llave de apertura '}'
                                        #Muestra un error en la lógica de las llaves
                                        columna_error = 1
                                        print(f"Error de formato en la línea {numero_fila}, cerca de la columna {columna_error}: ya hay una llave de apertura '{'{'}' sin cerrar")
                                        break

                                    #Sino declara que existe una llave abierta que no se ha cerrado
                                    llave_abierta = True
                                    continue

                                # Verifica cierre de llave
                                elif '}' in linea:
                                    #Si no había una llave abierta sin cerrar
                                    if not llave_abierta:
                                        columna_error = 1
                                        print(f"Error de formato en la línea {numero_fila}, cerca de la columna {columna_error}:: se encontró una llave de cierre {'}'} sin una llave de apertura '{'{'}'")
                                        break

                                    llave_abierta = False  # Cierra la función actual
                                    f_activa = False #Declara que la función ha terminado
                                    continue

                                else: #Viene el identificador de una función cualquiera


                                    #Si hay una función ya activa y viene un simbolo que no es ni una llave
                                    if f_activa:
                                        columna_error = 1
                                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba una llave de apertura '{'{'}'")

                                    if '(' not in linea:#Si no se encuentra un paréntesis abierto "("
                                        columna_error = len(linea_error)
                                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un parentesis abierto '('")

                                    #Se divide la cadena a partir del paréntesis abierto "("
                                    partes = linea.split('(')

                                    #Si la división no es exactamente en dos partes, significa que hay más de un paréntesis abierto
                                    if len(partes) != 2:
                                        columna_error = linea_error.rfind('(')
                                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un solo parentesis abierto '('")
                                        break

                                    #Se divide la cadena en un identificador y en el paréntesis de cierre ")"
                                    identificador = partes[0].strip()
                                    cierre = partes[1].strip()

                                    #Si el identificador no son letras y no están en mayúsculas
                                    if not identificador.isalpha() & identificador.isupper():
                                        columna_error = linea_error.find(identificador)
                                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un identificador con letras mayusculas '('")
                                        break

                                    #Si no hay paréntesis de cierre
                                    if not cierre == ')':
                                        columna_error = linea_error.find(cierre)
                                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba un parentesis de cierre ')'")
                                        break

                                    #Valida que la declaración de una función está activa
                                    f_activa = True

                            else:#Si no concuerda con ninguna cadena
                                columna_error = 1
                                print(f"Error de formato en la linea {numero_fila}, se esperaba un titulo de una seccion como 'TOKENS' o 'ACTIONS")


                    #Elimina los espacios que se encuentren la línea
                    linea = eliminar_espacios(linea)

                    #Si la sección SETS está activa
                    if seccion_SETS:

                        #Valida la sección SETS
                        validacion = parseo.validar_SET(linea, numero_fila,linea_error)

                        #Si la línea esta vacía, salta a la siguiente
                        if not linea:
                            i += 1
                            continue

                        #Si la línea tiene un error de formato
                        if validacion != "Formato valido":
                            #Imprime el error encontrado
                            print(validacion)
                            break;
                        else:
                        #Si la línea tiene un formato correcto, pasa a la siguiente línea del archivo .txt
                            continue

                    #Si la sección TOKENS está activa
                    if seccion_TOKENS:

                        #Si la línea esta vacía, salta a la siguiente
                        if not linea:
                            i += 1

                        else:
                            #Valida la sección TOKENS
                            validacion = parseo.validar_TOKENS(linea,numero_fila,linea_error)

                            #Si la línea tiene un error de formato
                            if validacion != "Formato valido":
                                #Imprime el error encontrado
                                print(validacion)
                                break;

                            else:
                            #Si la línea tiene un formato correcto, pasa a la siguiente línea del archivo .txt
                                continue

                    #Si la sección ACTIONS está activa
                    if seccion_ACTIONS:

                        #Si la línea esta vacía, salta a la siguiente
                        if not linea:
                            i += 1
                            continue

                        #Valida la sección ACTIONS
                        validacion = parseo.validar_ACTIONS(linea, numero_fila,linea_error)



                        #Si la línea tiene un error de formato
                        if validacion != "Formato valido":
                            #Imprime el error encontrado
                            print(validacion)
                            break;

                        else:
                        #Si la línea tiene un formato correcto, pasa a la siguiente línea del archivo .txt
                            continue

                    #Si la sección ERROR está activa
                    if seccion_ERROR:

                        #Si la línea esta vacía, salta a la siguiente
                        if not linea:
                            i += 1
                            continue


                        #Valida la sección ERROR
                        validacion = parseo.validar_ERROR(linea,numero_fila,linea_error)

                        #Si la línea tiene un error de formato
                        if validacion != "Formato valido":

                            #Imprime el error encontrado
                            print(validacion)
                            break;
                        else:

                        #Si la línea tiene un formato correcto, pasa a la siguiente línea del archivo .txt
                            continue
                else:

                    if secciones[1] == False: #Si en el archivo no se encontró ninguna sección válida
                        columna_error = 1
                        print(f"Error de formato: el archivo no sigue ninguna de las reglas establecidas")

                    elif secciones[3] == False:#Si no se encontró la sección ERROR
                        #Muestra error
                        columna_error = 1
                        print(f"Error de formato en la linea {numero_fila}, cerca de la columna {columna_error}: se esperaba por lo menos un 'ERROR'")

                    else:
                        #Imprime la validación de que el formato del archivo .txt estuvo correcto
                        print ("Formato correcto")

        except FileNotFoundError:
            print ("el archivo no existe, intente de nuevo")

        except IOError:
            print("No se puede acceder al archivo, intente de nuevo")

        op = input("¿Desea leer otro archivo? Y/N (Y = si / N = no) \n")

        if op == "Y":

            os.system('cls')

            continue

        elif op == "N":

            break









if __name__ == "__main__":
    main()