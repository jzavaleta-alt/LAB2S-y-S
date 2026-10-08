# lti.py - Paso 7: verificación numérica de linealidad e invarianza
import numpy as np
from convolucion import convolucion
from senales import dt


def es_lineal(x1, x2, tx, h, th, a=2, b=3):
    """Revisa que (a*x1 + b*x2)*h == a*(x1*h) + b*(x2*h)."""
    y1, _ = convolucion(x1, tx, h, th)
    y2, _ = convolucion(x2, tx, h, th)
    ysuma, _ = convolucion(a * x1 + b * x2, tx, h, th)
    return np.allclose(ysuma, a * y1 + b * y2)


def es_invariante(x, tx, h, th, n=100):
    """Retrasa la entrada n muestras y revisa que la salida también se retrase n muestras."""
    y, _ = convolucion(x, tx, h, th)
    x_retrasada = np.concatenate((np.zeros(n), x))      # x(t - n*dt)
    y_retrasada, _ = convolucion(x_retrasada, tx, h, th)
    y_esperada = np.concatenate((np.zeros(n), y))        # y(t - n*dt)
    return np.allclose(y_retrasada, y_esperada)