El parser (es un parser LL(1)) toma el archivo "dibujo.txt" para poner todas las instrucciones en una lista y luego las interpreta. El interprete esta en "maquinaDibujar.js"

El programa principal esta en "sketch.js". Las funciones principales son "setup()" y "draw()". Estas son funciones de p5.js, la primera se ejecuta al comenzar y la segunda se ejecuta en loop (es la usada para mostrar.)

Miren que les parece.

Sería bueno poder mostrar la cuadricula en 3D y dibujar cubos apilados.
Es decir, permitir apilar cubos. Moverse por la cuadricula con las direcciones y en vez de dibujar seria una instruccion de colocar un cubo. Poner dos cubos en la misma cuadricula apila el primero arriba del segundo.
Cada lugar de la cuadricula tenga cero o mas cubos.
Luego dibujar eso. Las imagenes son ejemplos de lo que buscamos y el juego que implementa la idea (pero solo con cubos por ahora y en blanco y negro).

Y paso una presentacion sobre como usamos dibujar en la cuadricula para enseñar a programar.