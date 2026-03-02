/********************************************************/
/* DC-FCEFQyN-UNRC                                      */
/* Parser de lenguaje de la Maquina de dibujar en la    */
/* cuadricula                                           */
/*  2024                                                */
/********************************************************/

/** Gramática del lenguaje:

 Program = Function+
 Function = "function" "(" (IDENTIFIER ",")* ")" Block 
 Block = "{" Instr+  "}"
 Instr = "arriba();" | "abajo();" | "izquierda();" | "derecha();" | "pintar();" |  Repeat | Call
 Repeat = "repetir" "(" ( NUMBER | IDENTIFIER ) ")" Block 
 Call = IDENTIFIER "(" ( ( NUMBER | IDENTIFIER ) "," )* ");"
 
 Es obligatorio la definición de al menos una función (la función "main")
 
 El parser traduce los programas a una secuencia de primitivas
*/

class Parser {

    parse(input) { //GENERA UN NUEVO TOKEN, INPUT y TOMA EL SIGUIENTE TOKEN devuelve un programa

        this.input = input;
        this.tokenizer = new Tokenizer(input);
        this.lookhead = this.tokenizer.getNext();

        this.symbolTable = [];

        let result = this.Program();

        //console.log("Symbol Table"+this.symbolTable.length);
        //this.symbolTable.forEach((element) => console.log(element.name+" "+element.param+" "+element.body));

        return result;
    }

    parseBlock(input, TS) {//GENERA UN NUEVO TOKEN, INPUT y TOMA EL SIGUIENTE TOKEN devuelve un bloque

        this.input = input;
        this.tokenizer = new Tokenizer(input);
        this.lookhead = this.tokenizer.getNext();

        this.symbolTable = TS;

        let result = this.Block();

        //console.log("Symbol Table"+this.symbolTable.length);
        //this.symbolTable.forEach((element) => console.log(element.name+" "+element.param+" "+element.body));

        return result;
    }

    consume(tokenType) { //CONTROLA EL TOKEN Y LO CAMBIA AL SIGUIENTE
        const token = this.lookhead;

        if (token == null) {
            throw new SyntaxError(`Unexpected EOF, expected: "${tokenType}"`);
        }
        if (token.type !== tokenType) {
            throw new SyntaxError(`Unexpected token: "${token.value}", expected "${tokenType}" at line "${token.line}"`);
        }

        this.lookhead = this.tokenizer.getNext();

        return token;
    }

    Program() {// PARSEA EL BLOQUE DE LA FUNCION MAIN 
        this.Function();

        const findFun = this.symbolTable.find(x => x.name === "main");

        if (findFun) {
            let result = this.parseBlock(findFun.body, this.symbolTable);
            return result;
        } else {
            throw new Error(`Undefined function: main`);
        }

    }

    Function() {
        while (this.lookhead && this.lookhead.type === TokenTypes.FUNCTION) {
            this.consume(TokenTypes.FUNCTION);
            let nameFunction = this.consume(TokenTypes.IDENTIFIER).value;
            this.consume(TokenTypes.PARENTHESIS_LEFT);
            let paramsArray = this.paramsForm();
            this.consume(TokenTypes.PARENTHESIS_RIGHT);

            const findFun = this.symbolTable.find(x => x.name === nameFunction);
            if (findFun) {
                throw new Error(`Redefined function: "${nameFunction}"`);
            }

            let blockString = this.BlockFun();
            this.symbolTable.push({ name: nameFunction, param: paramsArray, body: blockString });
        }
    }

    Block() { //
        let result = "";
        this.consume(TokenTypes.BRACES_LEFT);

        while (this.lookhead && !(this.lookhead.type === TokenTypes.BRACES_RIGHT)) {
            const token = this.consume(this.lookhead.type)
            const instr = token.type;
            switch (instr) {
                case TokenTypes.ARRIBA:
                    //   this.consume(TokenTypes.ARRIBA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "arriba();";
                    break;
                case TokenTypes.ABAJO:
                    //  this.consume(TokenTypes.ABAJO);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "abajo();";
                    break;
                case TokenTypes.IZQUIERDA:
                    //  this.consume(TokenTypes.IZQUIERDA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "izquierda();";
                    break;
                case TokenTypes.DERECHA:
                    //   this.consume(TokenTypes.DERECHA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "derecha();";
                    break;
                case TokenTypes.PINTAR:
                    //   this.consume(TokenTypes.DERECHA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "pintar();";
                    break;
                case TokenTypes.REPEAT:
                    //   this.consume(TokenTypes.REPEAT);
                    this.consume(TokenTypes.PARENTHESIS_LEFT);

                    let cond = this.condRepeat();

                    this.consume(TokenTypes.PARENTHESIS_RIGHT);
                    let bodyRep = this.Block();
                    result = result + bodyRep.repeat(cond);
                    break;
                case TokenTypes.IDENTIFIER:
                    const nameFunction = token.value;
                    this.consume(TokenTypes.PARENTHESIS_LEFT);

                    let params = this.paramsAct();

                    this.consume(TokenTypes.PARENTHESIS_RIGHT);
                    this.consume(TokenTypes.SEMICOLON);

                    const findFun = this.symbolTable.find(x => x.name === nameFunction);

                    let bodyNew = "";

                    if (findFun) {
                        if (findFun.param.length === params.length) {
                            bodyNew = this.replaceParams(findFun.body, findFun.param, params);
                        } else {
                            throw new Error(`Number of parameters does not match for the function: "${nameFunction}"`);
                        }
                    } else {
                        throw new Error(`Undefined function: "${nameFunction}"`);
                    }

                    result = result + bodyNew;
                    break;
            }
        }

        this.consume(TokenTypes.BRACES_RIGHT);

        return result;
    }

    BlockFun() {
        let result = "{";
        this.consume(TokenTypes.BRACES_LEFT);

        while (this.lookhead && !(this.lookhead.type === TokenTypes.BRACES_RIGHT)) {
            const token = this.consume(this.lookhead.type)
            const instr = token.type;
            switch (instr) {
                case TokenTypes.ARRIBA:
                    //   this.consume(TokenTypes.ARRIBA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "arriba();";
                    break;
                case TokenTypes.ABAJO:
                    //  this.consume(TokenTypes.ABAJO);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "abajo();";
                    break;
                case TokenTypes.IZQUIERDA:
                    //  this.consume(TokenTypes.IZQUIERDA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "izquierda();";
                    break;
                case TokenTypes.DERECHA:
                    //   this.consume(TokenTypes.DERECHA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "derecha();";
                    break;
                case TokenTypes.PINTAR:
                    //   this.consume(TokenTypes.DERECHA);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + "pintar();";
                    break;
                case TokenTypes.REPEAT:
                    //   this.consume(TokenTypes.REPEAT);
                    this.consume(TokenTypes.PARENTHESIS_LEFT);

                    let cond = this.condRepeat();

                    this.consume(TokenTypes.PARENTHESIS_RIGHT);
                    let bodyRep = this.BlockFun();
                    result = result + "repetir(" + cond + ")" + bodyRep;
                    break;
                case TokenTypes.IDENTIFIER:
                    const nameFunction = token.value;
                    this.consume(TokenTypes.PARENTHESIS_LEFT);

                    // const findFun = this.symbolTable.find(x=> x.name === nameFunction);                        //   if (!findFun){
                    //     throw new Error(`Undefined function: "${nameFunction}"`);
                    // } 

                    let params = this.paramsAct();

                    this.consume(TokenTypes.PARENTHESIS_RIGHT);
                    this.consume(TokenTypes.SEMICOLON);
                    result = result + nameFunction + "(" + params + ");";
                    break;
            }
        }
        this.consume(TokenTypes.BRACES_RIGHT);
        return result + "}";
    }

    paramsForm() {
        let result = [];
        while (this.lookhead && !(this.lookhead.type === TokenTypes.PARENTHESIS_RIGHT)) {
            const nameParam = this.consume(TokenTypes.IDENTIFIER).value;
            if (this.lookhead.type === TokenTypes.COLON) {
                this.consume(TokenTypes.COLON);
            }
            result.push(nameParam); // controlar redeclaracion de param
        }
        return result;
    }

    paramsAct() {
        let result = [];
        while (this.lookhead && !(this.lookhead.type === TokenTypes.PARENTHESIS_RIGHT)) {
            let param = "";
            if (this.lookhead.type === TokenTypes.IDENTIFIER) {
                param = this.consume(TokenTypes.IDENTIFIER).value;
            } else {
                if (this.lookhead.type === TokenTypes.NUMBER) {
                    param = this.consume(TokenTypes.NUMBER).value;
                }
            }
            if (this.lookhead.type === TokenTypes.COLON) {
                this.consume(TokenTypes.COLON);
            }
            result.push(param);
        }
        return result;
    }

    condRepeat() {
        let result = "";
        if (this.lookhead) {
            if (this.lookhead.type === TokenTypes.IDENTIFIER) {
                result = this.consume(TokenTypes.IDENTIFIER).value;
            } else {
                //if (this.lookhead.type === TokenTypes.NUMBER){ 
                result = this.consume(TokenTypes.NUMBER).value;
                //}  
            }
        }
        return result;
    }

    replaceParams(body, paramsForm, paramsAct) {
        let result = body;

        //iterar en los parametros por indice reemplazando 
        // el nesimo parametroForm por el enesimo parametro act en body

        for (var i = 0; i <= paramsForm.length; i++) {
            result = result.replaceAll(paramsForm[i] + ",", paramsAct[i] + ",");
            result = result.replaceAll(paramsForm[i] + "\)", paramsAct[i] + "\)");
        }

        const parserAux = new Parser();
        result = parserAux.parseBlock(result, this.symbolTable);

        return result;
    }

}