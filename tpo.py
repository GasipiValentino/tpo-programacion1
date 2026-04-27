# from datetime import datetime

# def crearEspectaculo(nombres, fechas, horas, descripciones, estados):
#     nombre = input("Ingrese el nombre del espectaculo: ")

#     while True:
#         fecha_str = input("Ingrese la fecha (dd/mm/aaaa): ")
#         try:
#             fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
#             break
#         except ValueError:
#             print("Fecha inválida.")

#     hora = int(input("Ingrese la hora del espectaculo: "))
#     descripcion = input("Ingrese la descripcion: ")
#     estado = "activo"

#     nombres.append(nombre)
#     fechas.append(fecha.strftime("%d/%m/%Y"))
#     horas.append(hora)
#     descripciones.append(descripcion)
#     estados.append(estado)


# def listarEspectaculos(nombres, fechas, horas, estados):
#     for i in range(len(nombres)):
#         print(f"{i} - {nombres[i]} | {fechas[i]} | {horas[i]} | {estados[i]}")
        

# def modificarEspectaculo(nombres, fechas, horas, descripciones, estados):
#     # mostrar lista
#     for i in range(len(nombres)):
#         print(f"{i} - {nombres[i]} | {fechas[i]} | {horas[i]} | {estados[i]}")

#     i = int(input("Ingrese el índice a modificar: "))

#     print("¿Qué desea modificar?")
#     print("1. Nombre")
#     print("2. Fecha")
#     print("3. Hora")
#     print("4. Descripción")
#     print("5. Estado")

#     opcion = int(input("Opción: "))

#     if opcion == 1:
#         nombres[i] = input("Nuevo nombre: ")

#     elif opcion == 2:
#         fechas[i] = input("Nueva fecha (dd/mm/aaaa): ")

#     elif opcion == 3:
#         horas[i] = input("Nueva hora: ")

#     elif opcion == 4:
#         descripciones[i] = input("Nueva descripción: ")

#     elif opcion == 5:
#         estados[i] = input("Nuevo estado (activo/cancelado): ")

#     else:
#         print("Opción inválida")


# def cancelarEspectaculo(nombres, estados):
#     listarEspectaculos(nombres, fechas, horas, estados)
#     i = int(input("Ingrese el índice a cancelar: "))
#     estados[i] = "cancelado"



# nombres = []
# fechas = []
# horas = []
# descripciones = []
# estados = []

# crearEspectaculo(nombres, fechas, horas, descripciones, estados)

# listarEspectaculos(nombres, fechas, horas, estados)

# modificarEspectaculo(nombres, fechas, horas, descripciones, estados)

# listarEspectaculos(nombres, fechas, horas, estados)

from datetime import datetime

# listas con los datos de los espectaculos
espectaculos_nombres = ["Coldplay", "Duki", "Tini Stoessel"]
espectaculos_fechas  = ["15/06/2025", "22/06/2025", "30/06/2025"]
espectaculos_horas   = ["20:00", "21:00", "19:30"]
espectaculos_descripciones = ["", "", ""]
espectaculos_estados = ["activo", "activo", "activo"]

# listas con los datos de los sectores
sectores_nombres   = ["Campo", "Platea Baja", "Platea Alta"]
sectores_precios   = [5000.0, 3500.0, 2000.0]
sectores_recargos  = [0.20, 0.10, 0.05]
sectores_filas     = [5, 4, 3]
sectores_columnas  = [6, 6, 6]

# variables para la venta de entradas
ventas = []
contador_ventas = 1

def inicializar_disponibilidad():
    """Construye la estructura de disponibilidad según los espectáculos actuales. Recorre cada espectaculo y para cada uno crea sus sectores en una matriz filas x columnas. Le pone 0 si el asiento esta libre. Todas las ubicaciones van a tener 6 columnas y 5, 4 y 3 filas el campo, platea baja y platea alta respectivamente"""
    disp = []
    for e in range(len(espectaculos_nombres)):
        sectores_del_espectaculo = []
        for s in range(len(sectores_nombres)):
            filas = sectores_filas[s]
            columnas = sectores_columnas[s]
            matriz = [[0] * columnas for i in range(filas)]
            sectores_del_espectaculo.append(matriz)
        disp.append(sectores_del_espectaculo)
    return disp

disponibilidad = inicializar_disponibilidad()

# FUNCIONES PARA LA GESTIÓN DE ESPECTÁCULOS
def crearEspectaculo():
    """Agrega un nuevo espectáculo con todos sus datos."""
    nombre = input("Ingrese el nombre del artista/banda: ")

    # while True:
    #     fecha_str = input("Ingrese la fecha (dd/mm/aaaa): ")
    #     try:
    #         datetime.strptime(fecha_str, "%d/%m/%Y")
    #         break
    #     except ValueError:
    #         print("Fecha inválida.")
    # Lo saco porque no vimos try y except

    while True:
        fecha_str = input("Ingrese la fecha (dd/mm/aaaa): ")
        
        partes = fecha_str.split("/")
        
        if len(partes) == 3:
            dia, mes, anio = partes
            
            if dia.isdigit() and mes.isdigit() and anio.isdigit():
                dia = int(dia)
                mes = int(mes)
                anio = int(anio)
                
                if 1 <= dia <= 31 and 1 <= mes <= 12 and anio > 0:
                    break
    
        print("Fecha inválida.")

    hora = input("Ingrese la hora (HH:MM): ")
    # descripcion = input("Ingrese la descripción: ") La saco porque los primeros tres no tienen
    estado = "activo"

    espectaculos_nombres.append(nombre)
    espectaculos_fechas.append(fecha_str)
    espectaculos_horas.append(hora)
    # espectaculos_descripciones.append(descripcion)
    espectaculos_estados.append(estado)

    # Agregar las matrices de disponibilidad para el nuevo espectáculo
    nuevas_matrices = []
    for s in range(len(sectores_nombres)):
        filas = sectores_filas[s]
        columnas = sectores_columnas[s]
        matriz = [[0] * columnas for i in range(filas)]
        nuevas_matrices.append(matriz)
    disponibilidad.append(nuevas_matrices)
    print("Espectáculo creado correctamente.")

def listarEspectaculos():
    """Muestra todos los espectáculos (activos y cancelados) con índice."""
    print("\n--- Listado completo de espectáculos ---")
    for i in range(len(espectaculos_nombres)):
        print(f"{i} - {espectaculos_nombres[i]} | {espectaculos_fechas[i]} | "
              f"{espectaculos_horas[i]} | {espectaculos_estados[i]} | "
              f"{espectaculos_descripciones[i]}")
        # VERIFICAR SI LOS ESPECTACULOS VAN A TENER DESCRIPCIÓN

# Muy buena funcion, habria que ver si el estado lo podemos manejar con un booleano tipo activo: true o activo: false, asi evitamos confuciones
def modificarEspectaculo():
    """Permite modificar los datos de un espectáculo existente."""
    listarEspectaculos()
    i = int(input("Ingrese el índice del espectáculo a modificar: "))
    if i < 0 or i >= len(espectaculos_nombres):
        print("Índice inválido.")
        return

    print("¿Qué desea modificar?")
    print("1. Nombre")
    print("2. Fecha")
    print("3. Hora")
    print("4. Descripción")
    print("5. Estado")

    opcion = int(input("Opción: "))

    if opcion == 1:
        espectaculos_nombres[i] = input("Nuevo nombre: ")
    elif opcion == 2:
        espectaculos_fechas[i] = input("Nueva fecha (dd/mm/aaaa): ")
    elif opcion == 3:
        espectaculos_horas[i] = input("Nueva hora (HH:MM): ")
    elif opcion == 4:
        espectaculos_descripciones[i] = input("Nueva descripción: ")
    elif opcion == 5:
        espectaculos_estados[i] = input("Nuevo estado (activo/cancelado): ")
    else:
        print("Opción inválida.")

def cancelarEspectaculo():
    """Cambia el estado de un espectáculo a cancelado manualmente."""
    listarEspectaculos()
    i = int(input("Ingrese el índice del espectáculo a cancelar: "))
    if i < 0 or i >= len(espectaculos_nombres):
        print("Índice inválido.")
        return
    espectaculos_estados[i] = "cancelado"
    print(f"Espectáculo '{espectaculos_nombres[i]}' cancelado.")



# FUNCIONES PARA LA VENTA DE ENTRADAS
def generarCodigo(contador_ventas):
    """Genera un código único de venta."""
    # global contador_ventas saque global porque no lo vimos, agregue el parametro y lo devuelvo modificado
    # VTA-%04d crea un numero entero con 4 digitos rellenando con ceros a la izq
    codigo = "VTA-%04d" % contador_ventas
    contador_ventas += 1
    return codigo, contador_ventas

def mostrarEspectaculos():
    """Muestra solamente los espectáculos activos (usado en la venta)."""
    print("\n===== ESPECTACULOS DISPONIBLES =====")
    for i in range(len(espectaculos_nombres)):
        if espectaculos_estados[i] == "activo":
            # %d muestra un entero, %s un string, y %-20s un string pero deja un espacio de 20 caracteres
            print("%d. %-20s %s  %s" % (i + 1, espectaculos_nombres[i],
                                         espectaculos_fechas[i], espectaculos_horas[i]))
    print("=====================================")

def elegirEspectaculo():
    """Pide al usuario que elija un espectáculo (activo) y devuelve su índice. se va a usar en venderEntradas()"""
    mostrarEspectaculos()
    opcion = int(input("Seleccione el espectáculo: "))
    indice = opcion - 1
    if indice < 0 or indice >= len(espectaculos_nombres):
        print("Opción inválida.")
        return -1
    if espectaculos_estados[indice] != "activo":
        print("Ese espectáculo no está activo.")
        return -1
    return indice

def mostrarSectores():
    """Muestra los sectores con sus precios finales (incluye recargo)."""
    print("\n===== SECTORES Y PRECIOS =====")
    for i in range(len(sectores_nombres)):
        precio_final = sectores_precios[i] * (1 + sectores_recargos[i])
        # %.2f muestra dos decimales
        print("%d. %-15s $%.2f" % (i + 1, sectores_nombres[i], precio_final))
    print("===============================")

def elegirSector():
    """Pide al usuario que elija un sector y devuelve su índice."""
    mostrarSectores()
    opcion = int(input("Seleccione el sector: "))
    indice = opcion - 1
    if indice < 0 or indice >= len(sectores_nombres):
        print("Opción inválida.")
        return -1
    return indice

# recibe el espectaculo que se eligio y el sector
def mostrarMapa(indice_espectaculo, indice_sector):
    """Muestra el mapa de asientos del sector elegido."""
    # matriz es la grilla de asientos con su respectiva disponibilidad del espectaculo y del sector seleccionado
    matriz = disponibilidad[indice_espectaculo][indice_sector]

    # Obtenemos las respectivas dimensiones de cada sector
    filas = sectores_filas[indice_sector]
    columnas = sectores_columnas[indice_sector]

    # Imprime el nombre del espectaculo y sector elegido
    print("\n--- Mapa: %s - %s ---" % (espectaculos_nombres[indice_espectaculo],
                                      sectores_nombres[indice_sector]))
    
    # Recorre de manera prolija la cantidad de columnas y las enumera. + 1 es para que no empiece desde 0. end="" reemplaza el salto de linea para que cada numero se ponga uno al lado del otro
    print("    ", end="")
    for c in range(columnas):
        print("%3d" % (c + 1), end="")
    print()
    # Ahora recorre cada fila imprimiendo el numero de cada una y luego recorre cada asiento de la fila (columna) y si es 0 muestra O seguido de un end="" para que se sigan impriendo numeros continuos en esa fila
    for f in range(filas):
        print("%2d  " % (f + 1), end="")
        for c in range(columnas):
            if matriz[f][c] == 0:
                print("  O", end="")
            else:
                print("  X", end="")
        print()
    print("O = libre   X = ocupado")

def elegirAsiento(indice_espectaculo, indice_sector):
    """Pide fila y asiento, verifica que esté libre y devuelve las coordenadas."""
    mostrarMapa(indice_espectaculo, indice_sector)
    filas = sectores_filas[indice_sector]
    columnas = sectores_columnas[indice_sector]

    fila = int(input("Ingrese la fila: ")) - 1
    columna = int(input("Ingrese el número de asiento: ")) - 1

    if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
        print("Asiento fuera de rango.")
        return -1, -1
    # Esto significa por ej: Espectaculo 0 = Coldpay, Sector 1 = Platea baja, fila 2, columna 3
    if disponibilidad[indice_espectaculo][indice_sector][fila][columna] == 1:
        print("Ese asiento ya está ocupado.")
        return -1, -1
    return fila, columna

# recibe si es el comprador, sino, es acompañante 
def pedirDatos(es_comprador):
    """Solicita nombre, DNI y teléfono del comprador/acompañante."""
    if es_comprador:
        print("\n--- Datos del comprador ---")
    else:
        print("\n--- Datos del acompañante ---")
    nombre   = input("Nombre completo: ")
    dni      = input("DNI: ")
    telefono = input("Teléfono: ")
    return nombre, dni, telefono

def calcularPrecio(indice_sector):
    """Calcula el precio final con recargo incluido."""
    return sectores_precios[indice_sector] * (1 + sectores_recargos[indice_sector])

# me quede aca
def mostrarResumen(codigo, indice_espectaculo, indice_sector, fila, columna,
                   nombre, dni, telefono, precio_final):
    """Muestra el resumen de una entrada confirmada."""
    print("\n========== ENTRADA CONFIRMADA ==========")
    print("Código      : %s" % codigo)
    print("Espectáculo : %s" % espectaculos_nombres[indice_espectaculo])
    print("Fecha       : %s  %s" % (espectaculos_fechas[indice_espectaculo],
                                     espectaculos_horas[indice_espectaculo]))
    print("Sector      : %s" % sectores_nombres[indice_sector])
    print("Asiento     : Fila %d - Asiento %d" % (fila + 1, columna + 1))
    print("Comprador   : %s" % nombre)
    print("DNI         : %s" % dni)
    print("Teléfono    : %s" % telefono)
    print("Precio      : $%.2f" % precio_final)
    print("=========================================")

def registrarVenta(codigo, indice_espectaculo, indice_sector, fila, columna,
                   nombre, dni, precio_final):
    """Guarda la venta y marca el asiento como ocupado."""
    venta = (codigo, indice_espectaculo, indice_sector, fila, columna,
             nombre, dni, precio_final)
    ventas.append(venta)
    # Aca es donde cambia el valor de O (libre)
    disponibilidad[indice_espectaculo][indice_sector][fila][columna] = 1

def venderEntradas(contador_ventas):
    """Proceso completo de venta de una o varias entradas."""
    print("\n====== VENTA DE ENTRADAS ======")

    indice_espectaculo = elegirEspectaculo()
    while indice_espectaculo == -1:
        print("Espectáculo inválido. Intente nuevamente.")
        indice_espectaculo = elegirEspectaculo()

    indice_sector = elegirSector()
    while indice_sector == -1: 
        print("Sector inválido. Intente nuevamente.")
        indice_sector = elegirSector()

    cantidad = int(input("\n¿Cuántas entradas desea comprar? "))
    while cantidad < 1:
        print("Cantidad inválida.")
        cantidad = int(input("¿Cuántas entradas desea comprar? "))

    for i in range(cantidad):
        print("\n--- Entrada %d de %d ---" % (i + 1, cantidad))

        fila, columna = elegirAsiento(indice_espectaculo, indice_sector)
        while fila == -1:
            print("Asiento inválido. Intente nuevamente.")
            fila, columna = elegirAsiento(indice_espectaculo, indice_sector)

        if i == 0:
            nombre, dni, telefono = pedirDatos(True)
        else:
            nombre, dni, telefono = pedirDatos(False)

        precio_final = calcularPrecio(indice_sector)
        codigo, nuevo_contador = generarCodigo(contador_ventas)
        contador_ventas = nuevo_contador

        mostrarResumen(codigo, indice_espectaculo, indice_sector, fila, columna,
                       nombre, dni, telefono, precio_final)

        confirmacion = input("\n¿Confirmar compra? (s/n): ")
        if confirmacion == "s":
            registrarVenta(codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, precio_final)
            print("Compra registrada correctamente.")
        else:
            print("Compra cancelada.")

    return contador_ventas

# me gustaria que por ejemplo despues de poner mal un sector, por ejemplo poner 4 en vez de 1, 2 o 3 te vuelva a preguntar el sector, no que vaya de vuelta al principio

# Menu
def main():
    contador_ventas = 1
    while True:
        print("\n====== SISTEMA DE GESTIÓN DE ESPECTÁCULOS ======")
        print("1. Comprar entradas")
        print("2. Ver espectáculos activos")
        print("3. Listar todos los espectáculos")
        print("4. Crear nuevo espectáculo")
        print("5. Modificar espectáculo")
        print("6. Cancelar espectáculo")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            contador_ventas = venderEntradas(contador_ventas)
        elif opcion == "2":
            mostrarEspectaculos()
        elif opcion == "3":
            listarEspectaculos()
        elif opcion == "4":
            crearEspectaculo()
        elif opcion == "5":
            modificarEspectaculo()
        elif opcion == "6":
            cancelarEspectaculo()
        elif opcion == "7":
            print("Gracias por usar la plataforma!")
            break
        else:
            print("Opción inválida, intente de nuevo.")

main()
