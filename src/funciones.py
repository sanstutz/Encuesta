from src.utils import crear_archivo, mostrar_ruta_archivo, date_to_int, int_to_date, day_to_week


# 1. horas de estudio en una materia por cada alumno en funcion de la fecha
def horas_por_codigo_por_fecha(materia, respuestas, file):
    # fecha    cod1    cod2    codn
    # celda ij = data[j][materia][i]
    codigos = respuestas.obtener_codigos()

    file.write("{:<}".format('Fecha'))
    for c in codigos:  # encabezado
        file.write(f"{c:>6}")
    file.write('\n')
    for i in range(respuestas.obtener_cant_dias()):
        dia, mes = int_to_date(i, respuestas.fecha_inicio, respuestas.fecha_fin)
        fecha = f"{dia:>02}/{mes:>02}"
        file.write(f"{fecha:<}")
        for c in codigos:
            file.write(f"{respuestas.obtener_respuestas(c)[materia][i]:>6}")
        file.write('\n')

    mostrar_ruta_archivo(file)


# 2 horas de estudio en una materia por cada alumno por semana en vez de por dia
def horas_por_codigo_por_semana(materia, respuestas, file):
    codigos = respuestas.obtener_codigos()
    cant_dias = respuestas.obtener_cant_dias()

    file.write("{:<7}".format('Fecha'))
    for c in codigos:  # encabezado
        file.write(f"{c:>7}")
    file.write('\n')
    cant_semanas = day_to_week(cant_dias - 1) + 1
    for s in range(cant_semanas):
        file.write(f"Sem. {s + 1:>2}")
        for c in codigos:
            suma = 0
            for j in range(7):
                dia = s * 7 + j
                if dia < cant_dias:
                    suma += respuestas.obtener_respuestas(c)[materia][dia]
                else:
                    break  # se acabaron los dias
            file.write(f"{suma:>7}")
        file.write('\n')

    mostrar_ruta_archivo(file)



# 3. horas de estudio de un alumno en cada materia en funcion de la fecha
def horas_por_materia_por_fecha(codigo, respuestas, file):
    # fecha materia1 materia2 materian
    # celda ij = data[codigo][j][i]
    materias = respuestas.obtener_materias()

    file.write("{:<15}".format('Fecha'))  # encabezado
    for m in materias:
        file.write(f"{m.nombre_corto:^22}")
    file.write('\n')
    for i in range(respuestas.cant_dias):
        dia, mes = int_to_date(i, respuestas.fecha_inicio, respuestas.fecha_fin)
        fecha = f"{dia:>02}/{mes:>02}"
        file.write(f"{fecha:<}")
        for j in range(len(materias)):
            file.write(f"{respuestas.obtener_respuestas(codigo)[j][i]:>22}")
        file.write('\n')

    mostrar_ruta_archivo(file)


# 4. horas totales de estudio de cada alumno en cada materia
def total_horas_por_materia_por_codigo(respuestas, file):
    # alumno materia1 materia2 materian
    # celda ij = sumatoria k de data[i][j][k]
    materias = respuestas.obtener_materias()

    file.write("{:<12}".format('Codigo'))
    for m in materias:  # encabezado
        file.write(f"{m.nombre_corto:^22}")
    file.write('\n')
    for c in respuestas.obtener_codigos():
        file.write(f"{c:<3}")
        for j in range(len(materias)):
            suma = 0
            for k in range(respuestas.cant_dias):
                suma += respuestas.obtener_respuestas(c)[j][k]
            file.write(f"{suma:>22}")
        file.write('\n')

    mostrar_ruta_archivo(file)


# 5. cuantas horas estudio cada alumno cada semana
def total_horas_por_semana_por_codigo(respuestas, file):
    cant_semanas = day_to_week(respuestas.cant_dias - 1) + 1  # el indice en el que cae el ultimo dia + 1
    file.write("{:<7}".format('Codigo'))
    for i in range(cant_semanas):  # encabezado
        file.write("{:^8}".format(f"Sem {i + 1}"))
    file.write('\n')

    for c in respuestas.obtener_codigos():
        file.write(f"{c:<3}")
        semanas = [0] * cant_semanas  # lista de la cantidad de horas en cada semana para ese codigo
        for j in range(respuestas.obtener_cant_materias()):
            for k in range(respuestas.cant_dias):
                semanas[day_to_week(k)] += respuestas.obtener_respuestas(c)[j][k]  # suma en la semana correspondiente las horas
        for s in semanas:  # recorre la lisa de sumas y va escribiendo
            file.write(f"{s:>8}")
        file.write('\n')

    mostrar_ruta_archivo(file)


# 6. cuantas horas estudiaron cada materia todos los alumnos por semana
def total_horas_por_materia_por_semana(respuestas, file):
    materias = respuestas.obtener_materias()

    file.write("{:<11}".format('Semana'))  # encabezado
    for m in materias:
        file.write(f"{m.nombre_corto:^22}")
    file.write('\n')

    cant_semanas = day_to_week(respuestas.cant_dias - 1) + 1  # el indice en el que cae el ultimo dia + 1
    for s in range(cant_semanas):  # cada semana
        file.write(f"{s+1:>02}")
        for j in range(len(materias)):
            suma = 0
            for c in respuestas.obtener_codigos():
                for k in range(7):  # cada dia de la semana
                    dia = s * 7 + k
                    if dia >= respuestas.cant_dias:  # la ultima semana esta incompleta porque no esta el sabado ni el domingo
                        break
                    suma += respuestas.obtener_respuestas(c)[j][dia]
            file.write(f"{suma:>22}")
        file.write('\n')

    mostrar_ruta_archivo(file)


# 7. cuantos alumnos estudiaron cada materia cada semana
def total_codigos_por_materia_por_semana(respuestas, file):
    materias = respuestas.obtener_materias()
    codigos = respuestas.obtener_codigos()

    file.write("{:<11}".format('Semana'))  # encabezado
    for m in materias:
        file.write(f"{m.nombre_corto:^22}")
    file.write('\n')

    cant_semanas = day_to_week(respuestas.cant_dias - 1) + 1  # el indice en el que cae el ultimo dia + 1
    for s in range(cant_semanas):  # cada semana
        file.write(f"{s+1:>02}")
        for j in range(len(materias)):
            contador = 0
            c = 0
            for c in codigos:  # debe ser while para tener control de los valores que toma c
                for k in range(7):  # cada dia de la semana
                    dia = s * 7 + k
                    if dia >= respuestas.cant_dias:  # la ultima semana esta incompleta porque no esta el sabado ni el domingo
                        break
                    horas = respuestas.obtener_respuestas(c)[j][dia]
                    if horas > 0:
                        contador += 1
                        break  # este codigo ya sumo, dejo de buscar y paso al siguiente
            file.write(f"{contador:>22}")
        file.write('\n')

    mostrar_ruta_archivo(file)


# 8. cuantos registros hubo por cada alumno
def registros_por_codigo(respuestas, file):
    contador = respuestas.cant_respuestas_por_codigo

    file.write("{:<10}{}".format('Codigo', 'Registros\n'))
    for c in respuestas.obtener_codigos():
        file.write(f"{c:<10}{contador[c]:>5}\n")

    mostrar_ruta_archivo(file)


# 9. cuantos registros hubo cada semana
def registros_por_semana(respuestas, file):
    contador = respuestas.cant_respuestas_por_semana

    file.write("{:<10}{}".format('Semana', 'Registros\n'))
    for i in range(len(contador)):
        file.write(f"{i + 1:<10}{contador[i]:>6}\n")

    mostrar_ruta_archivo(file)


# 10. cuantos alumnos respondieron en cada semana
def codigos_por_semana(respuestas, file):
    file.write("{:<10}{}".format('Semana', 'Estudiantes\n'))
    semanas = [0] * (day_to_week(respuestas.cant_dias - 1) + 1)  # el indice en el que cae el ultimo dia + 1
    for c in respuestas.obtener_codigos():
        d = 0
        while d < respuestas.cant_dias:  # recorre todos los dias, si en alguna materia registro suma en la semana y pasa a la siguiente
            for m in range(respuestas.obtener_cant_materias()):
                if respuestas.obtener_respuestas(c)[m][d] > 0:
                    s = day_to_week(d)
                    semanas[s] += 1
                    d = (s + 1) * 7 - 1  # siguiente semana - 1 porque le voy a sumar 1 en el while
                    break
            d += 1
    for i in range(len(semanas)):
        file.write(f"{i + 1:<10}{semanas[i]:>6}\n")

    mostrar_ruta_archivo(file)
