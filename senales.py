# senales.py - Pasos 1 y 2: parámetros y señales
import numpy as np
from scipy import signal

# ---------- Parámetros globales ----------
fs = 1000            # frecuencia de muestreo [Hz]
dt = 1 / fs          # periodo de muestreo [s]
f0 = 5               # frecuencia de las señales periódicas [Hz]

t  = np.arange(0, 2, dt)    # tiempo de las señales periódicas: 0 a 2 s
th = np.arange(-3, 3, dt)   # tiempo de las señales aperiódicas: -3 a 3 s


def escalon(s):
    """Escalón unitario u(s): 0 si s<0, 1 si s>=0."""
    return (s >= 0) * 1.0


# ---------- Paso 1: señales periódicas ----------
periodicas = {
    "Senoidal":         np.sin(2 * np.pi * f0 * t),
    "Cuadrada":         signal.square(2 * np.pi * f0 * t),
    "Triangular":       signal.sawtooth(2 * np.pi * f0 * t, 0.5),
    "Diente de sierra": signal.sawtooth(2 * np.pi * f0 * t),
}

# ---------- Paso 2: señales aperiódicas ----------
# Impulso discreto: una sola muestra de valor 1/dt (así su área es 1)
impulso = np.zeros(len(th))
impulso[np.argmin(abs(th))] = 1 / dt

aperiodicas = {
    "Exp. decreciente": np.exp(-th) * (escalon(th) - escalon(th - 1)),
    "Exp. creciente":   np.exp(th) * (escalon(th) - escalon(th - 1)),
    "Impulso":          impulso,
    "Escalón":          escalon(th),
    "Sinc":             np.sinc(th / np.pi),   # np.sinc usa pi*x, por eso se divide por pi: sen(t)/t
}