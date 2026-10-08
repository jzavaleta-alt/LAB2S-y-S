# graficos.py - gráficos vectoriales (PDF)
import os
import matplotlib.pyplot as plt


def graficar(casos, titulo, archivo):
    """Una fila por caso: entrada | respuesta a impulso | salida.
    casos = lista de (nombre_x, x, tx, nombre_h, h, th, y, ty)
    Guarda figuras/<archivo>.pdf"""
    os.makedirs("figuras", exist_ok=True)
    n = len(casos)
    fig, ejes = plt.subplots(n, 3, figsize=(13, 2.2 * n + 0.9), squeeze=False)

    for i, (nx, x, tx, nh, h, th, y, ty) in enumerate(casos):
        ejes[i, 0].plot(tx, x)
        ejes[i, 0].set_title(f"Entrada x(t): {nx}")
        ejes[i, 1].plot(th, h, color="green")
        ejes[i, 1].set_title(f"Respuesta a impulso h(t): {nh}")
        ejes[i, 2].plot(ty, y, color="red")
        ejes[i, 2].set_title("Salida y(t) = x(t) * h(t)")
        for eje in ejes[i]:
            eje.set_xlabel("Tiempo [s]")
            eje.set_ylabel("Amplitud")
            eje.grid(True)

    fig.suptitle(titulo)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(f"figuras/{archivo}.pdf")    # PDF = formato vectorial
    plt.close(fig)


def graficar_superpuestas(curvas, titulo, archivo):
    """Varias salidas en un mismo gráfico. curvas = lista de (etiqueta, ty, y)"""
    os.makedirs("figuras", exist_ok=True)
    fig, eje = plt.subplots(figsize=(10, 4))
    for etiqueta, ty, y in curvas:
        eje.plot(ty, y, label=etiqueta)
    eje.set_title(titulo)
    eje.set_xlabel("Tiempo [s]")
    eje.set_ylabel("Amplitud")
    eje.grid(True)
    eje.legend()
    fig.tight_layout()
    fig.savefig(f"figuras/{archivo}.pdf")
    plt.close(fig)