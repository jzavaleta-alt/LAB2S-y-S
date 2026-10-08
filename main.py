# main.py - Experiencia 2, ordenado según la planilla del informe
import numpy as np
from senales import t, th, dt, fs, f0, periodicas, aperiodicas
from convolucion import convolucion, modificar_h
from metricas import fila_tabla
from lti import es_lineal, es_invariante
from graficos import graficar, graficar_superpuestas

# Nombres cortos (sin tildes) para los archivos y para la tabla
corto = {"Exp. decreciente": "decreciente", "Exp. creciente": "creciente",
         "Impulso": "impulso", "Escalón": "escalon", "Sinc": "sinc"}
tabla_h = {"Exp. decreciente": "Decreciente", "Exp. creciente": "Creciente",
           "Impulso": "Impulso", "Escalón": "Escalón", "Sinc": "Sinc"}
corto_x = {"Senoidal": "senoidal", "Cuadrada": "cuadrada",
           "Triangular": "triangular", "Diente de sierra": "diente_sierra"}
letras = "abcdefghijklmnopqrst"

txt = []    # archivo resultados_planilla.txt
guia = []   # archivo guia_figuras.txt


def bloque_latex(archivos, pie, etiqueta):
    """Texto LaTeX para pegar: una figura con varios PDF apilados."""
    s = "\\begin{figure}[H]\n\\centering\n"
    for a in archivos:
        s += "\\includegraphics[width=0.9\\textwidth]{figuras/" + a + ".pdf}\n\\par\\vspace{2mm}\n"
    s += "\\caption{" + pie + "}\n\\label{" + etiqueta + "}\n\\end{figure}\n"
    return s


# ======================= Parámetros (secciones 2.1.1 y 2.1.2) =======================
txt.append("PARAMETROS (para la sección 2.1)")
txt.append(f"fs = {fs} Hz, dt = {dt} s, N periodicas = {len(t)}, N aperiodicas = {len(th)}")
txt.append(f"Periodicas: A = 1, f0 = {f0} Hz, ventana 0 a 2 s ({int(2 * f0)} periodos)")
txt.append("Cuadrada: ciclo de trabajo 50%. Triangular: simetrica (width = 0.5). Diente de sierra: rampa creciente (width = 1)")
txt.append("Aperiodicas: ventana -3 a 3 s. Impulso: una muestra de valor 1/dt en t = 0. Escalon: u(t) = 1 para t >= 0")
txt.append("Tolerancia LTI: np.allclose (rtol = 1e-5, atol = 1e-8). Invarianza: retraso de 100 muestras (0.1 s)")

# ======================= Identificadores P01..P20 y cálculo =======================
pid = {}
salidas = {}
n = 1
for nx, x in periodicas.items():
    for nh, h in aperiodicas.items():
        pid[(nx, nh)] = f"P{n:02d}"
        salidas[(nx, nh)] = convolucion(x, t, h, th)
        n += 1

# ======================= FIGURA 1: 20 archivos (1a ... 1t) =======================
print("=== FIGURA 1 (20 archivos) ===")
k = 0
for nh, h in aperiodicas.items():
    archivos = []
    for nx, x in periodicas.items():
        y, ty = salidas[(nx, nh)]
        nombre = f"S2-2-1_Fig1{letras[k]}_{pid[(nx, nh)]}_{corto_x[nx]}_{corto[nh]}"
        graficar([(nx, x, t, nh, h, th, y, ty)], f"{pid[(nx, nh)]}: {nx} con h(t) = {nh}", nombre)
        archivos.append(nombre)
        print(f"figuras/{nombre}.pdf")
        k += 1
    guia.append(f"--- SECCION 2.2.1 / FIGURA 1: grupo h = {nh} ---")
    guia.append("Archivos: " + ", ".join(a + ".pdf" for a in archivos))
    guia.append(bloque_latex(archivos, f"Entradas periódicas, respuesta al impulso {nh.lower()} y salidas.",
                             "fig:1_" + corto[nh]))

# ======================= FIGURA 2: factor a y corrimiento t0 (2a ... 2e) =======================
print("\n=== FIGURA 2 ===")
a, t0 = 2, 0.5
x = periodicas["Senoidal"]
h = aperiodicas["Exp. decreciente"]
variantes = [("S2-2-2_Fig2a_original", 1, 0), ("S2-3-2_Fig2b_solo_a", a, 0),
             ("S2-3-2_Fig2c_solo_t0", 1, t0), ("S2-2-2_Fig2d_a_y_t0", a, t0)]
curvas = []
archivos2 = []
for nombre, a_, t0_ in variantes:
    h_mod, th_mod = modificar_h(h, th, a_, t0_)
    y_, ty_ = convolucion(x, t, h_mod, th_mod)
    etiqueta = "Exp. decreciente (original)" if (a_, t0_) == (1, 0) else f"{a_}*Exp. decreciente(t - {t0_})"
    graficar([("Senoidal", x, t, etiqueta, h_mod, th_mod, y_, ty_)], f"a = {a_}, t0 = {t0_} s", nombre)
    curvas.append((f"a = {a_}, t0 = {t0_} s", ty_, y_))
    print(f"figuras/{nombre}.pdf -> a = {a_}, t0 = {t0_}: max|y| = {np.max(np.abs(y_)):.4f}, "
          f"la salida parte en {ty_[0]:.2f} s")
    txt.append(f"FIGURA 2 ({nombre}): a = {a_}, t0 = {t0_} s, max|y| = {np.max(np.abs(y_)):.4f}, "
               f"inicio de la salida = {ty_[0]:.2f} s")
graficar_superpuestas(curvas, "Salidas con distintos a y t0 (entrada senoidal)", "S2-2-2_Fig2e_comparacion")
print("figuras/S2-2-2_Fig2e_comparacion.pdf")
guia.append("--- SECCION 2.2.2 / FIGURA 2 --- (a = 2, t0 = 0.5 s)")
guia.append("Archivos: S2-2-2_Fig2a_original, S2-2-2_Fig2d_a_y_t0, S2-2-2_Fig2e_comparacion (principales); S2-3-2_Fig2b_solo_a y S2-3-2_Fig2c_solo_t0 (extras, van en el analisis 2.3.2)")
guia.append(bloque_latex(["S2-2-2_Fig2a_original", "S2-2-2_Fig2d_a_y_t0", "S2-2-2_Fig2e_comparacion"],
                         "Efecto del factor de proporcionalidad y del corrimiento temporal.", "fig:2"))
guia.append("% Extras opcionales (efecto por separado):\n"
            "% \\includegraphics[width=0.9\\textwidth]{figuras/S2-3-2_Fig2b_solo_a.pdf}\n"
            "% \\includegraphics[width=0.9\\textwidth]{figuras/S2-3-2_Fig2c_solo_t0.pdf}\n")

# ======================= FIGURA 3: A1 a A5 (3a ... 3e) =======================
print("\n=== FIGURA 3 / CUADRO 1 ===")
pares = [("Exp. decreciente", "Escalón"), ("Exp. creciente", "Sinc"), ("Escalón", "Sinc"),
         ("Exp. decreciente", "Exp. creciente"), ("Impulso", "Sinc")]
filas_A, cuadro1, archivos3 = [], [], []
for i, (nx, nh) in enumerate(pares):
    xa, ha = aperiodicas[nx], aperiodicas[nh]
    y, ty = convolucion(xa, th, ha, th)
    caso = f"A{i + 1}"
    nombre = f"S2-2-3_Fig3{letras[i]}_{caso}_{corto[nx]}_{corto[nh]}"
    graficar([(nx, xa, th, nh, ha, th, y, ty)], f"{caso}: {nx} * {nh}", nombre)
    archivos3.append(nombre)
    filas_A.append(fila_tabla(caso, nx, nh, xa, y))
    cuadro1.append(f"{caso} & {nx} & {nh} & 3{letras[i]} \\\\")
    y2, _ = convolucion(ha, th, xa, th)
    print(f"figuras/{nombre}.pdf | conmutativa: {np.allclose(y, y2)}, "
          f"lineal: {es_lineal(xa, np.flip(xa), th, ha, th)}, invariante: {es_invariante(xa, th, ha, th)}")
guia.append("--- SECCION 2.2.3 / FIGURA 3 / CUADRO 1 ---")
guia.append("Archivos: " + ", ".join(a + ".pdf" for a in archivos3))
guia.append(bloque_latex(archivos3, "Convoluciones entre señales aperiódicas (casos A1 a A5).", "fig:3"))

# ======================= CUADRO 2 (P01..P20, A1..A5) =======================
cuadro2 = []
for nx, x in periodicas.items():
    for nh in aperiodicas:
        y, ty = salidas[(nx, nh)]
        cuadro2.append(fila_tabla(pid[(nx, nh)], nx, tabla_h[nh], x, y))
cuadro2 += filas_A

# ======================= CUADRO 3 (LTI por sistema) =======================
print("\n=== CUADRO 3 ===")
cuadro3 = []
for nh, h in aperiodicas.items():
    lineal, invariante = True, True
    for nx, x in periodicas.items():
        otra = periodicas["Cuadrada"] if nx != "Cuadrada" else periodicas["Senoidal"]
        lineal = lineal and es_lineal(x, otra, t, h, th)
        invariante = invariante and es_invariante(x, t, h, th)
    print(f"{nh:17s} -> lineal: {lineal}, invariante: {invariante}")
    cuadro3.append(f"{nh} & {'Cumple' if lineal else 'No cumple'} & "
                   f"{'Cumple' if invariante else 'No cumple'} \\\\")

# ======================= Guardar archivos de texto =======================
txt.append("\nCUADRO 1 (Caso & Entrada & h & Figura)")
txt += cuadro1
txt.append("\nCUADRO 2 (Caso & Entrada & h & Ex & Px & Ey & Py)  [E en unidades^2*s, P en unidades^2]")
txt += cuadro2
txt.append("\nCUADRO 3 (Sistema & Linealidad & Invariancia)")
txt += cuadro3
with open("resultados_planilla.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(txt))
with open("guia_figuras.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(guia))
print("\nListo: 30 figuras en figuras/, valores en resultados_planilla.txt, ubicacion en guia_figuras.txt")