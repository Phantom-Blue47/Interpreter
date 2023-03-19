from lexer import *
from parser_ import *
from symboltable import *

class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.declared_variables= {}

    def visit_Program(self, node):
        self.visit(node.body)
        
    def visit_Body(self,node):
         for child in node.children:
            self.visit(child)

    def visit_Type(self, node):
        # Do nothing
        pass
    
    def visit_list(self, node):
        for child in node:
            self.visit(child)
    
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == REM:
            return self.visit(node.left) % self.visit(node.right)
        if node.op.type == 'GREATHAN':
            return self.visit(node.left) > self.visit(node.right)
        if node.op.type == 'LESSTHAN' :
            return self.visit(node.left) < self.visit(node.right)
        if node.op.type == 'DEQUAL':
            return self.visit(node.left) == self.visit(node.right)
        if node.op.type == 'NOTEQUAL':
            return self.visit(node.left) != self.visit(node.right)
        if node.op.type == 'LEQUAL':
            return self.visit(node.left) <= self.visit(node.right)
        if node.op.type == 'GEQUAL':
            return self.visit(node.left) >= self.visit(node.right)
        if node.op.type is None:
            return node.value
        
    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)
    
    def visit_Body(self, node):
        for child in node.children:
            self.visit(child)
            
    def visit_Declaration(self,node):
        var_name = node.var_node.value
        var_value = self.visit(node.right)
        self.declared_variables[var_name] = var_value
    
    def visit_Assign_stmt(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.declared_variables[var_name] = var_value
        
    def visit_If_stmt(self,node):
        if self.visit_BinOp(node.condition):
            self.visit(node.body)
        else:
            self.visit(node.else_block)
    
    def visit_Do_stmt(self,node):
        while self.visit(node.condition):
            self.visit(node.do_body)
            
    def visit_Cond_stmt(self,node):
        pass
                    
    def visit_Var(self, node):
        var_name = node.value
        var_value = self.declared_variables.get(var_name)
        return var_value
    
    def visit_NoOp(self, node):
        pass
    
    def interpret(self):
        tree = self.tree
        if tree is None:
            return ''
        return self.visit(tree)