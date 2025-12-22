from src.utils import date_to_int, day_to_week


class ResultadoRespuestas:
    def __init__(self, materias, fecha_inicio, fecha_fin):
        self.materias = materias
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.cant_dias = date_to_int(fecha_fin, fecha_inicio, fecha_fin) + 1
        self.codigos_ordenados = None
        self.respuestas = dict()
        self.cant_respuestas_por_codigo = dict()
        self.cant_respuestas_por_semana = [0] * (day_to_week(self.cant_dias - 1) + 1)

    def agregar_respuesta(self, codigo, fecha_index, horas):
        if fecha_index >= self.cant_dias:
            raise ValueError("El indice de fecha esta fuera de rango al agregar respuesta.")

        if codigo in self.respuestas:
            if len(horas) > len(self.respuestas[codigo]):
                raise ValueError("La cantidad de materias no coincide al agregar respuesta.")
            for i in range(len(horas)):
                self.respuestas[codigo][i][fecha_index] += horas[i]
            self.cant_respuestas_por_codigo[codigo] += 1
            self.cant_respuestas_por_semana[day_to_week(fecha_index)] += 1
        else:
            self.respuestas[codigo] = [[0 for _ in range(self.cant_dias)] for _ in range(len(self.materias))]
            self.cant_respuestas_por_codigo[codigo] = 1
            self.cant_respuestas_por_semana[day_to_week(fecha_index)] = 1
            self.codigos_ordenados = None  # se invalida el orden
            for i in range(len(horas)):
                self.respuestas[codigo][i][fecha_index] = horas[i]

    def obtener_respuestas(self, codigo):
        return self.respuestas.get(codigo, None)

    def obtener_codigos(self):
        if self.codigos_ordenados is None:
            # key de orden natural: divide la cadena en trozos de texto y números,
            # convierte los trozos numéricos a int para que 'B2'/'B02' < 'B10'
            def _natural_key(s):
                return [s[0], int(s[1:])]
            self.codigos_ordenados = sorted(self.respuestas.keys(), key=_natural_key)
        return self.codigos_ordenados

    def incluye_codigo(self, codigo):
        return codigo in self.respuestas

    def obtener_materias(self):
        return self.materias

    def obtener_cant_materias(self):
        return len(self.materias)

    def obtener_cant_dias(self):
        return self.cant_dias

    def __str__(self):
        return str(self.respuestas)