import os


# se asegura que los codigos esten todos con el mismo formato (letra en mayuscula, numeros sin 0 a la izquierda)
def format_code(cod):
    try:
        letra = cod[0].upper()
        num = cod[1:].lstrip('0').rstrip('\n')
        if not (letra.isupper() and num.isnumeric()):  # letra no es letra o num no es numero
            return None
        return letra + num
    except ValueError or IndexError:
        return None


# transforma un entero positivo en el dia correspondiente contando desde la fecha inicial y sin pasar la final
def int_to_date(i, start, end, united=False):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    s = start.split('/')
    start_day, start_month = int(s[0]), int(s[1])
    e = end.split('/')
    end_day, end_month = int(e[0]), int(e[1])
    day = ""
    month = ""
    #  cuando i sea menor a la cantidad de dias del mes encontre la fecha, sino le resto la cantidad de dias y sigo
    for m in range(start_month, end_month + 1):  # m puede ir de 1 a 12, cuando se acceda a la lista hay que restar 1
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
            if i <= days[m-1]:
                month = str(m)
                day = str(i)
                break
            else:
                i -= days[m-1]
    if united:
        return day + '/' + month  # devuelve un solo string, usado para mostrar fecha en las salidas
    else:
        return day, month  # devuelve los valores separados en tupla por si los necesito ver individualmente


# transorma una fecha en formato string dd/mm en el numero de dia correspondiente partiendo de una fecha inicial
def date_to_int(date, start, end):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    s = start.split('/')
    start_day, start_month = int(s[0]), int(s[1])
    e = end.split('/')
    end_day, end_month = int(e[0]), int(e[1])
    d = date.split('/')
    day, month = int(d[0]), int(d[1])
    if day <= 0 or 12 < month <= 0:
        return -1
    i = 0
    # cuando encuentre el mes, si el dia no se me pasa de largo ya encontre el indice, sino sigo aumentando i
    for m in range(start_month, end_month + 1):
        if m == month:  # este es el mes de la fecha
            if day > days[m - 1]:  # el 30 de febrero no existe...
                return -1
            if m == start_month:
                if day < start_day:
                    return -1
                i = day - start_day  # no paso ningun mes, no hay que sumar ningun dia, devuelvo el indice directamente
                break
            elif m == end_month:
                if day > end_day:
                    return -1
                i += day
                break
            else:
                i += day  # voy a devolver todos los dias que ya pasaron mas el de la fecha
                break
        else:
            if m == start_month:
                i += days[m - 1] - start_day  # sumo los dias del primer mes que cuentan
            elif m == end_month:  # ya me quede sin meses, no puedo seguir
                return -1
            else:
                i += days[m - 1]  # sumo los dias de este mes (m va adelantado en 1)
    return i


# recibe el indice de un dia y devuelve en que semana estuvo, partiendo de la semana 0
def day_to_week(i):
    return i // 7


# transforma un codigo en formato string en un numero entre 0 y cantidad de codigos - 1
def code_to_int(code, CODIGOS):
    code = format_code(code)
    if code is None:
        return -1
    try:
        return CODIGOS.index(code)
    except ValueError:
        return -1
    # return -1  # la letra estaba mal


# transforma un entero entre 0 y cantidad de codigos - 1 en el codigo correspondiente en formato string
def int_to_code(c, CODIGOS):
    try:
        return CODIGOS[c]
    except IndexError:
        return "Codigo invalido"


def listar_materias(MATERIAS, NOMBRES_MATERIAS):
    print("Listado de Materias:")
    for i in range(len(MATERIAS)):  # las lista con su indice + 1 para que el usuario pueda ingresar el numero
        print(f"{i + 1}: " + NOMBRES_MATERIAS[MATERIAS[i]])  # el nombre de la materia en el indice i


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
        # crear directorios, os.mkdir() sirve para crear un directorio por vez, por eso voy uno a uno
        directorios = path.split('/')  # cada directorio en la ruta
        # si era una ruta absoluta en Windows, sera la particion (C:, D:, o lo que sea)
        dire = ""
        for d in directorios:
            dire += d + '/'
            if not os.path.exists(dire):
                try:
                    os.mkdir(dire)
                except PermissionError:
                    print("Error: no hay permisos para crear esa ruta.")
                    return None
                except OSError:  # esta tambien incluye permisos, pero quiero separar los tipos de errores
                    print("Error: la ruta ingresada no es valida.")
                    return None
        if path[-1:] != '/':  # si la ruta no termina en / la agrego para poder concatenar
            path = path + '/'
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
