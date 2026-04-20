from datetime import datetime

def crearEspectaculo(nombres, fechas, horas, descripciones, estados):
    nombre = input("Ingrese el nombre del espectaculo: ")

    while True:
        fecha_str = input("Ingrese la fecha (dd/mm/aaaa): ")
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha inválida.")

    hora = int(input("Ingrese la hora del espectaculo: "))
    descripcion = input("Ingrese la descripcion: ")
    estado = "activo"

    nombres.append(nombre)
    fechas.append(fecha.strftime("%d/%m/%Y"))
    horas.append(hora)
    descripciones.append(descripcion)
    estados.append(estado)


def listarEspectaculos(nombres, fechas, horas, estados):
    for i in range(len(nombres)):
        print(f"{i} - {nombres[i]} | {fechas[i]} | {horas[i]} | {estados[i]}")
        

def modificarEspectaculo(nombres, fechas, horas, descripciones, estados):
    # mostrar lista
    for i in range(len(nombres)):
        print(f"{i} - {nombres[i]} | {fechas[i]} | {horas[i]} | {estados[i]}")

    i = int(input("Ingrese el índice a modificar: "))

    print("¿Qué desea modificar?")
    print("1. Nombre")
    print("2. Fecha")
    print("3. Hora")
    print("4. Descripción")
    print("5. Estado")

    opcion = int(input("Opción: "))

    if opcion == 1:
        nombres[i] = input("Nuevo nombre: ")

    elif opcion == 2:
        fechas[i] = input("Nueva fecha (dd/mm/aaaa): ")

    elif opcion == 3:
        horas[i] = input("Nueva hora: ")

    elif opcion == 4:
        descripciones[i] = input("Nueva descripción: ")

    elif opcion == 5:
        estados[i] = input("Nuevo estado (activo/cancelado): ")

    else:
        print("Opción inválida")


def cancelarEspectaculo(nombres, estados):
    listarEspectaculos(nombres, fechas, horas, estados)
    i = int(input("Ingrese el índice a cancelar: "))
    estados[i] = "cancelado"



nombres = []
fechas = []
horas = []
descripciones = []
estados = []

crearEspectaculo(nombres, fechas, horas, descripciones, estados)

listarEspectaculos(nombres, fechas, horas, estados)

modificarEspectaculo(nombres, fechas, horas, descripciones, estados)

listarEspectaculos(nombres, fechas, horas, estados)