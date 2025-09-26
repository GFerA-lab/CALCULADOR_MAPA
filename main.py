from collections import deque
import copy

def cerar_matriz(matriz, cant_fila, cant_col):
    for _ in range(cant_fila):
        fila = []
        for _ in range(cant_col):
            fila.append(0)
        matriz.append(fila)

def imprimir_matriz(matriz):
    #for fila in matriz:
        #print(fila)
    mapa = {
        0: "⬜",   # libre
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

def verificar_valor_inicial(valor):
    while valor <= 0:
        print("Valor no valido. Intente de nuevo.")
        valor = int(input("Ingrese un valor mayor a 0: "))
    return valor



# Funcion para verificar que la posicion este dentro del rango
def verificar_posicion(fila, col, matriz):

    if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]) and matriz[fila][col] == 0:
        return fila, col

    while True:
        print("Valor fuera de rango. Intente de nuevo.")
        fila = int(input("Ingrese el valor de la fila: "))
        col = int(input("Ingrese el valor de la columna: "))
        if 0 <= fila < len(matriz) and 0 <= col < len(matriz[0]) and matriz[fila][col] == 0:
            break
    
    return fila, col

def limpiar_obtaculo(matriz, posicion):
    fila, col = posicion
    mov= [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha

    # Limpiar las celdas adyacentes
    for x, y in mov:
        aux_fila, aux_col = fila + x, col + y
        if 0 <= aux_fila < len(matriz) and 0 <= aux_col < len(matriz[0]):
            matriz[aux_fila][aux_col] = 0 

def agregar_obstaculo(matriz, fila, col, valor, posicion):
    pos_obstaculo = []
    if valor == 2:  # Agua
        mov= [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
    else:
        mov= [(-1, -1), (-1, 0), (-1, 1),(0, 1), (1, 0), (0, -1), (1, -1), (1, 1)]  # Todas las direcciones

    fila_obstaculo, col_obstaculo = posicion

    matriz[fila_obstaculo][col_obstaculo] = valor  # Marcar la celda del obstaculo
    pos_obstaculo.append(posicion)

    # Marcar las celdas adyacentes
    for x, y in mov:
        aux_fila, aux_col = fila_obstaculo + x, col_obstaculo + y
        if 0 <= aux_fila < fila and 0 <= aux_col < col:
            if matriz[aux_fila][aux_col] == 0:  # No sobrescribir si ya es un obstaculo
                matriz[aux_fila][aux_col] = valor  # Marcar las celdas adyacentes como obstaculos
                pos_obstaculo.append((aux_fila, aux_col))

    return pos_obstaculo

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
            camino = []
            while actual in padre:
                camino.append(actual)
                actual = padre[actual]
            camino.append(inicio)
            camino.reverse()
            return camino

        for x, y in movimientos:
            aux_fila, aux_columna = fila + x, colum + y
            vecino = (aux_fila, aux_columna)

            if (0 <= vecino[0] < filas and 0 <= vecino[1] < cols 
            and vecino not in visitado):
                if matriz[vecino[0]][vecino[1]] == 0 or (imprevistos and matriz[vecino[0]][vecino[1]] == 2):
                    visitado.add(vecino)
                    padre[vecino] = actual
                    cola.append(vecino)

    return None


def colocar_camino(mapa_camino, camino, valor):
    if camino:
        for fila, col in camino:
            if mapa_camino[fila][col] == 7:
                mapa_camino[fila][col] = 5
            else:
                mapa_camino[fila][col] = valor

def imprimir_mensaje(camino_sin, camino_alt):
    if camino_sin:
        print("Camino sin imprevistos encontrado")
    else:
        print("No se encontró un camino sin imprevistos.")
    
    if camino_alt == camino_sin and camino_alt is not None:
        print("No un camino alternativo mejor al original")
    elif camino_alt:
        print("Camino alternativo encontrado")
    else:
        print("No se encontró un camino alternativo.")

def main():
    while True:
        ban_camino = False
        imprevistos = True
        sin_imprevistos = False
        inicio = None
        fin = None
        pos_zonasbloqueadas = []

        fila_matriz = int(input("Ingrese la cantidad de filas: "))
        fila_matriz = verificar_valor_inicial(fila_matriz)

        col_matriz = int(input("Ingrese la cantidad de columnas: "))
        col_matriz = verificar_valor_inicial(col_matriz)

        matriz = []
        cerar_matriz(matriz, fila_matriz, col_matriz)
        imprimir_matriz(matriz)
        while True:
            opcion = input("Elija una opcion 1-Agregar Obstaculo, 2-Buscar un camino, 3-Crear nuevo mapa, 4-Terminar programa: ")
            if opcion == "1":
                while True:
                    obstaculo = int(input("Desea agregar 1-Edificio, 2-Agua, 3-Zona bloqueada, 4-Salir, 5-Liberar zonas: "))
                    if obstaculo == 4:
                        break
                    elif obstaculo in [1, 2, 3, 5]:
                        if obstaculo == 5:
                            if pos_zonasbloqueadas:
                                for x,y in pos_zonasbloqueadas:
                                    matriz[x][y] = 0
                                pos_zonasbloqueadas = []
                            else:
                                print("No hay zonas bloqueadas para liberar.")
                        else:   
                            fila_obs = int(input("Ingrese la fila de la posicion: "))                
                            col_obs = int(input("Ingrese la columna de la posicion: "))
                            pos_obstaculo = verificar_posicion(fila_obs, col_obs, matriz)

                            aux = agregar_obstaculo(matriz, fila_matriz, col_matriz, obstaculo, pos_obstaculo)
                            if obstaculo == 3:
                                pos_zonasbloqueadas.extend(aux)

                        if ban_camino:
                            camino_sin = buscar_camino(matriz, inicio, fin, sin_imprevistos)
                            camino_alt = buscar_camino(matriz, inicio, fin, imprevistos)

                            mapa_camino = copy.deepcopy(matriz)
                            colocar_camino(mapa_camino, camino_alt, 7)
                            colocar_camino(mapa_camino, camino_sin, 6)
                            mapa_camino[fila_pos][col_pos] = 8
                            mapa_camino[fila_fin][col_fin] = 9
                            imprimir_matriz(mapa_camino)

                            imprimir_mensaje(camino_sin, camino_alt)

                        else:
                            imprimir_matriz(matriz)
                    elif obstaculo == 5:
                        if pos_zonasbloqueadas:
                            for posicion in pos_zonasbloqueadas:
                                limpiar_obtaculo(matriz, posicion)
                            pos_zonasbloqueadas = []
                            if ban_camino:
                                camino_sin = buscar_camino(matriz, inicio, fin, sin_imprevistos)
                                camino_alt = buscar_camino(matriz, inicio, fin, imprevistos)

                                mapa_camino = copy.deepcopy(matriz)
                                colocar_camino(mapa_camino, camino_alt, 7)
                                colocar_camino(mapa_camino, camino_sin, 6)
                                mapa_camino[fila_pos][col_pos] = 8
                                mapa_camino[fila_fin][col_fin] = 9
                                imprimir_matriz(mapa_camino)

                                imprimir_mensaje(camino_sin, camino_alt)
                            else:
                                imprimir_matriz(matriz)
                        else:
                            print("No hay zonas bloqueadas para liberar.")
                    else:
                        print("Opcion no valida.")
                    
            elif opcion == "2":

                fila_pos = int(input("Ingrese la fila de la posicion inicial: "))        
                col_pos = int(input("Ingrese la columna de la posicion inicial: "))

                fila_pos, col_pos = verificar_posicion(fila_pos, col_pos, matriz)

                fila_fin = int(input("Ingrese la fila de la posicion final: "))
                col_fin = int(input("Ingrese la columna de la posicion final: "))
                fila_fin, col_fin = verificar_posicion(fila_fin, col_fin, matriz)

                ban_camino = True

                inicio = (fila_pos, col_pos)
                fin = (fila_fin, col_fin)

                camino_sin = buscar_camino(matriz, inicio, fin, sin_imprevistos)
                camino_alt = buscar_camino(matriz, inicio, fin, imprevistos)

                mapa_camino = copy.deepcopy(matriz)
                colocar_camino(mapa_camino, camino_alt, 7)
                colocar_camino(mapa_camino, camino_sin, 6)
                mapa_camino[fila_pos][col_pos] = 8
                mapa_camino[fila_fin][col_fin] = 9

                imprimir_matriz(mapa_camino)

                imprimir_mensaje(camino_sin, camino_alt)
            elif opcion == "3" or opcion =="4":
                break
        
        if opcion == "4":
            print("Programa terminado.")
            break
    
if __name__ == "__main__":
    main()