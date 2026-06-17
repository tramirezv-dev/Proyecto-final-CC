# GUÍA DEL PROYECTO — Qué es cada cosa y para qué sirve

**Proyecto 4: Muestra Inteligente**
Universidad Nacional de Colombia — Sede Manizales
Introducción a las Ciencias de la Computación · Prof. Carlos Manuel Orrego Franco

---

## 1. ¿CUÁL ES EL COLAB?

El archivo para Google Colab es:

```
notebook/proyecto.py
```

**Cómo usarlo en Colab:**
1. Entrar a https://colab.research.google.com
2. Crear un nuevo notebook (Archivo → Nuevo notebook)
3. Copiar el contenido de `notebook/proyecto.py` en celdas separadas
4. Cada bloque marcado con `# ── CELDA N` es una celda distinta en Colab
5. Ejecutar todo en orden: Entorno de ejecución → Ejecutar todo

No se instala nada extra: Colab ya tiene pandas y matplotlib incluidos.

---

## 2. QUÉ PEDÍA CADA ENTREGABLE — MAPA COMPLETO

| Entregable pedido | Archivo en el proyecto | Estado |
|---|---|---|
| Código ejecutable en Google Colab (celdas) | `notebook/proyecto.py` | Listo |
| Módulo de funciones reutilizables | `src/funciones.py` | Listo |
| Presentación Beamer para exponer | `presentacion/presentacion.tex` | Listo |
| Informe escrito completo | `informe/informe.tex` | Listo |
| Demo interactiva (opcional/extra) | `demo/index.html` | Listo |
| Gráfica comparación pool vs muestra | `resultados/comparacion_distribuciones.png` | Listo |
| Gráfica eficiencia del backtracking | `resultados/eficiencia_backtracking.png` | Listo |
| Bitácora de trabajo semanal | `bitacora.md` | Listo |

---

## 3. NOMBRES — ¿HAY QUE CAMBIAR ALGO?

Los nombres actuales son correctos y descriptivos. No se requiere renombrar nada.
El único punto a tener en cuenta es el Colab:

- El archivo `notebook/proyecto.py` **no es un `.ipynb`** — es un `.py` organizado por celdas.
- Para subirlo a Colab como notebook real, se puede hacer File → Upload notebook y seleccionar el `.py`, o copiar y pegar celda por celda.
- Si el profesor pide entregar un `.ipynb`, hay que ejecutar el `.py` en Colab y luego descargar como notebook (Archivo → Descargar → Descargar .ipynb).

---

## 4. QUÉ HIZO CADA INTEGRANTE

| Integrante | Archivos principales |
|---|---|
| Sebastián Gutiérrez | `src/funciones.py`, celdas 5–7 y 15 de `notebook/proyecto.py` |
| Mateo Bernal | Dataset (celda 2), análisis (celda 3), gráficas (celdas 13–14), extensión (celda 15) |
| Thomas Ramírez | `presentacion/presentacion.tex`, `informe/informe.tex`, `demo/index.html`, `README.md` |

---

## 5. LAS 16 CELDAS DEL COLAB — QUÉ HACE CADA UNA

| Celda | Título | Lo que hace |
|---|---|---|
| 1 | Importaciones | Carga pandas, matplotlib, configura el backend y crea la carpeta `resultados/` |
| 2 | Dataset | Define los 20 estudiantes sintéticos en la lista `POOL` |
| 3 | Exploración | Imprime la distribución del pool por programa, semestre, ciudad y jornada |
| 4 | Cuotas | Define los tres conjuntos de restricciones (C1 base, C2 diversidad, C3 imposible) |
| 5 | Funciones auxiliares | Define `obtener_conteos()` y `candidatos_validos()` |
| 6 | Núcleo backtracking | Define las 5 funciones: `es_solucion_completa`, `obtener_candidatos`, `es_valido`, `puede_podar`, `backtracking` |
| 7 | Reporte | Define `ejecutar_busqueda()` que corre el algoritmo y muestra resultados en pantalla |
| 8 | Ejemplo manual | Corre el algoritmo sobre 5 estudiantes para mostrar el árbol de búsqueda didáctico |
| 9 | Prueba C1 | Ejecuta el Conjunto 1 (Base) — resultado en 7 llamadas |
| 10 | Prueba C2 | Ejecuta el Conjunto 2 (Alta diversidad) — resultado en 7 llamadas |
| 11 | Prueba C3 | Ejecuta el Conjunto 3 (Sin solución) — detectado en 1 llamada |
| 12 | Tabla resumen | Compara las tres pruebas en una tabla de resultados |
| 13 | Gráfica distribución | Genera y guarda `comparacion_distribuciones.png` |
| 14 | Gráfica eficiencia | Genera y guarda `eficiencia_backtracking.png` |
| 15 | Extensión muestra óptima | Busca las 10,734 muestras válidas del C1 y elige la más equilibrada |
| 16 | Conclusiones | Imprime las 4 conclusiones del proyecto |

---

## 6. ARCHIVOS DE PRESENTACIÓN E INFORME

### `presentacion/presentacion.tex`
- Formato Beamer (LaTeX para diapositivas)
- Se compila en Overleaf: https://overleaf.com → Nuevo proyecto → Subir archivo
- Colores UNAL: verde `#006847` y amarillo `#FDD000`
- Incluye árbol de búsqueda dibujado con TikZ

### `informe/informe.tex`
- Informe académico completo en LaTeX (12pt, A4)
- Se compila en Overleaf igual que la presentación
- Tiene portada, tabla de contenidos, 8 secciones, árbol TikZ, código fuente, referencias bibliográficas y declaración de autoría

### `demo/index.html`
- Demo interactiva que corre en el navegador sin instalar nada
- Abrir directamente haciendo doble clic en el archivo
- El algoritmo backtracking está reimplementado en JavaScript, idéntico al Python

---

## 7. EVIDENCIAS VISUALES (CAPTURAS)

Las gráficas generadas por el código están en `resultados/`:

**Comparación Pool vs. Muestras:**
![Comparacion distribuciones](resultados/comparacion_distribuciones.png)

**Eficiencia del backtracking:**
![Eficiencia backtracking](resultados/eficiencia_backtracking.png)

---

## 8. RESULTADOS CLAVE (resumen para exponer)

| Conjunto | Llamadas recursivas | Ramas podadas | Solución |
|---|---|---|---|
| C1 — Base | 7 | 0 | Sí |
| C2 — Alta diversidad | 7 | 0 | Sí |
| C3 — Sin solución | **1** | **1** | **No** |

- Sin backtracking habría que evaluar C(20,6) = **38,760 combinaciones**.
- Con poda, los conjuntos C1 y C2 se resuelven en **7 llamadas**.
- El C3 (imposible) se detecta en **1 sola llamada** gracias a la poda global de ciudades.
- Extensión: se encontraron **10,734 muestras válidas** en C1; la mejor tiene score de balance **0.7667**.
