/********************************************************/
/* DC-FCEFQyN-UNRC                                      */
/* Interprete de programa para la Maquina de dibujar en */
/* la cuadricula                                        */
/*  2024                                                */
/********************************************************/

/**
  Conjunto de instrucciones
  izquierda() : mueve el cursor 1 paso a la izquierda
  derecha() : mueve el cursor 1 paso a la derecha
  abajo() : mueve el cursor 1 paso hacia abajo
  arriba() : mueve el cursor 1 paso hacia abajo
  pintar() : pinta en color gris la posición actual del cursor
 
*/


var posx;
var posy;
var posz; // Nueva posición del cursor en el eje z
var nroInst = 0;
var cuadricula = {}; // Cambiar a objeto para usar coordenadas 3D como claves
var instrucciones = [];

// Posición inicial del cursor en 3D
function inicPosCursor() {
    posx = 10;
    posy = 10;
    posz = 10; // Nueva posición inicial en el eje z
}

// Mover el cursor en 3D
function derecha() { posx += 1; }
function izquierda() { posx -= 1; }
function abajo() { posy += 1; }
function arriba() { posy -= 1; }
function frente() { posz += 1; }  // Nueva función para mover hacia adelante en z
function atras() { posz -= 1; }   // Nueva función para mover hacia atrás en z

// Pinta en la posición actual (3D)
function pintar() {
    cuadricula[`${posx},${posy},${posz}`] = 1; // Guardar en la posición 3D
}

// Ejecuta la instruccion corriente (la instrucción nroInst)
function ejecutarInstruccion() {
    if (nroInst == (instrucciones.length)) noLoop();
    else {
        try {
            eval(instrucciones[nroInst]);
        } catch (e) {
            console.log(e);
        }
        console.log("Instrucción " + (nroInst + 1) + " : " + instrucciones[nroInst]);
        nroInst++;
    }
}

// Dibujar la cuadricula en 3D
function dibujarEnLaCuadricula() {
    for (let key in cuadricula) {
        if (cuadricula[key] === 1) {
            const [i, j, k] = key.split(',').map(Number);
            // Ajusta el cubo en 3D
            push();
            translate((i - 1) * 25, (j - 1) * 25, (k - 1) * 25);
            box(25); // Dibuja un cubo en lugar de un rectángulo
            pop();
        }
    }
}

// Inicializa la cuadricula sin dibujo
function inicializarCuadricula() {
    for (var i = 0; i < 20; i++) {
        for (var j = 0; j < 20; j++) {
            cuadricula[[i, j]] = 0;
        }
    }
}

// Imprimir cuadrícula en 3D
function dibujarCuadricula() {
    // Dibuja las líneas de la cuadrícula en un plano 3D
    for (var i = 0; i <= 500; i += 25) {
        for (var j = 0; j <= 500; j += 25) {
            line(i, 0, 0, i, 500, 0);    // eje X-Y
            line(0, i, 0, 0, i, 500);    // eje Y-Z
            line(0, 0, i, 500, 0, i);    // eje X-Z
        }
    }
}

// Modifica posicionarCursor() para mostrar la posición en 3D
function posicionarCursor() {
    push();
    fill(255, 204, 0);
    translate(posx * 25 - 12.5, posy * 25 - 12.5, posz * 25 - 12.5);
    sphere(10); // Dibuja una esfera pequeña en lugar de un círculo
    pop();
}

/* Activar loop de draw con click mouse*/
function mousePressed() {
    loop();
    // save("dibujo.tif");
}

function repetir(n) {
    return 0;
}