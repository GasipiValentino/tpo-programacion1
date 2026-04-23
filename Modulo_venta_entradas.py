# listas con los datos de los espectaculos
espectaculos_nombres = ["Coldplay", "Duki", "Tini Stoessel"]
espectaculos_fechas  = ["15/06/2025", "22/06/2025", "30/06/2025"]
espectaculos_horas   = ["20:00", "21:00", "19:30"]
espectaculos_estados = ["activo", "activo", "activo"]

# listas con los datos de los sectores
sectores_nombres   = ["Campo", "Platea Baja", "Platea Alta"]
sectores_precios   = [5000.0, 3500.0, 2000.0]
sectores_recargos  = [0.20, 0.10, 0.05]
sectores_filas     = [5, 4, 3]
sectores_columnas  = [6, 6, 6]

# lista donde se guardan las ventas realizadas
ventas = []

# contador para generar el codigo de cada venta
contador_ventas = 1

# creo las matrices de disponibilidad para cada espectaculo y sector
disponibilidad = []
for e in range(len(espectaculos_nombres)):
    sectores_del_espectaculo = []
    for s in range(len(sectores_nombres)):
        filas = sectores_filas[s]
        columnas = sectores_columnas[s]
        matriz = [[0] * columnas for _ in range(filas)]
        sectores_del_espectaculo.append(matriz)
    disponibilidad.append(sectores_del_espectaculo)


# genera el codigo unico de venta
def generarCodigo():
    global contador_ventas
    codigo = "VTA-%04d" % contador_ventas
    contador_ventas += 1
    return codigo


# muestra los espectaculos disponibles
def mostrarEspectaculos():
    print("\n===== ESPECTACULOS DISPONIBLES =====")
    for i in range(len(espectaculos_nombres)):
        if espectaculos_estados[i] == "activo":
            print("%d. %-20s %s  %s" % (i + 1, espectaculos_nombres[i], espectaculos_fechas[i], espectaculos_horas[i]))
    print("=====================================")


# pide al usuario que elija un espectaculo y devuelve el indice
def elegirEspectaculo():
    mostrarEspectaculos()
    opcion = int(input("Seleccione el espectaculo: "))
    indice = opcion - 1
    if indice < 0 or indice >= len(espectaculos_nombres):
        print("Opcion invalida.")
        return -1
    if espectaculos_estados[indice] != "activo":
        print("Ese espectaculo no esta activo.")
        return -1
    return indice


# muestra los sectores con sus precios finales
def mostrarSectores():
    print("\n===== SECTORES Y PRECIOS =====")
    for i in range(len(sectores_nombres)):
        precio_final = sectores_precios[i] * (1 + sectores_recargos[i])
        print("%d. %-15s $%8.2f" % (i + 1, sectores_nombres[i], precio_final))
    print("===============================")


# pide al usuario que elija un sector y devuelve el indice
def elegirSector():
    mostrarSectores()
    opcion = int(input("Seleccione el sector: "))
    indice = opcion - 1
    if indice < 0 or indice >= len(sectores_nombres):
        print("Opcion invalida.")
        return -1
    return indice


# muestra el mapa de asientos del sector elegido
def mostrarMapa(indice_espectaculo, indice_sector):
    matriz = disponibilidad[indice_espectaculo][indice_sector]
    filas = sectores_filas[indice_sector]
    columnas = sectores_columnas[indice_sector]

    print("\n--- Mapa: %s - %s ---" % (espectaculos_nombres[indice_espectaculo],sectores_nombres[indice_sector]))
    print("    ", end="")
    for c in range(columnas):
        print("%3d" % (c + 1), end="")
    print()
    for f in range(filas):
        print("%2d  " % (f + 1), end="")
        for c in range(columnas):
            if matriz[f][c] == 0:
                print("  O", end="")
            else:
                print("  X", end="")
        print()
    print("O = libre   X = ocupado")


# pide la fila y asiento y verifica que este disponible
def elegirAsiento(indice_espectaculo, indice_sector):
    mostrarMapa(indice_espectaculo, indice_sector)
    filas = sectores_filas[indice_sector]
    columnas = sectores_columnas[indice_sector]

    fila = int(input("Ingrese la fila: ")) - 1
    columna = int(input("Ingrese el numero de asiento: ")) - 1

    if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
        print("Asiento fuera de rango.")
        return -1, -1
    if disponibilidad[indice_espectaculo][indice_sector][fila][columna] == 1:
        print("Ese asiento ya esta ocupado.")
        return -1, -1
    return fila, columna


# pide nombre, dni y telefono
def pedirDatos(es_comprador):
    if es_comprador:
        print("\n--- Datos del comprador ---")
    else:
        print("\n--- Datos del acompanante ---")
    nombre   = input("Nombre completo: ")
    dni      = input("DNI: ")
    telefono = input("Telefono: ")
    return nombre, dni, telefono


# calcula el precio final con recargo segun el sector
def calcularPrecio(indice_sector):
    precio_base = sectores_precios[indice_sector]
    recargo = precio_base * sectores_recargos[indice_sector]
    precio_final = precio_base + recargo
    return precio_final


# muestra el resumen de la entrada
def mostrarResumen(codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, telefono, precio_final):
    print("\n========== ENTRADA CONFIRMADA ==========")
    print("Codigo      : %s" % codigo)
    print("Espectaculo : %s" % espectaculos_nombres[indice_espectaculo])
    print("Fecha       : %s  %s" % (espectaculos_fechas[indice_espectaculo], espectaculos_horas[indice_espectaculo]))
    print("Sector      : %s" % sectores_nombres[indice_sector])
    print("Asiento     : Fila %d - Asiento %d" % (fila + 1, columna + 1))
    print("Comprador   : %s" % nombre)
    print("DNI         : %s" % dni)
    print("Telefono    : %s" % telefono)
    print("Precio      : $%8.2f" % precio_final)
    print("=========================================")


# guarda la venta en la lista y marca el asiento como ocupado
def registrarVenta(codigo, indice_espectaculo, indice_sector, fila, columna,nombre, dni, precio_final):
    venta = (codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, precio_final)
    ventas.append(venta)
    disponibilidad[indice_espectaculo][indice_sector][fila][columna] = 1


# modulo principal de venta de entradas
def venderEntradas():
    print("\n====== VENTA DE ENTRADAS ======")

    # elegir espectaculo
    indice_espectaculo = elegirEspectaculo()
    if indice_espectaculo == -1:
        return

    # elegir sector
    indice_sector = elegirSector()
    if indice_sector == -1:
        return

    # preguntar cuantas entradas quiere
    cantidad = int(input("\nCuantas entradas desea comprar? "))
    if cantidad < 1:
        print("Cantidad invalida.")
        return

    # procesar cada entrada
    for i in range(cantidad):
        print("\n--- Entrada %d de %d ---" % (i + 1, cantidad))

        fila, columna = elegirAsiento(indice_espectaculo, indice_sector)
        if fila == -1:
            print("No se pudo registrar esta entrada.")
            continue

        if i == 0:
            nombre, dni, telefono = pedirDatos(True)
        else:
            nombre, dni, telefono = pedirDatos(False)

        precio_final = calcularPrecio(indice_sector)
        codigo = generarCodigo()

        mostrarResumen(codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, telefono, precio_final)

        confirmacion = input("\nConfirmar compra? (s/n): ")
        if confirmacion == "s":
            registrarVenta(codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, precio_final)
            print("Compra registrada correctamente.")
        else:
            print("Compra cancelada.")


# menu principal del sistema
def menuPrincipal():
    opcion = 0
    while opcion != 3:
        print("\n====== SISTEMA DE ENTRADAS ======")
        print("1. Comprar entradas")
        print("2. Ver espectaculos")
        print("3. Salir")
        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            venderEntradas()
        elif opcion == 2:
            mostrarEspectaculos()
        elif opcion == 3:
            print("Hasta luego!")
        else:
            print("Opcion invalida, intente de nuevo.")


menuPrincipal()