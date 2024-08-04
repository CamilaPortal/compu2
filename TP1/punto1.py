from PIL import Image
from scipy.ndimage import gaussian_filter
from multiprocessing import Process, Pipe, shared_memory
import numpy as np
import signal
import sys
import time

shm = None
procesos = []
procesamiento_exitoso = False

def cargar_y_dividir_imagen(ruta_imagen, n_partes):
    imagen = Image.open(ruta_imagen)
    ancho, alto = imagen.size
    alto_parte = alto // n_partes
    partes = []
    for i in range(n_partes):
        izquierda = 0
        arriba = i * alto_parte
        derecha = ancho
        abajo = (i + 1) * alto_parte if i < n_partes - 1 else alto
        parte = imagen.crop((izquierda, arriba, derecha, abajo))
        parte = parte.convert('RGB')
        partes.append(parte)
    return partes, ancho, alto

def aplicar_filtro(parte):
    parte_np = np.array(parte, dtype=np.float64)
    parte_filtrada = gaussian_filter(parte_np, sigma=2)
    return np.clip(parte_filtrada, 0, 255).astype(np.uint8)

def procesar_parte(parte, conn):
    parte_np = np.array(parte)
    parte_filtrada = aplicar_filtro(parte_np)
    print(f"Procesando parte de la imagen con tamaño {parte_np.shape}...")
    time.sleep(10)
    conn.send(parte_filtrada)
    conn.close()

def coordinador(partes, n_partes, ancho, alto):
    global shm
    global procesamiento_exitoso

    tamaño_total = alto * ancho * 3
    shm = shared_memory.SharedMemory(create=True, size=tamaño_total)
    array_compartido = np.ndarray((alto, ancho, 3), dtype=np.uint8, buffer=shm.buf)
    
    pipes = []

    try:
        for i, parte in enumerate(partes):
            parent_conn, child_conn = Pipe()
            pipes.append(parent_conn)
            p = Process(target=procesar_parte, args=(parte, child_conn))
            procesos.append(p)
            p.start()

        for i, p in enumerate(procesos):
            p.join()
            parte_filtrada = pipes[i].recv()
            offset = i * (alto // n_partes)
            array_compartido[offset:offset + parte_filtrada.shape[0], :, :] = parte_filtrada
            pipes[i].close()

        imagen_final = Image.fromarray(array_compartido)
        imagen_final.save('imagen_final_filtrada.jpg')
        procesamiento_exitoso = True

    finally:
        if shm:
            try:
                shm.close()
                shm.unlink()
            except FileNotFoundError:
                pass

        if procesamiento_exitoso:
            print("Las partes de la imagen se han procesado y combinado correctamente.")

def manejador_senal(sig, frame):
    print('Interrupción recibida. Terminando los procesos...')
    for p in procesos:
        p.terminate()
    if shm:
        try:
            shm.close()
            shm.unlink()
        except FileNotFoundError:
            pass
    sys.exit(0)

ruta_imagen = '/home/camilaportal/Documentos/compu2/TP1/UM_logo.png'
n_partes = 4

signal.signal(signal.SIGINT, manejador_senal)

partes, ancho, alto = cargar_y_dividir_imagen(ruta_imagen, n_partes)

coordinador(partes, n_partes, ancho, alto)
