public class Nodo {
    
    public Info info;
    public Nodo izq;
    public Nodo der;
    public int graphId;

    public Nodo(){

    }

    public Nodo(Info info,int id){
        this.info = info;
        this.graphId = id;
    }

    //getters

    
    //agregar hijos

    public void addHijoIzq(Nodo hijo){
        izq = hijo;
    }

    public void addHijoDer(Nodo hijo){
        der = hijo;
    }
}
