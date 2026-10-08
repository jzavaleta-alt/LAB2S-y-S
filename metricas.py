# metricas.py - Paso 6: energía y potencia media
import numpy as np
from senales import dt


def energia(x):
    """E = suma de |x|^2 * dt"""
    return np.sum(np.abs(x) ** 2) * dt


def potencia(x):
    """P = energía / duración de la ventana (N*dt)"""
    duracion = len(x) * dt
    return energia(x) / duracion


def fila_tabla(caso, nx, nh, x, y):
    """Una fila del Cuadro 2: Caso & Entrada & h & Ex & Px & Ey & Py"""
    return (f"{caso} & {nx} & {nh} & {energia(x):.4g} & {potencia(x):.4g} & "
            f"{energia(y):.4g} & {potencia(y):.4g} \\\\")