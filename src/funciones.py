from src.utils import int_to_date, day_to_week
from src.respuestas.ResultadoRespuestas import ResultadoRespuestas


# 1. horas de estudio en una materia por cada alumno en funcion de la fecha
def horas_por_codigo_por_fecha(materia: int, respuestas: ResultadoRespuestas) -> str:
    # fecha    cod1    cod2    codn
    # celda ij = data[j][materia][i]

    codigos = respuestas.obtener_codigos()

    resultado = "{:<}".format('Fecha')
    for c in codigos:  # encabezado
        resultado += f"{c:>6}"
    resultado += '\n'
    for i in range(respuestas.obtener_cant_dias()):
        dia, mes = int_to_date(i, respuestas.fecha_inicio, respuestas.fecha_fin)
        fecha = f"{dia:>02}/{mes:>02}"
        resultado += f"{fecha:<}"
        for c in codigos:
            resultado += f"{respuestas.obtener_respuestas(c)[materia][i]:>6}"
        resultado += '\n'

    return resultado


# 2 horas de estudio en una materia por cada alumno por semana en vez de por dia
def horas_por_codigo_por_semana(materia: int, respuestas: ResultadoRespuestas) -> str:
    codigos = respuestas.obtener_codigos()
    cant_dias = respuestas.obtener_cant_dias()

    resultado = "{:<7}".format('Fecha')
    for c in codigos:  # encabezado
        resultado += f"{c:>7}"
    resultado += '\n'
    cant_semanas = day_to_week(cant_dias - 1) + 1
    for s in range(cant_semanas):
        resultado += f"Sem. {s + 1:>2}"
        for c in codigos:
            suma = 0
            for j in range(7):
                dia = s * 7 + j
                if dia < cant_dias:
                    suma += respuestas.obtener_respuestas(c)[materia][dia]
                else:
                    break  # se acabaron los dias
            resultado += f"{suma:>7}"
        resultado += '\n'
    return resultado



# 3. horas de estudio de un alumno en cada materia en funcion de la fecha
def horas_por_materia_por_fecha(codigo: int, respuestas: ResultadoRespuestas) -> str:
    # fecha materia1 materia2 materian
    # celda ij = data[codigo][j][i]
    materias = respuestas.obtener_materias()

    resultado = "{:<15}".format('Fecha')  # encabezado
    for m in materias:
        resultado += f"{m.nombre_corto:^22}"
    resultado += '\n'
    for i in range(respuestas.cant_dias):
        dia, mes = int_to_date(i, respuestas.fecha_inicio, respuestas.fecha_fin)
        fecha = f"{dia:>02}/{mes:>02}"
        resultado += f"{fecha:<}"
        for j in range(len(materias)):
            resultado += f"{respuestas.obtener_respuestas(codigo)[j][i]:>22}"
        resultado += '\n'
    return resultado


# 4. horas totales de estudio de cada alumno en cada materia
def total_horas_por_materia_por_codigo(respuestas: ResultadoRespuestas) -> str:
    # alumno materia1 materia2 materian
    # celda ij = sumatoria k de data[i][j][k]
    materias = respuestas.obtener_materias()

    resultado = "{:<12}".format('Codigo')
    for m in materias:  # encabezado
        resultado += f"{m.nombre_corto:^22}"
    resultado += '\n'
    for c in respuestas.obtener_codigos():
        resultado += f"{c:<3}"
        for j in range(len(materias)):
            suma = 0
            for k in range(respuestas.cant_dias):
                suma += respuestas.obtener_respuestas(c)[j][k]
            resultado += f"{suma:>22}"
        resultado += '\n'
    return resultado


# 5. cuantas horas estudio cada alumno cada semana
def total_horas_por_semana_por_codigo(respuestas: ResultadoRespuestas) -> str:
    cant_semanas = day_to_week(respuestas.cant_dias - 1) + 1  # el indice en el que cae el ultimo dia + 1
    resultado = "{:<7}".format('Codigo')
    for i in range(cant_semanas):  # encabezado
        resultado += "{:^8}".format(f"Sem {i + 1}")
    resultado += '\n'

    for c in respuestas.obtener_codigos():
        resultado += f"{c:<3}"
        semanas = [0] * cant_semanas  # lista de la cantidad de horas en cada semana para ese codigo
        for j in range(respuestas.obtener_cant_materias()):
            for k in range(respuestas.cant_dias):
                semanas[day_to_week(k)] += respuestas.obtener_respuestas(c)[j][k]  # suma en la semana correspondiente las horas
        for s in semanas:  # recorre la lisa de sumas y va escribiendo
            resultado += f"{s:>8}"
        resultado += '\n'
    return resultado


# 6. cuantas horas estudiaron cada materia todos los alumnos por semana
def total_horas_por_materia_por_semana(respuestas: ResultadoRespuestas) -> str:
    materias = respuestas.obtener_materias()

    resultado = "{:<11}".format('Semana')  # encabezado
    for m in materias:
        resultado += f"{m.nombre_corto:^22}"
    resultado += '\n'

    cant_semanas = day_to_week(respuestas.cant_dias - 1) + 1  # el indice en el que cae el ultimo dia + 1
    for s in range(cant_semanas):  # cada semana
        resultado += f"{s+1:>02}"
        for j in range(len(materias)):
            suma = 0
            for c in respuestas.obtener_codigos():
                for k in range(7):  # cada dia de la semana
                    dia = s * 7 + k
                    if dia >= respuestas.cant_dias:  # la ultima semana esta incompleta porque no esta el sabado ni el domingo
                        break
                    suma += respuestas.obtener_respuestas(c)[j][dia]
            resultado += f"{suma:>22}"
        resultado += '\n'
    return resultado

# 7. cuantos alumnos estudiaron cada materia cada semana
def total_codigos_por_materia_por_semana(respuestas: ResultadoRespuestas) -> str:
    materias = respuestas.obtener_materias()
    codigos = respuestas.obtener_codigos()

    resultado = "{:<11}".format('Semana')  # encabezado
    for m in materias:
        resultado += f"{m.nombre_corto:^22}"
    resultado += '\n'

    cant_semanas = day_to_week(respuestas.cant_dias - 1) + 1  # el indice en el que cae el ultimo dia + 1
    for s in range(cant_semanas):  # cada semana
        resultado += f"{s+1:>02}"
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
            resultado += f"{contador:>22}"
        resultado += '\n'
    return resultado

# 8. cuantos registros hubo por cada alumno
def registros_por_codigo(respuestas: ResultadoRespuestas) -> str:
    contador = respuestas.cant_respuestas_por_codigo

    resultado = "{:<10}{}".format('Codigo', 'Registros\n')
    for c in respuestas.obtener_codigos():
        resultado += f"{c:<10}{contador[c]:>5}\n"
    return resultado


# 9. cuantos registros hubo cada semana
def registros_por_semana(respuestas: ResultadoRespuestas) -> str:
    contador = respuestas.cant_respuestas_por_semana

    resultado = "{:<10}{}".format('Semana', 'Registros\n')
    for i in range(len(contador)):
        resultado += f"{i + 1:<10}{contador[i]:>6}\n"
    return resultado


# 10. cuantos alumnos respondieron en cada semana
def codigos_por_semana(respuestas: ResultadoRespuestas) -> str:
    resultado = "{:<10}{}".format('Semana', 'Estudiantes\n')
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
        resultado += f"{i + 1:<10}{semanas[i]:>6}\n"
    return resultado
