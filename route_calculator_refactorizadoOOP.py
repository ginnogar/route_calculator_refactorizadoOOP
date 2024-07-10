"""Busqueda de Ruta RefactorizadoOOP"""
class Nodo:
    def __init__(self, x, y, g_cost=0, h_cost=0):
        self.x = x  # Coordenada x del nodo
        self.y = y  # Coordenada y del nodo
        self.g_cost = g_cost  # Costo desde el inicio hasta este nodo
        self.h_cost = h_cost  # Costo estimado desde este nodo hasta el final
        self.padre = None  # Nodo padre para reconstruir la ruta

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost  # Costo total (g_cost + h_cost)

class Mapa:
    def __init__(self, tamaño):
        self.tamaño = tamaño  # Tamaño del mapa (n x n)
        self.mapa = [[0 for _ in range(tamaño)] for _ in range(tamaño)]  # Inicializa el mapa con ceros (celdas vacías)
        self.inicio = None  # Punto de inicio
        self.fin = None  # Punto final

    def es_accesible(self, x, y):
        return 0 <= x < self.tamaño and 0 <= y < self.tamaño  # Verifica si las coordenadas están dentro del rango del mapa

    def agregar_obstaculo(self, x, y, tipo_obstaculo=1):
        if self.es_accesible(x, y):  # Verifica si las coordenadas son válidas
            self.mapa[x][y] = tipo_obstaculo  # Agrega un obstáculo en las coordenadas especificadas
        else:
            print("Coordenadas fuera del rango del mapa.")  # Muestra un mensaje de error si las coordenadas son inválidas

    def quitar_obstaculo(self, x, y):
        if self.es_accesible(x, y):  # Verifica si las coordenadas son válidas
            if self.mapa[x][y] != 0:  # Verifica si hay un obstáculo en las coordenadas
                self.mapa[x][y] = 0  # Quita el obstáculo (lo establece a 0)
            else:
                print("No hay obstáculo en las coordenadas especificadas.")  # Mensaje si no hay obstáculo para quitar
        else:
            print("Coordenadas fuera del rango del mapa.")  # Mensaje si las coordenadas son inválidas

    def establecer_inicio(self, x, y):
        if self.es_accesible(x, y):  # Verifica si las coordenadas son válidas
            self.inicio = (x, y)  # Establece el punto de inicio
        else:
            print("Coordenadas fuera del rango del mapa.")  # Mensaje si las coordenadas son inválidas

    def establecer_fin(self, x, y):
        if self.es_accesible(x, y):  # Verifica si las coordenadas son válidas
            self.fin = (x, y)  # Establece el punto final
        else:
            print("Coordenadas fuera del rango del mapa.")  # Mensaje si las coordenadas son inválidas

    def es_celda_accesible(self, x, y):
        return self.es_accesible(x, y) and self.mapa[x][y] == 0  # Verifica si la celda es accesible (dentro del rango y vacía)

    def mostrar(self):
        simbolos = {0: '.', 1: 'X', 2: 'X', 3: 'X'}  # Diccionario para convertir valores del mapa a símbolos
        for fila in self.mapa:  # Recorre cada fila del mapa
            linea = ' '.join([simbolos[celda] for celda in fila])  # Convierte cada celda en su símbolo correspondiente
            print(linea)  # Imprime la línea del mapa

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa  # Asigna el mapa a la calculadora de rutas

    def calcular_h_cost(self, nodo_actual, nodo_final):
        return abs(nodo_actual.x - nodo_final.x) + abs(nodo_final.y - nodo_actual.y)  # Calcula el costo heurístico (distancia Manhattan)

    def obtener_vecinos(self, nodo):
        vecinos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lista de direcciones (arriba, abajo, izquierda, derecha)
        for dx, dy in direcciones:  # Recorre cada dirección
            nuevo_x, nuevo_y = nodo.x + dx, nodo.y + dy  # Calcula las nuevas coordenadas
            if self.mapa.es_celda_accesible(nuevo_x, nuevo_y):  # Verifica si la nueva celda es accesible
                vecinos.append(Nodo(nuevo_x, nuevo_y))  # Agrega el nuevo nodo a la lista de vecinos
        return vecinos  # Devuelve la lista de vecinos

    def a_estrella(self):
        nodo_inicio = Nodo(self.mapa.inicio[0], self.mapa.inicio[1])  # Crea el nodo inicial
        nodo_final = Nodo(self.mapa.fin[0], self.mapa.fin[1])  # Crea el nodo final
        nodo_inicio.h_cost = self.calcular_h_cost(nodo_inicio, nodo_final)  # Calcula el costo heurístico del nodo inicial

        abierta = [nodo_inicio]  # Lista de nodos por explorar
        cerrada = []  # Lista de nodos ya explorados

        while abierta:  # Mientras haya nodos por explorar
            nodo_actual = min(abierta, key=lambda nodo: nodo.f_cost)  # Selecciona el nodo con el menor costo total (f_cost)
            abierta.remove(nodo_actual)  # Elimina el nodo actual de la lista abierta
            cerrada.append(nodo_actual)  # Agrega el nodo actual a la lista cerrada

            if nodo_actual.x == nodo_final.x and nodo_actual.y == nodo_final.y:  # Si el nodo actual es el nodo final
                camino = []
                while nodo_actual:  # Reconstruye el camino desde el nodo final hasta el inicio
                    camino.append((nodo_actual.x, nodo_actual.y))
                    nodo_actual = nodo_actual.padre
                return camino[::-1]  # Devuelve el camino invertido (desde inicio a final)

            vecinos = self.obtener_vecinos(nodo_actual)  # Obtiene los vecinos del nodo actual
            for vecino in vecinos:  # Recorre cada vecino
                if vecino in cerrada:  # Si el vecino ya está en la lista cerrada, continúa con el siguiente
                    continue

                vecino.g_cost = nodo_actual.g_cost + 1  # Calcula el costo desde el inicio hasta el vecino
                vecino.h_cost = self.calcular_h_cost(vecino, nodo_final)  # Calcula el costo heurístico del vecino
                vecino.padre = nodo_actual  # Establece el nodo actual como el padre del vecino

                if vecino not in abierta:  # Si el vecino no está en la lista abierta, lo agrega
                    abierta.append(vecino)
                else:
                    abierto_vecino = next(n for n in abierta if n.x == vecino.x and n.y == vecino.y)
                    if vecino.g_cost < abierto_vecino.g_cost:  # Si encuentra un mejor camino, actualiza el nodo en la lista abierta
                        abierto_vecino.g_cost = vecino.g_cost
                        abierto_vecino.padre = nodo_actual
        return None  # Si no encuentra un camino, devuelve None

    def imprimir_mapa_con_ruta(self, ruta):
        mapa_con_ruta = [fila[:] for fila in self.mapa.mapa]  # Crea una copia del mapa
        for x, y in ruta:  # Recorre cada coordenada en la ruta
            mapa_con_ruta[x][y] = '*'  # Marca la ruta en el mapa
        simbolos = {0: '.', 1: 'X', 2: 'X', 3: 'X', '*': '*'}  # Diccionario para convertir valores del mapa a símbolos
        for fila in mapa_con_ruta:  # Recorre cada fila del mapa con la ruta
            linea = ' '.join([simbolos[celda] for celda in fila])  # Convierte cada celda en su símbolo correspondiente
            print(linea)  # Imprime la línea del mapa con la ruta

# Crear el mapa
mapa = Mapa(5)
print("Mapa Inicial: ")
mapa.mostrar()

# Permitir al usuario agregar obstáculos
while True:
    agregar = input("¿Desea agregar un obstáculo? (s/n): ").lower()
    if agregar == 's':
        x = int(input("Ingrese la coordenada x del obstáculo: "))
        y = int(input("Ingrese la coordenada y del obstáculo: "))
        tipo_obstaculo = int(input("Ingrese el tipo de obstáculo (1, 2, o 3): "))
        mapa.agregar_obstaculo(x, y, tipo_obstaculo)
        print("\nMapa después de agregar un obstáculo en ({}, {}):".format(x, y))
        mapa.mostrar()
    else:
        break

# Permitir al usuario quitar obstáculos
while True:
    quitar = input("¿Desea quitar un obstáculo? (s/n): ").lower()
    if quitar == 's':
        x = int(input("Ingrese la coordenada x del obstáculo a quitar: "))
        y = int(input("Ingrese la coordenada y del obstáculo a quitar: "))
        mapa.quitar_obstaculo(x, y)
        print("\nMapa después de quitar un obstáculo en ({}, {}):".format(x, y))
        mapa.mostrar()
    else:
        break

# Ingresar puntos de inicio y fin
punto_inicio = (int(input("Ingrese la coordenada x del punto de inicio: ")),
                int(input("Ingrese la coordenada y del punto de inicio: ")))
mapa.establecer_inicio(punto_inicio[0], punto_inicio[1])

punto_fin = (int(input("Ingrese la coordenada x del punto de fin: ")),
             int(input("Ingrese la coordenada y del punto de fin: ")))
mapa.establecer_fin(punto_fin[0], punto_fin[1])

# Crear la calculadora de rutas
calculadora = CalculadoraRutas(mapa)

# Encontrar la ruta
ruta = calculadora.a_estrella()

# Imprimir el mapa con la ruta
if ruta:
    print("\nRuta encontrada:")
    calculadora.imprimir_mapa_con_ruta(ruta)
else:
    print("No se encontró una ruta.")
