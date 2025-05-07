# emisor_local.py
import numpy as np
import sounddevice as sd
import time

# Mapa de frecuencias para cada símbolo
frecuencias_digitos = {
    '0': 1000, '1': 1100, '2': 1200, '3': 1300,
    '4': 1400, '5': 1500, '6': 1600, '7': 1700,
    '8': 1800, '9': 1900, '.': 2000, ',': 2100
}

fs = 44100  # Frecuencia de muestreo
duracion_tono = 1  # Duración de cada tono (segundos)
amplitud = 0.5       # Volumen

def generar_tono(frecuencia, duracion):
    t = np.linspace(0, duracion, int(fs * duracion), False)
    tono = np.sin(2 * np.pi * frecuencia * t)
    return tono * amplitud

mensaje = input("[EMISOR] Ingrese el mensaje a enviar (números, punto y coma): ")

print("[EMISOR] Enviando mensaje...")

for caracter in mensaje:
    frecuencia = frecuencias_digitos.get(caracter)
    if frecuencia:
        tono = generar_tono(frecuencia, duracion_tono)
        sd.play(tono, samplerate=fs)
        sd.wait()
        time.sleep(0.05)  # Pequeña pausa entre tonos
    else:
        print(f"[EMISOR] Caracter no reconocido: {caracter}")

print("[EMISOR] Mensaje enviado.")