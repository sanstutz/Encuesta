import random
from datetime import datetime, timedelta

# Configuración
NUM_ALUMNOS = 200
LETRAS = ['A', 'B', 'C', 'D', 'E']
FECHA_INICIO = datetime(2024, 8, 12)
FECHA_FIN = datetime(2024, 11, 22)
NUM_COLUMNAS_MATERIAS = 110

# Observaciones posibles
OBSERVACIONES = [
    "Me dedico completamente al estudio",
    "Tengo otras ocupaciones demandantes",
    "",
]

OBSERVACIONES_EXTRA = [
    "Practico deporte federado",
    "Tengo personas a cargo",
    "Voy al gym",
    "Trabajo part-time",
    "",
]

HORAS_EXTRA = [
    "6-8 aprox",
    "42 horas",
    "12",
    "20 horas semanales",
    "",
]

# Definir grupos de materias por "carrera" (índices de columnas 0-109)
# Cada grupo simula una carrera/año diferente
GRUPOS_MATERIAS = {
    'A': {  # Grupo A: primeras materias (ej: primer año matemática)
        'base': list(range(0, 15)) + list(range(55, 70)),  # Teoría y práctica
        'variacion': 3,
    },
    'B': {  # Grupo B: materias de física
        'base': list(range(15, 30)) + list(range(70, 85)),
        'variacion': 3,
    },
    'C': {  # Grupo C: materias de computación
        'base': list(range(30, 45)) + list(range(85, 100)),
        'variacion': 3,
    },
    'D': {  # Grupo D: materias avanzadas
        'base': list(range(40, 55)) + list(range(95, 110)),
        'variacion': 3,
    },
    'E': {  # Grupo E: mezcla
        'base': list(range(5, 25)) + list(range(60, 80)),
        'variacion': 3,
    },
}

def generar_codigo(letra, numero):
    """Genera código como A01, B15, etc."""
    return f"{letra}{numero:02d}"

def obtener_materias_alumno(letra, numero):
    """Obtiene las materias que cursa un alumno basándose en su código."""
    grupo = GRUPOS_MATERIAS[letra]
    base = grupo['base']
    variacion = grupo['variacion']
    
    # Alumnos con números cercanos cursan materias similares
    # Usamos el número para hacer pequeñas variaciones
    random.seed(letra + str(numero // 5))  # Grupos de 5 alumnos similares
    
    # Seleccionar 5-10 materias del grupo base con pequeñas variaciones
    num_materias = random.randint(5, 10)
    materias = random.sample(base, min(num_materias, len(base)))
    
    # Añadir pequeña variación individual
    random.seed(letra + str(numero))
    for _ in range(variacion):
        if random.random() > 0.5:
            nueva = random.randint(0, NUM_COLUMNAS_MATERIAS - 1)
            if nueva not in materias:
                materias.append(nueva)
    
    return materias[:10]  # Máximo 10 materias

def generar_horas():
    """Genera horas de estudio aleatorias."""
    opciones = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6]
    pesos = [10, 20, 15, 25, 10, 10, 5, 3, 1, 1]  # Más probable 1-2 horas
    return random.choices(opciones, weights=pesos, k=1)[0]

def formatear_hora(hora):
    """Formatea la hora como string (con coma decimal)."""
    if hora == int(hora):
        return str(int(hora))
    return str(hora).replace('.', ',')

def generar_fechas_respuesta(fecha_inicio, fecha_fin, tasa_abandono=0.05):
    """Genera las fechas en las que un alumno responde."""
    fechas = []
    fecha_actual = fecha_inicio
    semana_actual = 0
    respondio_esta_semana = False
    abandono = random.random() < tasa_abandono
    fecha_abandono = fecha_inicio + timedelta(days=random.randint(30, 80)) if abandono else fecha_fin
    
    while fecha_actual <= min(fecha_fin, fecha_abandono):
        # Calcular semana
        dias_desde_inicio = (fecha_actual - fecha_inicio).days
        semana = dias_desde_inicio // 7
        
        if semana != semana_actual:
            semana_actual = semana
            respondio_esta_semana = False
        
        # Probabilidad de responder este día
        # Mayor probabilidad si no ha respondido esta semana
        prob = 0.3 if not respondio_esta_semana else 0.15
        
        if random.random() < prob:
            fechas.append(fecha_actual)
            respondio_esta_semana = True
        
        fecha_actual += timedelta(days=1)
    
    return fechas

def generar_timestamp(fecha):
    """Genera un timestamp realista (mismo día o días después)."""
    dias_despues = random.choices([0, 1, 2, 3], weights=[70, 20, 7, 3])[0]
    fecha_ts = fecha + timedelta(days=dias_despues)
    hora = random.randint(8, 23)
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    return f"{fecha_ts.day}/{fecha_ts.month}/{fecha_ts.year} {hora}:{minuto:02d}:{segundo:02d}"

def generar_fila(timestamp, codigo, fecha, materias_alumno):
    """Genera una fila completa del CSV."""
    fecha_str = f"{fecha.day}/{fecha.month}/{fecha.year}"
    
    # Inicializar columnas de materias vacías
    columnas_materias = [''] * NUM_COLUMNAS_MATERIAS
    
    # Llenar solo las materias que cursa el alumno
    # No siempre estudia todas sus materias cada día
    materias_hoy = random.sample(materias_alumno, random.randint(1, len(materias_alumno)))
    
    for materia in materias_hoy:
        columnas_materias[materia] = formatear_hora(generar_horas())
    
    # Observaciones
    obs1 = random.choice(OBSERVACIONES)
    obs2 = random.choice(OBSERVACIONES_EXTRA) if obs1 == "Tengo otras ocupaciones demandantes" else ""
    obs3 = random.choice(HORAS_EXTRA) if obs2 else ""
    
    # Construir fila
    fila = [timestamp, codigo, fecha_str] + columnas_materias + [obs1, obs2, obs3]
    
    return ';'.join(fila)

def main():
    random.seed(42)  # Para reproducibilidad
    
    # Generar alumnos: 40 por cada letra (A01-A40, B01-B40, etc.)
    alumnos = []
    for letra in LETRAS:
        for numero in range(1, 41):
            codigo = generar_codigo(letra, numero)
            materias = obtener_materias_alumno(letra, numero)
            alumnos.append((codigo, letra, numero, materias))
    
    # Generar todas las filas
    filas = []
    
    for codigo, letra, numero, materias in alumnos:
        fechas = generar_fechas_respuesta(FECHA_INICIO, FECHA_FIN)
        for fecha in fechas:
            timestamp = generar_timestamp(fecha)
            fila = generar_fila(timestamp, codigo, fecha, materias)
            filas.append((fecha, fila))
    
    # Ordenar por fecha (para que sea más realista)
    filas.sort(key=lambda x: x[0])
    
    # Si no llegamos a 5000, duplicar algunas respuestas con variaciones
    while len(filas) < 5000:
        # Agregar más respuestas aleatorias
        codigo, letra, numero, materias = random.choice(alumnos)
        fecha = FECHA_INICIO + timedelta(days=random.randint(0, (FECHA_FIN - FECHA_INICIO).days))
        timestamp = generar_timestamp(fecha)
        fila = generar_fila(timestamp, codigo, fecha, materias)
        filas.append((fecha, fila))
    
    # Reordenar
    filas.sort(key=lambda x: x[0])
    
    # Escribir archivo
    with open('Respuestas_test.csv', 'w', encoding='utf-8') as f:
        for _, fila in filas:
            f.write(fila + '\n')
    
    print(f"Archivo generado con {len(filas)} filas")
    
    # Estadísticas
    codigos_unicos = set()
    for _, fila in filas:
        partes = fila.split(';')
        codigos_unicos.add(partes[1])
    
    print(f"Alumnos únicos: {len(codigos_unicos)}")
    print(f"Códigos: {sorted(codigos_unicos)[:10]}... (primeros 10)")

if __name__ == "__main__":
    main()

