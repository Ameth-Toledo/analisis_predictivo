# Diagnóstico y Modelos Predictivos de una Planta Solar Fotovoltaica

Proyecto de Minería de Datos — Universidad Politécnica de Chiapas.

Análisis completo (comprensión del problema, EDA, preparación de datos, aprendizaje
supervisado, aprendizaje no supervisado, forecasting y evaluación) sobre
`2107_electrical_data.csv`: 632,952 mediciones cada 5 minutos de los 24 inversores
de una planta solar fotovoltaica (noviembre 2017 – noviembre 2023).

## Contenido del repositorio

- `plan_mineria.ipynb` — notebook principal, ejecutado de punta a punta.
- `figuras/` — figuras generadas por el notebook (usadas también en el reporte).
- `reporte/` — código fuente LaTeX del reporte técnico (14 secciones + referencias).
- `reporte_electrico.pdf` — reporte técnico compilado.
- `generar_pdf_electrico.py` — script que genera el PDF con `fpdf2` (alternativa
  usada porque el entorno de desarrollo no tenía `pdflatex` instalado; si tienes
  una distribución LaTeX puedes compilar `reporte/main.tex` directamente, p. ej.
  en Overleaf).

## Reproducibilidad

1. Coloca el archivo `2107_electrical_data.csv` en la raíz de este repositorio
   (no se incluye aquí por su tamaño, ~400 MB).
2. Crea un entorno con: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`,
   `statsmodels`, `torch`, `fpdf2`.
3. Ejecuta `plan_mineria.ipynb` desde la raíz del repositorio.
4. (Opcional) Ejecuta `python generar_pdf_electrico.py` para regenerar el PDF.

## Resultados principales

| Línea de análisis | Métrica | Resultado |
|---|---|---|
| Supervisado (potencia AC total) | R² / RMSE | 0.9992 / 6.94 W (Regresión Lineal) |
| No supervisado (diagnóstico) | % registros anómalos | 1.99% (Isolation Forest) |
| Forecasting (energía semanal) | MAPE | 21.79% (Holt-Winters) |

Un hallazgo notable: la **Regresión Lineal superó a Random Forest y a un MLP**
(PyTorch) en la tarea supervisada — la potencia AC es aproximadamente el producto
de corriente y voltaje, una relación casi algebraica que un modelo lineal ya
aproxima muy bien. El detalle de esta interpretación está en `reporte/12_discusion.tex`.

El análisis no supervisado identificó a los **inversores 04 y 07** como un grupo
atípico (mayor tiempo fuera de línea, picos de potencia anómalos), consistente
tanto en el EDA como en el clustering.
