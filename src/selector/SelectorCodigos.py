from src.utils import format_code


class ValidadorCodigos:
    def es_valido(self, code):
        raise NotImplementedError()


class ValidadorArchivo(ValidadorCodigos):
    def __init__(self, archivo):
        self.validadores = list()

        for linea in archivo:
            linea = linea.strip()
            if linea == "" or linea[0] == "#":
                continue

            if linea == "*":
                validador = ValidadorUniversal()
                self.validadores = [validador]
                break

            partes = linea.split("-")
            if len(partes) == 2:
                try:
                    validador = ValidadorRango(partes[0].strip(), partes[1].strip())
                    self.validadores.append(validador)
                except ValueError as e:
                    print("Error al crear validador de rango en la linea:", linea, '\n', e)
            elif len(partes) == 1:
                if linea[-1] == '*':
                    try:
                        validador = ValidadorLetra(linea[0].strip())
                        self.validadores.append(validador)
                    except ValueError as e:
                        print("Error al crear validador de letra en la linea:", linea, '\n', e)
                else:
                    try:
                        validador = ValidadorPuntual(linea.strip())
                        self.validadores.append(validador)
                    except ValueError as e:
                        print("Error al crear validador puntual en la linea:", linea, '\n', e)
        if len(self.validadores) == 0:
            raise ValueError("El archivo no contiene validadores validos")

    def es_valido(self, codigo):
        for validador in self.validadores:
            if validador.es_valido(codigo):
                return True
        return False


class ValidadorPuntual(ValidadorCodigos):
    def __init__(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            raise ValueError("El codigo es invalido")
        self.codigo = codigo

    def es_valido(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            return False
        return codigo == self.codigo


class ValidadorRango(ValidadorCodigos):
    def __init__(self, cod1, cod2):
        cod1 = format_code(cod1)
        cod2 = format_code(cod2)
        if (cod1 is None) or (len(cod1) < 2) or (cod2 is None) or (len(cod2) < 2):
            raise ValueError("Los codigos no pueden ser nulos y deben tener una letra y un numero")

        if cod1[0] != cod2[0]:
            raise ValueError("Los codigos deben tener la misma letra inicial")
        self.letra = cod1[0]

        num1 = int(cod1[1:])
        num2 = int(cod2[1:])
        if num1 >= num2:
            raise ValueError("El primer codigo debe ser menor que el segundo")

        self.num1 = num1
        self.num2 = num2

    def es_valido(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            return False
        if codigo[0] != self.letra:
            return False
        try:
            num = int(codigo[1:])
        except ValueError:
            return False
        return self.num1 <= num <= self.num2


class ValidadorLetra(ValidadorCodigos):
    def __init__(self, letra):
        if (letra is None) or (len(letra) != 1) or (not letra.isalpha()):
            raise ValueError("La letra debe ser un caracter alfabetico")
        self.letra = letra.upper()

    def es_valido(self, codigo):
        codigo = format_code(codigo)
        if codigo is None:
            return False
        return codigo[0] == self.letra


class ValidadorUniversal(ValidadorCodigos):
    def es_valido(self, codigo):
        return True