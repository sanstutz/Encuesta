import json
from src.materia import Materia


def cargar_materias(archivo_lista_materias, archivo_incluidas):
    materias_data = json.load(archivo_lista_materias)
    materias = [Materia(m["columna"], m["nombre_corto"], m["nombre_sin_espacios"]) for m in materias_data]

    if len(materias) == 0:
        raise ValueError("El archivo de materias no contiene materias validas")

    materias_incluidas = list()
    for linea in archivo_incluidas:
        linea = linea.strip()
        if linea == "" or linea[0] == "#":
            continue

        if linea == "*":
            return materias  # Todas las materias incluidas

        partes = linea.split("-")
        if len(partes) == 2:
            try:
                inicio = int(partes[0].strip())
                fin = int(partes[1].strip())
                for materia in materias:
                    if inicio <= materia.columna <= fin:
                        materias_incluidas.append(materia)
                        break
            except ValueError as e:
                print("Error al procesar rango en la linea:", linea, '\n', e)
        elif len(partes) == 1:
            try:
                columna = int(linea.strip())
                for materia in materias:
                    if materia.columna == columna:
                        materias_incluidas.append(materia)
                        break
            except ValueError as e:
                print("Error al procesar columna en la linea:", linea, '\n', e)
        else:
            print("Linea con formato invalido:", linea)
    return materias_incluidas