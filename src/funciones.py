"""
Módulo de backtracking — Proyecto 4: Muestra Inteligente
Universidad Nacional de Colombia — Sede Manizales
Introducción a las Ciencias de la Computación
"""

from collections import Counter


# ── Conteos auxiliares ────────────────────────────────────────────────────────

def obtener_conteos(muestra):
    """Devuelve conteos de la muestra actual por cada dimensión relevante."""
    por_programa = Counter(e["programa"] for e in muestra)
    por_ciudad   = Counter(e["ciudad"]   for e in muestra)
    por_jornada  = Counter(e["jornada"]  for e in muestra)
    semestre_1   = sum(1 for e in muestra if e["semestre"] == 1)
    return por_programa, por_ciudad, por_jornada, semestre_1


def candidatos_validos(pool_restante, muestra, cuotas):
    """
    Filtra pool_restante eliminando estudiantes que ya no pueden agregarse
    sin violar max_por_ciudad.  Esto es necesario para que la poda calcule
    correctamente cuántos candidatos reales quedan disponibles.
    """
    max_c = cuotas.get("max_por_ciudad", float("inf"))
    _, por_ciudad, _, _ = obtener_conteos(muestra)
    return [e for e in pool_restante
            if por_ciudad.get(e["ciudad"], 0) < max_c]


# ── Las cinco funciones base del backtracking ─────────────────────────────────

def es_solucion_completa(muestra, cuotas):
    """
    Condición de parada exitosa:
      - La muestra alcanzó el tamaño exacto requerido.
      - Se cumplen TODOS los mínimos (programa, semestre, jornada).
    """
    if len(muestra) != cuotas["tamano"]:
        return False

    por_prog, _, por_jornada, sem1 = obtener_conteos(muestra)

    for prog, minimo in cuotas["min_programa"].items():
        if por_prog.get(prog, 0) < minimo:
            return False

    if sem1 < cuotas["min_semestre_1"]:
        return False

    if por_jornada.get("Nocturna", 0) < cuotas["min_nocturna"]:
        return False

    return True


def obtener_candidatos(pool, inicio):
    """
    Candidatos: estudiantes del pool desde la posición 'inicio' en adelante.
    El índice creciente evita generar la misma muestra en distinto orden
    (elimina permutaciones duplicadas sin necesitar un conjunto de visitados).
    """
    return pool[inicio:]


def es_valido(muestra, candidato, cuotas):
    """
    Restricciones MAX — ¿agregar este candidato viola algún techo?
    Solo verifica max_por_ciudad porque es la única restricción de cota superior.
    Las restricciones mínimas se verifican en puede_podar y es_solucion_completa.
    """
    max_c = cuotas.get("max_por_ciudad", float("inf"))
    ya_en_ciudad = sum(1 for e in muestra if e["ciudad"] == candidato["ciudad"])
    return ya_en_ciudad < max_c


def puede_podar(muestra, pool_restante, cuotas):
    """
    Poda anticipada: retorna True si es IMPOSIBLE completar la muestra.

    Casos que activan la poda:
      0. Capacidad global de ciudades insuficiente (poda fuerte, detecta
         imposibilidades globales como C3 en la primera llamada).
      1. Los candidatos válidos restantes son menos que los que faltan.
      2. No hay suficientes candidatos de algún programa mínimo requerido.
      3. No hay suficientes candidatos de semestre 1 para cubrir el mínimo.
      4. No hay suficientes candidatos nocturnos para cubrir el mínimo.
    """
    faltantes = cuotas["tamano"] - len(muestra)
    _, por_ciudad, _, _ = obtener_conteos(muestra)

    # Condición 0: capacidad máxima de ciudades < estudiantes que aún faltan
    max_c = cuotas.get("max_por_ciudad", float("inf"))
    if max_c < float("inf"):
        todas_ciudades = set(e["ciudad"] for e in pool_restante) | set(por_ciudad)
        capacidad = sum(max(0, max_c - por_ciudad.get(c, 0)) for c in todas_ciudades)
        if capacidad < faltantes:
            return True

    efectivos = candidatos_validos(pool_restante, muestra, cuotas)

    if len(efectivos) < faltantes:
        return True

    por_prog, _, por_jornada, sem1 = obtener_conteos(muestra)

    for prog, minimo in cuotas["min_programa"].items():
        disp = sum(1 for e in efectivos if e["programa"] == prog)
        if por_prog.get(prog, 0) + disp < minimo:
            return True

    disp_sem1 = sum(1 for e in efectivos if e["semestre"] == 1)
    if sem1 + disp_sem1 < cuotas["min_semestre_1"]:
        return True

    disp_noct = sum(1 for e in efectivos if e["jornada"] == "Nocturna")
    if por_jornada.get("Nocturna", 0) + disp_noct < cuotas["min_nocturna"]:
        return True

    return False


def backtracking(pool, muestra, cuotas, soluciones, contadores, inicio=0, limite=1):
    """
    Algoritmo principal de backtracking para selección de muestra representativa.

    Parámetros
    ----------
    pool        : lista completa de estudiantes ordenada por id
    muestra     : solución parcial actual (se modifica in-place)
    cuotas      : dict con las restricciones del conjunto de cuotas
    soluciones  : lista acumuladora de muestras válidas encontradas
    contadores  : dict {'llamadas': int, 'podas': int}
    inicio      : índice mínimo en pool para el siguiente candidato
    limite      : máximo de soluciones a encontrar (None = todas)
    """
    contadores["llamadas"] += 1

    if es_solucion_completa(muestra, cuotas):
        soluciones.append(list(muestra))
        return

    if limite is not None and len(soluciones) >= limite:
        return

    pool_restante = obtener_candidatos(pool, inicio)

    if puede_podar(muestra, pool_restante, cuotas):
        contadores["podas"] += 1
        return

    if len(muestra) >= cuotas["tamano"]:
        return

    for i, candidato in enumerate(pool_restante):
        if limite is not None and len(soluciones) >= limite:
            return

        if es_valido(muestra, candidato, cuotas):
            muestra.append(candidato)                            # ELEGIR
            backtracking(pool, muestra, cuotas, soluciones,
                         contadores, inicio + i + 1, limite)
            muestra.pop()                                        # RETROCEDER
        else:
            contadores["podas"] += 1
