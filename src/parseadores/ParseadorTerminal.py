from src.utils import format_code


def parsear_materias(inputs, cant_materias):
    partes = inputs.split(',')
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


def parsear_codigos(inputs, codigos_disponibles):
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