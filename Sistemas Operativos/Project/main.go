package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"os/exec"
	"sync/atomic"
	"syscall"
	"time"
)

// SpinLock manual (mutex desde cero con atomic)
type SpinLock struct {
	state uint32 // 0 = libre, 1 = ocupado
}

func (l *SpinLock) Lock() {
	for !atomic.CompareAndSwapUint32(&l.state, 0, 1) {
		// spin (busy-wait)
		// Podemos agregar runtime.Gosched() para ceder, pero para demo puro spin
	}
}

func (l *SpinLock) Unlock() {
	atomic.StoreUint32(&l.state, 0)
}

// Estructura para pasar argumentos a goroutine productor
type ProducerArgs struct {
	id     int
	writer *os.File
	lock   *SpinLock
}

// Goroutine productor (escribe en el pipe protegido por spinlock)
func producer(args ProducerArgs) {
	rand.Seed(time.Now().UnixNano() + int64(args.id))

	for i := 0; i < 5; i++ { // cada productor envía 5 mensajes
		msg := fmt.Sprintf("Mensaje de productor %d: %d\n", args.id, rand.Intn(100))

		time.Sleep(time.Duration(rand.Intn(400)+100) * time.Millisecond) // simula trabajo

		args.lock.Lock()
		fmt.Printf("Productor %d adquirió lock y escribe: %s", args.id, msg)
		_, err := args.writer.WriteString(msg)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error escribiendo: %v\n", err)
		}
		args.writer.Flush() // importante para que el hijo lo vea rápido
		args.lock.Unlock()
	}

	// Enviar FIN
	args.lock.Lock()
	args.writer.WriteString("FIN\n")
	args.writer.Flush()
	args.lock.Unlock()
}

func consumer(reader *os.File) {
	scanner := bufio.NewScanner(reader)
	count := 0

	for scanner.Scan() {
		line := scanner.Text()
		if line == "FIN" {
			continue
		}
		fmt.Printf("Consumidor recibió: %s\n", line)
		count++
		if count >= 10 { // suponiendo 2 productores × 5
			break
		}
	}

	if err := scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "Error leyendo pipe: %v\n", err)
	}
	fmt.Println("Consumidor terminó.")
}

func main() {
	// Crear pipe anónimo (unidireccional)
	r, w, err := os.Pipe()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error creando pipe: %v\n", err)
		os.Exit(1)
	}
	defer r.Close()
	defer w.Close()

	// Crear proceso hijo (consumidor)
	cmd := exec.Command(os.Args[0], "--child")
	cmd.Stdin = r          // el hijo lee del pipe
	cmd.Stdout = os.Stdout // para que vea la salida
	cmd.Stderr = os.Stderr
	cmd.SysProcAttr = &syscall.SysProcAttr{}

	err = cmd.Start()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error fork/exec: %v\n", err)
		os.Exit(1)
	}

	// Proceso padre: cierra lectura, usa escritura
	r.Close()

	// Nuestro mutex manual
	var lock SpinLock

	// Crear 2 goroutines productores
	var producers []ProducerArgs
	for i := 1; i <= 2; i++ {
		args := ProducerArgs{
			id:     i,
			writer: bufio.NewWriter(w), // usamos buffered para mejor perf
			lock:   &lock,
		}
		producers = append(producers, args)
		go producer(args)
	}

	// Esperamos a que terminen los productores (goroutines)
	// En Go real usaríamos sync.WaitGroup, pero para no usar sync...
	// Simulamos una espera burda (mejor usar WG en producción)
	time.Sleep(8 * time.Second) // suficiente para 2×5 mensajes + sleeps

	// Cerramos escritura para que el hijo vea EOF
	w.Close()

	// Esperamos al hijo
	cmd.Wait()
	fmt.Println("Programa principal terminado.")
	os.Exit(0)
}

// Parte que ejecuta el hijo
func init() {
	if len(os.Args) > 1 && os.Args[1] == "--child" {
		// Modo consumidor (hijo)
		consumer(os.Stdin) // lee de stdin (que es el pipe)
		os.Exit(0)
	}
}
