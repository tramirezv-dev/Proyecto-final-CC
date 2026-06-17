# Proyecto 4 — Muestra Inteligente

**Una Encuesta Pequeña pero Equilibrada**

Universidad Nacional de Colombia — Sede Manizales  
Introducción a las Ciencias de la Computación  
Profesor: Carlos Manuel Orrego Franco  
Exposición: 17 de junio de 2026

---

## Integrantes

| Nombre | Rol |
|--------|-----|
| Sebastián Gutiérrez | Algoritmo backtracking |
| Mateo Bernal | Dataset y análisis |
| Thomas Ramírez | Presentación e informe |

---

## El problema

Bienestar Universitario quiere realizar una encuesta piloto sobre hábitos de estudio pero no puede entrevistar a todos los estudiantes. Necesita elegir una **muestra pequeña y representativa** que no quede sesgada hacia un solo programa, semestre o ciudad.

El problema se modela con **backtracking**: la computadora construye la muestra paso a paso, aplica restricciones de cuota en cada paso, y retrocede cuando una selección viola una regla o hace imposible cumplir otra.

---

## Estructura del repositorio

```
muestra-inteligente/
├── README.md
├── notebook/
│   └── proyecto.py        ← código completo para Google Colab
├── src/
│   └── funciones.py       ← funciones de backtracking reutilizables
├── presentacion/
│   └── presentacion.tex   ← presentación Beamer para Overleaf
├── informe/               ← informe escrito (PDF)
└── resultados/            ← gráficas generadas
    ├── comparacion_distribuciones.png
    └── eficiencia_backtracking.png
```

---

## Cómo ejecutar en Google Colab

1. Abrir [Google Colab](https://colab.research.google.com)
2. Crear un nuevo notebook
3. Copiar el contenido de `notebook/proyecto.py` en celdas separadas (cada bloque `# ── CELDA N` es una celda)
4. Ejecutar en orden (Runtime → Run all)

**No se requiere instalar nada**: Colab ya incluye `pandas` y `matplotlib`.

---

## Modelamiento con backtracking

| Componente | Definición en este proyecto |
|-----------|----------------------------|
| **Solución parcial** | Lista de estudiantes ya seleccionados |
| **Candidatos** | Estudiantes del pool aún no seleccionados (hacia adelante en el índice) |
| **Restricciones** | Tamaño exacto, cuotas mínimas por programa, máximo por ciudad, mínimo jornada |
| **Solución completa** | Muestra del tamaño requerido que cumple TODOS los mínimos |
| **Retroceso** | Cuando agregar un estudiante excede una cuota máxima |
| **Poda** | Cuando los candidatos restantes no alcanzan para cubrir alguna cuota mínima |

---

## Dataset

20 estudiantes sintéticos con campos:
- `programa`: Computacion / Matematicas / Estadistica / Fisica
- `semestre`: 1 a 5
- `ciudad`: Manizales / Pereira / Armenia
- `jornada`: Diurna / Nocturna

---

## Tres conjuntos de cuotas probados

| Conjunto | Tamaño | Restricciones | Resultado |
|---------|--------|--------------|-----------|
| 1 — Base | 6 | ≥2 Comp, ≥1 Mat, ≤3/ciudad, ≥2 sem1 | Solución en 7 llamadas |
| 2 — Diversidad | 6 | ≥2 Comp, ≥1 Mat, ≥1 Est, ≤3/ciudad, ≥2 Noct | Solución en 7 llamadas |
| 3 — Sin solución | 7 | ≤2/ciudad (3 ciudades × 2 = 6 < 7) | Imposible: detectado en 1 llamada |

---

## Resultados destacados

- El Conjunto 3 demuestra que la **poda global** detecta imposibilidad antes de explorar ninguna rama.
- Extensión opcional: el backtracking encontró **10,734 muestras válidas** para el Conjunto 1.
- La mejor muestra equilibrada obtuvo un **score de balance de 0.7667** sobre 1.0.

---

## Ejemplo de entrada y salida

**Entrada (Conjunto 1):**
```python
CUOTAS_1 = {
    "tamano": 6,
    "min_programa": {"Computacion": 2, "Matematicas": 1},
    "max_por_ciudad": 3,
    "min_semestre_1": 2,
    "min_nocturna": 0,
}
```

**Salida:**
```
id  programa     semestre  ciudad     jornada
 1  Computacion  1         Manizales  Diurna
 2  Matematicas  1         Pereira    Diurna
 3  Estadistica  2         Armenia    Nocturna
 4  Computacion  2         Manizales  Diurna
 5  Matematicas  3         Pereira    Nocturna
 6  Estadistica  1         Armenia    Diurna

Llamadas recursivas: 7 | Ramas podadas: 0
```
