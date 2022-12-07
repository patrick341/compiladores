from AnalizadorLex import get_tokens
from Ll1 import parser, print_tree, update_stack
from AnalizadorSem import findVal
import sys
import pandas as pd

#C:\Users\Propietario\Desktop\prueba_final_sino gg\compiladorv2-main
file_out=open("/Users/Propietario/Desktop/prueba_final_sino gg/compiladorv2-main/salida4","w")

def codigo_asignacion(vertice):
    print("iniciacion la asignacion")
    if vertice.symbol.symbol=="assign":
        print("signo")
        node_e=vertice.father.children[2]
        node_id=vertice.father.children[0]
        codigo_paraT(node_e.children[0])
        codigo_paraE_1(node_e.children[1])
        file_out.write("\n\tla  $t1, var_"+ str(node_id.lexeme)+ "\n"+"\tsw  $a0, 0($t1)\n")
    for child in vertice.children:
        codigo_asignacion(child)
    print("terminando evaluacion")
def codigo_paraT(vertice):
    print(vertice.symbol.symbol)
    if vertice.children[0].symbol.symbol=="TERM":
        codigo_terminal(vertice.children[0])


def codigo_paraE_1(vertice):
    print(vertice.symbol.symbol)
    if len(vertice.children)>1:
        file_out.write("")
        file_out.write("")
        codigo_paraT(vertice.children[1])
        file_out.write(" \tlw $t1 4($sp)\n")
        if vertice.children[0].children[0].symbol.symbol=="opesuma":
            file_out.write("\tadd $a0, $a0, $t1")
        file_out.write("\n \taddiu $sp $sp 4\n")
        codigo_paraE_1(vertice.children[2])

def codigo_terminal(vertice):
    if (vertice.children[0].symbol.symbol =="num" and vertice.father.father.symbol.symbol =="E" and vertice.father.father.children[1].children[0].symbol.symbol != 'e' ): #and vertice.father.father.father == "E"):
        print("LECTURA DE CODIGO PARA E Y E'")
        print(vertice.father.father.symbol.symbol)
        file_out.write("\tli"+ " $a0,"+ str(vertice.children[0].lexeme)+ "\n")
        file_out.write("\tsw"+ " $a0   " +" 0($sp)" +"\n"+ ("\tadd $sp $sp-4 \n" ))

    if (vertice.children[0].symbol.symbol =="num" and vertice.father.father.symbol.symbol !="E" ): #and vertice.father.father.father == "E"):
        print("LECTURA DE CODIGO PARA E Y E'")
        print(vertice.father.father.symbol.symbol)
        file_out.write("\tli"+ " $a0,"+ str(vertice.children[0].lexeme)+ "\n")
        #file_out.write("\tsw"+ " $a0   " +" 0($sp)" +"\n"+ ("\tadd $sp $sp-4 \n" ))    

    if (vertice.children[0].symbol.symbol =="num" and vertice.father.father.symbol.symbol =="E" and vertice.father.father.children[1].children[0].symbol.symbol == 'e' ): #and vertice.father.father.father == "E"):
        print("LECTURA DE CODIGO PARA E Y E'")
        print(vertice.father.father.symbol.symbol)
        file_out.write("\tli"+ " $a0,"+ str(vertice.children[0].lexeme)+ "\n")

    if(vertice.children[0].symbol.symbol =="id"):
        codigo_variable(vertice)

def codigo_variable(vertice):
    if vertice.symbol.symbol=="TYPE":
        if vertice.father.symbol.symbol=="STATEMENT":
            codigo_id(vertice.father.children[1].children[0])

    for i in vertice.children:
        codigo_variable(i)

def codigo_id(vertice):
    file_out.write("\tvar_" + str(vertice.lexeme) + ": .word 0:1\n")

#codigo funcion
##empezamos

def generar_funcionM(node):
    if node.symbol.symbol == 'FUNCTION_M':
        print("encontre una funcionM")
        node_f=node.children[0]
        generar_funcion(node_f)
        #generar_exprT(node)
        for child in node.children:
            generar_funcionM(child)

def generar_funcion(node):
    print("encontre una funcion ") 
    if node.children[0].symbol.symbol=='TYPE':
        print("encontre un type")
    if node.children[2].symbol.symbol=='id':
        print("encontre un id")
        node_nomF=node.children[2].lexeme
        print(node_nomF)
        file_out.write("\n"+str(node_nomF)+":\n")
    if node.children[4].symbol.symbol=="PARAM_DEF_M":
        print("encontre un param_def_M")
        node_param=node.children[4]
        generar_param_def_M(node_param)
    #debo ir a return y luego a t y eprima
    if node.children[8].symbol.symbol=="RETURN":
        print("encontre un return")
        node_ex=node.children[8]
        generar_expr(node_ex.children[1])
        #print(node_ex.children[1].symbol.symbol)
        file_out.write("\n \tlw $ra 4($sp)")
        file_out.write("\n \taddiu $sp $sp 12")
        file_out.write("\n \tlw $fp 0($sp)")

##codigo generar_expr

def generar_expr(node):
    if node.symbol.symbol == "E":
        #escribe_num(node.children[0])
        #print("encontrando node:",node.symbol.symbol)
        codigo_paraT(node.children[0])
        codigo_paraE_1(node.children[1])
        #registrar_operandos(node)#tiene que ir en un for pero cuando lo pongo me sale fallas
    for child in node.children:
        generar_expr(child)

##fin de codigo



def generar_param_def_M(node):
     print("parametros")
     if len(node.children)>0:
      file_out.write("\tmove $fp $sp\n")
      file_out.write("\n \tsw $ra 0 $sp"+"\n")
      file_out.write("\taddiu $sp $sp -4 \n")
      file_out.write("\n \tlw $a0, 8($sp) \n")



def genera_assembler(root):
    file_out.write(".data\n")
    codigo_variable(root)#escribe cada variable
    file_out.write(".text\nmain:\n")
    #sentencia(root)
    #generar_assing(root)
    #generar_funcionM(root)
    codigo_asignacion(root)
    ##generar_statement(root)
    #(root)
    ##   sentencia(root)
    ##   codigo_asignacion(root)
    ##   codigo_paraT(root)
    ##   codigo_paraE_1(root)
    ##   codigo_asignacion(root)
    #if(codigo_asignacion(root)=="TERM_FUNC"):
    print(root)
    file_out.write("\n \t$v0,1 \n")
    file_out.write("\n \tsyscall \n")

    file_out.write("\n \tjr $ra ")
    #codigo_block(root)
    #generar_funcionM(root)




#if __name__ == "__main__":
file_name="/Users/Propietario/Desktop/prueba_final_sino gg/compiladorv2-main/test/test10.txt"
    #C:\Users\Propietario\Desktop\prueba_final_sino gg\compiladorv2-main\test
    #file_name=sys.argv[0]
    #file_name="/Users/Propietario/Desktop/generacion de codigo/Compiladores-main/Compilador/test/test8.txt"
    #file_name=file_name.sys.arg[0]

    #lexer
tokens = get_tokens(file_name)
tokens.append (['$', None, None])
    
    #analizador sintatico
    #root=parser(tokens)
root, node_list = parser(tokens)
print("mi rooot es \n")
print(root)
#print(node_list.split())
#print(root)
print("mi nodelist es \n")
print(node_list)
    #analizador semantico
    #buscar_if_else(root)
    
findVal(root)#check_nodes(root)
    
#set_types(root)
    #code generation
#codigo_block(root)
genera_assembler(root)

file_out.close()

    #print_tree(root, node_list, True)
    #print symbol_table()


