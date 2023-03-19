from lexer import *
from parser_ import *

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type    
        
class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__
    

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__
    
class SymbolTable(object):
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
    
    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self._symbols.values()]
        )
        return s

    __repr__ = __str__

    def define(self, symbol):
        print('Define: %s' % symbol)
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        print('Lookup: %s' % name)
        symbol = self._symbols.get(name)
        # 'symbol' is either an instance of the Symbol class or 'None'
        return symbol  

class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()
        
    def visit_Program(self,node):
        self.visit(node.body)
    
    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        
    def visit_Num(self, node):
        pass
    
    def visit_UnaryOp(self, node):
        self.visit(node.expr)
        
    def visit_Body(self, node):
        for child in node.children:
            self.visit(child)
            
    def visit_NoOp(self, node):
        pass
    
    def visit_Assign_stmt(self, node):
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

        self.visit(node.right)
        
    def visit_Declaration(self, node):
        type_name = node.type_node
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)
        self.visit(node.right)
    
    def visit_If_stmt(self,node):
        pass
    
    def visit_Cond_stmt(self,node):
        return 1
    
    def visit_Do_stmt(self,node):
        pass
            
    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)

        if var_symbol is None:
            raise NameError(repr(var_name))