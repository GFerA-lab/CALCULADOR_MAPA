from collections import deque
import copy

# Funcion para llenar el mapa con ceros/caminos
def cerar_matriz(matriz, cant_fila, cant_col):
    for _ in range(cant_fila):
        fila = []
        for _ in range(cant_col):
            fila.append(0)
        matriz.append(fila)

# Funcion para imprimir matriz
def imprimir_matriz(matriz):
    mapa = {
        0: "⬜",   # camino libre
        1: "🏢",   # edificio
        2: "💧",   # agua
        3: "⛔",   # zona bloqueada
        5: "🟦",   # camino junto
        6: "🟩",   # camino sin imprevistos
        7: "🟨",   # camino alternativo
        8: "🚩",   # inicio
        9: "🏁"    # fin
    }

    for fila in matriz:
        print(" ".join(mapa.get(valor, "?") for valor in fila))


# Funcion para verificar que el valor inicial sea mayor a 0
def verificar_valor_inicial(valor):
    while valor <= 0:
        print("Valor no valido. Intente de nuevo.")
        valor = int(input("Ingrese un valor mayor a 0: "))
    return valor


# Funcion para verificar que la posicion este dentro del rango
def verificar_posicion(fila, col, matriz):

    # Verificar si la posicion es valida
    if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]) and matriz[fila][col] == 0:
        return fila, col

    # Si la posicion no es valida, pedir una nueva posicion
    while True:

        print("Valor fuera de rango. Intente de nuevo.")
        fila = int(input("Ingrese el valor de la fila: "))
        col = int(input("Ingrese el valor de la columna: "))
        # Verificar si la nueva posicion es valida sino se repite el ciclo
        if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]) and matriz[fila][col] == 0:
            break
    
    return fila, col

# Limpiar obstaculos
def limpiar_obtaculo(matriz, posicion):
    fila, col = posicion
    mov= [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha

    # Limpiar las celdas adyacentes
    for x, y in mov:
        aux_fila, aux_col = fila + x, col + y
        if 0 <= aux_fila < len(matriz) and 0 <= aux_col < len(matriz[0]):
            matriz[aux_fila][aux_col] = 0 

# Agregar obstaculos y marcar las celdas adyacentes
def agregar_obstaculo(matriz, fila, col, valor, posicion):

    pos_obstaculo = [] # Lista para almacenar las posiciones de los obstaculos

    if valor == 2:  # Agua en cruz
        mov= [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
    else: # Edificio o zona bloqueada en cuadrado
        mov= [(-1, -1), (-1, 0), (-1, 1),(0, 1), (1, 0), (0, -1), (1, -1), (1, 1)]  # Todas las direcciones

    fila_obstaculo, col_obstaculo = posicion # Obtener fila y columna de la posicion

    matriz[fila_obstaculo][col_obstaculo] = valor  # Marcar la celda del obstaculo
    pos_obstaculo.append(posicion) # Agregar la posicion del obstaculo a la lista

    # Marcar las celdas adyacentes
    for x, y in mov:
        aux_fila, aux_col = fila_obstaculo + x, col_obstaculo + y # Recorrer vecinos

        # Verificar que la posicion este dentro del rango
        if 0 <= aux_fila < fila and 0 <= aux_col < col:
            if matriz[aux_fila][aux_col] == 0:  # No sobrescribir si ya es un obstaculo

                matriz[aux_fila][aux_col] = valor  # Marcar las celdas adyacentes como obstaculos
                pos_obstaculo.append((aux_fila, aux_col))

    return pos_obstaculo

# Funcion para buscar el camino usando BFS
def buscar_camino(matriz, inicio, fin, imprevistos):

    filas = len(matriz)
    cols = len(matriz[0]) if filas > 0 else 0
    visitado = set()
    padre = {}
    cola = deque([inicio])
    visitado.add(inicio)

    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha

    while cola:
        actual = cola.popleft()
        fila, colum = actual

        if actual == fin:
            camino = [] # Lista para almacenar el camino

            # Reconstruir el camino desde el nodo final hasta el inicio
            while actual in padre:
                camino.append(actual)
                actual = padre[actual]
            
            camino.append(inicio)
            camino.reverse()
            return camino

        # Explorar vecinos
        for x, y in movimientos:
            aux_fila, aux_columna = fila + x, colum + y
            vecino = (aux_fila, aux_columna)

            if (0 <= vecino[0] < filas and 0 <= vecino[1] < cols 
            and vecino not in visitado):
                # Verificar si es camino libre o si se permiten imprevistos
                if matriz[vecino[0]][vecino[1]] == 0 or (imprevistos and matriz[vecino[0]][vecino[1]] == 2):
                    visitado.add(vecino)
                    padre[vecino] = actual
                    cola.append(vecino)

    return None

# Colocar el camino en el mapa
def colocar_camino(mapa_camino, camino, valor):
    
    if camino:
        for fila, col in camino:
            if mapa_camino[fila][col] == 7:
                mapa_camino[fila][col] = 5
            else:
                mapa_camino[fila][col] = valor

# Imprimir mensajes segun el resultado de la busqueda
def imprimir_mensaje(camino_sin, camino_alt):

    # Mensajes para caminos sin imorevistos
    if camino_sin:
        print("Camino sin imprevistos encontrado")
    else:
        print("No se encontró un camino sin imprevistos.")
    
    # Mensajes para caminos con imprevistos
    if camino_alt == camino_sin and camino_alt is not None:
        print("No un camino alternativo mejor al original")
    elif camino_alt:
        print("Camino alternativo encontrado")
    else:
        print("No se encontró un camino alternativo.")

def main():
    while True:
        # Variables iniciales y banderas
        ban_camino = False
        imprevistos = True
        sin_imprevistos = False
        inicio = None
        fin = None
        pos_zonasbloqueadas = []

        fila_matriz = int(input("Ingrese la cantidad de filas: "))
        fila_matriz = verificar_valor_inicial(fila_matriz) # Verificar que el valor sea mayor a 0

        col_matriz = int(input("Ingrese la cantidad de columnas: "))
        col_matriz = verificar_valor_inicial(col_matriz) # Verificar que el valor sea mayor a 0

        matriz = []
        cerar_matriz(matriz, fila_matriz, col_matriz) # Cerar la matriz
        imprimir_matriz(matriz)

        while True:
            # Menu de opciones
            opcion = input("Elija una opcion 1-Agregar Obstaculo, 2-Buscar un camino, 3-Crear nuevo mapa, 4-Terminar programa: ")
            
            if opcion == "1":
                # Ciclo para agregar obstaculos
                while True:

                    obstaculo = int(input("Desea agregar 1-Edificio, 2-Agua, 3-Zona bloqueada, 4-Salir, 5-Liberar zonas: "))
                    
                    # Si es 4 se sale del ciclo
                    if obstaculo == 4:
                        break

                    elif obstaculo in [1, 2, 3, 5]:

                        # Si es 5 se liberan las zonas bloqueadas
                        if obstaculo == 5:
                            if pos_zonasbloqueadas:
                                for x,y in pos_zonasbloqueadas:
                                    matriz[x][y] = 0
                                pos_zonasbloqueadas = []
                            else:
                                print("No hay zonas bloqueadas para liberar.")
                        
                        # Si es 1, 2 o 3 se agrega el obstaculo
                        else:
                            # Pedir la posicion del obstaculo
                            fila_obs = int(input("Ingrese la fila de la posicion: "))                
                            col_obs = int(input("Ingrese la columna de la posicion: "))

                            # Verificar que la posicion sea valida
                            pos_obstaculo = verificar_posicion(fila_obs, col_obs, matriz)

                            # Agregar el obstaculo a la matriz
                            aux = agregar_obstaculo(matriz, fila_matriz, col_matriz, obstaculo, pos_obstaculo)

                            # Si se agrego una zona bloqueada, guardar sus posiciones
                            if obstaculo == 3:
                                pos_zonasbloqueadas.extend(aux)
                        
                        # Imprimir el mapa con el obstaculo agregado
                        if ban_camino:

                            # Buscar caminos
                            camino_sin = buscar_camino(matriz, inicio, fin, sin_imprevistos)
                            camino_alt = buscar_camino(matriz, inicio, fin, imprevistos)

                            # Mostrar el mapa con los caminos
                            mapa_camino = copy.deepcopy(matriz)
                            colocar_camino(mapa_camino, camino_alt, 7)
                            colocar_camino(mapa_camino, camino_sin, 6)

                            # Marcar inicio y fin
                            mapa_camino[fila_pos][col_pos] = 8
                            mapa_camino[fila_fin][col_fin] = 9

                            #imprimir el mapa
                            imprimir_matriz(mapa_camino)
                            
                            # Imprimir mensajes segun el resultado de la busqueda
                            imprimir_mensaje(camino_sin, camino_alt)
                        
                        # Si no se ha buscado un camino, solo imprimir la matriz
                        else:
                            imprimir_matriz(matriz)
                    # Si la opcion no es valida, mostrar mensaje
                    else:
                        print("Opcion no valida.")
            
            # Si la opcion es 2, buscar caminos
            elif opcion == "2":
                
                # Pedir la posicion inicial y final
                fila_pos = int(input("Ingrese la fila de la posicion inicial: "))        
                col_pos = int(input("Ingrese la columna de la posicion inicial: "))

                fila_pos, col_pos = verificar_posicion(fila_pos, col_pos, matriz) # Verificar que la posicion sea valida

                fila_fin = int(input("Ingrese la fila de la posicion final: "))
                col_fin = int(input("Ingrese la columna de la posicion final: "))
                fila_fin, col_fin = verificar_posicion(fila_fin, col_fin, matriz)

                ban_camino = True # Indicar que ya se ha buscado un camino

                inicio = (fila_pos, col_pos)
                fin = (fila_fin, col_fin)

                # Buscar caminos
                camino_sin = buscar_camino(matriz, inicio, fin, sin_imprevistos)
                camino_alt = buscar_camino(matriz, inicio, fin, imprevistos)

                # Mostrar el mapa con los caminos
                mapa_camino = copy.deepcopy(matriz)
                colocar_camino(mapa_camino, camino_alt, 7)
                colocar_camino(mapa_camino, camino_sin, 6)
                mapa_camino[fila_pos][col_pos] = 8
                mapa_camino[fila_fin][col_fin] = 9

                imprimir_matriz(mapa_camino)

                imprimir_mensaje(camino_sin, camino_alt)

            # Si la opcion es 3 o 4, salir del ciclo
            elif opcion == "3" or opcion =="4":
                break
        
        # Si la opcion es 4, terminar el programa
        if opcion == "4":
            print("Programa terminado.")
            break
    
if __name__ == "__main__":
    main()