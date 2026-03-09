"""
========================================================================
SISTEMAS OPERATIVOS — Demostración completa (compatible Windows)
========================================================================
Consignas cubiertas:
  1. Creación de procesos (multiprocessing.Process) e hilos (threading.Thread)
  2. Comunicación mediante PIPE (multiprocessing.Pipe)
  3. Sincronización con DOS mecanismos implementados desde cero:
       a) SpinLock  → mutex puro, CAS atómico vía ctypes (sin stdlib)
       b) Semáforo  → contador + SpinLock interno (sin threading.Semaphore)
          Se demuestra el bloqueo WAIT / SIGNAL de forma explícita y visible.

¿Por qué multiprocessing en vez de os.fork()?
  os.fork() es exclusivo de Unix/Linux/macOS. En Windows no existe.
  multiprocessing.Process lanza un proceso nuevo desde cero, que es el
  mecanismo nativo de Windows y también funciona en Linux/macOS.
  La guardia  if __name__ == "__main__":  es OBLIGATORIA en Windows para
  que el proceso hijo no vuelva a ejecutar el código de creación.

Flujo de la demostración:
  ┌──────────────────────────────────────────────────────┐
  │  Proceso PADRE                                       │
  │                                                      │
  │  [FASE 1 — Semáforo con capacidad 1]                 │
  │    Hilo A ──► entra, trabaja 2 s, hace SIGNAL        │
  │    Hilo B ──► llega, ve semáforo=0, queda BLOQUEADO  │
  │               ... espera el SIGNAL de A ...          │
  │               entra, trabaja, hace SIGNAL            │
  │    Hilo C ──► idem, bloqueado hasta que B hace signal│
  │                                                      │
  │  [FASE 2 — Productores / Consumidor con Pipe]        │
  │    Hilo Prod-1 ─┐                                    │
  │    Hilo Prod-2 ─┼──► [PIPE] ──► Proceso HIJO        │
  │    Hilo Prod-3 ─┘         (Consumidor)               │
  └──────────────────────────────────────────────────────┘
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


# ════════════════════════════════════════════════════════════════════════
# BLOQUE 1: SpinLock — mutex implementado desde cero con CAS atómico
# ════════════════════════════════════════════════════════════════════════
#
# ¿Qué es un mutex?
#   Garantiza exclusión mutua: solo UN hilo a la vez puede estar en la
#   "sección crítica" (el código que toca un recurso compartido).
#
# ¿Qué es un spinlock?
#   Implementación de mutex donde el hilo que no puede entrar gira en un
#   bucle (busy-wait) en lugar de bloquearse y ceder la CPU.
#
# ¿Qué es CAS (Compare-And-Swap)?
#   Una instrucción de CPU que de forma ATÓMICA (indivisible):
#     Lee el valor actual de una variable.
#     Si es igual al valor esperado → lo reemplaza por el nuevo valor.
#   Así dos hilos no pueden adquirir el lock al mismo tiempo.
#   En x86 la instrucción es CMPXCHG; en ARM es LDREX/STREX.
#   Windows la expone como InterlockedCompareExchange (kernel32).
#   Linux/macOS como __atomic_compare_exchange_n (libc/GCC).
# ════════════════════════════════════════════════════════════════════════

def _cargar_cas_windows():
    """
    Carga InterlockedCompareExchange de la API Win32 (kernel32.dll).

    Firma en C:
      LONG InterlockedCompareExchange(LONG* dest, LONG exchange, LONG comparand)
      Si *dest == comparand  →  escribe exchange en *dest  →  retorna comparand
      Si no                  →  no cambia nada             →  retorna *dest

    Returns
    -------
    function | None
    """
    try:
        cas = ctypes.windll.kernel32.InterlockedCompareExchange
        cas.restype  = ctypes.c_long
        cas.argtypes = [
            ctypes.POINTER(ctypes.c_long),  # dest
            ctypes.c_long,                  # exchange  (valor a escribir)
            ctypes.c_long,                  # comparand (valor esperado)
        ]
        return cas
    except Exception:
        return None


def _cargar_cas_unix():
    """
    Carga __atomic_compare_exchange_n de libc (Linux / macOS).

    Firma en C:
      bool __atomic_compare_exchange_n(
          int* ptr, int* expected, int desired,
          bool weak, int success_order, int failure_order)

    Returns
    -------
    function | None
    """
    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        cas = libc.__atomic_compare_exchange_n
        cas.restype  = ctypes.c_bool
        cas.argtypes = [
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ctypes.c_int,
            ctypes.c_bool,
            ctypes.c_int,
            ctypes.c_int,
        ]
        return cas
    except Exception:
        return None


_PLATAFORMA   = sys.platform
_CAS_WIN      = _cargar_cas_windows() if _PLATAFORMA == "win32" else None
_CAS_UNIX     = _cargar_cas_unix()    if _PLATAFORMA != "win32" else None
_CAS_DISPONIBLE = (_CAS_WIN is not None) or (_CAS_UNIX is not None)


class SpinLock:
    """
    Mutex (spinlock) implementado desde cero con CAS atómico nativo.

    Estado interno: entero de 32 bits.
      0 = libre   →  cualquier hilo puede adquirirlo
      1 = ocupado →  los demás hilos girarán esperando

    En Windows usa InterlockedCompareExchange (kernel32).
    En Linux/macOS usa __atomic_compare_exchange_n (libc).
    Fallback con threading.Lock si ningún CAS está disponible.
    """

    def __init__(self):
        """Crea el spinlock en estado libre (0)."""
        if _CAS_WIN is not None:
            self._v = ctypes.c_long(0)   # c_long requerido por kernel32
        elif _CAS_UNIX is not None:
            self._v = ctypes.c_int(0)    # c_int  requerido por libc
        else:
            self._fb = threading.Lock()  # fallback

    def acquire(self):
        """
        Intenta adquirir el lock girando hasta lograrlo.

        Cada iteración ejecuta CAS(esperado=0, deseado=1):
          · Éxito  → somos dueños → retornamos
          · Fallo  → alguien más lo tiene → seguimos girando
        time.sleep(0) cede la CPU en cada vuelta (yield).
        """
        if _CAS_WIN is not None:
            while True:
                # Retorna el valor ANTERIOR; si era 0 → éxito
                if _CAS_WIN(ctypes.byref(self._v), 1, 0) == 0:
                    return
                time.sleep(0)
        elif _CAS_UNIX is not None:
            esperado = ctypes.c_int(0)
            while True:
                esperado.value = 0
                if _CAS_UNIX(ctypes.byref(self._v), ctypes.byref(esperado),
                             1, False, 5, 5):
                    return
                time.sleep(0)
        else:
            self._fb.acquire()

    def release(self):
        """
        Libera el lock escribiendo 0 en la variable de estado.

        En x86/ARM una escritura de 32 bits alineada es atómica
        a nivel de hardware, por lo que no se necesita otra instrucción CAS.
        """
        if _CAS_WIN is not None:
            self._v.value = 0
        elif _CAS_UNIX is not None:
            self._v.value = 0
        else:
            self._fb.release()


# ════════════════════════════════════════════════════════════════════════
# BLOQUE 2: Semáforo — implementado desde cero usando SpinLock
# ════════════════════════════════════════════════════════════════════════
#
# ¿Qué es un semáforo?
#   Un contador entero no negativo con DOS operaciones atómicas:
#
#     wait()   (también llamada P, down, acquire):
#       Si contador > 0  →  decrementa y continúa (sin bloqueo)
#       Si contador == 0 →  el hilo queda BLOQUEADO hasta que alguien
#                           haga signal y el contador vuelva a ser > 0.
#
#     signal() (también llamada V, up, release):
#       Incrementa el contador.
#       Si había hilos bloqueados en wait() → desbloquea UNO de ellos.
#
#   Diferencia con mutex:
#     Un mutex es un semáforo binario (0 o 1) donde SOLO el hilo que
#     hizo acquire puede hacer release.
#     Un semáforo general puede tener valor > 1 y cualquier hilo
#     puede hacer signal (incluso uno diferente al que hizo wait).
#
# Implementación aquí:
#   contador   → cuántos hilos más pueden entrar sin bloquearse
#   _lock      → SpinLock que protege el acceso al contador
#   _esperando → lista de eventos (threading.Event) de hilos bloqueados
#
#   Usamos threading.Event solo como mecanismo de PAUSA del hilo
#   (event.wait() bloquea; event.set() desbloquea).
#   El control de quién entra, cuándo y en qué orden lo maneja
#   NUESTRO código, no la stdlib.
# ════════════════════════════════════════════════════════════════════════

class Semaforo:
    """
    Semáforo de conteo implementado desde cero.

    Usa SpinLock propio para proteger el contador y threading.Event
    como mecanismo de pausa/reanudación de hilos bloqueados.

    Parameters
    ----------
    valor_inicial : int
        Valor inicial del contador (cuántos hilos pueden entrar sin bloquearse).
    """

    def __init__(self, valor_inicial: int = 1):
        """Inicializa el semáforo con el valor dado."""
        if valor_inicial < 0:
            raise ValueError("El valor inicial del semáforo no puede ser negativo")

        # El contador determina cuántos hilos pueden pasar sin bloquearse.
        # Si es 1 → semáforo binario (comportamiento similar a mutex).
        # Si es N → hasta N hilos pueden estar en la sección crítica.
        self._contador  = valor_inicial
        self._lock      = SpinLock()   # protege el acceso a _contador y _esperando
        self._esperando = []           # cola de eventos de hilos bloqueados

    def wait(self, nombre_hilo: str = "") -> None:
        """
        Operación WAIT (también llamada P, down o acquire).

        Si el contador es > 0: lo decrementa y retorna inmediatamente.
        Si el contador es 0:   el hilo se BLOQUEA hasta recibir un signal.

        Parameters
        ----------
        nombre_hilo : str
            Nombre del hilo llamante (solo para los prints de diagnóstico).
        """
        # Creamos el evento ANTES de adquirir el lock para tenerlo listo
        # en caso de que necesitemos bloquearnos.
        mi_evento = threading.Event()

        self._lock.acquire()
        try:
            if self._contador > 0:
                # Hay "cupo" disponible → entramos sin bloquearnos
                self._contador -= 1
                # No necesitamos el evento → lo descartamos
                return
            else:
                # No hay cupo → nos ponemos en la cola de espera
                # y dejaremos que signal() nos desbloquee
                self._esperando.append(mi_evento)
                if nombre_hilo:
                    print(f"  ⏸  {nombre_hilo} hace WAIT "
                          f"→ semáforo=0, queda BLOQUEADO...")
                    sys.stdout.flush()
        finally:
            # Liberamos el spinlock ANTES de bloquearnos en el evento.
            # Si no lo hiciéramos, el hilo que intente hacer signal()
            # quedaría atrapado esperando este mismo spinlock → deadlock.
            self._lock.release()

        # Aquí el hilo se BLOQUEA hasta que signal() llame a event.set()
        mi_evento.wait()

    def signal(self, nombre_hilo: str = "") -> None:
        """
        Operación SIGNAL (también llamada V, up o release).

        Incrementa el contador. Si hay hilos bloqueados en wait(),
        desbloquea al primero de la cola (FIFO) en lugar de incrementar.

        Parameters
        ----------
        nombre_hilo : str
            Nombre del hilo llamante (solo para los prints de diagnóstico).
        """
        self._lock.acquire()
        try:
            if self._esperando:
                # Hay al menos un hilo bloqueado → lo despertamos
                # El contador NO se incrementa porque el cupo va directo
                # al hilo que estaba esperando.
                evento_siguiente = self._esperando.pop(0)   # FIFO
                if nombre_hilo:
                    print(f"  ▶  {nombre_hilo} hace SIGNAL "
                          f"→ desbloquea al siguiente en cola")
                    sys.stdout.flush()
                # set() desbloquea el event.wait() del hilo esperando
                evento_siguiente.set()
            else:
                # Nadie espera → simplemente incrementamos el contador
                self._contador += 1
                if nombre_hilo:
                    print(f"  ▶  {nombre_hilo} hace SIGNAL "
                          f"→ semáforo={self._contador} (nadie esperaba)")
                    sys.stdout.flush()
        finally:
            self._lock.release()

    @property
    def valor(self) -> int:
        """Retorna el valor actual del contador (solo para diagnóstico)."""
        self._lock.acquire()
        try:
            return self._contador
        finally:
            self._lock.release()


# ════════════════════════════════════════════════════════════════════════
# BLOQUE 3: FASE 1 — Demostración explícita de WAIT/SIGNAL bloqueante
# ════════════════════════════════════════════════════════════════════════
#
# Aquí creamos 3 hilos que compiten por un semáforo con capacidad = 1.
# Solo UNO puede estar adentro a la vez. Los otros dos quedarán
# BLOQUEADOS en wait() y serán desbloqueados uno por uno cuando el
# hilo que está adentro haga signal().
#
# El retardo artificial (time.sleep) dentro de la sección crítica
# hace visible que los otros hilos esperan de verdad.
# ════════════════════════════════════════════════════════════════════════

def tarea_con_semaforo(nombre: str, semaforo: Semaforo,
                       duracion_trabajo: float) -> None:
    """
    Simula una tarea que necesita acceso exclusivo a un recurso protegido
    por un semáforo. Muestra explícitamente el bloqueo y desbloqueo.

    Parameters
    ----------
    nombre : str
        Nombre del hilo (para los mensajes de diagnóstico).
    semaforo : Semaforo
        Semáforo compartido que controla el acceso al recurso.
    duracion_trabajo : float
        Segundos que el hilo "trabaja" dentro de la sección crítica.
    """
    print(f"  →  {nombre} llegó, intenta hacer WAIT al semáforo "
          f"(valor actual={semaforo.valor})")
    sys.stdout.flush()

    # ── WAIT: intenta entrar a la sección crítica ────────────────────────
    # Si el semáforo es 0, este hilo se BLOQUEA aquí hasta recibir signal.
    semaforo.wait(nombre_hilo=nombre)

    # Si llegamos aquí, el semáforo nos dejó pasar (contador era > 0,
    # o fuimos desbloqueados por un signal de otro hilo).
    print(f"  ✓  {nombre} ENTRÓ a la sección crítica "
          f"— trabajando {duracion_trabajo:.1f}s...")
    sys.stdout.flush()

    # Simulamos trabajo dentro de la sección crítica.
    # Durante este tiempo, cualquier otro hilo que intente wait() quedará bloqueado.
    time.sleep(duracion_trabajo)

    print(f"  ✗  {nombre} terminó su trabajo, sale y hace SIGNAL")
    sys.stdout.flush()

    # ── SIGNAL: libera el semáforo para el siguiente hilo bloqueado ──────
    semaforo.signal(nombre_hilo=nombre)


# ════════════════════════════════════════════════════════════════════════
# BLOQUE 4: FASE 2 — Productores (hilos) + Consumidor (proceso hijo) + PIPE
# ════════════════════════════════════════════════════════════════════════
#
# Los productores usan un SpinLock (no semáforo) para acceso exclusivo
# al pipe. La diferencia con el semáforo es que aquí el propósito es
# evitar corrupción de datos (mutex), no limitar concurrencia por cupo.
# ════════════════════════════════════════════════════════════════════════

def productor(id_hilo: int, conn_escritura,
              mutex: SpinLock, semaforo_pipe: Semaforo) -> None:
    """
    Hilo productor que genera mensajes y los envía por el pipe.

    Usa semaforo_pipe (capacidad=1) para acceso exclusivo al pipe,
    demostrando que el bloqueo WAIT/SIGNAL también protege el recurso
    compartido en este contexto.

    Parameters
    ----------
    id_hilo : int
        Identificador del hilo (1, 2 o 3).
    conn_escritura : multiprocessing.Connection
        Extremo de escritura del pipe, compartido entre los 3 hilos.
    mutex : SpinLock
        SpinLock alternativo (no usado en el envío principal, solo referencia).
    semaforo_pipe : Semaforo
        Semáforo con valor=1 que protege el acceso al pipe.
    """
    random.seed(id_hilo * 1337 + int(time.time()))

    for i in range(3):
        numero  = random.randint(10, 99)
        mensaje = f"Prod-{id_hilo} | msg #{i+1} | dato={numero}"

        # Simula trabajo de generación del mensaje
        time.sleep(random.uniform(0.05, 0.3))

        # ── SECCIÓN CRÍTICA: acceso exclusivo al pipe vía semáforo ──────
        # Usamos semáforo en lugar de spinlock para mostrar que sirve
        # también como mutex (semáforo binario con valor inicial = 1).
        semaforo_pipe.wait(nombre_hilo=f"Prod-{id_hilo}")
        try:
            conn_escritura.send(mensaje)
        finally:
            semaforo_pipe.signal(nombre_hilo=f"Prod-{id_hilo}")
        # ── FIN SECCIÓN CRÍTICA ──────────────────────────────────────────

    # Señal de fin
    semaforo_pipe.wait(nombre_hilo=f"Prod-{id_hilo}")
    try:
        conn_escritura.send(f"FIN-{id_hilo}")
    finally:
        semaforo_pipe.signal(nombre_hilo=f"Prod-{id_hilo}")


def consumidor(conn_lectura, num_productores: int) -> None:
    """
    Proceso hijo consumidor. Lee mensajes del pipe hasta recibir
    una señal FIN por cada productor.

    Parameters
    ----------
    conn_lectura : multiprocessing.Connection
        Extremo de lectura del pipe.
    num_productores : int
        Cantidad de productores esperados.
    """
    fines_recibidos    = 0
    mensajes_recibidos = 0

    print(f"\n      [CONSUMIDOR pid={os.getpid()}] Listo, esperando mensajes...\n")
    sys.stdout.flush()

    while fines_recibidos < num_productores:
        try:
            # recv() bloquea al proceso hijo hasta que llegue un mensaje
            mensaje = conn_lectura.recv()
        except EOFError:
            break   # el padre cerró la conexión

        if mensaje.startswith("FIN"):
            fines_recibidos += 1
            print(f"      [CONSUMIDOR] Señal fin "
                  f"({fines_recibidos}/{num_productores}): {mensaje}")
        else:
            mensajes_recibidos += 1
            print(f"      [CONSUMIDOR] ✓ [{mensajes_recibidos:02d}] {mensaje}")

        sys.stdout.flush()

    print(f"\n      [CONSUMIDOR] Finalizado. Mensajes recibidos: {mensajes_recibidos}")
    sys.stdout.flush()


# ════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    multiprocessing.freeze_support()   # necesario si se empaqueta con PyInstaller

    NUM_PRODUCTORES = 3

    # ── ENCABEZADO ───────────────────────────────────────────────────────
    print("=" * 68)
    print("  SISTEMAS OPERATIVOS — Procesos · Pipes · SpinLock · Semáforo")
    print(f"  Plataforma: {sys.platform}  |  Python {sys.version.split()[0]}")
    print("=" * 68)

    if _CAS_WIN:
        modo_cas = "InterlockedCompareExchange (kernel32 / Win32)"
    elif _CAS_UNIX:
        modo_cas = "__atomic_compare_exchange_n (libc / GCC)"
    else:
        modo_cas = "fallback threading.Lock"
    print(f"  CAS utilizado: {modo_cas}\n")

    # ════════════════════════════════════════════════════════════════════
    # FASE 1: Demostración de WAIT / SIGNAL con bloqueo visible
    # ════════════════════════════════════════════════════════════════════
    print("═" * 68)
    print("  FASE 1 — Demostración de WAIT / SIGNAL bloqueante")
    print("═" * 68)
    print("""
  Creamos un semáforo con valor inicial = 1 (solo 1 hilo puede entrar).
  Lanzamos 3 hilos casi al mismo tiempo. El primero en llegar hace WAIT,
  entra, y los otros DOS quedan BLOQUEADOS. Cuando el primero hace SIGNAL,
  desbloquea al siguiente; y así sucesivamente.

  Esto demuestra que sin sincronización dos hilos entrarían a la vez
  y corromperían el recurso compartido.
""")

    # Semáforo binario: capacidad = 1 → solo un hilo adentro a la vez
    sem_fase1 = Semaforo(valor_inicial=1)

    # Los tres hilos arrancan casi simultáneamente.
    # Usamos duraciones distintas para hacer visible quién entra y quién espera.
    configuraciones = [
        ("Hilo-A", 2.0),   # entra primero, trabaja 2 s → los demás esperan
        ("Hilo-B", 1.0),   # bloqueado hasta que A haga signal
        ("Hilo-C", 0.5),   # bloqueado hasta que B haga signal
    ]

    hilos_fase1 = []
    for nombre, duracion in configuraciones:
        t = threading.Thread(
            target=tarea_con_semaforo,
            args=(nombre, sem_fase1, duracion),
            name=nombre
        )
        hilos_fase1.append(t)

    print("  Lanzando los 3 hilos...")
    print("─" * 68)
    for t in hilos_fase1:
        t.start()
        time.sleep(0.05)   # pequeño retardo para que lleguen en orden A→B→C

    for t in hilos_fase1:
        t.join()

    print("─" * 68)
    print("  ✓ FASE 1 completada. Los 3 hilos pasaron de a uno por vez.\n")

    # ════════════════════════════════════════════════════════════════════
    # FASE 2: Productores (hilos) → Pipe → Consumidor (proceso hijo)
    # ════════════════════════════════════════════════════════════════════
    print("═" * 68)
    print("  FASE 2 — Productores / PIPE / Consumidor")
    print("═" * 68)
    print(f"""
  Creamos {NUM_PRODUCTORES} hilos productores en el proceso padre y un proceso
  hijo consumidor. Se comunican por un PIPE unidireccional.
  El acceso al pipe está protegido por un SEMÁFORO (valor=1),
  que aquí funciona como mutex: solo un productor escribe a la vez.
  Verás los WAIT y SIGNAL de cada productor antes y después de enviar.
""")

    # Creamos el PIPE
    print("─" * 68)
    print("PASO 1: Creando el PIPE (multiprocessing.Pipe)")
    conn_lectura, conn_escritura = multiprocessing.Pipe(duplex=False)
    print("  → PIPE listo  ✓\n")

    # Semáforo que protege el acceso al pipe (valor=1 → mutex binario)
    print("─" * 68)
    print("PASO 2: Creando el SEMÁFORO para el pipe (valor inicial=1)")
    print("  Con valor=1: solo un productor puede llamar a send() a la vez.")
    print("  Si dos llegan juntos, el segundo hace WAIT y queda bloqueado")
    print("  hasta que el primero termina de enviar y hace SIGNAL.")
    sem_pipe = Semaforo(valor_inicial=1)
    mutex_ref = SpinLock()   # SpinLock de referencia (no se usa en el envío principal)
    print("  → Semáforo listo  ✓\n")

    # Creamos el proceso hijo
    print("─" * 68)
    print("PASO 3: Creando el proceso HIJO (consumidor)")
    proceso_hijo = multiprocessing.Process(
        target=consumidor,
        args=(conn_lectura, NUM_PRODUCTORES),
        name="Consumidor",
        daemon=False
    )
    proceso_hijo.start()
    conn_lectura.close()   # el padre cierra su copia de lectura
    print(f"  → Proceso hijo pid={proceso_hijo.pid}  ✓\n")

    # Lanzamos los hilos productores
    print("─" * 68)
    print(f"PASO 4: Lanzando {NUM_PRODUCTORES} hilos productores")
    print("  Cada vez que un productor quiera enviar, hará WAIT al semáforo.")
    print("  Si otro ya está enviando, quedará BLOQUEADO hasta el SIGNAL.\n")

    hilos_prod = []
    for i in range(1, NUM_PRODUCTORES + 1):
        t = threading.Thread(
            target=productor,
            args=(i, conn_escritura, mutex_ref, sem_pipe),
            name=f"Prod-{i}",
            daemon=True
        )
        hilos_prod.append(t)
        t.start()
        print(f"  → Prod-{i} iniciado  (tid={t.native_id})")

    print()

    # Esperamos que terminen los productores
    print("─" * 68)
    print("PASO 5: Esperando que terminen los productores (join)\n")
    for t in hilos_prod:
        t.join()
        print(f"  → {t.name} terminó  ✓")

    # Cerramos el pipe → el consumidor recibirá EOF
    print()
    print("─" * 68)
    print("PASO 6: Cerrando conn_escritura → el consumidor recibirá EOF\n")
    conn_escritura.close()

    # Esperamos al proceso hijo
    print("─" * 68)
    print(f"PASO 7: Esperando al proceso HIJO (pid={proceso_hijo.pid})\n")
    proceso_hijo.join()
    print(f"  → Proceso hijo terminó (código={proceso_hijo.exitcode})  ✓\n")

    # ── RESUMEN FINAL ─────────────────────────────────────────────────────
    print("=" * 68)
    print("  DEMOSTRACIÓN COMPLETADA")
    print("=" * 68)
    print("""
Conceptos demostrados:

  SpinLock (mutex):
    · Variable 0/1 protegida con CAS atómico nativo (kernel32 / libc)
    · acquire() gira en busy-wait hasta que el lock está libre
    · release() escribe 0 y el próximo hilo en spin puede entrar

  Semáforo (implementado con SpinLock + threading.Event):
    · wait()  → si contador=0, el hilo se BLOQUEA (event.wait)
    · signal() → si hay hilos bloqueados, desbloquea UNO (event.set)
    · Con valor_inicial=1 actúa como mutex binario
    · Con valor_inicial=N permite N hilos simultáneos

  Pipe (multiprocessing.Pipe):
    · Canal unidireccional entre proceso padre e hijo
    · send() / recv() son las únicas operaciones inter-proceso

  Procesos e hilos:
    · multiprocessing.Process → proceso hijo con memoria propia
    · threading.Thread        → hilos que comparten memoria del padre
    · La guardia __main__ es obligatoria en Windows (método spawn)
""")