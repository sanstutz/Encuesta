import sys
import json
from json import JSONDecodeError

from src.selectores.SelectorCodigos import SelectorArchivoCodigos
from src.selectores.CargadorMaterias import cargar_materias
from src.parseadores.ParseadorTerminal import *
from src.respuestas.LectorRespuestas import LectorRespuestas

from src.utils import *
from src.funciones import *


# Variables Globales
START = "12/8"  # dia de inicio
END = "22/11"  # dia de finalizacion
# las siguientes se asignan en initialize()
CODIGOS = list()  # lista con todos los codigos
DIAS = 0  # cantidad de dias, son 103 del 12/8 al 22/11
MATERIAS = list()  # lista de ints, columnas donde estan las materias partiendo de la columna 4 (D)
NOMBRES_MATERIAS = list()  # lista de strings, nombres de todas las materias


def main():
    argumentos = parsear_argumentos(sys.argv[1:])

    # cargar configuracion
    if not "config" in argumentos:
        config_path = "config/config.json"
    else:
        config_path = argumentos["config"]
    config = leer_config(config_path)

    # crear el lector de respuestas
    lector_respuestas = inicializar_lector(config, argumentos)

    # cargar las respuestas
    resultado_respuestas = cargar_respuestas(lector_respuestas, config, argumentos)

    # menu de opciones
    opcion = -1
    while opcion != 0:
        listar_opciones()
        try:
            opcion = int(input("Ingrese la opcion: "))
        except ValueError:
            print("Ingrese solo el numero de la opcion.")
            continue
        if opcion == 1:
            llamar_opcion_1(resultado_respuestas, config, argumentos)
        elif opcion == 2:
            llamar_opcion_2(resultado_respuestas, config, argumentos)
        elif opcion == 3:
            llamar_opcion_3(resultado_respuestas, config, argumentos)
        elif opcion == 4:
            llamar_opcion_4(resultado_respuestas, config, argumentos)
        elif opcion == 5:
            llamar_opcion_5(resultado_respuestas, config, argumentos)
        elif opcion == 6:
            llamar_opcion_6(resultado_respuestas, config, argumentos)
        elif opcion == 7:
            llamar_opcion_7(resultado_respuestas, config, argumentos)
        elif opcion == 8:
            llamar_opcion_8(resultado_respuestas, config, argumentos)
        elif opcion == 9:
            llamar_opcion_9(resultado_respuestas, config, argumentos)
        elif opcion == 10:
            llamar_opcion_10(resultado_respuestas, config, argumentos)
        elif opcion != 0:
            print("Codigo invalido")


# guarda los argumentos pasados por linea de comando en un diccionario
def parsear_argumentos(arguments):
    argumentos = dict()
    for a in arguments:
        try:
            clave, valor = a.split('=', 1)
            argumentos[clave] = valor
        except ValueError:
            cerrar_programa_con_error(f"Argumento {a} desconocido.")
    return argumentos


# lee el archivo de configuracion en formato json
def leer_config(config_path):
    try:
        with open(config_path, 'rt', encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Advertencia: no se encontro el archivo de configuracion.")
        return None
    except JSONDecodeError:
        error = "Error leyendo el archivo de configuracion. Revise que el formato del archivo sea el correcto."
    except PermissionError as e:
        error = f"Error abriendo el archivo {config_path}: {e}"
    cerrar_programa_con_error(error)


# lee los archivos de inicializacion y carga que codigos y materias se van a usar y en que rango de dias
def inicializar_lector(config, argumentos):
    # codigos
    selector_codigos = inicializar_codigos(config, argumentos)

    # materias
    materias = inicializar_materias(config, argumentos)

    # dias
    fecha_inicio, fecha_fin = inicializar_dias(config, argumentos)

    return LectorRespuestas(selector_codigos, materias, fecha_inicio, fecha_fin)


def inicializar_codigos(config, argumentos):
    codigos_path = obtener_parametro("codigos", argumentos, config,
                                lambda: solicitar_archivo_existente("Ingrese la ruta del archivo con los codigos:\n"),
                                es_archivo_existente, False, "{valor} no es un archivo.")

    try:
        with open(codigos_path, 'rt', encoding='utf-8') as archivo_codigos:
            selector = SelectorArchivoCodigos(archivo_codigos)
            return selector
    except FileNotFoundError:
        error = f"Error: no se encontro el archivo de codigos: {codigos_path}."
    except PermissionError:
        error = f"Error: no hay permisos para abrir el archivo de codigos: {codigos_path}."
    except ValueError as e:
        error = f"Error al leer el archivo de codigos. Revise que el formato del archivo sea el correcto.\n{e}"
    cerrar_programa_con_error(error)


def inicializar_materias(config, argumentos):
    lista_materias_path = obtener_parametro("lista_materias", argumentos, config,
                        lambda: solicitar_archivo_existente("Ingrese la ruta del archivo con la lista de materias:\n"),
                        es_archivo_existente, False, "{valor} no es un archivo.")

    incluidas_path = obtener_parametro("materias", argumentos, config,
                    lambda: solicitar_archivo_existente("Ingrese la ruta del archivo con las materias incluidas:\n"),
                    es_archivo_existente, False, "{valor} no es un archivo.")

    # cargar datos
    try:
        with open(lista_materias_path, 'rt', encoding='utf-8') as archivo_lista_materias, \
                open(incluidas_path, 'rt') as archivo_materias_incluidas:
            materias = cargar_materias(archivo_lista_materias, archivo_materias_incluidas)
            return materias
    except FileNotFoundError as e:
        error = f"Error: no se encontro el archivo de materias:\n{e}"
    except PermissionError as e:
        error = f"Error: no hay permisos para abrir el archivo de materias:\n{e}."
    except (ValueError, KeyError) as e:
        error = f"Error al leer el archivo de materias. Revise que el formato del archivo sea el correcto.\n{e}"
    cerrar_programa_con_error(error)


def inicializar_dias(config, argumentos):
    fecha_inicio = obtener_parametro("fecha_inicio", argumentos, config,
                                     lambda: solicitar_fecha("Ingrese la fecha de inicio en formato dd/mm:\n"),
                                     validar_fecha, False, "Formato de fecha invalido.")

    fecha_fin = obtener_parametro("fecha_fin", argumentos, config,
                                  lambda: solicitar_fecha("Ingrese la fecha de fin en formato dd/mm:\n"),
                                  validar_fecha, False, "Formato de fecha invalido.")

    if fecha_es_anterior(fecha_inicio, fecha_fin):
        return fecha_inicio, fecha_fin

    else:
        cerrar_programa_con_error("Error: la fecha de inicio debe ser anterior a la fecha de fin.")


def cargar_respuestas(lector, config, argumentos):
    respuestas_path = obtener_parametro("respuestas", argumentos, config,
                                    lambda: solicitar_archivo_existente("Ingrese la ruta del archivo de respuestas:"),
                                    es_archivo_existente, False,"{valor} no es un archivo.")

    encoding = obtener_parametro("encoding", argumentos, config,
                                 lambda: input("Ingrese la codificacion del archivo de respuestas: "),
                                 None)
    separador = obtener_parametro("separador", argumentos, config,
                                lambda: input("Ingrese el caracter separador de columnas: "),
                                lambda x: x == ',' or x == ';', error_msg="El separador debe ser ',' o ';'.",)
    materias_offset = obtener_parametro("materias_offset", argumentos, config,
                            lambda: input("Ingrese la cantidad de columnas antes de la primer materia: "),
                            lambda x: str.isdigit(x) and int(x) >= 0 if isinstance(x, str) else x >= 0,
                            error_msg="El offset debe ser un numero entero mayor o igual a 0.")

    try:
        return lector.cargar_respuestas(respuestas_path, encoding=encoding, separador=separador, materias_offset=materias_offset)
    except Exception as e:
        cerrar_programa_con_error("Error al cargar respuestas: " + str(e))


def listar_opciones():
    print('\nOpciones:\n'
          '1: Para una determinada materia, ver cuanto estudio cada alumno cada dia.\n'
          '2: Para una determinada materia, ver cuanto etudio cada alumno cada semana\n'
          '3: Para un determinado alumno, ver cuanto estudio cada materia cada dia.\n'
          '4: Para cada alumno, ver cuantas horas estudio cada materia durante todo el periodo de la encuesta.\n'
          '5: Mostrar cuantas horas estudio cada alumno cada semana.\n'
          '6: Mostrar cuantas horas en total se estudiaron cada materia cada semana.\n'
          '7: Mostrar cuantos alumnos estudiaron cada materia cada semana.\n'
          '8: Mostrar la cantidad de registros de cada alumno en todo el semestre.\n'
          '9: Mostrar la cantidad de registros en cada semana por todos los alumnos.\n'
          '10: Mostrar la cantidad de alumnos con registros no vacios en cada semana.\n'
          '0: Salir.')


def obtener_archivo_manual(argumentos, config):
    nombre, ruta = solicitar_nombre_y_ruta(
        "Ingrese el nombre del archivo (con extension) donde se guardaran los datos: ",
        "Ingrese la ruta donde se guardara el archivo o presione enter para usar la ruta por defecto: ")
    if ruta == "":
        ruta = obtener_parametro("ruta_resultados_default", argumentos, config, None)
    file = crear_archivo(nombre, ruta)
    return file


def llamar_opcion_1(resultado_respuestas, config, argumentos):
    materias = resultado_respuestas.obtener_materias()
    listar_materias(materias)

    materias_seleccionadas = None
    while materias_seleccionadas is None or len(materias_seleccionadas) == 0:
        inputs = input("Ingrese la(s) materia(s) separadas por coma: ")
        materias_seleccionadas = parsear_materias(inputs, len(materias))
        if materias_seleccionadas is not None and len(materias_seleccionadas) == 0:
            print("Ingrese al menos una materia")

    if len(materias_seleccionadas) == 1:
        file = obtener_archivo_manual(argumentos, config)
        if file is not None:
            horas_por_codigo_por_fecha(materias_seleccionadas[0], resultado_respuestas, file)
    else:
        ruta = input("Ingrese la ruta donde se guardara el archivo o presione enter para usar la ruta por defecto: ")
        if ruta == "":
            ruta = obtener_parametro("ruta_resultados_default", argumentos, config, None)
        overwrite = input("Ingrese 'S' para sobreescribir todos los archivos existentes u otro caracter para preguntar"
                          "por cada uno: ") == 'S'
        for m in materias_seleccionadas:
            file = crear_archivo(f"op1_{materias[m].nombre_sin_espacios}.txt", ruta, overwrite)
            if file is None:
                print(f"No se pudo crear el archivo op1_{materias[m].nombre_sin_espacios}.txt en la ruta {ruta}.")
                continue
            horas_por_codigo_por_fecha(m, resultado_respuestas, file)


def llamar_opcion_2(resultado_respuestas, config, argumentos):
    materias = resultado_respuestas.obtener_materias()
    listar_materias(materias)

    materias_seleccionadas = None
    while materias_seleccionadas is None or len(materias_seleccionadas) == 0:
        inputs = input("Ingrese la(s) materia(s) separadas por coma: ")
        materias_seleccionadas = parsear_materias(inputs, len(materias))
        if materias_seleccionadas is not None and len(materias_seleccionadas) == 0:
            print("Ingrese al menos una materia")

    if len(materias_seleccionadas) == 1:
        file = obtener_archivo_manual(argumentos, config)
        if file is not None:
            horas_por_codigo_por_semana(materias_seleccionadas[0], resultado_respuestas, file)
    else:
        ruta = input("Ingrese la ruta donde se guardara el archivo o presione enter para usar la ruta por defecto: ")
        if ruta == "":
            ruta = obtener_parametro("ruta_resultados_default", argumentos, config, None)
        overwrite = input("Ingrese 'S' para sobreescribir todos los archivos existentes u otro caracter para preguntar"
                          "por cada uno: ") == 'S'
        for m in materias_seleccionadas:
            file = crear_archivo(f"op2_{materias[m].nombre_sin_espacios}.txt", ruta, overwrite)
            if file is None:
                print(f"No se pudo crear el archivo op1_{materias[m].nombre_sin_espacios}.txt en la ruta {ruta}.")
                continue
            horas_por_codigo_por_semana(m, resultado_respuestas, file)


def llamar_opcion_3(resultado_respuestas, config, argumentos):
    codigos_seleccionados = None
    while codigos_seleccionados is None or len(codigos_seleccionados) == 0:
        inputs = input("Ingrese el/los codigos de los alumnos separados por coma: ")
        codigos_seleccionados = parsear_codigos(inputs, resultado_respuestas.obtener_codigos())
        if codigos_seleccionados is not None and len(codigos_seleccionados) == 0:
            print("Ingrese al menos un codigo")

    if len(codigos_seleccionados) == 1:
        file = obtener_archivo_manual(argumentos, config)
        if file is not None:
            horas_por_materia_por_fecha(codigos_seleccionados[0], resultado_respuestas, file)
    else:
        ruta = input("Ingrese la ruta donde se guardara el archivo o presione enter para usar la ruta por defecto: ")
        if ruta == "":
            ruta = obtener_parametro("ruta_resultados_default", argumentos, config, None)
        overwrite = input("Ingrese 'S' para sobreescribir todos los archivos existentes u otro caracter para preguntar"
                          "por cada uno: ") == 'S'
        for codigo in codigos_seleccionados:
            file = crear_archivo(f"op3_{codigo}.txt", ruta, overwrite)
            if file is None:
                print(f"No se pudo crear el archivo op3_{codigo}.txt en la ruta {ruta}.")
                continue
            horas_por_materia_por_fecha(codigo, resultado_respuestas, file)


def llamar_opcion_4(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        total_horas_por_materia_por_codigo(resultado_respuestas, file)


def llamar_opcion_5(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        total_horas_por_semana_por_codigo(resultado_respuestas, file)


def llamar_opcion_6(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        total_horas_por_materia_por_semana(resultado_respuestas, file)


def llamar_opcion_7(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        total_codigos_por_materia_por_semana(resultado_respuestas, file)


def llamar_opcion_8(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        registros_por_codigo(resultado_respuestas, file)


def llamar_opcion_9(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        registros_por_semana(resultado_respuestas, file)


def llamar_opcion_10(resultado_respuestas, config, argumentos):
    file = obtener_archivo_manual(argumentos, config)
    if file is not None:
        codigos_por_semana(resultado_respuestas, file)

if __name__ == '__main__':
    main()
