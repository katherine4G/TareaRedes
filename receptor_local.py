# receptor_local.py
# receptor_local_loop.pyr
import numpy as np
import sounddevice as sd
from scipy.fft import rfft, rfftfreq

frecuencias_digitos = {
    1000: '0', 1100: '1', 1200: '2', 1300: '3',
    1400: '4', 1500: '5', 1600: '6', 1700: '7',
    1800: '8', 1900: '9', 2000: '.', 2100: ','
}

tolerancia = 40  # Hz
fs = 44100
duracion_tono = 1  # en segundos
frames_por_segmento = int(fs * duracion_tono)

def detectar_digito(segmento_audio):
    fft_data = np.abs(rfft(segmento_audio))
    freqs = rfftfreq(len(segmento_audio), 1/fs)
    pico = np.argmax(fft_data)
    frecuencia_detectada = freqs[pico]

    for freq_ref, digito in frecuencias_digitos.items():
        if abs(frecuencia_detectada - freq_ref) <= tolerancia:
            return digito
    return '?'

mensaje = ""

print("[RECEPTOR] Escuchando continuamente... (Ctrl+C para detener)")

try:
    while True:
        grabacion = sd.rec(frames_por_segmento, samplerate=fs, channels=1, dtype='float64')
        sd.wait()
        segmento = grabacion[:, 0]
        digito = detectar_digito(segmento)
        if digito != '?':
            mensaje += digito
        print(f"[RECEPTOR] Dato detectado: {digito}")
except KeyboardInterrupt:
    print("\n[RECEPTOR] Finalizado por el usuario.")
    print(f"[RECEPTOR] Mensaje completo recibido: {mensaje}")