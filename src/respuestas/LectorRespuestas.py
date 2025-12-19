class LectorRespuestas:
    def __init__(self, selector_codigos, materias, fecha_inicio, fecha_fin):
        self.selector_codigos = selector_codigos
        self.materias = materias

    def cargar_respuestas(self, ruta_respuestas, encoding="utf-8"):
        try:
            archivo = open(ruta_respuestas, 'rt', encoding=encoding)
        except PermissionError:  # los directorios tiran este error
            print(f"Error: no se puede abrir el archivo {ruta_respuestas} porque no hay permisos o es un directorio.")
        except FileNotFoundError:
            print(f"No se encontro el archivo {ruta_respuestas}.")
        except OSError:
            print(f"{ruta_respuestas} no es una ruta valida.")



