import sys
import json
from json import JSONDecodeError

from src.selectores.SelectorCodigos import SelectorArchivoCodigos
from src.selectores.CargadorMaterias import cargar_materias
from src.parseadores.ParseadorTerminal import *
from src.respuestas.LectorRespuestas import LectorRespuestas

from src.utils import *
from src.funciones import *
from src.output.output import Output, OutputConsola, OutputArchivo

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

    # obtener el destino
    tipo_output = obtener_parametro("output", argumentos, config)
    if tipo_output == "consola":
        out = OutputConsola()
    else:
        out = OutputArchivo()
        if tipo_output is None or tipo_output != "archivo":
            print("No se especifico un tipo de output valido. Se usara output a archivo por defecto.")

    # opciones automaticas
    funciones_auto = obtener_funciones_auto(argumentos)
    if len(funciones_auto) > 0:
        for f in funciones_auto:
            codigo = f.get("f", -1)
            params = f.get("p", "")
            if codigo == 0:
                exit()
            if codigo == 1:
                llamar_opcion_1(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 2:
                llamar_opcion_2(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 3:
                llamar_opcion_3(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 4:
                llamar_opcion_4(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 5:
                llamar_opcion_5(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 6:
                llamar_opcion_6(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 7:
                llamar_opcion_7(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 8:
                llamar_opcion_8(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 9:
                llamar_opcion_9(resultado_respuestas, config, argumentos, out, params)
            elif codigo == 10:
                llamar_opcion_10(resultado_respuestas, config, argumentos, out, params)
            else:
                cerrar_programa_con_error(f"Error: la funcion {codigo} no es una opcion valida.")

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
            llamar_opcion_1(resultado_respuestas, config, argumentos, out)
        elif opcion == 2:
            llamar_opcion_2(resultado_respuestas, config, argumentos, out)
        elif opcion == 3:
            llamar_opcion_3(resultado_respuestas, config, argumentos, out)
        elif opcion == 4:
            llamar_opcion_4(resultado_respuestas, config, argumentos, out)
        elif opcion == 5:
            llamar_opcion_5(resultado_respuestas, config, argumentos, out)
        elif opcion == 6:
            llamar_opcion_6(resultado_respuestas, config, argumentos, out)
        elif opcion == 7:
            llamar_opcion_7(resultado_respuestas, config, argumentos, out)
        elif opcion == 8:
            llamar_opcion_8(resultado_respuestas, config, argumentos, out)
        elif opcion == 9:
            llamar_opcion_9(resultado_respuestas, config, argumentos, out)
        elif opcion == 10:
            llamar_opcion_10(resultado_respuestas, config, argumentos, out)
        elif opcion != 0:
            print("Codigo invalido")


# guarda los argumentos pasados por linea de comando en un diccionario
def parsear_argumentos(arguments: list[str]):
    argumentos = dict()
    for a in arguments:
        try:
            clave, valor = a.split('=', 1)
            argumentos[clave] = valor
        except ValueError:
            cerrar_programa_con_error(f"Argumento {a} desconocido.")
    return argumentos


# lee el archivo de configuracion en formato json
def leer_config(config_path: str):
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


def obtener_funciones_auto(argumentos: dict) -> list[dict]:
    funciones_json = obtener_parametro("acciones", argumentos)
    if funciones_json is None:
        return list()
    try:
        funciones = json.loads(funciones_json)            
        return funciones
    except JSONDecodeError:
        cerrar_programa_con_error("Error: el valor de 'acciones' no es un JSON valido.")


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


def llamar_opcion_1(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default: str = None):
    materias = resultado_respuestas.obtener_materias()

    if default is not None:
        materias_seleccionadas = parsear_materias(default, len(materias))
        if materias_seleccionadas is None or len(materias_seleccionadas) == 0:
            cerrar_programa_con_error("Error: el valor de 'params' para la funcion 1 no es valido.")
    else:
        listar_materias(materias)

        materias_seleccionadas = None
        while materias_seleccionadas is None or len(materias_seleccionadas) == 0:
            inputs = input("Ingrese la(s) materia(s) separadas por coma: ")
            materias_seleccionadas = parsear_materias(inputs, len(materias))
            if materias_seleccionadas is not None and len(materias_seleccionadas) == 0:
                print("Ingrese al menos una materia")

    if len(materias_seleccionadas) == 1:
        # una sola materia
        resultado = horas_por_codigo_por_fecha(materias_seleccionadas[0], resultado_respuestas)
        out.mostrar_output(resultado, argumentos, config, "op1", default is not None)
    else:
        # muchos archivos
        resultados = []
        for m in materias_seleccionadas:
            resultado = horas_por_codigo_por_fecha(m, resultado_respuestas)
            resultados.append(resultado)
        out.mostrar_multiples_output(resultados, argumentos, config, "op1", default is not None)


def llamar_opcion_2(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default: str = None):
    materias = resultado_respuestas.obtener_materias()

    if default is not None:
        materias_seleccionadas = parsear_materias(default, len(materias))
        if materias_seleccionadas is None or len(materias_seleccionadas) == 0:
            cerrar_programa_con_error("Error: el valor de 'params' para la funcion 2 no es valido.")
    else:
        listar_materias(materias)

        materias_seleccionadas = None
        while materias_seleccionadas is None or len(materias_seleccionadas) == 0:
            inputs = input("Ingrese la(s) materia(s) separadas por coma: ")
            materias_seleccionadas = parsear_materias(inputs, len(materias))
            if materias_seleccionadas is not None and len(materias_seleccionadas) == 0:
                print("Ingrese al menos una materia")

    if len(materias_seleccionadas) == 1:
        # una materia
        resultado = horas_por_codigo_por_semana(materias_seleccionadas[0], resultado_respuestas)
        out.mostrar_output(resultado, argumentos, config, "op2", default is not None)
    else:
        resultados = []
        for m in materias_seleccionadas:
            resultado = horas_por_codigo_por_semana(m, resultado_respuestas)
            resultados.append(resultado)
        out.mostrar_multiples_output(resultados, argumentos, config, "op2", default is not None)


def llamar_opcion_3(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default: str = None):
    if default is not None:
        codigos_seleccionados = parsear_codigos(default, resultado_respuestas.obtener_codigos())
        if codigos_seleccionados is None or len(codigos_seleccionados) == 0:
            cerrar_programa_con_error("Error: el valor de 'params' para la funcion 3 no es valido.")
    else:
        codigos_seleccionados = None
        while codigos_seleccionados is None or len(codigos_seleccionados) == 0:
            inputs = input("Ingrese el/los codigos de los alumnos separados por coma: ")
            codigos_seleccionados = parsear_codigos(inputs, resultado_respuestas.obtener_codigos())
            if codigos_seleccionados is not None and len(codigos_seleccionados) == 0:
                print("Ingrese al menos un codigo")

    if len(codigos_seleccionados) == 1:
        # un codigo
        resultado = horas_por_materia_por_fecha(codigos_seleccionados[0], resultado_respuestas)
        out.mostrar_output(resultado, argumentos, config, "op3", default is not None)
    else:
        resultados = []
        for codigo in codigos_seleccionados:
            resultado = horas_por_materia_por_fecha(codigo, resultado_respuestas)
            resultados.append(resultado)
        out.mostrar_multiples_output(resultados, argumentos, config, "op3", default is not None)


def llamar_opcion_4(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = total_horas_por_materia_por_codigo(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op4", default is not None)


def llamar_opcion_5(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = total_horas_por_semana_por_codigo(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op5", default is not None)


def llamar_opcion_6(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = total_horas_por_materia_por_semana(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op6", default is not None)


def llamar_opcion_7(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = total_codigos_por_materia_por_semana(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op7", default is not None)


def llamar_opcion_8(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = registros_por_codigo(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op8", default is not None)


def llamar_opcion_9(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = registros_por_semana(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op9", default is not None)


def llamar_opcion_10(resultado_respuestas: ResultadoRespuestas, config: dict, argumentos: dict, out: Output, default = None):
    resultado = codigos_por_semana(resultado_respuestas)
    out.mostrar_output(resultado, argumentos, config, "op10", default is not None)

if __name__ == '__main__':
    main()
