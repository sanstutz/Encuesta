from src.respuestas.ResultadoRespuestas import ResultadoRespuestas
from src.utils import format_code, date_to_int, int_to_date


class LectorRespuestas:
    def __init__(self, selector_codigos, materias, fecha_inicio, fecha_fin):
        self.selector_codigos = selector_codigos
        self.materias = materias
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cant_dias = date_to_int(fecha_fin, fecha_inicio, fecha_fin) + 1

    def cargar_respuestas(self, ruta_respuestas, encoding="utf-8", separador=';', materias_offset=3):
        try:
            archivo = open(ruta_respuestas, 'rt', encoding=encoding)
        except PermissionError:  # los directorios tiran este error
            raise Exception(f"No se pudo abrir el archivo {ruta_respuestas} porque no hay permisos o es un directorio.")
        except FileNotFoundError:
            raise Exception(f"No se encontro el archivo {ruta_respuestas}.")
        except OSError:
            raise Exception(f"{ruta_respuestas} no es una ruta valida.")

        respuestas = ResultadoRespuestas(self.materias, self.fecha_inicio, self.fecha_fin)

        cant_materias = len(self.materias)

        # cargar codigos que deben estar presentes aunque no tengan respuestas
        codigos_obligatorios = self.selector_codigos.obtener_codigos_obligatorios()
        for codigo in codigos_obligatorios:
            respuestas.agregar_respuesta(codigo, 0, []) # respuesta vacia para que inicialice la matriz

        # cargar respuestas
        for linea in archivo:
            columnas = linea.split(separador)
            # estructura del registro: [emision, codigo, fecha, 110 materias, ...]
            codigo = columnas[1]
            if self.selector_codigos.incluido(codigo):
                fecha = date_to_int(columnas[2], self.fecha_inicio, self.fecha_fin)
                if fecha == -1:
                    continue  # fecha fuera de rango
                horas = [0 for _ in range(cant_materias)]
                for m in range(cant_materias):
                    materia = self.materias[m]
                    col = materia.columna + materias_offset
                    try:
                        if columnas[col].strip() == '':
                            continue # si no hay nada es 0
                        h = float(columnas[col].replace(',', '.'))
                        horas[m] += h
                    except (ValueError, IndexError) as e:
                        raise Exception(f"Error al procesar la columna {col} de una linea: {e}. "
                                        f"Linea que produjo el error:\n{linea}")
                respuestas.agregar_respuesta(format_code(codigo), fecha, horas)

        return respuestas


