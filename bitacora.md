# Bitácora de trabajo — Proyecto 4: Muestra Inteligente

Universidad Nacional de Colombia — Sede Manizales  
Introducción a las Ciencias de la Computación  
Grupo: Sebastián Gutiérrez, Mateo Bernal, Thomas Ramírez

---

## Semana 1 — Selección y entendimiento del problema

**Decisión tomada:** Elegimos el Proyecto 4 (Muestra Inteligente) porque el problema de selección de muestra con cuotas se mapea directamente a backtracking: cada estudiante elegido es una decisión parcial, y las cuotas son restricciones naturales que guían el retroceso.

**Avances:**
- Lectura completa del enunciado del proyecto.
- Discusión sobre cómo modelar el problema: decidimos usar listas de diccionarios para representar estudiantes.
- Diseño del dataset sintético de 20 estudiantes con cuatro atributos (programa, semestre, ciudad, jornada).
- Distribución equilibrada del pool: 6 Computación, 5 Matemáticas, 5 Estadística, 4 Física.

**Dificultades:**
- Al principio no teníamos claro si las cuotas mínimas iban en `es_valido()` o en `puede_podar()`. Concluimos que los máximos van en `es_valido()` (se pueden verificar inmediatamente) y los mínimos van en `puede_podar()` (se verifican mirando al futuro).

---

## Semana 1 — Implementación del algoritmo base

**Avances:**
- Implementación de `obtener_conteos()` como función auxiliar para no repetir lógica de conteo en múltiples funciones.
- Implementación de `es_solucion_completa()`: verifica tamaño exacto + todos los mínimos.
- Implementación de `obtener_candidatos()` con índice creciente para evitar permutaciones duplicadas.
- Implementación de `es_valido()`: solo verifica `max_por_ciudad`.
- Primera versión de `puede_podar()` con condiciones 1–4 (sin poda global de ciudades aún).
- Primera versión de `backtracking()` funcional.

**Prueba del Conjunto 1:** Solución encontrada en 7 llamadas. ✅

---

## Semana 1 — Bug con el Conjunto 3

**Bug encontrado:** Al probar el Conjunto 3 (`max_por_ciudad=2`, `tamano=7`), el algoritmo tardaba **8,380 llamadas recursivas** en concluir que no había solución. El comportamiento esperado era detectarlo de inmediato.

**Análisis:** La versión inicial de `puede_podar()` verificaba si había suficientes candidatos válidos en general, pero no calculaba si la capacidad total de las ciudades era suficiente para cubrir el tamaño requerido.

**Solución:** Se añadió la **Condición 0** (poda global de ciudades):
```
capacidad = suma de (max_por_ciudad - estudiantes_actuales_en_ciudad)
            para todas las ciudades disponibles
si capacidad < faltantes → podar
```
Con esta poda, el Conjunto 3 se resuelve en **1 sola llamada**. ✅

---

## Semana 1 — Extensión: muestra más equilibrada

**Avance:** Se implementó la función `calcular_balance()` que mide qué tan bien la distribución por programa de la muestra refleja la del pool original. Al ejecutar `backtracking()` con `limite=None` sobre el Conjunto 1, se encontraron **10,734 muestras válidas**.

**Resultado:** La mejor muestra obtuvo un score de balance de **0.7667**, incluyendo los cuatro programas.

---

## Semana 1 — Generación de entregables

**Avances:**
- Generación de gráficas en `resultados/`: comparación de distribuciones y eficiencia del backtracking.
- Redacción de la presentación en Beamer con colores UNAL (verde `#006847`, amarillo `#FDD000`).
- Construcción del árbol de búsqueda del ejemplo manual con TikZ.
- Implementación de la demo interactiva en HTML/JavaScript (traducción del algoritmo Python al navegador).
- Redacción del informe con todas las secciones requeridas.

---

## Resumen de decisiones clave

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| Diccionarios para estudiantes | Listas con índices | Más legible y fácil de depurar |
| Índice creciente de candidatos | Conjunto de visitados | Evita duplicados sin memoria extra |
| Mínimos en `puede_podar()` | Mínimos en `es_valido()` | Los mínimos requieren ver candidatos futuros |
| Poda global de ciudades | Sin poda global | Sin ella, el Conjunto 3 tardaba 8,380 llamadas |
| `limite` como parámetro | Parar siempre en la primera | Permite buscar todas las soluciones para la extensión |

---

## Reparto de trabajo

| Integrante | Tareas realizadas |
|---|---|
| Sebastián Gutiérrez | Algoritmo backtracking, funciones de poda, depuración del bug del Conjunto 3 |
| Mateo Bernal | Dataset sintético, análisis de distribuciones, gráficas, extensión de muestra óptima |
| Thomas Ramírez | Presentación Beamer, informe escrito, demo web, organización del repositorio |
