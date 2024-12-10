import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

class SymbolTable {
    private Stack<Map<String, Info>> scopes;

    public SymbolTable() {
        scopes = new Stack<>();
        // Iniciar con un scope global
        enterScope();
    }

    public void enterScope() {
        scopes.push(new HashMap<>());
    }

    public void exitScope() {
        scopes.pop();
    }

    public void addSymbol(String name, Integer etiqueta, Integer value, String type, Integer Offset) {
        Map<String, Info> currentScope = scopes.peek();
        if (currentScope.containsKey(name)) {
            System.out.println("Error: La variable '" + name + "' ya ha sido declarada en este alcance.");
        } else {
            currentScope.put(name, new Info(name, etiqueta, value, type, Offset));
        }
    }

    public Info lookup(String name) {
        for (int i = scopes.size() - 1; i >= 0; i--) {
            Map<String, Info> scope = scopes.get(i);
            if (scope.containsKey(name)) {
                return scope.get(name);
            }
        }
        return null; // Si no se encuentra en ningún scope
    }

    public void changeSymbolValue(String name,int value){
        Map<String, Info> currentScope = scopes.peek();
        Info newInfo = currentScope.get(name);
        newInfo.value = value;
        currentScope.replace(name, newInfo);
    }

    //codigo para el interprete

}