from lexer import *
from parser_ import *
from symboltable import *
from interpreter import *


def main():
    import sys
    text ="object demo{ def main (args: Array[String]){ var x: int = 5 if(x==5) x==6  }}"
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()
    symtab_builder = SymbolTableBuilder()
    symtab_builder.visit(tree)
    print('')
    print('Symbol Table contents:')
    print(symtab_builder.symtab)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()

    print('')
    print('Run-time declared_variables :')
    for k, v in sorted(interpreter.declared_variables.items()):
        print('{} = {}'.format(k, v))


if __name__ == '__main__':
    main()