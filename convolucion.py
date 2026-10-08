# convolucion.py - Pasos 3, 4 y 5
import numpy as np
from senales import dt


def convolucion(x, tx, h, th):
    """Convolución continua aproximada: np.convolve * dt.
    Devuelve la salida y su eje de tiempo."""
    y = np.convolve(x, h) * dt
    ty = tx[0] + th[0] + np.arange(len(y)) * dt   # el inicio de y es la suma de los inicios
    return y, ty


def modificar_h(h, th, a, t0):
    """Paso 4: devuelve a*h(t - t0). Se multiplica por a y se corre el eje de tiempo."""
    return a * h, th + t0