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
    # cargar el valor de las variables globales
    initialize()

    # cargar las respuestas

    # cuantos registros hay por codigo
    contador_codigos = [0] * len(CODIGOS)
    # cuantos registros hay por semana
    contador_semanas = [0] * ((DIAS - 1) // 7 + 1)  # el indice en el que cae el ultimo dia + 1
    data = cargar_respuestas(contador_codigos, contador_semanas)

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
            listar_materias(MATERIAS, NOMBRES_MATERIAS)
            materia = -1
            while not (0 <= materia < len(MATERIAS)):
                try:
                    materia = int(input("Ingrese el codigo de la materia: ")) - 1
                except ValueError:
                    print("Codigo Invalido.")
                    continue
            horas_por_codigo_por_fecha(materia, data, CODIGOS, DIAS, START, END)
        elif opcion == 11:
            listar_materias(MATERIAS, NOMBRES_MATERIAS)
            materia = -1
            while not (0 <= materia < len(MATERIAS)):
                try:
                    materia = int(input("Ingrese el codigo de la materia: ")) - 1
                except ValueError:
                    print("Codigo Invalido.")
                    continue
            horas_por_codigo_por_semana(materia, data, CODIGOS, DIAS)
        elif opcion == 2:
            codigo_str = input("Ingrese el codigo de alumno: ").upper()
            codigo = code_to_int(codigo_str, CODIGOS)
            while codigo == -1:
                codigo_str = input("El codigo no es de un alumno de fisica. Ingrese un codigo valido: ").upper()
                codigo = code_to_int(codigo_str, CODIGOS)
            horas_por_materia_por_fecha(codigo, data, MATERIAS, NOMBRES_MATERIAS, DIAS, START, END)
        elif opcion == 3:
            total_horas_por_materia_por_codigo(data, CODIGOS, MATERIAS, NOMBRES_MATERIAS, DIAS)
        elif opcion == 4:
            total_horas_por_semana_por_codigo(data, CODIGOS, MATERIAS, DIAS)
        elif opcion == 5:
            total_horas_por_materia_por_semana(data, CODIGOS, MATERIAS, NOMBRES_MATERIAS, DIAS)
        elif opcion == 6:
            total_codigos_por_materia_por_semaa(data, CODIGOS, MATERIAS, NOMBRES_MATERIAS, DIAS)
        elif opcion == 7:
            registros_por_codigo(contador_codigos, CODIGOS)
        elif opcion == 8:
            registros_por_semana(contador_semanas)
        elif opcion == 9:
            codigos_por_semana(data, CODIGOS, MATERIAS, DIAS)
        elif opcion != 0:
            print("Codigo invalido")


# asigna las variables globales que requieren algun calculo para obtener el valor
def initialize():
    global DIAS

    # cantidad de dias
    DIAS = date_to_int(END, START, END) - date_to_int(START, START, END) + 1

    initialize_codigos()

    initialize_materias()



def initialize_codigos():
    global CODIGOS

    try:
        archivo_codigos = open("codigos.txt", 'rt')
        for line in archivo_codigos:
            if line == "\n" or line[0] == '#':  # comentario o linea en blanco
                continue
            rango = line.split('-')
            if len(rango) == 1:  # habia un codigo individual
                c = format_code(rango[0])
                if c is not None:
                    CODIGOS.append(c)
                else:
                    print(f"{line.rstrip('\n')} es un codigo invalido.")
                    raise ValueError  # para que cancele la ejecucion, pero no quiero repetir el try
            else:  # habia un rango, hay que agregar todos los codigos dentro del rango
                start = int(rango[0][1:])  # lo que le siga a la letra en el primer codigo
                end = int(rango[1][1:])  # lo que le siga a la letra en el segundo codigo
                if rango[0][0] == rango[1][0]:  # el primer caracter de ambos codigos debe ser la misma letra
                    letra = rango[0][0]
                else:
                    print(f"{line.rstrip('\n')} es rango invalido, se va a ignorar.")
                    raise ValueError
                for i in range(start, end + 1):  # el end si esta incluido en los codigos
                    c = format_code(letra + str(i))
                    CODIGOS.append(c)  # creo que al haber sacado letra y numero si hubiera algo invalido ya hubiera
                    # saltado y no hace falta revisar que sea valido de vuelta, espero que no se rompa
    except FileNotFoundError:
        print("Error: no se encontro el archivo codigos.txt con los codigos.")
        input()  # para que no se cierre la terminal
        exit()
    except PermissionError:
        print("Error: no hay permisos para abrir el archivo codigos.txt con los codigos.")
        input()  # para que no se cierre la terminal
        exit()
    except ValueError or IndexError:
        print("Error al leer el archivo codigos.txt. Revise que el formato del archivo sea el correcto.")
        input()  # para que no se cierre la terminal
        exit()
    archivo_codigos.close()


def initialize_materias():
    global NOMBRES_MATERIAS
    global MATERIAS

    # nombres
    try:
        archivo_nombres = open("nombres_materias.txt", 'rt')
        for line in archivo_nombres:
            nombre = line.split(':')[1]  # [columna: nombre]
            NOMBRES_MATERIAS.append(nombre.lstrip(' ').rstrip('\n'))
    except FileNotFoundError:
        print("Error: no se encontro el archivo nombres_materias.txt con los nombres de las materias.")
        input()  # para que no se cierre la terminal
        exit()
    except PermissionError:  # por que pasaria? no se pero como todos los open me tiraron este error alguna vez...
        print("Error: no hay permisos para abrir el archivo nombres_materias.txt con los nombres de las materias.")
        input()  # para que no se cierre la terminal
        exit()
    except ValueError:
        print("Error al leer el archivo nombres_materias.txt. Revise que el formato del archivo sea el correcto.")
        input()  # para que no se cierre la terminal
        exit()
    archivo_nombres.close()

    # materias
    try:
        archivo_materias = open("materias.txt", 'rt')
        for line in archivo_materias:
            if line == "\n" or line[0] == '#':  # comentario o linea en blanco
                continue
            rango = line.split('-')
            if len(rango) == 1:  # habia una materia individual
                if int(rango[0]) < len(NOMBRES_MATERIAS):  # la materia no existe
                    MATERIAS.append(int(rango[0]))
                else:
                    print(f"Error: la materia {rango[0]} no existe. Revise que las materias ingresadas existan en "
                          f"nombres_materias.txt")
            else:  # habia un rango de materias
                start = int(rango[0])
                end = int(rango[1])
                if end >= len(NOMBRES_MATERIAS):  # la materia no existe
                    print(f"Error: la materia {end} no existe. Revise que las materias ingresadas existan en "
                          f"nombres_materias.txt")
                for i in range(start, end + 1):  # end esta incluido
                    MATERIAS.append(i)
    except FileNotFoundError:
        print("Error: no se encontro el archivo materias.txt con las materias.")
        input()  # para que no se cierre la terminal
        exit()
    except PermissionError:  # por que pasaria? no se pero como todos los open me tiraron este error alguna vez...
        print("Error: no hay permisos para abrir el archivo materias.txt con las materias.")
        input()  # para que no se cierre la terminal
        exit()
    except ValueError:
        print("Error al leer el archivo materias.txt. Revise que el formato del archivo sea el correcto.")
        input()  # para que no se cierre la terminal
        exit()
    archivo_materias.close()


# abre el archivo de respuestas, lee todas las lineas y las va agregando a data, ademas de incrementar los contadores
# los contadores son para las opciones 5 y 6, porque sino tendria que abrir de vuelta el archivo y contar otra vez, y
# es mas facil contar mientras cargo los datos
def cargar_respuestas(contador_codigos=None, contador_semanas=None):
    # Estructura del archivo: fecha envio, codigo, fecha, 110 materias, otros campos no importantes
    file = None
    while file is None:
        path = input("Ingrese ruta y nombre del archivo (con extension) para cargar datos: ")
        try:
            file = open(path, 'rt', encoding="latin-1")
        except PermissionError:  # los directorios tiran este error
            print("Error: no se puede abrir el archivo debido a que no hay permisos o es un directorio.")
        except FileNotFoundError:
            print("No se encontro el archivo.")
        except OSError:
            print("Error: no se ingreso una ruta valida.")

    # codigos->dias->materias
    data = list(range(len(CODIGOS)))
    for i in range(len(CODIGOS)):
        data[i] = list(range(DIAS))
        for j in range(DIAS):
            data[i][j] = list(range(len(MATERIAS)))
            for k in range(len(MATERIAS)):
                data[i][j][k] = 0

    # dependiendo de si el archivo csv lo genero con excel u hojas de calculo de Google separa los campos con ; o ,
    s = None
    while s not in (1, 2):
        try:
            s = int(input(
                'Ingrese 1 si los campos están separados por coma (,) o 2 si están separados por punto y coma (;): '))
        except ValueError:
            print("Ingrese 1 o 2 sin ningun otro caracter.")
    if s == 1:
        separador = ','
    else:
        separador = ';'

    # lee linea por linea y las procesa en agregar_registro()
    line = file.readline()
    while line != "":
        registro = line.split(separador)
        agregar_registro(registro, data, contador_codigos, contador_semanas)
        line = file.readline()
    file.close()
    return data


# carga las respuestas de los codigos validos en la matriz data
def agregar_registro(registro, data, contador_codigos=None, contador_semanas=None):
    # los return se usaban para contar la cantidad de lineas exitosas o que tenian error, return 1 significa exito
    # estructura del registro: [emision, codigo, fecha, 110 materias, ...]
    try:
        cod = code_to_int(registro[1], CODIGOS)
        if cod == -1:  # el codigo no es valido
            # print(f"El codigo {line[1]} no es de fisica")
            return 0
        if contador_codigos is not None:
            contador_codigos[cod] += 1
        fecha = date_to_int(registro[2], START, END)
        if fecha == -1:  # la fecha esta fuera de rango
            # print(f"La respuesta del codigo {int_to_code(cod)} está fuera de la fecha permitida")
            return 0
        if contador_semanas is not None:
            contador_semanas[fecha // 7] += 1
        for i in range(len(MATERIAS)):
            if registro[MATERIAS[i] + 3] != "":  # si la celda de esta materia esta en blanco = 0 horas estudiadas
                horas = registro[MATERIAS[i] + 3]  # el indice de las materias es respecto a la columna D (0 = D, 1 = E)
                horas = horas.replace(',', '.')  # por si me andan cambiando que caracter separa valores decimales
                data[cod][fecha][i] += float(horas)
        return 1
    except IndexError:  # si pusiste que los campos estaban separados por , en vez de ; 99.9% seguro de que terminas aca
        print("Error al procesar una linea. Revise que el archivo este bien formateado. Linea que produjo el error:\n"
              f"{registro}")
        input()
        exit()


# funciones auxiliares



def listar_opciones():
    print('\nOpciones:\n'
          '1: Para una determinada materia, ver cuanto estudio cada alumno cada dia.\n'
          '11: Para una determinada materia, ver cuanto etudio cada alumno cada semana\n'
          '2: Para un determinado alumno, ver cuanto estudio cada materia cada dia.\n'
          '3: Para cada alumno, ver cuantas horas estudio cada materia durante todo el periodo de la encuesta.\n'
          '4: Mostrar cuantas horas estudio cada alumno cada semana.\n'
          '5: Mostrar cuantas horas en total se estudiaron cada materia cada semana.\n'
          '6: Mostrar cuantos alumnos estudiaron cada materia cada semana.\n'
          '7: Mostrar la cantidad de registros de cada alumno en todo el semestre.\n'
          '8: Mostrar la cantidad de registros en cada semana por todos los alumnos.\n'
          '9: Mostrar la cantidad de alumnos con registros no vacios en cada semana.\n'
          '0: Salir.')




# opciones del menu



if __name__ == '__main__':
    main()
