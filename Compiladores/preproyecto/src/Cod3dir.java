public class Cod3dir {
    String opType; // Ass
    Info operando1;
    Info operando2;
    Info result;

    public Cod3dir(String opType, Info operando1, Info operando2, Info result) {
        this.opType = opType;
        this.operando1 = operando1;
        this.operando2 = operando2;
        this.result = result;
    }

    public static String genLine(String opType, Info operando1, Info operando2, Info result) {
        String c1, c2, r;
        r = result.nombre;
        String outputString;
        if (opType == "SUM" || opType == "MUL") {
            if (operando1.etiqueta == 10)
                c1 = operando1.value.toString();
            else
                c1 = operando1.nombre;
            if (operando2.etiqueta == 10)
                c2 = operando2.value.toString();
            else
                c2 = operando2.nombre;
            outputString = (opType + " " + c1 + " " + c2 + " " + r);
        } else if (opType == "ASSGN") {
            c1 = operando1.nombre;
            outputString = (opType + " " + c1 + " # " + r); // MOV
        } else if (opType == "RET") {
            outputString = (opType + " # # " + r);
        } else if (opType.equals("GREATER") || opType.equals("LESS")) {
            // Comparaciones
            c1 = (operando1.etiqueta == 10) ? operando1.value.toString() : operando1.nombre;
            c2 = (operando2.etiqueta == 10) ? operando2.value.toString() : operando2.nombre;
            outputString = (opType + " " + c1 + " " + c2 + " " + r); // Comparación
        } else {
            outputString = "error! opType erroneo!";
        }
        return outputString;
    }

}
