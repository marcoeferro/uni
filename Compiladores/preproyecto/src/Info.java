public class Info { 
    public Integer etiqueta; // numero de etiqueta
    public String nombre; // x y
    public Integer value; // 15 0 1
    public String tipo; // int o bool
    public Integer offSet; //desplazamiento en memoria
    
    public Info(String nombre, Integer etiqueta , Integer value , String tipo , Integer offSet){
        this.nombre = nombre;
        this.etiqueta = etiqueta;
        this.value = value;
        this.tipo = tipo;
        this.offSet = offSet;
    }
    public Info(String nombre, Integer etiqueta , Integer value , String tipo ){
        this.nombre = nombre;
        this.etiqueta = etiqueta;
        this.value = value;
        this.tipo = tipo;
        this.offSet = null;
    }

    public Info getInfo(){
        return this;
    }
}
