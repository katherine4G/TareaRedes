# emisor_local.py
import numpy as np
import sounddevice as sd
import random

# Codificación FSK (frecuencias más bajas y más audibles para pruebas locales)
mapa_frecuencias = {
    '0': 13000,
    '1': 13100,
    '2': 13200,
    '3': 13300,
    '4': 13400,
    '5': 13500,
    '6': 13600,
    '7': 13700,
    '8': 13800,
    '9': 13900,
    '.': 14000,
    ',': 14100
}

fs = 44100
duracion = 0.3  # segundos por tono

def generar_onda(frecuencia, duracion=duracion):
    t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * frecuencia * t)

# Generar valores simulados
temp = round(random.uniform(20.0, 35.0), 1)
hum = round(random.uniform(30.0, 80.0), 1)
mensaje = f"{temp},{hum}"
print(f"[EMISOR] Enviando: {mensaje}")

# Codificar mensaje
onda_total = np.array([], dtype=np.float32)
for char in mensaje:
    freq = mapa_frecuencias.get(char)
    if freq:
        onda = generar_onda(freq)
        onda_total = np.concatenate((onda_total, onda))

# Reproducir
sd.play(onda_total, samplerate=fs)
sd.wait()
print("[EMISOR] Transmisión completada.")
