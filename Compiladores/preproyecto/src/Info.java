public class Info {
    public Integer etiqueta; // numero de etiqueta
    public String nombre; // x y
    public Integer value; // 15 0 1
    public String tipo; // int o bool
    
    public Info(String nombre, Integer etiqueta , Integer value , String tipo){
        this.nombre = nombre;
        this.etiqueta = etiqueta;
        this.value = value;
        this.tipo = tipo;
    }

    public Info getInfo(){
        return this;
    }
}
