class Materia:
    def __init__(self, columna, nombre_corto, nombre_sin_espacios):
        self.columna = columna
        self.nombre_corto = nombre_corto
        self.nombre_sin_espacios = nombre_sin_espacios

    def __eq__(self, other):
        if not isinstance(other, Materia):
            return NotImplemented
        return self.columna == other.columna

    def __hash__(self):
        return hash((self.columna, self.nombre_corto))

    def __repr__(self):
        return f"Materia(columna={self.columna!r}, nombre_corto={self.nombre_corto!r})"
