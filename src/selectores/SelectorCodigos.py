from src.utils import format_code


class SelectorBase:
    def __init__(self):
        # self.codigos = list()
        pass

    """
    def seleccionar_codigo(self, codigo):
        self.codigos.append(codigo)
    """

    def incluido(self, codigo):
        raise NotImplementedError("Metodo incluido() no implementado en la clase base")

    def obtener_codigos_obligatorios(self):
        raise NotImplementedError("Metodo obtener_codigos_obligatorios() no implementado en la clase base")


class SelectorArchivoCodigos(SelectorBase):
    def __init__(self, archivo):
        super().__init__()
        selectores = list()
        for linea in archivo:
            linea = linea.strip()
            if linea == "" or linea[0] == "#":
                continue

            if linea == "*":
                selector = SelectorUniversal()
                selectores = [selector]
                break

            partes = linea.split("-")
            if len(partes) == 2:
                try:
                    selector = SelectorRangoCodigos(partes[0].strip(), partes[1].strip())
                    selectores.append(selector)
                except ValueError as e:
                    print("Error al crear selector de rango en la linea:", linea, '\n', e)
            elif len(partes) == 1:
                if linea[-1] == '*':
                    try:
                        selector = SelectorLetraCodigos(linea[0].strip())
                        selectores.append(selector)
                    except ValueError as e:
                        print("Error al crear selector de letra en la linea:", linea, '\n', e)
                else:
                    try:
                        selector = SelectorPuntualCodigos(linea.strip())
                        selectores.append(selector)
                    except ValueError as e:
                        print("Error al crear selector puntual en la linea:", linea, '\n', e)
            else:
                print("Linea con formato invalido:", linea)
        if len(selectores) == 0:
            raise ValueError("El archivo no contiene selectores validos")
        self.selectores = selectores

    def incluido(self, codigo):
        for selector in self.selectores:
            if selector.incluido(codigo):
                return True
        return False

    def obtener_codigos_obligatorios(self):
        codigos_obligatorios = set()
        for selector in self.selectores:
            codigos_obligatorios = codigos_obligatorios.union(selector.obtener_codigos_obligatorios())
        return codigos_obligatorios

    def __str__(self):
        return "Selectores:\n" + "\n".join([str(selector) for selector in self.selectores])


class SelectorUniversal(SelectorBase):
    def incluido(self, codigo):
        return True

    def obtener_codigos_obligatorios(self):
        return set()

    def __str__(self):
        return "*"


class SelectorPuntualCodigos(SelectorBase):
    def __init__(self, codigo):
        super().__init__()
        codigo = format_code(codigo)
        if codigo is None:
            raise ValueError("El codigo es invalido")
        self.codigo = codigo

    def incluido(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            return False
        return self.codigo == codigo

    def obtener_codigos_obligatorios(self):
        return {self.codigo}

    def __str__(self):
        return self.codigo


class SelectorRangoCodigos(SelectorBase):
    def __init__(self, cod1, cod2):
        super().__init__()
        cod1 = format_code(cod1)
        cod2 = format_code(cod2)
        if (cod1 is None) or (len(cod1) < 2) or (cod2 is None) or (len(cod2) < 2):
            raise ValueError("Los codigos no pueden ser nulos y deben tener una letra y un numero")

        if cod1[0] != cod2[0]:
            raise ValueError("Los codigos deben tener la misma letra inicial")
        self.letra = cod1[0]

        self.num1 = int(cod1[1:])
        self.num2 = int(cod2[1:])

    def incluido(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            return False
        if codigo[0] != self.letra:
            return False
        if str.isdigit(codigo[1:]):
            num = int(codigo[1:])
        else:
            return False
        return self.num1 <= num <= self.num2

    def obtener_codigos_obligatorios(self):
        codigos = set()
        for num in range(self.num1, self.num2 + 1):
            codigos.add(f"{self.letra}{num}")
        return codigos

    def __str__(self):
        return f"{self.letra}: {self.num1}-{self.num2}"


class SelectorLetraCodigos(SelectorBase):
    def __init__(self, letra):
        super().__init__()
        if (letra is None) or (len(letra) != 1) or (not letra.isalpha()):
            raise ValueError("La letra debe ser un caracter alfabetico")
        self.letra = letra.upper()

    def incluido(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            return False
        return codigo[0] == self.letra

    def obtener_codigos_obligatorios(self):
        return set()

    def __str__(self):
        return f"{self.letra}*"