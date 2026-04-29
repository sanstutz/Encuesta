from src.utils import format_code


def parsear_materias(inputs: str, cant_materias: int):
    partes = inputs.split(',')
    if len(partes) == 0:
        print("No se ingresaron materias.")
        return None
    materias = []
    for p in partes:
        try:
            indice = int(p.strip()) - 1  # el primer indice es 0 pero se lista como 1
            if 0 <= indice < cant_materias:
                materias.append(indice)
            else:
                print(f"Indice fuera de rango: {p.strip()}")
                return None
        except ValueError:
            print(f"Entrada invalida, no es un numero: {p.strip()}")
            return None
    return materias


def parsear_codigos(inputs: str, codigos_disponibles: list):
    partes = inputs.split(',')
    codigos = []
    for p in partes:
        codigo = format_code(p)
        if codigo in codigos_disponibles:
            codigos.append(codigo)
        else:
            print(f"Código no encontrado: {p.strip()}")
            return None
    return codigos