# receptor_local.py
import numpy as np
import sounddevice as sd
from scipy.fft import rfft, rfftfreq

# Mapa inverso (con frecuencias bajas para pruebas)
frecuencias_digitos = {
    13000: '0', 13100: '1', 13200: '2', 13300: '3',
    13400: '4', 13500: '5', 13600: '6', 13700: '7',
    13800: '8', 13900: '9', 14000: '.', 14100: ','
}

tolerancia = 40  # Hz
fs = 44100
duracion_tono = 0.3
cantidad_digitos = 8  # Ajusta si cambias el largo del mensaje

def detectar_digito(segmento_audio):
    fft_data = np.abs(rfft(segmento_audio))
    freqs = rfftfreq(len(segmento_audio), 1/fs)
    pico = np.argmax(fft_data)
    frecuencia_detectada = freqs[pico]

    for freq_ref, digito in frecuencias_digitos.items():
        if abs(frecuencia_detectada - freq_ref) <= tolerancia:
            return digito
    return '?'

print("[RECEPTOR] Escuchando...")
grabacion = sd.rec(int(fs * duracion_tono * cantidad_digitos), samplerate=fs, channels=1, dtype='float64')
sd.wait()
print("[RECEPTOR] Grabación completada.")

datos = []
for i in range(cantidad_digitos):
    inicio = int(i * duracion_tono * fs)
    fin = int((i + 1) * duracion_tono * fs)
    segmento = grabacion[inicio:fin, 0]
    digito = detectar_digito(segmento)
    datos.append(digito)

mensaje = ''.join(datos)
print(f"[RECEPTOR] Mensaje recibido: {mensaje}")
