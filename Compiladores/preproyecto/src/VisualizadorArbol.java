import java.util.ArrayList;

public class VisualizadorArbol {
    
    public static ArrayList<String> recorridoInOrden(Nodo actual){
        ArrayList<String> textAux = new ArrayList<>();

        if(actual.izq != null){
            textAux.addAll(VisualizadorArbol.recorridoInOrden(actual.izq));
            textAux.add(actual.graphId+ " -> "+actual.izq.graphId);
        }
        String nombre = actual.info.nombre;
        if(actual.info.etiqueta == 11) nombre = "\"+\"";
        if(actual.info.etiqueta == 12) nombre = "\"*\"";
        if(actual.info.etiqueta == 6) nombre = "return";
        textAux.add(actual.graphId+" [label="+nombre+"];");
        if(actual.der != null){
            textAux.addAll(VisualizadorArbol.recorridoInOrden(actual.der));
            textAux.add(actual.graphId+ " -> "+actual.der.graphId);
        }

        return textAux;
    }
    public static ArrayList<String> graficar(Nodo actual){
        ArrayList<String> textAux = new ArrayList<>();
        textAux.add("digraph G {");
        textAux.addAll(VisualizadorArbol.recorridoInOrden(actual));
        textAux.add("}");
        return textAux;
    }
    


}
