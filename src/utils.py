import os
from pathlib import Path


def obtener_parametro(nombre, argumentos, config, input_manual, validador=None, reintentar_manual=True,
                      error_msg="El valor de {nombre} es invalido.", cerrar_con_error=True):
    # primero revisar en los argumentos
    if nombre in argumentos:
        valor = argumentos[nombre]
    # despues revisar en el config
    elif config is not None and nombre in config:
        valor = config[nombre]
    # por ultimo solicitarlo manualmente
    else:
        valor = input_manual()
        if reintentar_manual and validador is not None:
            while not validador(valor):
                print(error_msg.replace("{nombre}", nombre).replace("{valor}", str(valor)))
                valor = input_manual()
    if validador is None or validador(valor):
        return valor
    elif cerrar_con_error:
        cerrar_programa_con_error(error_msg.replace("{nombre}", nombre).replace("{valor}", str(valor)))
    else:
        print(error_msg.replace("{nombre}", nombre).replace("{valor}", str(valor)))
        return None


# llamada en todas las opciones para crear el archivo donde se guardan los datos
def create_file():
    name = input("Ingrese el nombre del archivo (con extension) donde se guardaran los datos: ")
    while name == "":
        print("No se puede guardar un archivo con nombre vacio.")
        name = input("Ingrese el nombre del archivo (con extension) donde se guardaran los datos: ")
    path = input("Ingrese la ruta donde se guardara el archivo, o presione enter para guardar en la ruta por defecto: ")

    # revisar que la ruta sea valida y exista, si no es valida pasa a la por defecto y si no existe la crea
    if len(path) > 0:  # no es ruta por defecto
        path = path.replace('\\', '/')  # ya se que Windows usa \ pero las dos barras funcionan

        os.makedirs(path, exist_ok=True)

        if path[-1:] != '/':  # si la ruta no termina en / la agrego para poder concatenar
            path = path + '/'
    else:
        path = "resultados/"
        os.makedirs(path, exist_ok=True)
    # revisar que el archivo no exista
    if os.path.exists(path + name):
        op = input("El archivo ya existe, si crea un nuevo archivo se perderan los datos anteriores. "
                   "Ingrese 1 para confirmar o cualquier otro caracter para cancelar: ")
        if op != '1':
            print("Operacion cancelada.")
            return None
    try:
        return open(path + name, 'wt')
    except PermissionError:
        print("Error: el programa no tiene permisos para crear el archivo en la ruta " + path)
        return None  # podria volver a llamar la funcion para que empieze de nuevo pero no me quiero meter en
        # recursividad, mejor que vuelva al menu y el usuario decida si quiere volver a intentar


def mostrar_ruta_archivo(file):
    print("\nArchivo creado en " + os.path.abspath(file.name))


def solicitar_archivo_existente(msg="Ingrese la ruta del archivo:\n"):
    path = input(msg)
    file = Path(path)
    while not file.is_file():
        path = input(msg)
        file = Path(path)
    return path


def es_archivo_existente(path):
    return Path(path).is_file()


def solicitar_fecha(msg="Ingrese la fecha en formato dd/mm:\n"):
    date = input(msg)
    while not validar_fecha(date):
        date = input("Formato invalido. " + msg + "\n")
    return date


# se asegura que los codigos esten todos con el mismo formato (letra en mayuscula, numeros sin 0 a la izquierda)
def format_code(cod):
    try:
        codigo = cod.strip()
        letra = codigo[0].upper()
        num = codigo[1:].lstrip('0')
        if not (letra.isupper() and num.isnumeric()):  # letra no es letra o num no es numero
            return None
        return letra + num
    except ValueError or IndexError:
        return None


def listar_materias(materias):
    print("Listado de Materias:")
    for i in range(len(materias)):  # las lista con su indice + 1 para que el usuario pueda ingresar el numero
        print(f"{i + 1}: " + materias[i].nombre_corto)  # el nombre de la materia en el indice i


# transorma una fecha en formato string dd/mm en el numero de dia correspondiente partiendo de una fecha inicial
def date_to_int(date, start_date, end_date):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    start = start_date.split('/')
    start_day, start_month = int(start[0]), int(start[1])
    end = end_date.split('/')
    end_day, end_month = int(end[0]), int(end[1])
    d = date.split('/')
    day, month = int(d[0]), int(d[1])
    if day <= 0 or 12 < month <= 0:
        return -1
    i = 0
    # cuando encuentre el mes, si el dia no se me pasa de largo ya encontre el indice, sino sigo aumentando i
    for m in range(start_month, end_month + 1):
        if m == month:  # este es el mes de la fecha
            if day > days[m - 1]:  # fecha con mas dias de los que tiene el mes
                return -1
            if m == start_month:
                if day < start_day:
                    return -1
                i = day - start_day  # no paso ningun mes, no hay que sumar ningun dia, devuelvo el indice directamente
                break
            elif m == end_month:
                if day > end_day:
                    return -1
            i += day # voy a devolver todos los dias que ya pasaron mas el de la fecha
            break
        else:
            if m == start_month:
                i += days[m - 1] - start_day  # sumo los dias del primer mes que cuentan
            elif m == end_month:  # ya me quede sin meses, no puedo seguir
                return -1
            else:
                i += days[m - 1]  # sumo los dias de este mes (m va adelantado en 1)
    return i


# transforma un entero positivo en el dia correspondiente contando desde la fecha inicial y sin pasar la final
def int_to_date(i, start_date, end_date, united=False):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    start = start_date.split('/')
    start_day, start_month = int(start[0]), int(start[1])
    end = end_date.split('/')
    end_day, end_month = int(end[0]), int(end[1])
    day = ""
    month = ""
    #  cuando i sea menor a la cantidad de dias del mes encontre la fecha, sino le resto la cantidad de dias y sigo
    for m in range(start_month,
                   end_month + 1):  # m puede ir de 1 a 12, cuando se acceda a la lista hay que restar 1
        if m == start_month:
            if i <= days[start_month - 1] - start_day:
                month = str(m)
                day = str(start_day + i)
                break
            else:
                i -= days[start_month - 1] - start_day
        elif m == end_month:
            if i <= end_day:
                month = str(m)
                day = str(i)
                break
            else:
                day, month = '0', '0'  # fuera de rango
                break
        else:
            if i <= days[m - 1]:
                month = str(m)
                day = str(i)
                break
            else:
                i -= days[m - 1]
    if united:
        return day + '/' + month  # devuelve un solo string, usado para mostrar fecha en las salidas
    else:
        return day, month  # devuelve los valores separados en tupla por si los necesito ver individualmente


# recibe el indice de un dia y devuelve en que semana estuvo, partiendo de la semana 0 (asumiendo que el dia 0 es lunes)
def day_to_week(i):
    return i // 7


def validar_fecha(fecha):
    try:
        d, m = fecha.split('/')
        d = int(d)
        m = int(m)
        if not (1 <= m <= 12 and 1 <= d <= 31):
            return False
        return True
    except ValueError:
        return False


# no tiene en cuenta si la fecha existe
def fecha_es_anterior(fecha1, fecha2):
    try:
        d1, m1 = fecha1.split('/')
        d2, m2 = fecha2.split('/')
        d1 = int(d1)
        m1 = int(m1)
        d2 = int(d2)
        m2 = int(m2)
        if m1 < m2:
            return True
        elif m1 == m2 and d1 < d2:
            return True
        else:
            return False
    except ValueError:
        return False


def cerrar_programa_con_error(msg):
    print(msg)
    input()
    exit(1)