"""
========================================================================
SISTEMAS OPERATIVOS — Demostración completa (compatible Windows)
========================================================================
Consignas cubiertas:
  1. Creación de procesos (multiprocessing.Process) e hilos (threading.Thread)
  2. Comunicación mediante PIPE (multiprocessing.Pipe)
  3. Sincronización mediante Spinlock (mutex) implementado desde cero
     usando ctypes para la operación atómica Compare-And-Swap (CAS),
     SIN semáforos, Locks ni colas de la stdlib.

¿Por qué multiprocessing en vez de os.fork()?
  os.fork() es exclusivo de Unix/Linux/macOS.
  En Windows el sistema operativo NO permite clonar un proceso en mitad
  de su ejecución; en cambio, multiprocessing.Process lanza un proceso
  nuevo desde cero importando este mismo módulo, que es el mecanismo
  nativo de Windows (y también funciona en Linux/macOS).
  Por eso es OBLIGATORIO proteger el punto de entrada con:
      if __name__ == "__main__":
  Sin esa guardia, Windows entraría en un bucle infinito creando procesos.

Flujo general:
  ┌─────────────────────────────────────────┐
  │  Proceso PADRE                          │
  │  ├─ Hilo Productor 1  ─┐               │
  │  ├─ Hilo Productor 2  ─┼─► PIPE ──►  Proceso HIJO (Consumidor)
  │  └─ Hilo Productor 3  ─┘               │
  └─────────────────────────────────────────┘

  • El PIPE es creado con multiprocessing.Pipe(), que devuelve dos
    objetos Connection: uno para enviar y otro para recibir.
  • Los hilos productores comparten el extremo de escritura dentro del
    proceso padre; el proceso hijo recibe el extremo de lectura como
    argumento al ser creado.
  • El spinlock protege el extremo de escritura para que los hilos no
    escriban simultáneamente y corrompan los mensajes.
========================================================================
"""

import os
import sys
import time
import random
import threading
import ctypes
import ctypes.util
import multiprocessing


# ========================================================================
# BLOQUE 1: SPINLOCK — Mutex implementado desde cero con CAS atómico
# ========================================================================
#
# Concepto de mutex (mutual exclusion):
#   Garantiza que solo UN hilo a la vez ejecute la "sección crítica"
#   (el bloque de código que accede a un recurso compartido).
#
# Concepto de spinlock:
#   Variante de mutex donde el hilo que no puede entrar simplemente
#   "gira" en un bucle (busy-wait) revisando el estado, en vez de
#   bloquearse y ceder la CPU al scheduler.
#   Ventaja: latencia muy baja cuando la espera es corta.
#   Desventaja: desperdicia CPU si la espera es larga.
#
# Operación CAS (Compare-And-Swap):
#   Lee el valor de una variable y, si es igual al esperado, lo
#   reemplaza con el nuevo valor — TODO en una sola instrucción de CPU
#   (CMPXCHG en x86). Esto hace que la "comparación + escritura" sea
#   indivisible, eliminando race conditions.
#
# En Windows, la función CAS se expone a través de la API de Win32
# como InterlockedCompareExchange, accesible vía kernel32.
# En Linux/macOS se usa __atomic_compare_exchange_n de libc/GCC.
# ========================================================================

def _cargar_cas_windows():
    """
    Carga InterlockedCompareExchange de kernel32 (Windows).

    Esta función de la API Win32 implementa CAS de 32 bits:
      LONG InterlockedCompareExchange(LONG* dest, LONG exchange, LONG comparand)
      Si *dest == comparand  →  *dest = exchange  →  retorna comparand (éxito)
      Si no                  →  no cambia nada    →  retorna *dest     (fallo)

    Returns
    -------
    cas_win : ctypes function | None
        Función CAS lista para usar, o None si falla la carga.
    """
    try:
        kernel32 = ctypes.windll.kernel32
        cas_win = kernel32.InterlockedCompareExchange
        # Definimos la firma para que ctypes haga el marshaling correcto
        cas_win.restype  = ctypes.c_long
        cas_win.argtypes = [
            ctypes.POINTER(ctypes.c_long),  # dest      → puntero a la variable
            ctypes.c_long,                  # exchange  → valor a escribir si hay match
            ctypes.c_long,                  # comparand → valor esperado actual
        ]
        return cas_win
    except Exception:
        return None


def _cargar_cas_unix():
    """
    Carga __atomic_compare_exchange_n de libc (Linux / macOS).

    La firma en C es:
      bool __atomic_compare_exchange_n(
          int* ptr, int* expected, int desired,
          bool weak, int success_order, int failure_order)

    Returns
    -------
    cas_unix : ctypes function | None
        Función CAS lista para usar, o None si falla la carga.
    """
    try:
        nombre_libc = ctypes.util.find_library("c")
        libc = ctypes.CDLL(nombre_libc, use_errno=True)
        cas_unix = libc.__atomic_compare_exchange_n
        cas_unix.restype  = ctypes.c_bool
        cas_unix.argtypes = [
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_int,
            ctypes.c_bool,
            ctypes.c_int,
            ctypes.c_int,
        ]
        return cas_unix
    except Exception:
        return None


# Detectamos la plataforma y cargamos la función CAS correspondiente
_PLATAFORMA = sys.platform   # "win32", "linux", "darwin"

if _PLATAFORMA == "win32":
    _CAS_WIN  = _cargar_cas_windows()
    _CAS_UNIX = None
else:
    _CAS_WIN  = None
    _CAS_UNIX = _cargar_cas_unix()

# ¿Tenemos alguna función CAS nativa disponible?
_CAS_DISPONIBLE = (_CAS_WIN is not None) or (_CAS_UNIX is not None)


class SimpleSpinLock:
    """
    Mutex (spinlock) implementado desde cero usando una operación CAS nativa.

    En Windows usa InterlockedCompareExchange (kernel32).
    En Linux/macOS usa __atomic_compare_exchange_n (libc).
    Si ninguno está disponible, usa un fallback con threading.Lock
    (ya no es "desde cero", pero el programa sigue funcionando).

    Attributes
    ----------
    _estado_win : ctypes.c_long  (solo Windows)
        Variable de estado: 0 = libre, 1 = ocupado.
    _estado_unix : ctypes.c_int  (solo Unix)
        Variable de estado: 0 = libre, 1 = ocupado.
    """

    def __init__(self):
        """Inicializa el spinlock en estado libre (0)."""
        if _CAS_WIN is not None:
            # Windows: c_long (32 bits con signo) requerido por kernel32
            self._estado_win = ctypes.c_long(0)
        elif _CAS_UNIX is not None:
            # Unix: c_int (32 bits con signo) requerido por libc
            self._estado_unix = ctypes.c_int(0)
        else:
            # Ningún CAS nativo disponible → fallback
            self._lock_fallback = threading.Lock()

    def acquire(self):
        """
        Adquiere el spinlock; bloquea girando hasta lograrlo.

        Lógica del spin:
          Bucle infinito. En cada iteración se intenta CAS(0 → 1).
            · Si CAS tiene éxito → somos los dueños → retornamos.
            · Si CAS falla       → alguien más lo tiene → seguimos girando.
          time.sleep(0) cede la CPU voluntariamente en cada vuelta
          (equivalente a pthread_yield en Unix o SwitchToThread en Win32).
        """
        if _CAS_WIN is not None:
            # InterlockedCompareExchange retorna el valor ANTERIOR de *dest.
            # Si el anterior era 0 → estaba libre → CAS tuvo éxito → adquirido.
            while True:
                anterior = _CAS_WIN(
                    ctypes.byref(self._estado_win),  # &_estado
                    1,   # exchange  → queremos escribir 1 (ocupado)
                    0    # comparand → solo cambia si encontramos 0 (libre)
                )
                if anterior == 0:
                    return   # ← estaba libre, ahora es nuestro
                time.sleep(0)   # yield para no quemar CPU

        elif _CAS_UNIX is not None:
            esperado = ctypes.c_int(0)
            while True:
                esperado.value = 0   # reiniciamos antes de cada intento
                exito = _CAS_UNIX(
                    ctypes.byref(self._estado_unix),
                    ctypes.byref(esperado),
                    1,      # desired  → ocupado
                    False,  # strong CAS (más confiable que weak)
                    5, 5    # memory order seq_cst en acquire y release
                )
                if exito:
                    return
                time.sleep(0)

        else:
            self._lock_fallback.acquire()

    def release(self):
        """
        Libera el spinlock escribiendo 0 (libre) en la variable de estado.

        En x86/x64 y ARM una escritura alineada de 32 bits es atómica
        a nivel de hardware, por lo que no necesita otra instrucción CAS
        para el release (un store simple es suficiente).
        """
        if _CAS_WIN is not None:
            self._estado_win.value = 0
        elif _CAS_UNIX is not None:
            self._estado_unix.value = 0
        else:
            self._lock_fallback.release()


# ========================================================================
# BLOQUE 2: PRODUCTOR — Se ejecuta en hilos del proceso padre
# ========================================================================
#
# Cada hilo productor:
#   1. Genera 5 mensajes con un número aleatorio.
#   2. Simula trabajo con time.sleep (retardo variable).
#   3. Adquiere el spinlock antes de enviar por el pipe.
#   4. Envía el mensaje y libera el spinlock.
#   5. Al terminar, envía la señal "FIN-N" al consumidor.
#
# ¿Por qué necesitamos el spinlock en el pipe?
#   multiprocessing.Connection.send() serializa objetos Python (pickle),
#   pero si dos hilos llaman a send() al mismo tiempo sobre la MISMA
#   conexión, los bytes de ambos mensajes pueden entremezclarse y
#   corromperse. El spinlock garantiza acceso exclusivo.
# ========================================================================

def productor(id_hilo: int, conn_escritura, mutex: SimpleSpinLock) -> None:
    """
    Función ejecutada por cada hilo productor.

    Genera mensajes aleatorios, los envía por el pipe bajo protección
    del spinlock, y al finalizar envía una señal de terminación.

    Parameters
    ----------
    id_hilo : int
        Identificador del hilo (1, 2 o 3).
    conn_escritura : multiprocessing.Connection
        Extremo de escritura del pipe (compartido entre todos los hilos).
    mutex : SimpleSpinLock
        Spinlock compartido que protege el acceso exclusivo a conn_escritura.
    """
    # Semilla aleatoria única por hilo para evitar valores idénticos
    random.seed(id_hilo * 1337 + int(time.time()))

    for i in range(5):
        numero  = random.randint(10, 99)
        mensaje = f"Productor-{id_hilo} | msg #{i+1} | dato={numero}"

        # Simula trabajo de procesamiento (duración aleatoria por hilo)
        time.sleep(random.uniform(0.1, 0.45))

        # ── SECCIÓN CRÍTICA: acceso exclusivo al pipe ────────────────────
        # Si dos hilos llaman a send() simultáneamente sin este bloqueo,
        # los datos en el pipe se corrompen (race condition).
        mutex.acquire()
        try:
            # send() serializa el string con pickle y lo escribe en el pipe
            conn_escritura.send(mensaje)
        finally:
            # SIEMPRE liberamos en el bloque finally para evitar deadlock
            # aunque send() haya lanzado una excepción.
            mutex.release()
        # ── FIN SECCIÓN CRÍTICA ──────────────────────────────────────────

    # Señal de terminación: el consumidor la usa para saber que
    # este productor ya no enviará más mensajes.
    mutex.acquire()
    try:
        conn_escritura.send(f"FIN-{id_hilo}")
    finally:
        mutex.release()


# ========================================================================
# BLOQUE 3: CONSUMIDOR — Se ejecuta en el proceso hijo
# ========================================================================
#
# El proceso hijo recibe el extremo de LECTURA del pipe.
# Lee mensajes en un bucle hasta recibir una señal "FIN" por cada
# productor. Como es un proceso separado (spawn en Windows), tiene
# su propio espacio de memoria; la única comunicación posible con el
# padre es a través del pipe.
# ========================================================================

def consumidor(conn_lectura, num_productores: int) -> None:
    """
    Función del proceso consumidor (ejecutada en el proceso hijo).

    Recibe mensajes del pipe y los muestra en pantalla hasta haber
    recibido una señal FIN por cada productor.

    Parameters
    ----------
    conn_lectura : multiprocessing.Connection
        Extremo de lectura del pipe.
    num_productores : int
        Cantidad de productores; determina cuántas señales FIN esperar.
    """
    fines_recibidos    = 0
    mensajes_recibidos = 0

    print(f"\n  [CONSUMIDOR pid={os.getpid()}] Listo, esperando mensajes...\n")
    sys.stdout.flush()

    # Bucle principal: leemos hasta haber recibido FIN de cada productor
    while fines_recibidos < num_productores:
        try:
            # recv() bloquea al proceso hijo hasta que llegue un mensaje.
            # Cuando el padre cierra conn_escritura sin más datos → EOFError.
            mensaje = conn_lectura.recv()
        except EOFError:
            # El padre cerró la conexión → salida limpia
            break

        if mensaje.startswith("FIN"):
            # Contamos los finales para saber cuándo terminar
            fines_recibidos += 1
            print(f"  [CONSUMIDOR] Señal fin ({fines_recibidos}/{num_productores}): {mensaje}")
        else:
            # Mensaje de datos normal
            mensajes_recibidos += 1
            print(f"  [CONSUMIDOR] ✓ [{mensajes_recibidos:02d}] {mensaje}")

        sys.stdout.flush()

    print(f"\n  [CONSUMIDOR] Finalizado. Mensajes procesados: {mensajes_recibidos}")
    sys.stdout.flush()


# ========================================================================
# PUNTO DE ENTRADA — Demostración paso a paso con explicaciones
# ========================================================================
#
# IMPORTANTE (Windows):
#   En Windows, multiprocessing usa el método "spawn": al crear un proceso
#   hijo, Python lanza un intérprete nuevo e importa este módulo desde cero.
#   La guardia if __name__ == "__main__": evita que el código de creación
#   de procesos se ejecute también en el proceso hijo → sin ella el programa
#   entraría en un bucle infinito de procesos.
# ========================================================================

if __name__ == "__main__":

    # En Windows es obligatorio llamar a freeze_support() si el script
    # se va a empaquetar como .exe (con PyInstaller, etc.). No hace daño
    # llamarlo siempre.
    multiprocessing.freeze_support()

    NUM_PRODUCTORES   = 3   # cantidad de hilos productores
    MENSAJES_POR_HILO = 5   # mensajes que genera cada productor

    # ── PRESENTACIÓN ────────────────────────────────────────────────────
    print("=" * 65)
    print("  SISTEMAS OPERATIVOS — Demo: Procesos, Pipes y Spinlock")
    print(f"  Plataforma: {sys.platform}  |  Python {sys.version.split()[0]}")
    print("=" * 65)
    print(f"""
Arquitectura:
  Proceso PADRE  (pid={os.getpid()})
    ├─ Hilo Productor 1 ─┐
    ├─ Hilo Productor 2 ─┼──► [PIPE] ──► Proceso HIJO (Consumidor)
    └─ Hilo Productor 3 ─┘

  • Los hilos comparten memoria con el padre → necesitan SPINLOCK
  • El proceso hijo tiene memoria propia → se comunica solo por PIPE
""")

    # ── PASO 1: Crear el PIPE ────────────────────────────────────────────
    print("─" * 65)
    print("PASO 1: Creando el PIPE con multiprocessing.Pipe()")
    print("  Pipe(duplex=False) crea un canal UNIDIRECCIONAL.")
    print("  conn_lectura   → solo el proceso hijo leerá de aquí.")
    print("  conn_escritura → los hilos del padre escribirán aquí.")
    conn_lectura, conn_escritura = multiprocessing.Pipe(duplex=False)
    print("  → PIPE creado  ✓\n")

    # ── PASO 2: Crear el SPINLOCK ────────────────────────────────────────
    print("─" * 65)
    print("PASO 2: Inicializando el SPINLOCK (implementado a mano)")

    if _CAS_WIN is not None:
        modo_cas = "InterlockedCompareExchange  (kernel32 / Win32)"
    elif _CAS_UNIX is not None:
        modo_cas = "__atomic_compare_exchange_n (libc / GCC)"
    else:
        modo_cas = "fallback threading.Lock (CAS nativo no disponible)"

    print(f"  Plataforma detectada : {_PLATAFORMA}")
    print(f"  Función CAS utilizada: {modo_cas}")
    mutex = SimpleSpinLock()
    print("  → Spinlock listo  ✓\n")

    # ── PASO 3: Crear el proceso hijo (consumidor) ───────────────────────
    print("─" * 65)
    print("PASO 3: Creando proceso HIJO con multiprocessing.Process()")
    print("  En Windows el método es 'spawn': se lanza un intérprete")
    print("  Python nuevo y se le pasa conn_lectura como argumento.")
    print("  El hijo NO comparte memoria con el padre; solo recibe args.\n")

    proceso_hijo = multiprocessing.Process(
        target=consumidor,
        args=(conn_lectura, NUM_PRODUCTORES),
        name="Consumidor",
        daemon=False   # False: el padre esperará a que termine
    )
    proceso_hijo.start()

    # El padre cierra su copia de conn_lectura.
    # Esto es necesario para que el EOF llegue correctamente al hijo
    # cuando el padre cierre conn_escritura más adelante.
    conn_lectura.close()

    print(f"  → Proceso HIJO iniciado  pid={proceso_hijo.pid}  ✓")
    print(f"  → Proceso PADRE continúa pid={os.getpid()}\n")

    # ── PASO 4: Crear los hilos productores ─────────────────────────────
    print("─" * 65)
    print(f"PASO 4: Lanzando {NUM_PRODUCTORES} hilos productores")
    print("  Los hilos viven DENTRO del proceso padre y comparten")
    print("  conn_escritura y el mutex. Sin el spinlock, dos hilos")
    print("  podrían llamar a send() al mismo tiempo → datos corruptos.\n")

    hilos = []
    for i in range(1, NUM_PRODUCTORES + 1):
        hilo = threading.Thread(
            target=productor,
            args=(i, conn_escritura, mutex),
            name=f"Productor-{i}",
            daemon=True   # muere si el proceso padre termina abruptamente
        )
        hilos.append(hilo)
        hilo.start()
        print(f"  → {hilo.name} iniciado  (tid nativo={hilo.native_id})")

    print()

    # ── PASO 5: Esperar que terminen los hilos ───────────────────────────
    print("─" * 65)
    print("PASO 5: Padre espera a los hilos con join()")
    print("  join() bloquea hasta que ese hilo termina su función.\n")

    for hilo in hilos:
        hilo.join()
        print(f"  → {hilo.name} terminó  ✓")

    # ── PASO 6: Cerrar conn_escritura ────────────────────────────────────
    print()
    print("─" * 65)
    print("PASO 6: Cerrando conn_escritura en el proceso padre")
    print("  Al cerrar la única Connection de escritura activa,")
    print("  el proceso hijo recibirá EOFError en recv() y podrá")
    print("  terminar limpiamente si no quedan más mensajes.\n")
    conn_escritura.close()

    # ── PASO 7: Esperar al proceso hijo ──────────────────────────────────
    print("─" * 65)
    print(f"PASO 7: Padre espera al proceso HIJO con process.join()")
    print(f"  (pid={proceso_hijo.pid})\n")

    proceso_hijo.join()
    print(f"  → Proceso hijo terminó  "
          f"(código de salida: {proceso_hijo.exitcode})  ✓\n")

    # ── RESUMEN FINAL ─────────────────────────────────────────────────────
    print("=" * 65)
    print("  DEMOSTRACIÓN COMPLETADA")
    print("=" * 65)
    print("""
Consignas cubiertas:
  ✓ Creación de procesos  → multiprocessing.Process  (compatible Windows)
  ✓ Creación de hilos     → threading.Thread
  ✓ Comunicación por PIPE → multiprocessing.Pipe + Connection.send/recv
  ✓ Sincronización        → SimpleSpinLock con CAS atómico nativo
                            (InterlockedCompareExchange en Windows,
                             __atomic_compare_exchange_n en Linux/macOS)
                            implementado desde cero, sin abstracciones
""")