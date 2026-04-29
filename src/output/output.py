from src.utils import solicitar_nombre_y_ruta, crear_archivo, mostrar_ruta_archivo, obtener_parametro


class Output:
    def mostrar_output(self, contenido: str, args: dict, config: dict, auto: bool = False):
        pass

    def mostrar_multiples_output(self, contenido: list[str], args: dict, config: dict, nombre_default: str = "Resultados", auto: bool = False):
        pass


class OutputConsola(Output):
    def mostrar_output(self, contenido: str, args: dict, config: dict, auto: bool = False):
        print(contenido)

    def mostrar_multiples_output(self, contenido: list[str], args: dict, config: dict, nombre_default: str = "", auto: bool = False):
        for resultado in contenido:
            print(resultado)


class OutputArchivo(Output):
    def mostrar_output(self, contenido: str, args: dict, config: dict, auto: bool = False):
        nombre, ruta = solicitar_nombre_y_ruta(
            "Ingrese el nombre del archivo (con extension) donde se guardaran los datos: ",
            "Ingrese la ruta donde se guardara el archivo o presione enter para usar la ruta por defecto: ") if not auto else "", ""
        if ruta == "":
            ruta = obtener_parametro("ruta_resultados_default", args, config)
        file = crear_archivo(nombre, ruta)
        if file is not None:
            with file:
                file.write(contenido)
                mostrar_ruta_archivo(file)
        else:
            print("No se pudo crear el archivo para guardar los resultados.")

    def mostrar_multiples_output(self, contenido: list[str], args: dict, config: dict, nombre_default: str = "Resultados", auto: bool = False):
        ruta = input("Ingrese la ruta donde se guardaran los archivos o presione enter para usar la ruta por defecto: ") if not auto else ""
        if ruta == "":
            ruta = obtener_parametro("ruta_resultados_default", args, config)
        overwrite = auto or input("Ingrese 'S' para sobreescribir todos los archivos existentes u otro caracter para preguntar"
                          "por cada uno: ") == 'S'
        for i, resultado in enumerate(contenido):
            file = crear_archivo(f"{nombre_default}_{i+1}.txt", ruta, overwrite)
            if file is not None:
                with file:
                    file.write(resultado)
                    mostrar_ruta_archivo(file)
            else:
                print(f"No se pudo crear el archivo para guardar el resultado {i+1}.")