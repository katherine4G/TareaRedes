# emisor_local.py
import numpy as np
import sounddevice as sd
from scipy.fft import rfft, rfftfreq
import time

# Mapa de frecuencias para cada símbolo
frecuencias_digitos_E = {
    '0': 1000, '1': 1100, '2': 1200, '3': 1300,
    '4': 1400, '5': 1500, '6': 1600, '7': 1700,
    '8': 1800, '9': 1900, '.': 2000, ',': 2100,
    'S' :2200, 'F': 2300
}

frecuencias_digitos_R = {
    1000: '0', 1100: '1', 1200: '2', 1300: '3',
    1400: '4', 1500: '5', 1600: '6', 1700: '7',
    1800: '8', 1900: '9', 2000: '.', 2100: ',',
    2200: 'S', 2300: 'F'
}

fs = 44100  # Frecuencia de muestreo
duracion_tono = 1  # Duración de cada tono (segundos)
amplitud = 0.5       # Volumen
frames_por_segmento = int(fs * duracion_tono)
tolerancia = 40  # Hz

def detectar_digito(segmento_audio):
    fft_data = np.abs(rfft(segmento_audio))
    freqs = rfftfreq(len(segmento_audio), 1/fs)
    pico = np.argmax(fft_data)
    frecuencia_detectada = freqs[pico]

    for freq_ref, digito in frecuencias_digitos_R.items():
        if abs(frecuencia_detectada - freq_ref) <= tolerancia:
            return digito
    return '?'

def generar_tono(frecuencia, duracion):
    t = np.linspace(0, duracion, int(fs * duracion), False)
    tono = np.sin(2 * np.pi * frecuencia * t)
    return tono * amplitud

def enviarMensaje(mensaje):
    for caracter in mensaje:
        frecuencia = frecuencias_digitos_E.get(caracter)
        if frecuencia:
            tono = generar_tono(frecuencia, duracion_tono)
            sd.play(tono, samplerate=fs)
            sd.wait()
            time.sleep(0.05)  # Pequeña pausa entre tonos
        else:
            print(f"[EMISOR] Caracter no reconocido: {caracter}")

def verificarMedio():
    i = 0
    try:
        while i <= 7 :
            grabacion = sd.rec(frames_por_segmento, samplerate=fs, channels=1, dtype='float64')
            sd.wait()
            segmento = grabacion[:, 0]
            digito = detectar_digito(segmento)
            print(f"[EMISOR] Dato detectado de alguien más: {digito}")
            i = i + 1
            if digito != '?':
                i = 0
    except KeyboardInterrupt:
        print("\n[EMISOR] Finalizado por el usuario.")
        print(f"[EMISOR] Mensaje completo recibido: {mensaje}")

#---------------------------------------------------------
id = input("[EMISOR] Ingrese el ID del nodo: ")
id += ','
while True:
    temp = input("[EMISOR] Ingrese la temperatura a enviar (números y punto): ")
    hum = input("[EMISOR] Ingrese la humedad a enviar (números y punto): ")
    mensaje = "S," + id+ ',' + temp + ',' + hum+ ",F"
    verificarMedio()
    enviarMensaje(mensaje)