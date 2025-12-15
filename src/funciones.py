from src.utils import *


# 1. horas de estudio en una materia por cada alumno en funcion de la fecha
def horas_por_codigo_por_fecha(materia, data, CODIGOS, DIAS, START_DATE, END_DATE):
    # fecha    cod1    cod2    codn
    # celda ij = data[j][i][materia]
    file = create_file()
    if file is None:
        return

    file.write("{:<}".format('Fecha'))
    for i in range(len(data)):  # encabezado
        file.write(f"{int_to_code(i, CODIGOS):>6}")
    file.write('\n')
    for i in range(DIAS):
        dia, mes = int_to_date(i, START_DATE, END_DATE)
        fecha = f"{dia:>02}/{mes:>02}"
        file.write(f"{fecha:<}")
        for j in range(len(CODIGOS)):
            file.write(f"{data[j][i][materia]:>6}")
        file.write('\n')
    file.close()
    mostrar_ruta_archivo(file)

# 1.5 horas de estudio en una materia por cada alumno por semana en vez de por dia
def horas_por_codigo_por_semana(materia, data, CODIGOS, DIAS):
    file = create_file()
    if file is None:
        return

    file.write("{:<7}".format('Fecha'))
    for i in range(len(data)):  # encabezado
        file.write(f"{int_to_code(i, CODIGOS):>7}")
    file.write('\n')
    cant_semanas = day_to_week(DIAS - 1) + 1
    for s in range(cant_semanas):
        file.write(f"Sem. {s + 1:>2}")
        for i in range(len(CODIGOS)):
            suma = 0
            for j in range(7):
                dia = s * 7 + j
                if dia < DIAS:
                    suma += data[i][dia][materia]
                else:
                    break  # se acabaron los dias
            file.write(f"{suma:>7}")
        file.write('\n')

    file.close()
    mostrar_ruta_archivo(file)



# 2. horas de estudio de un alumno en cada materia en funcion de la fecha
def horas_por_materia_por_fecha(codigo, data, MATERIAS, NOMBRES_MATERIAS, DIAS, START_DATE, END_DATE):
    # fecha materia1 materia2 materian
    # celda ij = data[codigo][i][j]
    file = create_file()
    if file is None:
        return

    file.write("{:<15}".format('Fecha'))  # encabezado
    for i in MATERIAS:
        file.write(f"{NOMBRES_MATERIAS[i]:^22}")
    file.write('\n')
    for i in range(DIAS):
        dia, mes = int_to_date(i, START_DATE, END_DATE)
        fecha = f"{dia:>02}/{mes:>02}"
        file.write(f"{fecha:<}")
        for j in range(len(MATERIAS)):
            file.write(f"{data[codigo][i][j]:>22}")
        file.write('\n')
    file.close()
    mostrar_ruta_archivo(file)


# 3. horas totales de estudio de cada alumno en cada materia
def total_horas_por_materia_por_codigo(data, CODIGOS, MATERIAS, NOMBRES_MATERIAS, DIAS):
    # alumno materia1 materia2 materian
    # celda ij = sumatoria k de data[i][k][j]
    file = create_file()
    if file is None:
        return

    file.write("{:<12}".format('Codigo'))
    for i in MATERIAS:  # encabezado
        file.write(f"{NOMBRES_MATERIAS[i]:^22}")
    file.write('\n')
    for i in range(len(CODIGOS)):
        file.write(f"{int_to_code(i, CODIGOS):<3}")
        for j in range(len(MATERIAS)):
            suma = 0
            for k in range(DIAS):
                suma += data[i][k][j]
            file.write(f"{suma:>22}")
        file.write('\n')
    file.close()
    mostrar_ruta_archivo(file)


# 4. cuantas horas estudio cada alumno cada semana
def total_horas_por_semana_por_codigo(data, CODIGOS, MATERIAS, DIAS):
    file = create_file()
    if file is None:
        return

    cant_semanas = day_to_week(DIAS - 1) + 1  # el indice en el que cae el ultimo dia + 1
    file.write("{:<7}".format('Codigo'))
    for i in range(cant_semanas):  # encabezado
        file.write("{:^8}".format(f"Sem {i + 1}"))
    file.write('\n')

    for i in range(len(CODIGOS)):
        file.write(f"{int_to_code(i, CODIGOS):<3}")
        semanas = [0] * cant_semanas  # lista de la cantidad de horas en cada semana para ese codigo
        for j in range(DIAS):
            for k in range(len(MATERIAS)):
                semanas[day_to_week(j)] += data[i][j][k]  # suma en la semana correspondiente las horas
        for s in semanas:  # recorre la lisa de sumas y va escribiendo
            file.write(f"{s:>8}")
        file.write('\n')
    file.close()
    mostrar_ruta_archivo(file)


# 5. cuantas horas estudiaron cada materia todos los alumnos por semana
def total_horas_por_materia_por_semana(data, CODIGOS, MATERIAS, NOMBRES_MATERIAS, DIAS):
    file = create_file()
    if file is None:
        return

    file.write("{:<11}".format('Semana'))  # encabezado
    for i in MATERIAS:
        file.write(f"{NOMBRES_MATERIAS[i]:^22}")
    file.write('\n')

    cant_semanas = day_to_week(DIAS - 1) + 1  # el indice en el que cae el ultimo dia + 1
    for s in range(cant_semanas):  # cada semana
        file.write(f"{s+1:>02}")
        for m in range(len(MATERIAS)):
            suma = 0
            for c in range(len(CODIGOS)):
                for d in range(7):  # cada dia de la semana
                    if s * 7 + d >= DIAS:  # la ultima semana esta incompleta porque no esta el sabado ni el domingo
                        break
                    suma += data[c][s * 7 + d][m]
            file.write(f"{suma:>22}")
        file.write('\n')
    file.close()
    mostrar_ruta_archivo(file)


# 6. cuantos alumnos estudiaron cada materia cada semana
def total_codigos_por_materia_por_semaa(data, CODIGOS, MATERIAS, NOMBRES_MATERIAS, DIAS):
    file = create_file()
    if file is None:
        return

    file.write("{:<11}".format('Semana'))  # encabezado
    for i in MATERIAS:
        file.write(f"{NOMBRES_MATERIAS[i]:^22}")
    file.write('\n')

    cant_semanas = day_to_week(DIAS - 1) + 1  # el indice en el que cae el ultimo dia + 1
    for s in range(cant_semanas):  # cada semana
        file.write(f"{s+1:>02}")
        for m in range(len(MATERIAS)):
            contador = 0
            c = 0
            while c < len(CODIGOS):  # debe ser while para tener control de los valores que toma c
                for d in range(7):  # cada dia de la semana
                    if s * 7 + d >= DIAS:  # la ultima semana esta incompleta porque no esta el sabado ni el domingo
                        break
                    horas = data[c][s*7 + d][m]
                    if horas > 0:
                        contador += 1
                        break  # este codigo ya sumo, dejo de buscar y paso al siguiente
                c += 1
            file.write(f"{contador:>22}")
        file.write('\n')
    file.close()
    mostrar_ruta_archivo(file)


# 7. cuantos registros hubo por cada alumno
def registros_por_codigo(contador, CODIGOS):
    file = create_file()
    if file is None:
        return
    file.write("{:<10}{}".format('Codigo', 'Registros\n'))
    for i in range(len(contador)):
        file.write(f"{int_to_code(i, CODIGOS):<10}{contador[i]:>5}\n")
    file.close()
    mostrar_ruta_archivo(file)


# 8. cuantos registros hubo cada semana
def registros_por_semana(contador):
    file = create_file()
    if file is None:
        return

    file.write("{:<10}{}".format('Semana', 'Registros\n'))
    for i in range(len(contador)):
        file.write(f"{i + 1:<10}{contador[i]:>6}\n")
    file.close()
    mostrar_ruta_archivo(file)


# 9. cuantos alumnos respondieron en cada semana
def codigos_por_semana(data, CODIGOS, MATERIAS, DIAS):
    file = create_file()
    if file is None:
        return

    file.write("{:<10}{}".format('Semana', 'Estudiantes\n'))
    semanas = [0] * (day_to_week(DIAS - 1) + 1)  # el indice en el que cae el ultimo dia + 1
    for c in range(len(CODIGOS)):
        d = 0
        while d < DIAS:  # recorre todos los dias, si en alguna materia registro suma en la semana y pasa a la siguiente
            for m in range(len(MATERIAS)):
                if data[c][d][m] > 0:
                    s = day_to_week(d)
                    semanas[s] += 1
                    d = (s + 1) * 7 - 1  # siguiente semana - 1 porque le voy a sumar 1 en el while
                    break
            d += 1
    for i in range(len(semanas)):
        file.write(f"{i + 1:<10}{semanas[i]:>6}\n")

    file.close()
    mostrar_ruta_archivo(file)
