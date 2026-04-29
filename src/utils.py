from io import TextIOWrapper
import os
from pathlib import Path
from src.materia import Materia
from collections.abc import Callable

def obtener_parametro(nombre: str, argumentos: dict, config: dict = None, input_manual: Callable[[], str] = None, validador: Callable[[str], bool] = None, reintentar_manual: bool = True,
                      error_msg: str = "El valor de {nombre} es invalido.", cerrar_con_error: bool = True):
    # primero revisar en los argumentos
    if nombre in argumentos:
        valor = argumentos[nombre]
    # despues revisar en el config
    elif config is not None and nombre in config:
        valor = config[nombre]
    # por ultimo solicitarlo manualmente
    elif input_manual is not None:
        valor = input_manual()
        if reintentar_manual and validador is not None:
            while not validador(valor):
                print(error_msg.replace("{nombre}", nombre).replace("{valor}", str(valor)))
                valor = input_manual()
    else:
        if cerrar_con_error:
            cerrar_programa_con_error(f"No se encontro el parametro {nombre} y no se proporciono un metodo "
                                      f"para solicitarlo manualmente.")
        else:
            print(f"No se encontro el parametro {nombre} y no se proporciono un metodo "
                  f"para solicitarlo manualmente.")
            return None
    if validador is None or validador(valor):
        return valor
    elif cerrar_con_error:
        cerrar_programa_con_error(error_msg.replace("{nombre}", nombre).replace("{valor}", str(valor)))
    else:
        print(error_msg.replace("{nombre}", nombre).replace("{valor}", str(valor)))
        return None


def solicitar_nombre_y_ruta(msg_archivo: str, msg_ruta: str)-> tuple[str, str]:
    # "Ingrese el nombre del archivo (con extension) donde se guardaran los datos: "
    archivo = input(msg_archivo)
    while archivo == "":
        print("No se puede guardar un archivo con nombre vacio.")
        archivo = input(msg_archivo)
    #
    ruta = input(msg_ruta)
    return archivo, ruta


# solicita el nombre y la ruta de un archivo y lo crea
def obtener_archivo_manual(argumentos: dict, config: dict) -> TextIOWrapper | None:
    nombre, ruta = solicitar_nombre_y_ruta(
        "Ingrese el nombre del archivo (con extension) donde se guardaran los datos: ",
        "Ingrese la ruta donde se guardara el archivo o presione enter para usar la ruta por defecto: ")
    if ruta == "":
        ruta = obtener_parametro("ruta_resultados_default", argumentos, config, None)
    file = crear_archivo(nombre, ruta)
    return file


# crea un archivo, valida que no exista y devuelve el objeto file
def crear_archivo(nombre: str, ruta: str, overwrite: bool = False) -> TextIOWrapper | None:
    # revisar que la ruta sea valida y exista, si no es valida pasa a la por defecto y si no existe la crea
    if len(ruta) > 0:  # no es ruta por defecto
        ruta = ruta.replace('\\', '/')  # ya se que Windows usa \ pero las dos barras funcionan
        os.makedirs(ruta, exist_ok=True)
    if ruta[-1:] != '/':  # si la ruta no termina en / la agrego para poder concatenar
        ruta = ruta + '/'
    # revisar que el archivo no exista
    if os.path.exists(ruta + nombre) and not overwrite:
        op = input("El archivo ya existe, si crea un nuevo archivo se perderan los datos anteriores. "
                   "Ingrese 'S' para continuar o cualquier otro caracter para cancelar: ")
        if op != 'S':
            print("Operacion cancelada.")
            return None
    try:
        return open(ruta + nombre, 'wt')
    except PermissionError:
        print("Error: el programa no tiene permisos para crear el archivo en la ruta " + ruta)
        return None  # podria volver a llamar la funcion para que empieze de nuevo pero no me quiero meter en
        # recursividad, mejor que vuelva al menu y el usuario decida si quiere volver a intentar


def mostrar_ruta_archivo(file: TextIOWrapper):
    print("\nArchivo creado en " + os.path.abspath(file.name))


def solicitar_archivo_existente(msg: str = "Ingrese la ruta del archivo:\n") -> str:
    path = input(msg)
    file = Path(path)
    while not file.is_file():
        path = input(msg)
        file = Path(path)
    return path


def es_archivo_existente(path: str) -> bool:
    return Path(path).is_file()


def solicitar_fecha(msg: str = "Ingrese la fecha en formato dd/mm:\n") -> str:
    date = input(msg)
    while not validar_fecha(date):
        date = input("Formato invalido. " + msg + "\n")
    return date


# se asegura que los codigos esten todos con el mismo formato (letra en mayuscula, numeros sin 0 a la izquierda)
def format_code(cod: str) -> str | None:
    try:
        codigo = cod.strip()
        letra = codigo[0].upper()
        num = codigo[1:].lstrip('0')
        if not (letra.isupper() and num.isnumeric()):  # letra no es letra o num no es numero
            return None
        return letra + num
    except ValueError or IndexError:
        return None


def listar_materias(materias: list[Materia]):
    print("Listado de Materias:")
    for i in range(len(materias)):  # las lista con su indice + 1 para que el usuario pueda ingresar el numero
        print(f"{i + 1}: " + materias[i].nombre_corto)  # el nombre de la materia en el indice i


# transorma una fecha en formato string dd/mm en el numero de dia correspondiente partiendo de una fecha inicial
def date_to_int(date: str, start_date: str, end_date: str) -> int:
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
def int_to_date(i: int, start_date: str, end_date: str, united: bool = False) -> str | tuple[str, str]:
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
def day_to_week(i: int) -> int:
    return i // 7


# valida que la fecha este en formato dd/mm y que el dia y el mes sean validos
def validar_fecha(fecha: str) -> bool:
    try:
        d, m = fecha.split('/')
        d = int(d)
        m = int(m)
        if not (1 <= m <= 12 and 1 <= d <= 31):
            return False
        return True
    except ValueError:
        return False


# verifica si la fecha 1 es anterior a la fecha 2
def fecha_es_anterior(fecha1: str, fecha2: str) -> bool:
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


def cerrar_programa_con_error(msg: str):
    print(msg)
    input()
    exit(1)