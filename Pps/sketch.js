/********************************************************/
/* DC-FCEFQyN-UNRC                                      */
/* Maquina de dibujar en la cuadricula                  */
/*                                                      */
/*  2024                                                */
/********************************************************/

function setup() {
    createCanvas(500, 520);
    background(999);
    inic();
    fill('black');
    text('Seleccione un archivo con su programa:', 0, 515);
    noLoop()

    createFileInput(openFile);

    loadStrings("dibujo.txt", openf);

}

function openf(archivoIn) {
    inic();
    const parser = new Parser();
    const result = parser.parse(archivoIn.join(" "));
    instrucciones = result.split('\;');

    frameRate(5)
    loop();

}

function openFile(file) {
    inic();

    let aux = "";
    if (file.type === 'text') {
        aux = file.data;
    } else {
        if (file.type === 'application') {
            aux = atob(file.data.replace("data:application/x-javascript;base64,", ""));
        } else {
            throw new Error(`File format error`);
        }
    }

    const parser = new Parser();
    const result = parser.parse(aux);
    instrucciones = result.split('\;');

    frameRate(5)
    loop();
}

function draw() {
    if (isLooping()) {
        background(999);
        fill('black');
        text('Seleccione un archivo con su programa:', 0, 515);

        dibujarCuadricula();
        ejecutarInstruccion();
        dibujarEnLaCuadricula();

    }
    posicionarCursor();
}

function inic() {
    nroInst = 0; // número de instrucción corriente
    cuadricula = [[]]; // Representación de la cuadricula
    instrucciones = []; //
    inicPosCursor();
    inicializarCuadricula();
    dibujarCuadricula();
    posicionarCursor();
}

