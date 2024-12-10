//codigo de usuario

import java_cup.runtime.*;

//opciones y declaraciones

%%
%{    
    //codigo en java
    
%}

%class lexer
%unicode
%cup
%line
%column
%cupsym Simbolo
%cup
%ignorecase


//macros
espacio =   (" " | \r | \n | \t | \f)+
cadena  =   ([a-zA-Z]+[0-9]*)+

%%

//reglas lexicas

// Palabras reservadas
"int"       { return new Symbol(Simbolo.INT, yyline, yycolumn); }
"bool"      { return new Symbol(Simbolo.BOOL, yyline, yycolumn); }
"void"      { return new Symbol(Simbolo.VOID, yyline, yycolumn); }
"main"      { return new Symbol(Simbolo.MAIN, yyline, yycolumn); }
"true"      { return new Symbol(Simbolo.TRUE, yyline, yycolumn); }
"false"     { return new Symbol(Simbolo.FALSE, yyline, yycolumn); }
"return"     { return new Symbol(Simbolo.RETURN, yyline, yycolumn); }
"if"     { return new Symbol(Simbolo.IF, yyline, yycolumn); }
"else"     { return new Symbol(Simbolo.ELSE, yyline, yycolumn); }
"while"     { return new Symbol(Simbolo.WHILE, yyline, yycolumn); }


// Delimitadores
";"         { return new Symbol(Simbolo.SEMICOLON, yyline, yycolumn); }
"="         { return new Symbol(Simbolo.EQUAL, yyline, yycolumn); }
"("         { return new Symbol(Simbolo.LPAREN, yyline, yycolumn); }
")"         { return new Symbol(Simbolo.RPAREN, yyline, yycolumn); }
"{"         { return new Symbol(Simbolo.LBRACE, yyline, yycolumn); }
"}"         { return new Symbol(Simbolo.RBRACE, yyline, yycolumn); }

// Operadores
"+"         { return new Symbol(Simbolo.PLUS, yyline, yycolumn); }
"*"         { return new Symbol(Simbolo.STAR, yyline, yycolumn); }
"<"         { return new Symbol(Simbolo.LESS, yyline, yycolumn); }
">"         { return new Symbol(Simbolo.GREATER, yyline, yycolumn); }

// Identificadores y números
{cadena}  { return new Symbol(Simbolo.ID, yyline, yycolumn, yytext()); }
[0-9]+  { return new Symbol(Simbolo.NUMBER, yyline, yycolumn, Integer.parseInt(yytext())); }

// Espacios en blanco (se ignoran)
{espacio}               { /* NO HACER NADA */}
.                       { System.out.println("Caracter no reconocido: " + yytext() + " en línea: " + yyline + ", columna: " + yycolumn); }