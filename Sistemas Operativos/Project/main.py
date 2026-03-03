import os
import sys
import time
import random
import threading
import atomic  # ← solo usamos esto para la variable atómica (viene en Python 3.11+)
                # si usas Python < 3.11 puedes reemplazar con una variable normal + busy-wait
                # pero con race condition visible

# -------------------------------------------------------------------------
# Mutex (spinlock) implementado desde cero
# -------------------------------------------------------------------------

class SimpleSpinLock:
    def __init__(self):
        # 0 = libre, 1 = ocupado
        self._locked = atomic.AtomicInt(0)

    def acquire(self):
        while True:
            # Intentamos cambiar de 0 a 1 atómicamente
            if self._locked.compare_exchange(0, 1):
                return
            # Si falló → alguien más lo tiene → seguimos girando

    def release(self):
        self._locked.store(0)


# -------------------------------------------------------------------------
# Productor (se ejecuta en hilos del proceso padre)
# -------------------------------------------------------------------------

def productor(id_hilo, fd_escritura, mutex):
    random.seed(id_hilo + int(time.time()))

    for i in range(5):
        mensaje = f"Productor {id_hilo} → {random.randint(10,99)}\n"
        
        # Simulamos algo de trabajo
        time.sleep(random.uniform(0.15, 0.6))

        mutex.acquire()
        try:
            print(f"  [{id_hilo}] adquirió mutex y escribe → {mensaje.strip()}")
            os.write(fd_escritura, mensaje.encode('utf-8'))
            os.fsync(fd_escritura)           # forzamos que salga ya
        finally:
            mutex.release()

    # Señal de fin para este productor
    mutex.acquire()
    try:
        os.write(fd_escritura, b"FIN\n")
        os.fsync(fd_escritura)
    finally:
        mutex.release()


# -------------------------------------------------------------------------
# Consumidor (se ejecuta en proceso hijo)
# -------------------------------------------------------------------------

def consumidor(fd_lectura):
    leidos = 0
    buffer = b""

    while leidos < 15:  # esperamos 3 productores × 5 mensajes
        chunk = os.read(fd_lectura, 1024)
        if not chunk:
            break

        buffer += chunk

        while b"\n" in buffer:
            linea, buffer = buffer.split(b"\n", 1)
            linea = linea.decode('utf-8', errors='replace').strip()

            if linea == "FIN":
                continue

            print(f"Consumidor recibió: {linea}")
            leidos += 1

    print("\nConsumidor terminó.")
    sys.stdout.flush()


# -------------------------------------------------------------------------
# Programa principal
# -------------------------------------------------------------------------

def main():
    # Creamos el pipe
    r, w = os.pipe()

    # Fork → creamos proceso hijo
    pid = os.fork()

    if pid == 0:
        # === Proceso hijo (consumidor) ===
        os.close(w)           # no escribimos
        consumidor(r)
        os.close(r)
        sys.exit(0)

    else:
        # === Proceso padre (productores) ===
        os.close(r)           # no leemos

        mutex = SimpleSpinLock()

        hilos = []

        # Creamos 3 hilos productores
        for i in range(1, 4):
            t = threading.Thread(
                target=productor,
                args=(i, w, mutex),
                daemon=True
            )
            hilos.append(t)
            t.start()

        # Esperamos a que terminen los hilos
        for t in hilos:
            t.join()

        # Cerramos escritura → el hijo verá EOF
        os.close(w)

        # Esperamos al hijo
        os.waitpid(pid, 0)

        print("\nPrograma principal terminado.")


if __name__ == "__main__":
    if sys.version_info < (3, 11):
        print("Advertencia: atomic requiere Python 3.11+")
        print("Para versiones anteriores se puede usar una variable normal (habrá race conditions visibles)")
        # Alternativa muy básica sin atomic (solo para versiones antiguas)
        class SimpleSpinLock:
            def __init__(self):
                self._locked = 0
            def acquire(self):
                while self._locked != 0:
                    pass
                self._locked = 1
            def release(self):
                self._locked = 0
    main()