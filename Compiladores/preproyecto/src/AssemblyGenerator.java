import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class AssemblyGenerator {

    public static void generateAssembly(List<Cod3dir> cod3dirList) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("assembly.txt"))) {
            // Prologue de la función
            writer.write("main:\n");
            writer.write("pushq %rbp\n");
            writer.write("movq %rsp, %rbp\n");

            // Cuerpo de las instrucciones
            for (Cod3dir c3d : cod3dirList) {

                switch (c3d.opType) {
                    case "SUM":
                        if (isConstant(c3d.operando1)) {
                            writer.write("movq $" + c3d.operando1.value + ", %rax\n");
                        } else {
                            writer.write("movq " + c3d.operando1.offSet + "(%rbp), %rax\n");
                        }

                        if (isConstant(c3d.operando2)) {
                            writer.write("addq $" + c3d.operando2.value + ", %rax\n");
                        } else {
                            writer.write("addq " + c3d.operando2.offSet + "(%rbp), %rax\n");
                        }

                        writer.write("movq %rax, " + c3d.result.offSet + "(%rbp)\n");
                        break;

                    case "ASSGN":
                        if (isConstant(c3d.operando1)) {
                            writer.write("movl $" + c3d.operando1.value + ", " + c3d.result.offSet + "(%rbp)\n");
                        } else {
                            writer.write("movq " + c3d.operando1.offSet + "(%rbp), %rax\n");
                            writer.write("movq %rax, " + c3d.result.offSet + "(%rbp)\n");
                        }
                        break;

                    case "MUL":
                        if (isConstant(c3d.operando1)) {
                            writer.write("movq $" + c3d.operando1.value + ", %rax\n");
                        } else {
                            writer.write("movq " + c3d.operando1.offSet + "(%rbp), %rax\n");
                        }

                        if (isConstant(c3d.operando2)) {
                            writer.write("imulq $" + c3d.operando2.value + ", %rax\n");
                        } else {
                            writer.write("imulq " + c3d.operando2.offSet + "(%rbp), %rax\n");
                        }

                        writer.write("movq %rax, " + c3d.result.offSet + "(%rbp)\n");
                        break;

                    case "RET":
                        // Epilogue de la función
                        writer.write("movq " + c3d.result.offSet + "(%rbp), %rax\n"); // Mueve el resultado a rax
                        writer.write("popq %rbp\n"); // Restaura el base pointer
                        writer.write("ret\n"); // Retorna al llamador
                        break;

                    case "GREATER":
                        // Comparamos los dos operandos
                        if (isConstant(c3d.operando1)) {
                            writer.write("movl $" + c3d.operando1.value + ", %eax\n");
                        } else {
                            writer.write("movl " + c3d.operando1.offSet + "(%rbp), %eax\n");
                        }

                        if (isConstant(c3d.operando2)) {
                            writer.write("cmpl $" + c3d.operando2.value + ", %eax\n");
                        } else {
                            writer.write("cmpl " + c3d.operando2.offSet + "(%rbp), %eax\n");
                        }

                        // Resultado del GREATER
                        writer.write("setg %al\n"); // Si es mayor, se coloca 1 en %al
                        writer.write("movzbl %al, %eax\n"); // Expande el valor de %al a %eax (para asegurarse que todo
                                                            // %eax tiene el valor correcto)
                        writer.write("movl %eax, " + c3d.result.offSet + "(%rbp)\n"); // Guarda el resultado
                        break;

                    case "LESS":
                        // Comparamos los dos operandos
                        if (isConstant(c3d.operando1)) {
                            writer.write("movl $" + c3d.operando1.value + ", %eax\n");
                        } else {
                            writer.write("movl " + c3d.operando1.offSet + "(%rbp), %eax\n");
                        }

                        if (isConstant(c3d.operando2)) {
                            writer.write("cmpl $" + c3d.operando2.value + ", %eax\n");
                        } else {
                            writer.write("cmpl " + c3d.operando2.offSet + "(%rbp), %eax\n");
                        }

                        // Resultado del LESS
                        writer.write("setl %al\n"); // Si es menor, se coloca 1 en %al
                        writer.write("movzbl %al, %eax\n"); // Expande el valor de %al a %eax
                        writer.write("movl %eax, " + c3d.result.offSet + "(%rbp)\n"); // Guarda el resultado
                        break;

                    // Otros casos como "/" y más operaciones
                    default:
                        writer.write("Unsupported operation: " + c3d.opType + "\n");
                        break;
                }
            }
        } catch (IOException e) {
            System.err.println("Error writing to file: " + e.getMessage());
        }
    }

    // Función que verifica si un operando es constante o no
    public static boolean isConstant(Info operando) {
        return operando.etiqueta == 10;
    }
}
