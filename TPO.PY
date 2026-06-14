import json
import hashlib


# campo no esta numerado
# la estrucutra de 3 sectores queda pero el campo se usa con capacidad (30)
# Quedan las filas y columnas del campo en 0 para que concuerden los nombres, precios etc

CAMPO_CAPACIDAD    = 30
GENEROS              = ["Rock Nacional", "Pop", "Cumbia", "Electronica", "Jazz", "Reggaeton", "Otro"]
# Roles con contraseñas hardcodeadasdiferenciando administrador y boletero.
# usuarios admin/boletero y contraselas admin123/bole123
# en el segundo valor se indica el rol, para despues con un if, mostrar el menu correspondiente a caad uno


# el archivo de espectaculos en json
ARCHIVO_ESPECTACULOS = "espectaculos.json"
ARCHIVO_VENTAS = "ventas.json"
ARCHIVO_USUARIOS     = "usuarios.json"
ARCHIVO_SECTORES = "sectores.json"

# FUNCIONES PARA LA PERSISTENCIA EN SESIONES CON ARCHIVOS
def guardarEspectaculos(espectaculos_nombres, espectaculos_fechas,
                        espectaculos_horas, espectaculos_descripciones,
                        espectaculos_estados, espectaculos_generos,  disponibilidad):
    # recibe los datos, que antes eran listas, mediante un bloque try catch abre el archivo y grba estos datos que recibe. Se usa esta funcion para crear, modificar y eliminar archivos
    datos = {
        "nombres":        espectaculos_nombres,
        "fechas":         espectaculos_fechas,
        "horas":          espectaculos_horas,
        "descripciones":  espectaculos_descripciones,
        "estados":        espectaculos_estados,
        "generos":        espectaculos_generos,
        "disponibilidad": disponibilidad,
    }
    try:
        archivo = open(ARCHIVO_ESPECTACULOS, "wt", encoding="UTF-8")
        json.dump(datos, archivo)
        archivo.close()
    except FileNotFoundError as error:
        print("Error: no se puede crear el archivo de espectáculos: ", error)
    except OSError as error:
        print("Error al grabar espectáculos: ", error)

# obtiene el archivo y lee los datos del json y retorna los datos  en el orden preestablecido. Si no encuentra el archivo devuelve 6 listas vacias (cantidad de datos). El OSError tambien devuelve 6 listas vacias indicando que no se peude leer el archivo
def cargarEspectaculos():
    try:
        # usamos rt solo para leer
        archivo = open(ARCHIVO_ESPECTACULOS, "rt", encoding="UTF-8")
        datos = json.load(archivo)
        archivo.close()
        return (
            datos["nombres"],
            datos["fechas"],
            datos["horas"],
            datos["descripciones"],
            datos["estados"],
            datos["generos"],
            datos["disponibilidad"],
        )
    except FileNotFoundError:
        print("Archivo de espectáculos no encontrado. Iniciando sin datos.")
        return [], [], [], [], [], [], []
    except OSError as error:
        print("Error al leer espectáculos:", error)
        return [], [], [], [], [], [], []

# guarda las ventas y el contador en el archivo json
def guardarVentas(ventas, contador_ventas):
    datos = {
        "contador": contador_ventas,
        "ventas":   [list(v) for v in ventas],
    }
    try:
        archivo = open(ARCHIVO_VENTAS, "wt", encoding="UTF-8")
        json.dump(datos, archivo)
        archivo.close()
    except OSError as error:
        print("Error al guardar ventas: ", error)

# carga las ventas y el contador desde el archivo json
def cargarVentas():
    try:
        archivo = open(ARCHIVO_VENTAS, "rt", encoding="UTF-8")
        datos = json.load(archivo)
        archivo.close()
        ventas = [tuple(v) for v in datos["ventas"]]
        return ventas, datos["contador"]
    except FileNotFoundError:
        return [], 1
    except OSError as error:
        print("Error al leer ventas:", error)
        return [], 1

# convierte la clave a un hash md5 para no guardarla en texto plano
def encriptarClave(clave):
    return hashlib.md5(clave.encode()).hexdigest()

# guarda el diccionario de usuarios en el archivo json
def guardarUsuarios(usuarios):
    try:
        archivo = open(ARCHIVO_USUARIOS, "wt", encoding="UTF-8")
        json.dump(usuarios, archivo)
        archivo.close()
    except OSError as error:
        print("Error al guardar usuarios: ", error)

# carga los usuarios desde el archivo, si no existe crea los usuarios por defecto
def cargarUsuarios():
    try:
        archivo = open(ARCHIVO_USUARIOS, "rt", encoding="UTF-8")
        usuarios = json.load(archivo)
        archivo.close()
        return usuarios
    except FileNotFoundError:
        # si no existe el archivo creamos los usuarios por defecto y los guardamos
        usuarios = {
            "admin":    [encriptarClave("admin123"), "administrador"],
            "boletero": [encriptarClave("bole123"),  "boletero"],
        }
        guardarUsuarios(usuarios)
        return usuarios
    except OSError as error:
        print("Error al leer usuarios:", error)
        return {}
    
# guarda el catalogo de sectores en el archivo json
def guardarSectores(sectores_nombres, sectores_precios, sectores_recargos, sectores_filas, sectores_columnas):
    datos = {
        "nombres":   sectores_nombres,
        "precios":   sectores_precios,
        "recargos":  sectores_recargos,
        "filas":     sectores_filas,
        "columnas":  sectores_columnas,
    }
    try:
        archivo = open(ARCHIVO_SECTORES, "wt", encoding="UTF-8")
        json.dump(datos, archivo)
        archivo.close()
    except OSError as error:
        print("Error al guardar sectores: ", error)

# carga el catalogo de sectores desde el archivo, si no existe usa los valores por defecto
def cargarSectores():
    try:
        archivo = open(ARCHIVO_SECTORES, "rt", encoding="UTF-8")
        datos = json.load(archivo)
        archivo.close()
        return (
            datos["nombres"],
            datos["precios"],
            datos["recargos"],
            datos["filas"],
            datos["columnas"],
        )
    except FileNotFoundError:
        # si no existe el archivo usamos los sectores por defecto y los guardamos
        nombres  = ["Campo", "Platea Baja", "Platea Alta"]
        precios  = [5000.0, 3500.0, 2000.0]
        recargos = [0.20, 0.10, 0.05]
        filas    = [0, 4, 3]
        columnas = [0, 6, 6]
        guardarSectores(nombres, precios, recargos, filas, columnas)
        return nombres, precios, recargos, filas, columnas
    except OSError as error:
        print("Error al leer sectores:", error)
        return [], [], [], [], []

# pide un numero entero y maneja el error si se ingresa texto
def leer_entero(mensaje):
    numero = None
    while numero is None:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: ingrese un número entero válido.")
    return numero


# pide usuario y clave, compara la clave encriptada con la guardada
def login(usuarios):
    print("\n===== INICIO DE SESIÓN =====")
    usuario = input("Usuario: ").strip()
    clave   = input("Contraseña: ").strip()

    if usuario not in usuarios:
        print("Usuario no encontrado.")
        return None

    clave_encriptada, rol = usuarios[usuario]

    if encriptarClave(clave) != clave_encriptada:
        print("Contraseña incorrecta.")
        return None

    print("Bienvenido %s" % rol)
    return rol

# pide y valida la fecha en formato dd/mm/aaaa, devuelve el string validado
def pedirFecha():
    fecha_str = ""
    fecha_valida = False
    while not fecha_valida:
        fecha_str = input("Ingrese la fecha (dd/mm/aaaa): ").strip()
        try:
            partes = fecha_str.split("/")
            if len(partes) != 3:
                print("Error: formato incorrecto.")
            else:
                dia, mes, anio = int(partes[0]), int(partes[1]), int(partes[2])
                if not (1 <= dia <= 31):
                    print("Error: día inválido.")
                elif not (1 <= mes <= 12):
                    print("Error: mes inválido.")
                elif anio <= 0:
                    print("Error: año inválido.")
                else:
                    fecha_valida = True
        except ValueError:
            print("Error: la fecha debe contener solo números.")
    return fecha_str

# pide y valida la hora en formato HH:MM, devuelve el string validado
def pedirHora():
    hora_str = ""
    hora_valida = False
    while not hora_valida:
        hora_str = input("Ingrese la hora (HH:MM): ").strip()
        try:
            partes = hora_str.split(":")
            if len(partes) != 2:
                print("Error: formato incorrecto.")
            else:
                hh, mm = int(partes[0]), int(partes[1])
                if not (0 <= hh <= 23):
                    print("Error: hora inválida.")
                elif not (0 <= mm <= 59):
                    print("Error: minutos inválidos.")
                else:
                    hora_valida = True
        except ValueError:
            print("Error: la hora debe contener solo números.")
    return hora_str

# muestra los generos disponibles y devuelve el elegido
def pedirGenero():
    print("Géneros disponibles:")
    for i in range(len(GENEROS)):
        print("%d. %s" % (i + 1, GENEROS[i]))
    indice = -1
    while indice < 0 or indice >= len(GENEROS):
        indice = leer_entero("Seleccione el género: ") - 1
        if indice < 0 or indice >= len(GENEROS):
            print("Error: opción fuera de rango.")
    return GENEROS[indice]

def crearEspectaculo(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_descripciones, espectaculos_estados, espectaculos_generos,  disponibilidad, sectores_nombres, sectores_filas, sectores_columnas):
    nombre      = input("Ingrese el nombre del artista/banda: ").strip()
    fecha_str   = pedirFecha()
    hora_str    = pedirHora()
    descripcion = input("Descripción del evento: ").strip()
    genero      = pedirGenero()

    # agregamos los datos a las listas y creamos la matriz de disponibilidad
    espectaculos_nombres.append(nombre)
    espectaculos_fechas.append(fecha_str)
    espectaculos_horas.append(hora_str)
    espectaculos_descripciones.append(descripcion)
    espectaculos_estados.append("activo")
    espectaculos_generos.append(genero)

    nuevas_matrices = []
    for s in range(len(sectores_nombres)):
        if s == 0:
            nuevas_matrices.append(0)
        else:
            filas    = sectores_filas[s]
            columnas = sectores_columnas[s]
            nuevas_matrices.append([[0] * columnas for _ in range(filas)])
    disponibilidad.append(nuevas_matrices)
    print("Espectáculo '%s' creado correctamente." % nombre)

def listarEspectaculos(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_estados, espectaculos_descripciones, espectaculos_generos):
    print("\n--- Listado completo de espectáculos ---")
    if not espectaculos_nombres:
        print("No hay espectáculos registrados.")
        return
    for i in range(len(espectaculos_nombres)):
        print("%d - %s | %s | %s | %s | %s | %s" % (i + 1, espectaculos_nombres[i], espectaculos_fechas[i], espectaculos_horas[i], espectaculos_estados[i], espectaculos_generos[i], espectaculos_descripciones[i]))

# recibe los datos para luego pasarselos a la funcion listar espectaculos, pedimos el indice del espectaculo a modificar y le restamos uno para que coinicda con el elegido (ya que no empieza en 0 la lista) y despues preguntamos que dato modificar con las misma validaciones de antes
def modificarEspectaculo(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_descripciones, espectaculos_estados, espectaculos_generos):
    if not espectaculos_nombres:
        print("No hay espectáculos para modificar.")
        return
    listarEspectaculos(espectaculos_nombres, espectaculos_fechas,
                       espectaculos_horas, espectaculos_estados,
                       espectaculos_descripciones, espectaculos_generos)
    while True:
        i = leer_entero("Índice del espectáculo a modificar: ")
        i = i - 1
        if 0 <= i < len(espectaculos_nombres):
            break
        print("Error: índice fuera de rango.")

    print("¿Qué desea modificar?")
    print("1. Nombre")
    print("2. Fecha")
    print("3. Hora")
    print("4. Descripción")
    print("5. Estado")
    print("6. Modificar genero")
    opcion = leer_entero("Opción: ")

    if opcion == 1:
        espectaculos_nombres[i] = input("Nuevo nombre: ").strip()

    elif opcion == 2:
        espectaculos_fechas[i] = pedirFecha()

    elif opcion == 3:
        espectaculos_horas[i] = pedirHora()

    elif opcion == 4:
        espectaculos_descripciones[i] = input("Nueva descripción: ").strip()

    elif opcion == 5:
        espectaculos_estados[i] = input("Nuevo estado (activo/cancelado): ").strip()
    
    elif opcion == 6:
        espectaculos_generos[i] = pedirGenero()

    else:
        print("Opción inválida.")

# no usamos listarEspectaculos para no tener que llamar a todos los datos, total necesitamos unicamente el nombre del espectaculo y su estado, los recorremos con un for tradicional
def cancelarEspectaculo(espectaculos_nombres, espectaculos_estados):
    if not espectaculos_nombres:
        print("No hay espectáculos para cancelar.")
        return
    for i, nombre in enumerate(espectaculos_nombres):
        print("%d - %s [%s]" % (i + 1, nombre, espectaculos_estados[i]))
    while True:
        i = leer_entero("Índice del espectáculo a cancelar: ")
        i = i - 1
        if 0 <= i < len(espectaculos_nombres):
            break
        print("Error: índice fuera de rango.")
    espectaculos_estados[i] = "cancelado"
    print("Espectáculo '%s' cancelado." % espectaculos_nombres[i])


# FUNCIONES PARA LA VENTA DE ENTRADAS
def generarCodigo(contador_ventas):
    # genera un codigo de venta que empieza con VTA
    codigo = "VTA-%04d" % contador_ventas
    return codigo, contador_ventas + 1


def mostrarEspectaculos(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_estados, espectaculos_generos):
    # Muestra solo los espectáculos activos preguntando si en cada indice el estado es activo
    print("\n===== ESPECTÁCULOS DISPONIBLES =====")
    hay_activos = False
    for i in range(len(espectaculos_nombres)):
        if espectaculos_estados[i] == "activo":
            print("%d. %-20s %s  %s  %s" % (i + 1, espectaculos_nombres[i], espectaculos_fechas[i], espectaculos_horas[i], espectaculos_generos[i]))
            hay_activos = True
    if not hay_activos:
        print("No hay espectáculos activos en este momento.")
    print("=====================================")


def elegirEspectaculo(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_estados, espectaculos_generos):
    mostrarEspectaculos(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_estados, espectaculos_generos)
    indice = -1
    while indice < 0 or indice >= len(espectaculos_nombres) or espectaculos_estados[indice] != "activo":
        opcion = leer_entero("Seleccione el espectáculo (número): ")
        indice = opcion - 1
        if not (0 <= indice < len(espectaculos_nombres)):
            print("Error: opción fuera de rango.")
        elif espectaculos_estados[indice] != "activo":
            print("Error: ese espectáculo no está activo.")
    return indice


def mostrarSectores(sectores_nombres, sectores_precios, sectores_recargos):
    # mostramos los sectories con sus respectivos precios y recargos
    print("\n===== SECTORES Y PRECIOS =====")
    for i in range(len(sectores_nombres)):
        precio_final = sectores_precios[i] * (1 + sectores_recargos[i])
        print("%d. %-15s $%.2f" % (i + 1, sectores_nombres[i], precio_final))
    print("================================")


def elegirSector(sectores_nombres, sectores_precios, sectores_recargos):
    mostrarSectores(sectores_nombres, sectores_precios, sectores_recargos)
    indice = -1
    while indice < 0 or indice >= len(sectores_nombres):
        opcion = leer_entero("Seleccione el sector: ")
        indice = opcion - 1
        if indice < 0 or indice >= len(sectores_nombres):
            print("Error: opción fuera de rango.")
    return indice

# imprime columna por columna de forma recursiva
# caso base: llegamos a la ultima columna, termina la fila
# caso recursivo: imprime la columna actual y pasa a la siguiente
def imprimirColumnasMapa(matriz, fila_actual, columna_actual, total_columnas):
    if columna_actual >= total_columnas:
        print()
        return
    if matriz[fila_actual][columna_actual] == 0:
        print("  O", end="")
    else:
        print("  X", end="")
    imprimirColumnasMapa(matriz, fila_actual, columna_actual + 1, total_columnas)

# imprime fila por fila de forma recursiva, usa imprimirColumnasMapa para cada fila
# caso base: llegamos a la ultima fila, no hay mas para imprimir
# caso recursivo: imprime la fila actual y pasa a la siguiente
def imprimirFilasMapa(matriz, fila_actual, total_filas, total_columnas):
    if fila_actual >= total_filas:
        return
    print("%2d  " % (fila_actual + 1), end="")
    imprimirColumnasMapa(matriz, fila_actual, 0, total_columnas)
    imprimirFilasMapa(matriz, fila_actual + 1, total_filas, total_columnas)


def mostrarMapa(disponibilidad, indice_espectaculo, indice_sector, espectaculos_nombres, sectores_nombres, sectores_filas, sectores_columnas):
    # se sigue mostrando el mapa como antes O libre y X ocupado, pero ahora se calculan los lugares del campo (que es 30 si no hay entradas compradas).
    # si el sector elegido no es campo, primero se guarda en la variable matriz la matriz de disponibilidad correspondiente a ese espectaculo y sector. Despues se obtienen la cantidad de filas y columnas de ese sector para saber cuantas posiciones tiene. Luego se muestra el nombre del espectaculo y del sector y se imprimen los numeros de los asientos en la parte superior usando un for que recorre todas las columnas. Despues otro for recorre cada fila de la matriz, imprime el numero de fila y dentro de ese for hay otro que recorre todas las columnas de esa fila. Si en la posicion de la matriz hay un 0 significa que el asiento esta libre y se muestra una O, pero si hay un 1 significa que ya fue vendido y se muestra una X. De esta forma se arma visualmente el mapa de ubicaciones para que el usuario pueda ver que asientos estan disponibles y cuales no. 
    if indice_sector == 0:
        ocupados = disponibilidad[indice_espectaculo][0]
        libres   = CAMPO_CAPACIDAD - ocupados
        print("\n--- CAMPO ABIERTO: %d lugares disponibles de %d ---" % (libres, CAMPO_CAPACIDAD))
        return

    matriz   = disponibilidad[indice_espectaculo][indice_sector]
    filas    = sectores_filas[indice_sector]
    columnas = sectores_columnas[indice_sector]

    print("\n--- Mapa: %s - %s ---" % (espectaculos_nombres[indice_espectaculo],
                                       sectores_nombres[indice_sector]))
    print("    ", end="")
    for c in range(columnas):
        print("%3d" % (c + 1), end="")
    print()
    imprimirFilasMapa(matriz, 0, filas, columnas)
    print("O = libre   X = ocupado")


def elegirAsiento(disponibilidad, indice_espectaculo, indice_sector,
                  sectores_filas, sectores_columnas):
    # para campono pide asiento (abierto), para lso otros sectores pide fila y columna    devulve (fila, columna) o (-1, -1) para Campo.
    if indice_sector == 0:
        ocupados = disponibilidad[indice_espectaculo][0]
        if ocupados >= CAMPO_CAPACIDAD:
            print("El Campo está lleno.")
            return None, None
        return -1, -1

    filas    = sectores_filas[indice_sector]
    columnas = sectores_columnas[indice_sector]

    while True:
        fila    = leer_entero("Ingrese la fila: ") - 1
        columna = leer_entero("Ingrese el número de asiento: ") - 1
        if not (0 <= fila < filas):
            print("Error: fila fuera de rango.")
        elif not (0 <= columna < columnas):
            print("Error: asiento fuera de rango.")
        elif disponibilidad[indice_espectaculo][indice_sector][fila][columna] != 0:
            print("Error: ese asiento ya está ocupado.")
        else:
            break
    return fila, columna


def pedirDatos(es_comprador):
    # pedimos din telefono y nombre, convertimos dni y telefono en string para poder aplicarles el .strip y despues verificamos que sean numeros con el bloque except (sni y telefono)
    if es_comprador:
        print("\n--- Datos del comprador ---")
    else:
        print("\n--- Datos del acompañante ---")

    while True:
        nombre = input("Nombre completo: ").strip()
        if nombre:
            break
        print("Error: el nombre no puede estar vacío.")

    while True:
        dni_str = input("DNI: ").strip()
        try:
            dni_int = int(dni_str)
            if 7 <= len(dni_str) <= 8:
                dni = dni_str 
                break
            else:
                print("Error: el DNI debe tener 7 u 8 dígitos.")
        except ValueError:
            print("Error: el DNI debe contener solo números.")

    while True:
        tel_str = input("Teléfono: ").strip()
        try:
            int(tel_str) 
            if tel_str:
                telefono = tel_str
                break
            else:
                print("Error: el teléfono no puede estar vacío.")
        except ValueError:
            print("Error: el teléfono debe contener solo números.")

    return nombre, dni, telefono


def calcularPrecio(indice_sector, sectores_precios, sectores_recargos):
    return round(sectores_precios[indice_sector] * (1 + sectores_recargos[indice_sector]), 2)


# recibimos TODOS los datos de la entrada para mostrarlos al final de cada venta de entrada, si elegimos comprar dos entradas, cuando terminamos de ingresar los datos de la primera se ejecuta esta funcion para mostrar los datos de esa entrada, y lo mismo con la segunda
def mostrarResumen(codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, telefono, precio_final,espectaculos_nombres, espectaculos_fechas, espectaculos_horas,sectores_nombres):
    print("\n========== ENTRADA CONFIRMADA ==========")
    print("Código: %s" % codigo)
    print("Espectáculo: %s" % espectaculos_nombres[indice_espectaculo])
    print("Fecha: %s  %s" % (espectaculos_fechas[indice_espectaculo], espectaculos_horas[indice_espectaculo]))
    print("Sector: %s" % sectores_nombres[indice_sector])
    if indice_sector == 0:
        print("Asiento: Campo Abierto")
    else:
        print("Asiento: Fila %d - Asiento %d" % (fila + 1, columna + 1))
    print("Comprador: %s" % nombre)
    print("DNI: %s" % dni)
    print("Teléfono: %s" % telefono)
    print("Precio: $%.2f" % precio_final)
    print("=========================================")


# recibimos todos los detalles de los datos de la venta y los agregamos al array de ventas.
def registrarVenta(ventas, disponibilidad, codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, precio_final):
    venta = (codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, precio_final)
    ventas.append(venta)
    if indice_sector == 0:
        disponibilidad[indice_espectaculo][0] += 1
    else:
        disponibilidad[indice_espectaculo][indice_sector][fila][columna] = 1

# funcion disponible para admin y para boletero, primero verificamos que existan espectaculos, ahora que agregamos archivos deberian existir permanentemente, salvo que sean cancelados
def venderEntradas(ventas, disponibilidad, contador_ventas,espectaculos_nombres, espectaculos_fechas, espectaculos_horas,espectaculos_estados, espectaculos_generos, sectores_nombres, sectores_precios, sectores_recargos, sectores_filas, sectores_columnas):
    if not espectaculos_nombres:
        print("No hay espectáculos disponibles.")
        return contador_ventas

    print("\n====== VENTA DE ENTRADAS ======")

    # preguntamos que espectaculo desean y que sector con las funciones desarrolladas anteriormente
    indice_espectaculo = elegirEspectaculo(espectaculos_nombres, espectaculos_fechas, espectaculos_horas, espectaculos_estados, espectaculos_generos)
    indice_sector = elegirSector(sectores_nombres, sectores_precios, sectores_recargos)

    # mostramos el mapa segun el sector y espectaculo que eligio el usuario
    mostrarMapa(disponibilidad, indice_espectaculo, indice_sector, espectaculos_nombres, sectores_nombres, sectores_filas, sectores_columnas)

    # pedimos cantidad de entradas, verificamos que sea mayor a 1 y menor a 5. ademas usamos la funicon helper que pide un numero entero para manejarmejor las excepciones
    cantidad = 0
    while cantidad < 1 or cantidad > 4:
        cantidad = leer_entero("¿Cuántas entradas desea comprar? ")
        if cantidad < 1:
            print("La cantidad debe ser al menos 1.")
        elif cantidad > 4:
            print("La cantidad debe ser menor de 5.")

    # mientras se recorre lacantidad de entradas que eligio, vamos pidiendo los datos de cada una
    for i in range(cantidad):
        # entrada 1 de 2 por ejemplo
        print("\n--- Entrada %d de %d ---" % (i + 1, cantidad))

        # desempaquetamos el asiento con fila y columna
        fila, columna = elegirAsiento(disponibilidad, indice_espectaculo, indice_sector, sectores_filas, sectores_columnas)
        if fila is None:
            print("No se pudo seleccionar asiento. Venta cancelada.")
            break

        # bloque para saber si es no el acompañante y mostrar: --datos del comprador-- o --datos del acompañante--
        if i == 0:
            # es_comprador = True. desempaquetamos la tupla con los tres valores de la entrada
            nombre, dni, telefono = pedirDatos(True)
        else:
            # es_comprador = False
            nombre, dni, telefono = pedirDatos(False)

        precio_final = calcularPrecio(indice_sector, sectores_precios,sectores_recargos)
        codigo, contador_ventas = generarCodigo(contador_ventas)

        mostrarResumen(codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, telefono, precio_final, espectaculos_nombres, espectaculos_fechas, espectaculos_horas, sectores_nombres)

        # Validar confirmación hasta que ingrese s, si, n o no
        while True:
            confirmacion = input("\n¿Confirmar compra? (s/n): ").strip().lower()
            if confirmacion in ("s", "si"):
                registrarVenta(ventas, disponibilidad, codigo, indice_espectaculo, indice_sector, fila, columna, nombre, dni, precio_final)
                print("Compra registrada correctamente.")
                break
            elif confirmacion in ("n", "no"):
                print("Compra cancelada.")
                break
            else:
                print("Opción no válida. Responda 's', 'si', 'n' o 'no'.")

    return contador_ventas


# FUNCION PARA LISTAR CANCELAR Y MODIFICAR VENTAS

# listar se usa unicamente para cancelar y modificar entradas, no tiene una funcionalidad especifica
def listarVentasUsuario(ventas, espectaculos_nombres, sectores_nombres):
    print("\n--- Ventas registradas ---")
    if not ventas:
        print("No hay ventas registradas.")
        return
    for id in range(len(ventas)):
        v = ventas[id]
        codigo, iespectaculo, isector, fila, col, nombre, dni, precio = v
        if isector == 0:
            sector_txt = "Campo Abierto"
        else:
            sector_txt = "Fila %d - Asiento %d" % (fila + 1, col + 1)
        print("[%d] %s | %s | %s | %s | %s | $%.2f" % (id + 1, codigo, espectaculos_nombres[iespectaculo], sectores_nombres[isector], sector_txt, nombre, precio))

# cancela una compra y libera el lugar
def cancelarCompra(ventas, disponibilidad, espectaculos_nombres, sectores_nombres):
    listarVentasUsuario(ventas, espectaculos_nombres, sectores_nombres)
    if not ventas:
        return

    while True:
        idventa = leer_entero("Índice de la venta a cancelar: ")
        idventa = idventa - 1
        if 0 <= idventa < len(ventas):
            break
        print("Error: índice fuera de rango.")

    while True:
        confirmacion = input("¿Confirmar cancelación? (s/n): ").strip().lower()
        if confirmacion in ("s", "si"):
            break
        elif confirmacion in ("n", "no"):
            print("Cancelación abortada.")
            return
        else:
            print("Opción no válida. Responda 's', 'si', 'n' o 'no'.")

    codigo, iespectaculo, isector, fila, col, nombre, dni, precio = ventas[idventa]
    if isector == 0:
        disponibilidad[iespectaculo][0] = max(0, disponibilidad[iespectaculo][0] - 1)
    else:
        # lo ponemos en 0 y no O porque al mostrar el mapa, se muestra O si el valor de la fila y asiento es 0
        disponibilidad[iespectaculo][isector][fila][col] = 0
    ventas.pop(idventa)
    print("Venta %s cancelada y asiento liberado." % codigo)

    # funcion para modificar los datos del comprador o acompañante en una venta existente.
def modificarCompra(ventas, disponibilidad, espectaculos_nombres, sectores_nombres, sectores_filas, sectores_columnas):
    listarVentasUsuario(ventas, espectaculos_nombres, sectores_nombres)
    if not ventas:
        return
    while True:
        id = leer_entero("Índice de la venta a modificar: ")
        id = id - 1
        if 0 <= id < len(ventas):
            break
        print("Error: índice fuera de rango.")

    codigo, iespectaculo, isector, fila, col, nombre_viejo, dni_viejo, precio = ventas[id]
    print("Comprador actual: %s | DNI: %s" % (nombre_viejo, dni_viejo))
    nuevo_nombre = input("Nuevo nombre (Enter para mantener): ").strip()
    nuevo_dni = input("Nuevo DNI (Enter para mantener): ").strip()
    if not nuevo_nombre:
        nuevo_nombre = nombre_viejo
    if not nuevo_dni:
        nuevo_dni = dni_viejo

    ventas[id] = (codigo, iespectaculo, isector, fila, col, nuevo_nombre, nuevo_dni, precio)
    print("Datos del comprador actualizados.")

# agrega un usuario nuevo con su clave encriptada
def crearUsuario(usuarios):
    print("\n--- Crear usuario ---")
    while True:
        nombre = input("Nombre de usuario: ").strip()
        if nombre:
            break
        print("Error: el nombre no puede estar vacío.")
    if nombre in usuarios:
        print("Error: ese usuario ya existe.")
        return
    clave = input("Contraseña: ").strip()
    print("1. Administrador")
    print("2. Boletero")
    opcion = leer_entero("Rol: ")
    if opcion == 1:
        rol = "administrador"
    elif opcion == 2:
        rol = "boletero"
    else:
        print("Opción inválida.")
        return
    usuarios[nombre] = [encriptarClave(clave), rol]
    guardarUsuarios(usuarios)
    print("Usuario '%s' creado correctamente." % nombre)

# modifica la clave o el rol de un usuario existente
def modificarUsuario(usuarios):
    print("\n--- Modificar usuario ---")
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for nombre in usuarios:
        print("- %s (%s)" % (nombre, usuarios[nombre][1]))
    nombre = input("Usuario a modificar: ").strip()
    if nombre not in usuarios:
        print("Error: usuario no encontrado.")
        return
    print("1. Cambiar contraseña")
    print("2. Cambiar rol")
    opcion = leer_entero("Opción: ")
    if opcion == 1:
        nueva_clave = input("Nueva contraseña: ").strip()
        usuarios[nombre][0] = encriptarClave(nueva_clave)
        print("Contraseña actualizada.")
    elif opcion == 2:
        print("1. Administrador")
        print("2. Boletero")
        opcion_rol = leer_entero("Nuevo rol: ")
        if opcion_rol == 1:
            usuarios[nombre][1] = "administrador"
        elif opcion_rol == 2:
            usuarios[nombre][1] = "boletero"
        else:
            print("Opción inválida.")
            return
        print("Rol actualizado.")
    else:
        print("Opción inválida.")
        return
    guardarUsuarios(usuarios)

    # recorre las ventas una vez y devuelve todos los datos calculados
def calcularEstadisticasVentas(ventas, espec_nombres, sectores_nombres):
    recaudacion_total = 0.0
    ventas_por_espec  = {}
    ventas_por_sector = {}

    for nombre in espec_nombres:
        ventas_por_espec[nombre] = {"entradas": 0, "recaudacion": 0.0}
    for nombre in sectores_nombres:
        ventas_por_sector[nombre] = 0

    for v in ventas:
        codigo, iespectaculo, isector, fila, col, nombre, dni, precio = v
        nombre_espec   = espec_nombres[iespectaculo]
        nombre_sector  = sectores_nombres[isector]
        recaudacion_total                          += precio
        ventas_por_espec[nombre_espec]["entradas"] += 1
        ventas_por_espec[nombre_espec]["recaudacion"] += precio
        ventas_por_sector[nombre_sector]           += 1

    return recaudacion_total, ventas_por_espec, ventas_por_sector


# muestra y exporta el reporte de recaudacion por espectaculo
def reporteRecaudacion(ventas, espec_nombres, sectores_nombres):
    if not ventas:
        print("No hay ventas registradas.")
        return

    recaudacion_total, ventas_por_espec, ventas_por_sector = calcularEstadisticasVentas(ventas, espec_nombres, sectores_nombres)

    print("\n===== REPORTE DE RECAUDACION =====")
    print("Recaudacion total: $%.2f" % recaudacion_total)
    print("\nPor espectaculo:")
    for nombre in ventas_por_espec:
        print("  %-25s %d entradas  $%.2f" % (nombre, ventas_por_espec[nombre]["entradas"], ventas_por_espec[nombre]["recaudacion"]))
    print("\nPor sector:")
    for nombre in ventas_por_sector:
        print("  %-15s %d entradas" % (nombre, ventas_por_sector[nombre]))

    try:
        archivo = open("reporte_recaudacion.csv", "wt", encoding="UTF-8")
        archivo.write("Espectaculo,Entradas,Recaudacion\n")
        for nombre in ventas_por_espec:
            archivo.write("%s,%d,%.2f\n" % (nombre, ventas_por_espec[nombre]["entradas"], ventas_por_espec[nombre]["recaudacion"]))
        archivo.write("\nSector,Entradas\n")
        for nombre in ventas_por_sector:
            archivo.write("%s,%d\n" % (nombre, ventas_por_sector[nombre]))
        archivo.close()
        print("\nReporte exportado a reporte_recaudacion.csv")
        input("\nPresione Enter para continuar...")
    except OSError as error:
        print("Error al exportar reporte: ", error)


# muestra y exporta el reporte de ocupacion por espectaculo y sector
def reporteOcupacion(ventas, disponibilidad, espec_nombres, espec_estados, sectores_nombres, sectores_filas, sectores_columnas):
    if not espec_nombres:
        print("No hay espectaculos registrados.")
        return

    recaudacion_total, ventas_por_espec, ventas_por_sector = calcularEstadisticasVentas(ventas, espec_nombres, sectores_nombres)

    print("\n===== REPORTE DE OCUPACION =====")
    print("%-25s" % "", end="")
    for nombre in sectores_nombres:
        print("%-15s" % nombre, end="")
    print()

    try:
        archivo = open("reporte_ocupacion.csv", "wt", encoding="UTF-8")
        archivo.write("Espectaculo")
        for nombre in sectores_nombres:
            archivo.write(",%s" % nombre)
        archivo.write("\n")

        for i in range(len(espec_nombres)):
            print("%-25s" % espec_nombres[i], end="")
            archivo.write(espec_nombres[i])
            for s in range(len(sectores_nombres)):
                if s == 0:
                    ocupados  = disponibilidad[i][0]
                    capacidad = CAMPO_CAPACIDAD
                else:
                    filas     = sectores_filas[s]
                    columnas  = sectores_columnas[s]
                    capacidad = filas * columnas
                    ocupados  = 0
                    for f in range(filas):
                        for c in range(columnas):
                            if disponibilidad[i][s][f][c] == 1:
                                ocupados += 1
                if capacidad > 0:
                    porcentaje = (ocupados * 100) / capacidad
                else:
                    porcentaje = 0.0
                print("%-15s" % ("%.1f%%" % porcentaje), end="")
                archivo.write(",%.1f%%" % porcentaje)
            print()
            archivo.write("\n")

        archivo.close()
        print("\nReporte exportado a reporte_ocupacion.csv")
        input("\nPresione Enter para continuar...")
    except OSError as error:
        print("Error al exportar reporte: ", error)

# permite al admin modificar el precio o recargo de un sector existente
def modificarSectores(sectores_nombres, sectores_precios, sectores_recargos):
    print("\n--- Modificar sectores ---")
    for i in range(len(sectores_nombres)):
        print("%d. %-15s $%.2f  recargo %.0f%%" % (i + 1, sectores_nombres[i], sectores_precios[i], sectores_recargos[i] * 100))
    while True:
        i = leer_entero("Índice del sector a modificar: ") - 1
        if 0 <= i < len(sectores_nombres):
            break
        print("Error: índice fuera de rango.")
    print("1. Modificar precio")
    print("2. Modificar recargo")
    opcion = leer_entero("Opción: ")
    if opcion == 1:
        while True:
            nuevo_precio = leer_entero("Nuevo precio: ")
            if nuevo_precio > 0:
                break
            print("Error: el precio debe ser mayor a 0.")
        sectores_precios[i] = float(nuevo_precio)
        print("Precio actualizado.")
    elif opcion == 2:
        while True:
            nuevo_recargo = leer_entero("Nuevo recargo (en porcentaje, ej: 20 para 20%%): ")
            if 0 <= nuevo_recargo <= 100:
                break
            print("Error: el recargo debe estar entre 0 y 100.")
        sectores_recargos[i] = nuevo_recargo / 100.0
        print("Recargo actualizado.")
    else:
        print("Opción inválida.")

# MENUU
def main():
    # Carga espectáculos desde JSON al iniciar y los guarda después de cada operación que los modifique (crear, modificar, cancelar).
    (espec_nombres, espec_fechas, espec_horas, espec_descripciones, espec_estados, espec_generos, disponibilidad) = cargarEspectaculos() 
    usuarios = cargarUsuarios() 
    ventas, contador_ventas = cargarVentas()
    sectores_nombres, sectores_precios, sectores_recargos, sectores_filas, sectores_columnas = cargarSectores()
    cad = "SISTEMA DE GESTIÓN DE ESPECTÁCULOS"
    cad2 = cad.center(60,'=')
    print(cad2)

    # login con 3 intentos, si no acierta el nombre y contrasñea sale del sistema
    while True:
        rol = None
        for intento in range(3):
            rol = login(usuarios)
            if rol:
                break
            intentos_restantes = 2 - intento
            if intentos_restantes > 0:
                print("Intento fallido. %d intento(s) restante(s)." % intentos_restantes)
        else:
            print("Demasiados intentos fallidos. Saliendo.")
            break

        # se muestra el menu según el rol y segun la opcion elegida se ejecuta la funcion correspondiente y se le pasan los parametros necesarios 
        if rol == "administrador":
            while True:
                print("\n====== MENÚ ADMINISTRADOR ======")
                print("1. Comprar entradas")
                print("2. Cancelar una compra")
                print("3. Modificar datos de una compra")
                print("4. Ver espectáculos activos")
                print("5. Listar todos los espectáculos")
                print("6. Crear nuevo espectáculo")
                print("7. Modificar espectáculo")
                print("8. Cancelar espectáculo")
                print("9.  Reporte de recaudacion")
                print("10. Reporte de ocupacion")
                print("11. Crear usuario")
                print("12. Modificar usuario")
                print("13. Modificar sectores")
                print("14. Cerrar sesión")
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    contador_ventas = venderEntradas(ventas, disponibilidad, contador_ventas,espec_nombres, espec_fechas, espec_horas, espec_estados, espec_generos, sectores_nombres, sectores_precios,sectores_recargos, sectores_filas, sectores_columnas)
                    guardarVentas(ventas, contador_ventas)
                elif opcion == "2":
                    cancelarCompra(ventas, disponibilidad, espec_nombres, sectores_nombres)
                    guardarVentas(ventas, contador_ventas)
                elif opcion == "3":
                    modificarCompra(ventas, disponibilidad, espec_nombres, sectores_nombres, sectores_filas, sectores_columnas)
                    guardarVentas(ventas, contador_ventas)
                elif opcion == "4":
                    mostrarEspectaculos(espec_nombres, espec_fechas, espec_horas, espec_estados, espec_generos)
                elif opcion == "5":
                    listarEspectaculos(espec_nombres, espec_fechas, espec_horas, espec_estados, espec_descripciones, espec_generos)
                elif opcion == "6":
                    crearEspectaculo(espec_nombres, espec_fechas, espec_horas, espec_descripciones, espec_estados, espec_generos, disponibilidad, sectores_nombres, sectores_filas, sectores_columnas)
                    guardarEspectaculos(espec_nombres, espec_fechas, espec_horas, espec_descripciones, espec_estados, espec_generos, disponibilidad)
                elif opcion == "7":
                    modificarEspectaculo(espec_nombres, espec_fechas, espec_horas, espec_descripciones, espec_estados, espec_generos)
                    guardarEspectaculos(espec_nombres, espec_fechas, espec_horas, espec_descripciones, espec_estados, espec_generos, disponibilidad)
                elif opcion == "8":
                    cancelarEspectaculo(espec_nombres, espec_estados)
                    guardarEspectaculos(espec_nombres, espec_fechas, espec_horas, espec_descripciones, espec_estados, espec_generos, disponibilidad)
                elif opcion == "9":
                    reporteRecaudacion(ventas, espec_nombres, sectores_nombres)
                elif opcion == "10":
                    reporteOcupacion(ventas, disponibilidad, espec_nombres, espec_estados, sectores_nombres, sectores_filas, sectores_columnas)
                elif opcion == "11":
                    crearUsuario(usuarios)
                elif opcion == "12":
                    modificarUsuario(usuarios)
                elif opcion == "13":
                    modificarSectores(sectores_nombres, sectores_precios, sectores_recargos)
                    guardarSectores(sectores_nombres, sectores_precios, sectores_recargos, sectores_filas, sectores_columnas)
                elif opcion == "14":
                    print("Sesión cerrada.")
                    break
                else:
                    print("Opción inválida, intente de nuevo.")

        elif rol == "boletero":
            while True:
                print("\n====== MENÚ BOLETERO ======")
                print("1. Comprar entradas")
                print("2. Cancelar una compra")
                print("3. Modificar datos de una compra")
                print("4. Ver espectáculos activos")
                print("5. Cerrar sesión")
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    contador_ventas = venderEntradas(ventas, disponibilidad, contador_ventas, espec_nombres, espec_fechas, espec_horas, espec_estados, espec_generos, sectores_nombres, sectores_precios, sectores_recargos, sectores_filas, sectores_columnas)
                    guardarVentas(ventas, contador_ventas)
                elif opcion == "2":
                    cancelarCompra(ventas, disponibilidad, espec_nombres, sectores_nombres)
                    guardarVentas(ventas, contador_ventas)
                elif opcion == "3":
                    modificarCompra(ventas, disponibilidad, espec_nombres, sectores_nombres, sectores_filas, sectores_columnas)
                    guardarVentas(ventas, contador_ventas)
                elif opcion == "4":
                    mostrarEspectaculos(espec_nombres, espec_fechas, espec_horas, espec_estados, espec_generos)
                elif opcion == "5":
                    print("Sesión cerrada.")
                    break
                else:
                    print("Opción inválida, intente de nuevo.")

        while True:
            continuar = input("\n¿Iniciar otra sesión? (s/n): ").strip().lower()
            if continuar in ("s", "si"):
                break
            elif continuar in ("n", "no"):
                print("Gracias por usar el sistema. Chau!")
                break
            else:
                print("Opción no válida. Responda 's', 'si', 'n' o 'no'.")



main()