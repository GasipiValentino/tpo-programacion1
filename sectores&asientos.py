# SECTORES (DICCIONARIO)

def inicializar_sectores():
    sectores = {
        "Campo": {"filas": 5, "columnas": 10, "precio_base": 5000},
        "Platea Baja": {"filas": 6, "columnas": 12, "precio_base": 8000},
        "Platea Alta": {"filas": 8, "columnas": 15, "precio_base": 6000},
        "Palcos": {"filas": 3, "columnas": 5, "precio_base": 15000}
    }
    return sectores


# CREAR MATRIZ DE ASIENTOS

def crear_matriz(filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            fila.append(0)  # 0 = disponible
        matriz.append(fila)
    return matriz


# CREAR TODAS LAS MATRICES (por sector)

def inicializar_disponibilidad(sectores):
    disponibilidad = {}

    for nombre_sector in sectores:
        filas = sectores[nombre_sector]["filas"]
        columnas = sectores[nombre_sector]["columnas"]
        disponibilidad[nombre_sector] = crear_matriz(filas, columnas)

    return disponibilidad


# MOSTRAR MAPA DE ASIENTOS

def mostrar_matriz(matriz):
    print("Mapa de asientos:")
    print("0 = Libre | X = Ocupado")

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 0:
                print("0", end=" ")
            else:
                print("X", end=" ")
        print() 


# MOSTRAR SECTORES Y PRECIOS

def mostrar_sectores(sectores):
    print("Sectores disponibles:")

    for nombre, datos in sectores.items():
        print(f"{nombre} - Precio: ${datos['precio_base']}")


# ELEGIR ASIENTO

def elegir_asiento(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    while True:
        fila = int(input("Ingrese fila: "))
        columna = int(input("Ingrese columna: "))

        # Validación
        if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
            print("Posición inválida. Intente de nuevo.")
            continue

        if matriz[fila][columna] != 0:
            print("Asiento ocupado. Elegí otro.")
            continue

        return fila, columna


# OCUPAR ASIENTO

def ocupar_asiento(matriz, fila, columna, codigo):
    matriz[fila][columna] = codigo


# LIBERAR ASIENTO (para devoluciones)

def liberar_asiento(matriz, fila, columna):
    matriz[fila][columna] = 0


# PRUEBA DEL MODULO

def test_modulo():
    sectores = inicializar_sectores()
    disponibilidad = inicializar_disponibilidad(sectores)

    mostrar_sectores(sectores)

    sector = input("Elegí un sector: ")

    if sector not in disponibilidad:
        print("Sector inválido")
        return

    matriz = disponibilidad[sector]

    mostrar_matriz(matriz)

    fila, columna = elegir_asiento(matriz)

    codigo = "VTA-0001"
    ocupar_asiento(matriz, fila, columna, codigo)

    print("Asiento reservado con éxito!")

    mostrar_matriz(matriz)


test_modulo()