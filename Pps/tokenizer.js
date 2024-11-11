/********************************************************/
/* DC-FCEFQyN-UNRC                                      */
/* Tokenizer de lenguaje de la Maquina de dibujar en la    */
/* cuadricula                                            */
/*  2024                                                */
/********************************************************/

const TokenTypes = {
    NUMBER: "NUMBER",
    ARRIBA: "ARRIBA",
    ABAJO: "ABAJO",
    IZQUIERDA: "IZQUIERDA",
    DERECHA: "DERECHA",
    FRENTE: "FRENTE", // Nuevo token para mover hacia adelante en z
    ATRAS: "ATRAS",   // Nuevo token para mover hacia atrás en z
    PINTAR: "PINTAR",
    REPETIR: "REPEAT",
    FUNCTION: "FUNCTION",
    IDENTIFIER: "IDENTIFIER",
    COLON: ",",
    SEMICOLON: ";",
    PLUS: "+",
    MINUS: "-",
    MULTIPLY: "*",
    DIVIDE: "/",
    EXP: "^",
    PARENTHESIS_LEFT: "(",
    PARENTHESIS_RIGHT: ")",
    BRACES_LEFT: "{",
    BRACES_RIGHT: "}",
    NEWLINE: "\n"
};

const TokenSpecials = [
    [/^\n/, TokenTypes.NEWLINE],
    [/^\s+/, null],
    [/^(?:\d+(?:\.\d*)?|\.\d+)/, TokenTypes.NUMBER],
    [/^arriba\(\)/, TokenTypes.ARRIBA],
    [/^abajo\(\)/, TokenTypes.ABAJO],
    [/^izquierda\(\)/, TokenTypes.IZQUIERDA],
    [/^derecha\(\)/, TokenTypes.DERECHA],
    [/^frente\(\)/, TokenTypes.FRENTE],   // Nueva expresión regular para frente
    [/^atras\(\)/, TokenTypes.ATRAS],     // Nueva expresión regular para atrás
    [/^pintar\(\)/, TokenTypes.PINTAR],
    [/^repetir/, TokenTypes.REPEAT],
    [/^function/, TokenTypes.FUNCTION],
    [/^[a-z]+/, TokenTypes.IDENTIFIER],
    [/^\,/, TokenTypes.COLON],
    [/^\;/, TokenTypes.SEMICOLON],
    [/^\+/, TokenTypes.PLUS],
    [/^\-/, TokenTypes.MINUS],
    [/^\*/, TokenTypes.MULTIPLY],
    [/^\//, TokenTypes.DIVIDE],
    [/^\^/, TokenTypes.EXP],
    [/^\(/, TokenTypes.PARENTHESIS_LEFT],
    [/^\)/, TokenTypes.PARENTHESIS_RIGHT],
    [/^\{/, TokenTypes.BRACES_LEFT],
    [/^\}/, TokenTypes.BRACES_RIGHT]
];

class Tokenizer {

    constructor(input1) {
        this.input = input1;
        this.cursor = 0;
        this.line = 1;
    }

    thereIsMore() { // check if there are more tokens in the input to be processed
        return this.cursor < this.input.length;
    }

    match(regex, inputText) { // return a match if the regex matches the input text
        const m = regex.exec(inputText)
        if (m == null) {
            return null;
        }
        this.cursor += m[0].length;
        return m[0];
    }

    getNext() { // retrieve the next token
        if (!this.thereIsMore()) { // if true there are more tokens in the input to be processed
            return null;
        }
        const inputText = this.input.slice(this.cursor); // slice function to lool at the remaining text

        for (let [regex, type] of TokenSpecials) {
            const tokenValue = this.match(regex, inputText);

            if (tokenValue === null) {
                continue;
            }
            if (type === null) {
                return this.getNext();
            }
            if (type === TokenTypes.NEWLINE) {
                this.line++;
                //continue; 
                return this.getNext();
            }
            return {
                type,
                value: tokenValue,
                line: this.line,
            }
        }

        throw new SyntaxError(`Unexpected token: "${inputText[0]}" at line "${this.line}"`);
    }
}