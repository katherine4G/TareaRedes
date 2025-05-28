# receptor_local.py
import numpy as np
import sounddevice as sd
from scipy.fft import rfft, rfftfreq

frecuencias_digitos = {
    1000: '0', 1100: '1', 1200: '2', 1300: '3',
    1400: '4', 1500: '5', 1600: '6', 1700: '7',
    1800: '8', 1900: '9', 2000: '.', 2100: ',',
    2200: 'S', 2300: 'F'
}

tolerancia = 40  # Hz
fs = 44100
duracion_tono = 1  # en segundos
frames_por_segmento = int(fs * duracion_tono)

def interpretar_digito(segmento_audio):
    fft_data = np.abs(rfft(segmento_audio))
    freqs = rfftfreq(len(segmento_audio), 1/fs)
    pico = np.argmax(fft_data)
    frecuencia_detectada = freqs[pico]

    for freq_ref, digito in frecuencias_digitos.items():
        if abs(frecuencia_detectada - freq_ref) <= tolerancia:
            return digito
    return '?'

def detectar_digito():
    grabacion = sd.rec(frames_por_segmento, samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    segmento = grabacion[:, 0]
    return interpretar_digito(segmento)

def recolectar_mensaje():
    mensaje = ""
    msgFlag = True

    while msgFlag:
        digito = interpretar_digito
        print(f"[RECEPTOR] Dato detectado: {digito}")
        if digito == 'F':
            return mensaje
        if digito != '?':
            mensaje += digito



print("[RECEPTOR] Escuchando continuamente... (Ctrl+C para detener)")

try:
    while True:
        digito = detectar_digito
        print(f"[RECEPTOR] Dato detectado: {digito}")
        if digito == 'S':
            mensaje = recolectar_mensaje
            print(f"[RECEPTOR] trama detectada: {mensaje}")        
except KeyboardInterrupt:
    print("\n[RECEPTOR] Finalizado por el usuario.")
    print(f"[RECEPTOR] Mensaje completo recibido: {mensaje}")