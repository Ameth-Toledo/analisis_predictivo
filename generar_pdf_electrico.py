"""
Genera reporte_electrico.pdf usando fpdf2 (fallback sin LaTeX/pdflatex disponible).
Ejecutar desde la raíz de este repositorio.
El contenido replica reporte/*.tex (Diagnóstico y Modelos Predictivos de una
Planta Solar Fotovoltaica) para producir un PDF entregable reproducible.
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

AZUL   = (0,  74, 128)
GRIS   = (80, 80, 80)
NEGRO  = (20, 20, 20)
BLANCO = (255, 255, 255)
FONDO  = (245, 248, 252)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FIG_DIR = "figuras/"


class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_font("DV",  "",  FONT_DIR + "DejaVuSans.ttf")
        self.add_font("DV",  "B", FONT_DIR + "DejaVuSans-Bold.ttf")
        self.add_font("DV",  "I", FONT_DIR + "DejaVuSans-Oblique.ttf")
        self.add_font("DVMono", "", FONT_DIR + "DejaVuSansMono.ttf")
        mono_bold = FONT_DIR + "DejaVuSansMono-Bold.ttf"
        self.add_font("DVMono", "B", mono_bold if os.path.exists(mono_bold) else FONT_DIR + "DejaVuSansMono.ttf")

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DV", "I", 8)
        self.set_text_color(*GRIS)
        self.cell(0, 6, "Mineria de Datos  |  Planta Solar Fotovoltaica - 2107_electrical_data", align="L")
        self.cell(0, 6, f"Pagina {self.page_no()}", align="R",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*AZUL)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("DV", "I", 7)
        self.set_text_color(*GRIS)
        self.cell(0, 5, "Universidad Politecnica de Chiapas - Julio 2026", align="C")

    def titulo_seccion(self, n, titulo):
        self.ln(4)
        self.set_fill_color(*FONDO)
        self.set_draw_color(*AZUL)
        self.set_font("DV", "B", 13)
        self.set_text_color(*AZUL)
        prefijo = f"  {n}.  " if n != "" else "  "
        self.cell(0, 8, f"{prefijo}{titulo}", fill=True, border="L",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        self.set_text_color(*NEGRO)

    def titulo_sub(self, titulo):
        self.ln(2)
        self.set_font("DV", "B", 11)
        self.set_text_color(*AZUL)
        self.multi_cell(0, 6, titulo)
        self.ln(1)
        self.set_text_color(*NEGRO)

    def parrafo(self, txt):
        self.set_font("DV", "", 10)
        self.set_text_color(*NEGRO)
        self.multi_cell(0, 5.5, txt)
        self.ln(1)

    def bullet(self, txt, bold_prefix=""):
        usable = self.w - self.l_margin - self.r_margin
        indent = 8
        bullet_w = 5
        text_w = usable - indent - bullet_w
        self.set_font("DV", "", 10)
        self.set_x(self.l_margin + indent)
        self.cell(bullet_w, 5.5, "-")
        if bold_prefix:
            self.set_font("DV", "B", 10)
            self.multi_cell(text_w, 5.5, bold_prefix + " " + txt,
                            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        else:
            self.set_font("DV", "", 10)
            self.multi_cell(text_w, 5.5, txt,
                            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(0.5)

    def codigo(self, lines):
        self.set_font("DVMono", "", 8.5)
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.set_text_color(30, 30, 30)
        margin_extra = 3
        x0 = self.l_margin + margin_extra
        w = self.w - self.l_margin - self.r_margin - margin_extra * 2
        self.rect(x0, self.get_y(), w, len(lines) * 5.2 + 3, style="DF")
        y0 = self.get_y() + 1.5
        for i, ln in enumerate(lines):
            self.set_xy(x0 + 2, y0 + i * 5.2)
            self.cell(w - 2, 5.2, ln)
        self.set_y(y0 + len(lines) * 5.2 + 2)
        self.set_text_color(*NEGRO)
        self.ln(2)

    def figura(self, path, caption, w_pct=0.88):
        full_path = os.path.join(FIG_DIR, path)
        if not os.path.exists(full_path):
            self.parrafo(f"[Figura no encontrada: {full_path}]")
            return
        img_w = (self.w - self.l_margin - self.r_margin) * w_pct
        img_x = self.l_margin + (self.w - self.l_margin - self.r_margin) * (1 - w_pct) / 2
        self.image(full_path, x=img_x, w=img_w)
        self.set_font("DV", "I", 8.5)
        self.set_text_color(*GRIS)
        self.multi_cell(0, 4.5, caption, align="C")
        self.set_text_color(*NEGRO)
        self.ln(3)

    def tabla_header(self, cols, widths):
        self.set_fill_color(*AZUL)
        self.set_text_color(*BLANCO)
        self.set_font("DV", "B", 9)
        for c, w in zip(cols, widths):
            self.cell(w, 7, c, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*NEGRO)

    def tabla_fila(self, vals, widths, aligns, alt=False):
        self.set_font("DV", "", 9)
        self.set_fill_color(235, 242, 250) if alt else self.set_fill_color(*BLANCO)
        for v, w, a in zip(vals, widths, aligns):
            self.cell(w, 6.5, str(v), border=1, fill=True, align=a)
        self.ln()


# ════════════════════════════════════════════════════════════════════════════
pdf = PDF(orientation="P", unit="mm", format="A4")
pdf.set_margins(left=20, top=20, right=15)
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# ── PORTADA ──────────────────────────────────────────────────────────────────
pdf.set_fill_color(*AZUL)
pdf.rect(0, 0, 210, 60, style="F")
pdf.set_font("DV", "B", 22)
pdf.set_text_color(*BLANCO)
pdf.set_y(15)
pdf.cell(0, 10, "Diagnostico y Modelos Predictivos de", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0, 10, "una Planta Solar Fotovoltaica", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("DV", "", 12)
pdf.cell(0, 8, "Analisis de Senales Electricas de 24 Inversores (2017-2023)", align="C",
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_text_color(*NEGRO)
pdf.set_y(80)

pdf.set_fill_color(*FONDO)
pdf.set_draw_color(*AZUL)
pdf.set_font("DV", "", 11)
meta = [
    ("Alumno:",  "Ameth de Jesus Mendez Toledo"),
    ("Matricula:", "233363"),
    ("Institucion:", "Universidad Politecnica de Chiapas"),
    ("Curso:",   "Mineria de Datos"),
    ("Fecha:",   "Julio 2026"),
    ("Dataset:", "2107_electrical_data.csv"),
]
for lbl, val in meta:
    pdf.set_x(40)
    pdf.set_font("DV", "B", 11)
    pdf.cell(35, 8, lbl)
    pdf.set_font("DV", "", 11)
    pdf.cell(0, 8, val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

# ── RESUMEN ──────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion("", "Resumen")
pdf.parrafo(
    "Este documento presenta un proceso completo de mineria de datos -comprension, "
    "exploracion, preparacion, modelado y evaluacion- sobre 2107_electrical_data.csv, "
    "un dataset de 632,952 registros (5 minutos de resolucion, ~6 anios) con las "
    "senales electricas de los 24 inversores de una planta solar fotovoltaica."
)
pdf.parrafo(
    "Tras identificar y corregir problemas de calidad (nulos por inversores fuera de "
    "linea, una asimetria estructural entre inversores y un error tipografico en un "
    "nombre de columna), se desarrollaron tres lineas de analisis complementarias: "
    "(1) un modelo supervisado que predice la potencia AC total de la planta a partir "
    "de sus senales de entrada, comparando Regresion Lineal, Random Forest y un "
    "Perceptron Multicapa (MLP) entrenado con PyTorch; (2) un analisis no supervisado "
    "que segmenta los 24 inversores por perfil de desempenio (K-Means sobre "
    "componentes de PCA) y detecta registros anomalos (Isolation Forest); y (3) un "
    "modelo de forecasting (Holt-Winters) que pronostica la energia semanal generada, "
    "aprovechando la estacionalidad anual del recurso solar."
)
pdf.parrafo(
    "El mejor modelo supervisado (Regresion Lineal) alcanzo un R2 de 0.9992 en el "
    "conjunto de prueba, y el modelo de forecasting supero al baseline ingenuo "
    "estacional con un MAPE de 21.79%. El periodo analizado abarca de noviembre de "
    "2017 a noviembre de 2023."
)

# ── 1. INTRODUCCION ──────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(1, "Introduccion")
pdf.parrafo(
    "Una planta solar fotovoltaica genera, a traves de sus inversores, un volumen "
    "continuo de mediciones electricas (corriente y voltaje DC de entrada, corriente, "
    "voltaje y potencia AC de salida) que reflejan tanto las condiciones ambientales "
    "(irradiancia solar) como el estado operativo del equipo. En este trabajo se "
    "analiza el dataset 2107_electrical_data.csv, que contiene mediciones cada 5 "
    "minutos de los 24 inversores de una planta solar durante aproximadamente 6 anios "
    "(noviembre de 2017 a noviembre de 2023). No se proporciono un problema especifico "
    "a resolver: el conjunto fue explorado para identificar oportunidades de analisis, "
    "resultando en tres lineas de trabajo (supervisado, no supervisado y forecasting)."
)

pdf.titulo_sub("Planteamiento del problema")
pdf.parrafo(
    "El dataset no incluye variables meteorologicas externas (irradiancia, "
    "temperatura ambiente), por lo que toda la informacion disponible para "
    "diagnostico y prediccion proviene unicamente de las senales electricas internas "
    "de la planta. Esto plantea tres preguntas concretas:"
)
for q in [
    "Es posible predecir la potencia AC total de la planta a partir de las senales "
    "de entrada de los inversores? (aprendizaje supervisado)",
    "Existen inversores con un perfil de desempenio distinto al resto de la flota, o "
    "intervalos anomalos que sugieran una falla o degradacion? (aprendizaje no "
    "supervisado / diagnostico)",
    "Puede anticiparse la energia que producira la planta en las proximas semanas a "
    "partir de su historial? (forecasting)",
]:
    pdf.bullet(q)

pdf.titulo_sub("Objetivo general")
pdf.parrafo(
    "Aplicar un proceso completo de ciencia de datos sobre el dataset electrico de la "
    "planta solar, para diagnosticar el comportamiento de sus variables y generar "
    "modelos predictivos que apoyen la toma de decisiones."
)

pdf.titulo_sub("Metodologia utilizada")
for b in [
    ("Carga y exploracion:", "pandas, revision de tipos, nulos, duplicados y rango temporal."),
    ("Preparacion:", "imputacion justificada de nulos, correccion de error tipografico, "
     "variables derivadas y escalamiento (StandardScaler)."),
    ("Aprendizaje supervisado:", "Regresion Lineal, Random Forest y MLP (PyTorch, "
     "optimizador Adam, perdida MSE)."),
    ("Aprendizaje no supervisado:", "perfilado de inversores, PCA, K-Means e "
     "Isolation Forest."),
    ("Forecasting:", "descomposicion estacional y Holt-Winters sobre la serie semanal "
     "de energia, contra un baseline ingenuo estacional."),
]:
    pdf.bullet(b[1], bold_prefix=b[0])

# ── 2. DESCRIPCION DEL DATASET ───────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(2, "Descripcion del Dataset")
pdf.parrafo(
    "El archivo 2107_electrical_data.csv contiene mediciones electricas cada 5 "
    "minutos de los 24 inversores de una planta solar fotovoltaica."
)

cols = ["Caracteristica", "Valor"]
widths = [55, 105]
aligns = ["L", "L"]
rows = [
    ("Registros", "632,952"),
    ("Columnas", "120 (119 numericas + 1 marca de tiempo)"),
    ("Periodo", "2017-11-01 a 2023-11-07 (~6 anios)"),
    ("Frecuencia de muestreo", "5 minutos"),
    ("Filas duplicadas", "0"),
]
pdf.tabla_header(cols, widths)
for i, row in enumerate(rows):
    pdf.tabla_fila(row, widths, aligns, alt=(i % 2 == 0))
pdf.ln(3)

pdf.titulo_sub("Estructura de columnas")
pdf.parrafo(
    "Cada uno de los 24 inversores aporta hasta 5 senales: corriente DC (24 "
    "columnas), voltaje DC (23, el inversor 05 no tiene esta columna), corriente AC "
    "(24), voltaje AC (24) y potencia AC (24)."
)

pdf.titulo_sub("Problemas de calidad detectados")
for b in [
    ("Valores nulos:", "183,372 celdas nulas (0.24% del total), en 114 de 119 "
     "columnas numericas. Corresponden a intervalos en que un inversor especifico "
     "estuvo fuera de linea (entre 366 y 1,728 registros faltantes por equipo)."),
    ("Asimetria estructural:", "el inversor 05 carece de la columna de voltaje DC "
     "presente en los otros 23 inversores."),
    ("Error tipografico:", "la columna de potencia AC del inversor 15 se llama "
     "inv_15_ac_power_iinv_149653 (nota 'iinv' en vez de 'inv')."),
]:
    pdf.bullet(b[1], bold_prefix=b[0])

# ── 3. PREPARACION DE DATOS ──────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(3, "Limpieza y Preparacion de Datos")
pdf.codigo([
    "df = df.rename(columns={",
    "    'inv_15_ac_power_iinv_149653': 'inv_15_ac_power_inv_149653'",
    "})",
    "df[feature_cols] = df[feature_cols].fillna(0)",
    "power_cols = [c for c in df.columns if 'ac_power' in c]",
    "df['total_ac_power'] = df[power_cols].sum(axis=1, min_count=1)",
    "df['hour']  = df['measured_on'].dt.hour",
    "df['month'] = df['measured_on'].dt.month",
])
for b in [
    ("Correccion de nombre de columna:", "se corrigio el typo para que la columna "
     "siga el mismo patron y pueda incluirse en operaciones agregadas."),
    ("Imputacion de nulos con 0:", "un nulo corresponde a un inversor fuera de linea "
     "(sin comunicacion); imputar con la media simularia generacion inexistente."),
    ("Variables derivadas:", "total_ac_power (suma de las 24 potencias), hour, "
     "month, year."),
    ("Filtro de horas sin generacion:", "solo para el modelo supervisado, se "
     "excluyen las horas nocturnas (todas las senales son 0 por definicion fisica), "
     "reduciendo el conjunto de 632,952 a 309,308 filas (48.9%)."),
    ("Escalamiento:", "StandardScaler en variables de entrada y objetivo antes de "
     "entrenar el MLP y la Regresion Lineal."),
]:
    pdf.bullet(b[1], bold_prefix=b[0])

# ── 4. ANALISIS DESCRIPTIVO (EDA) ────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(4, "Analisis Descriptivo (EDA)")

cols2 = ["Estadistico", "total_ac_power (W)"]
widths2 = [60, 100]
aligns2 = ["L", "R"]
rows2 = [
    ("count", "632,952"), ("media", "156.32"), ("desv. estandar", "230.96"),
    ("minimo", "0.00"), ("percentil 25", "0.00"), ("mediana", "0.00"),
    ("percentil 75", "291.60"), ("maximo", "721.61"),
]
pdf.tabla_header(cols2, widths2)
for i, row in enumerate(rows2):
    pdf.tabla_fila(row, widths2, aligns2, alt=(i % 2 == 0))
pdf.ln(3)
pdf.parrafo(
    "La mediana de total_ac_power es 0: mas de la mitad de los registros "
    "corresponden a horas sin generacion (nocturnas o inversores fuera de linea). "
    "El % de lecturas en cero por inversor varia entre 52.5% y 59.2%."
)

pdf.figura("fig_distribuciones.png",
           "Distribuciones de potencia AC total, corriente DC y voltaje AC.")
pdf.figura("fig_boxplot_inversores.png",
           "Distribucion de potencia AC por inversor (horas con generacion > 0).")
pdf.parrafo(
    "La mediana de potencia por inversor oscila entre 8.9 W (inversor 07) y 13.9 W "
    "(inversor 20). Los inversores 04 y 07 destacan por su mediana baja y por "
    "valores maximos anomalos (~104-105 W frente a ~30 W del resto de la flota)."
)

pdf.add_page()
pdf.figura("fig_perfiles_temporales.png",
           "Perfil diurno (izq.) y mensual (der.) de la potencia AC total.")
pdf.figura("fig_serie_diaria.png",
           "Potencia AC total de la planta - promedio diario, 2017-2023.")

# ── 5. RELACIONES ENTRE VARIABLES ────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(5, "Relaciones entre Variables")
pdf.figura("fig_correlacion_agregada.png",
           "Correlacion de Spearman entre variables agregadas de planta.", w_pct=0.65)

cols3 = ["Par de variables", "Spearman rho"]
widths3 = [110, 50]
aligns3 = ["L", "R"]
rows3 = [
    ("total_dc_current -- total_ac_power", "0.987"),
    ("total_ac_current -- total_ac_power", "0.984"),
    ("avg_ac_voltage -- total_ac_power", "0.890"),
    ("hour -- total_ac_power", "0.111"),
]
pdf.tabla_header(cols3, widths3)
for i, row in enumerate(rows3):
    pdf.tabla_fila(row, widths3, aligns3, alt=(i % 2 == 0))
pdf.ln(3)
pdf.parrafo(
    "Las corrientes DC y AC correlacionan casi perfectamente con la potencia total "
    "(rho > 0.98), consistente con P = V x I. Llama la atencion que la correlacion "
    "entre hour y total_ac_power es baja (0.111) pese al patron diurno evidente: "
    "esto no indica ausencia de relacion, sino una limitacion del coeficiente de "
    "Spearman, que solo capta relaciones monotonas -la potencia sube y luego baja a "
    "lo largo del dia, una relacion de campana, no monotona."
)

# ── 6. APRENDIZAJE SUPERVISADO ───────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(6, "Aprendizaje Supervisado")

pdf.titulo_sub("Definicion del problema predictivo")
pdf.parrafo(
    "Variable objetivo: total_ac_power (potencia AC total de la planta), continua "
    "=> problema de regresion. Variables de entrada (98): corriente DC (24), "
    "voltaje DC (23), corriente AC (24) y voltaje AC (24) por inversor, mas hour, "
    "month y year. Conjunto de datos: 309,308 registros con generacion > 0, "
    "particionados 70/15/15 en entrenamiento/validacion/prueba."
)

pdf.titulo_sub("Seleccion de modelos")
for b in [
    ("Regresion Lineal:", "baseline interpretable."),
    ("Random Forest Regressor:", "150 arboles, profundidad maxima 14."),
    ("MLP (PyTorch):", "256->128->64->1, ReLU, Dropout; optimizador Adam, "
     "perdida MSE, salida lineal (sin Softmax, reservado para clasificacion)."),
]:
    pdf.bullet(b[1], bold_prefix=b[0])

pdf.titulo_sub("Entrenamiento")
pdf.parrafo(
    "El MLP se entreno hasta 60 epocas con early stopping (paciencia 10), "
    "gradient clipping (norma maxima 1.0), scheduler ReduceLROnPlateau, y "
    "restauracion de los pesos de la epoca con menor error de validacion (no la "
    "ultima). El entrenamiento se detuvo por early stopping en la epoca 16."
)
pdf.figura("fig_curva_aprendizaje.png",
           "Curva de aprendizaje del MLP - MSE de entrenamiento y validacion.", w_pct=0.7)
pdf.parrafo(
    "La curva evidencia una perdida de validacion inestable y con picos de gran "
    "magnitud respecto a la de entrenamiento, sintoma de sensibilidad del MLP a "
    "valores extremos aislados (ver picos anomalos de potencia en los inversores 04 "
    "y 07, Seccion 7). La restauracion de la mejor epoca mitiga, pero no elimina, "
    "este efecto."
)

pdf.add_page()
pdf.titulo_sub("Evaluacion y comparacion de modelos")
cols4 = ["Modelo", "RMSE (W)", "MAE (W)", "R2"]
widths4 = [55, 35, 35, 35]
aligns4 = ["L", "R", "R", "R"]
rows4 = [
    ("Regresion Lineal", "6.94", "5.10", "0.9992"),
    ("Random Forest", "8.16", "4.86", "0.9988"),
    ("MLP (PyTorch)", "51.33", "44.52", "0.9536"),
]
pdf.tabla_header(cols4, widths4)
for i, row in enumerate(rows4):
    pdf.tabla_fila(row, widths4, aligns4, alt=(i % 2 == 0))
pdf.ln(3)
pdf.figura("fig_comparacion_modelos.png",
           "Potencia real vs. predicha en el conjunto de prueba, tres modelos.")
pdf.parrafo(
    "Modelo seleccionado: Regresion Lineal, por presentar el menor RMSE (6.94 W) y "
    "el mayor R2 (0.9992), superando a Random Forest (RMSE 8.16 W) y al MLP (RMSE "
    "51.33 W). Este resultado, a primera vista contraintuitivo (el modelo mas "
    "simple supero a los dos mas complejos), se explica en la Seccion de Discusion: "
    "la potencia AC de cada inversor es aproximadamente el producto de su corriente "
    "y voltaje, una relacion que 98 variables lineales ya aproximan muy bien, "
    "dejando poco margen a modelos no lineales y exponiendolos a mayor varianza."
)

pdf.figura("fig_importancia_variables.png",
           "Top 15 variables por Permutation Importance sobre Random Forest.", w_pct=0.75)
pdf.parrafo(
    "La variable mas importante por un margen amplio es inv_11_dc_current, seguida "
    "de inv_20_dc_current; el resto del top 15 esta dominado por corrientes AC de "
    "distintos inversores. Ninguna variable de voltaje aparece entre las 15 mas "
    "relevantes: la corriente, proporcional a la irradiancia solar instantanea, es "
    "el factor que realmente explica las variaciones de potencia."
)

# ── 7. APRENDIZAJE NO SUPERVISADO ─────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(7, "Aprendizaje No Supervisado y Diagnostico")
pdf.parrafo(
    "A diferencia de la Seccion 6, aqui no se predice un valor conocido: el "
    "objetivo es descubrir estructura -grupos de inversores con desempenio similar "
    "y registros que se desvian del comportamiento esperado- sin usar etiquetas."
)

pdf.titulo_sub("Perfilado de inversores y clustering")
pdf.parrafo(
    "Para cada uno de los 24 inversores se construyo un perfil (energia total, "
    "potencia media y maxima, desviacion estandar, % de tiempo en cero durante "
    "horas de luz). Los perfiles se estandarizaron, se proyectaron a 2 componentes "
    "principales (90.0% de varianza explicada) y se agruparon con K-Means (k=3)."
)
pdf.figura("fig_clustering_inversores.png",
           "Clustering de los 24 inversores por perfil de desempenio (PCA 2D).", w_pct=0.7)

cols5 = ["Cluster", "Inversores", "Perfil"]
widths5 = [22, 68, 70]
aligns5 = ["C", "L", "L"]
rows5 = [
    ("0 (n=14)", "08,09,10,11,12,13,14,15,17,18,20,22,23,24", "Mayor energia, menor % en cero"),
    ("1 (n=8)", "01,02,03,05,06,16,19,21", "Energia y % en cero intermedios"),
    ("2 (n=2)", "04, 07", "Atipico: menor energia, mas tiempo en cero, picos anomalos"),
]
pdf.tabla_header(cols5, widths5)
for i, row in enumerate(rows5):
    pdf.tabla_fila(row, widths5, aligns5, alt=(i % 2 == 0))
pdf.ln(3)
pdf.parrafo(
    "El cluster 2 (inversores 04 y 07) se separa claramente: son los dos con mayor "
    "% de tiempo en cero durante horas de luz (36.5% y 39.2%, los mas altos de toda "
    "la flota) y los unicos cuya potencia maxima (~104-105 W) casi cuadruplica el "
    "maximo tipico (~30 W) del resto. Esta coincidencia -senalada tanto por el "
    "boxplot comparativo como por el clustering no supervisado- es evidencia "
    "consistente de que los inversores 04 y 07 son candidatos prioritarios a "
    "revision de mantenimiento."
)

pdf.add_page()
pdf.titulo_sub("Deteccion de anomalias a nivel de registro")
pdf.parrafo(
    "Se aplico Isolation Forest sobre la relacion hora del dia -- potencia AC "
    "total, con contaminacion esperada de 2%, para senalar intervalos de 5 minutos "
    "cuyo comportamiento se aparta de la envolvente diurna tipica."
)
pdf.figura("fig_anomalias.png",
           "Registros anomalos (rojo) respecto al patron diurno esperado.", w_pct=0.75)
pdf.parrafo(
    "Se marcaron 8,405 registros como anomalos (1.99% del total de horas con luz, "
    "consistente con la tasa de contaminacion configurada). Este analisis "
    "complementa al modelo supervisado: mientras este predice cuanta potencia se "
    "genera, el analisis no supervisado identifica que inversores o intervalos "
    "requieren atencion, sin necesidad de historial de fallas etiquetado."
)

# ── 8. FORECASTING ────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(8, "Forecasting - Series de Tiempo")
pdf.parrafo(
    "Se busca pronosticar la energia semanal generada por la planta. La serie de "
    "5 minutos se agrego a frecuencia semanal (suma de total_ac_power), "
    "produciendo una serie de 313 semanas (2017-2023)."
)
pdf.figura("fig_serie_semanal.png", "Energia AC total generada por semana (2017-2023).")
pdf.figura("fig_descomposicion_estacional.png",
           "Descomposicion aditiva: tendencia, estacionalidad anual y residuo.", w_pct=0.75)
pdf.parrafo(
    "La descomposicion confirma una estacionalidad anual marcada y regular "
    "superpuesta a una tendencia de mas largo plazo; el residuo conserva "
    "variabilidad no explicada, atribuible a condiciones climaticas semanales no "
    "registradas en el dataset."
)

pdf.add_page()
pdf.titulo_sub("Modelos comparados")
pdf.parrafo(
    "Se reservo el ultimo anio (52 semanas) como prueba: (1) Baseline ingenuo "
    "estacional (valor de la misma semana del anio anterior); (2) Holt-Winters "
    "(suavizado exponencial triple, captura tendencia y estacionalidad)."
)
cols6 = ["Modelo", "RMSE", "MAE", "MAPE (%)"]
widths6 = [50, 35, 35, 40]
aligns6 = ["L", "R", "R", "R"]
rows6 = [
    ("Naive estacional", "110,050.42", "81,013.18", "29.64"),
    ("Holt-Winters", "66,010.72", "52,908.83", "21.79"),
]
pdf.tabla_header(cols6, widths6)
for i, row in enumerate(rows6):
    pdf.tabla_fila(row, widths6, aligns6, alt=(i % 2 == 0))
pdf.ln(3)
pdf.figura("fig_forecast.png",
           "Pronostico semanal - real vs. baseline ingenuo vs. Holt-Winters.")
pdf.parrafo(
    "Modelo seleccionado: Holt-Winters, con una reduccion de ~40% en RMSE y MAE, "
    "y de casi 8 puntos porcentuales de MAPE (21.79% vs. 29.64%) respecto al "
    "baseline ingenuo. La principal limitacion es que el modelo es univariado: no "
    "incorpora variables meteorologicas externas ni eventos de mantenimiento "
    "programado, por lo que su desempenio se degrada en semanas climaticamente "
    "atipicas."
)

# ── 9. EVALUACION GENERAL ────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(9, "Evaluacion General")
cols7 = ["Linea de analisis", "Metrica principal", "Resultado"]
widths7 = [55, 55, 55]
aligns7 = ["L", "L", "R"]
rows7 = [
    ("Supervisado (potencia)", "R2 / RMSE", "0.9992 / 6.94 W"),
    ("No supervisado (diagnostico)", "% registros anomalos", "1.99%"),
    ("Forecasting (energia semanal)", "MAPE", "21.79%"),
]
pdf.tabla_header(cols7, widths7)
for i, row in enumerate(rows7):
    pdf.tabla_fila(row, widths7, aligns7, alt=(i % 2 == 0))
pdf.ln(3)

# ── 10. DISCUSION ─────────────────────────────────────────────────────────────
pdf.titulo_seccion(10, "Discusion")
pdf.titulo_sub("Sobre el aprendizaje supervisado")
pdf.parrafo(
    "El hallazgo mas relevante es que el modelo mas simple (Regresion Lineal) fue "
    "el de mejor desempenio, por un margen claro sobre Random Forest y el MLP. Esto "
    "no es un fracaso de los modelos complejos: la potencia AC es aproximadamente "
    "el producto de corriente y voltaje, y con 98 variables de entrada una "
    "combinacion lineal ya aproxima muy bien esa relacion casi algebraica -hay poco "
    "margen para que la capacidad adicional de un modelo no lineal reduzca el "
    "error, y si margen para que introduzca varianza (el Dropout del MLP penaliza "
    "un problema con poco ruido real). Es un recordatorio: la complejidad del "
    "modelo debe elegirse segun la naturaleza de la relacion subyacente."
)
pdf.titulo_sub("Sobre el aprendizaje no supervisado")
pdf.parrafo(
    "El agrupamiento revelo que no todos los inversores se comportan igual pese a "
    "recibir, en principio, la misma irradiancia. Es consistente con diferencias "
    "reales de operacion: sombreado parcial, degradacion desigual o fallas "
    "intermitentes de comunicacion. La deteccion de anomalias, al no requerir "
    "historial de fallas etiquetado, es especialmente util en un escenario realista."
)
pdf.titulo_sub("Sobre el forecasting")
pdf.parrafo(
    "Holt-Winters aprovecha la fuerte estacionalidad anual del recurso solar, pero "
    "es univariado: no sabe nada sobre nubosidad, mantenimiento programado o "
    "expansion de capacidad. Su error se concentra, previsiblemente, en semanas con "
    "condiciones climaticas atipicas."
)
pdf.titulo_sub("Limitaciones generales")
for b in [
    "El dataset no incluye variables meteorologicas externas que explicarian una "
    "porcion relevante de la variabilidad no capturada por los modelos.",
    "La imputacion de nulos con 0 asume que todo valor faltante corresponde a un "
    "inversor apagado; razonable dado el contexto fisico, pero no verificable de "
    "forma independiente.",
    "El Random Forest se entreno sobre una submuestra de 150,000 registros (de "
    "309,308 disponibles) para mantener tiempos de entrenamiento razonables.",
    "El numero de clusters (k=3) se fijo de forma exploratoria; un analisis con "
    "series de tiempo completas por inversor podria refinar la segmentacion.",
]:
    pdf.bullet(b)

# ── 11. CONCLUSIONES ──────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion(11, "Conclusiones")
pdf.parrafo(
    "Se aplico un proceso completo de ciencia de datos -comprension, exploracion, "
    "preparacion, modelado y evaluacion- sobre el dataset electrico de una planta "
    "solar fotovoltaica de 24 inversores (632,952 registros, ~6 anios a 5 minutos)."
)
for b in [
    "Se identificaron y corrigieron problemas de calidad de datos concretos (nulos "
    "por inversores fuera de linea, asimetria estructural entre inversores y un "
    "error tipografico en un nombre de columna), documentando cada transformacion.",
    "Se demostro que la potencia AC total puede predecirse con altisima precision "
    "(R2 = 0.9992) a partir unicamente de las senales electricas de entrada. De "
    "forma reveladora, el modelo mas simple (Regresion Lineal) supero a Random "
    "Forest y al MLP, evidenciando que la relacion es casi algebraica (P = V x I) "
    "y que mayor complejidad no implica mejor desempenio en ese regimen.",
    "El analisis no supervisado segmento los 24 inversores en 3 clusters e "
    "identifico a los inversores 04 y 07 como un grupo claramente atipico (mayor "
    "tiempo fuera de linea, picos de potencia anomalos); ademas, se marco un 1.99% "
    "de los registros diurnos como anomalos.",
    "El pronostico semanal con Holt-Winters aprovecho la fuerte estacionalidad "
    "anual de la generacion solar, superando a un baseline ingenuo estacional "
    "(MAPE 21.79% vs. 29.64%).",
]:
    pdf.bullet(b)

pdf.titulo_sub("Aportacion del trabajo")
pdf.parrafo(
    "Mas alla de aplicar un algoritmo aislado, este trabajo integra sobre un mismo "
    "dataset industrial de alta frecuencia las tres perspectivas de mineria de "
    "datos solicitadas -prediccion supervisada, diagnostico no supervisado y "
    "forecasting- mostrando como cada una responde a una pregunta de negocio "
    "distinta (cuanto se genera, que componentes requieren atencion, y cuanto se "
    "generara a futuro) a partir de la misma fuente de datos electricos, sin "
    "depender de variables externas ni de un historial de fallas etiquetado."
)

# ── ANEXOS ────────────────────────────────────────────────────────────────────
pdf.add_page()
pdf.titulo_seccion("", "Anexos")
pdf.titulo_sub("A. Fuente del dataset")
pdf.parrafo(
    "Archivo 2107_electrical_data.csv: mediciones electricas cada 5 minutos de 24 "
    "inversores de una planta solar fotovoltaica (nov-2017 a nov-2023), "
    "proporcionado por la catedra de Mineria de Datos."
)
pdf.titulo_sub("B. Reproducibilidad")
for b in [
    "Notebook: plan_mineria.ipynb (raiz del repositorio)",
    "Figuras exportadas en: figuras/",
    "Entorno: Python 3.14, pandas, numpy, scikit-learn, statsmodels, PyTorch, "
    "seaborn, matplotlib",
    "Colocar 2107_electrical_data.csv en la raiz del repositorio (junto al "
    "notebook) antes de ejecutar; no se incluye en el repositorio por su tamanio "
    "(~400 MB).",
]:
    pdf.bullet(b)

pdf.titulo_sub("C. Referencias")
for ref in [
    "The pandas development team. pandas: powerful Python data analysis toolkit. "
    "https://pandas.pydata.org/",
    "scikit-learn developers. scikit-learn: Machine Learning in Python. "
    "https://scikit-learn.org/",
    "PyTorch Foundation. PyTorch Documentation. https://pytorch.org/docs/",
    "statsmodels developers. statsmodels: Statistical Models, Hypothesis Tests, "
    "and Data Exploration in Python. https://www.statsmodels.org/",
    "Winters, P. R. (1960). Forecasting Sales by Exponentially Weighted Moving "
    "Averages. Management Science, 6(3), 324-342.",
    "Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. 2008 Eighth "
    "IEEE International Conference on Data Mining, 413-422.",
]:
    pdf.bullet(ref)

pdf.output("reporte_electrico.pdf")
print("reporte_electrico.pdf generado correctamente.")
