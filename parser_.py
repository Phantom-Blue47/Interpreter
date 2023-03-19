from lexer import *





class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Body(AST):
    """Represents a 'BEGIN ... END' block"""

    def __init__(self):
        self.children = []

class Assign_stmt(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Declaration(AST):
    def __init__(self, var_node, type_node, op, right):
        self.var_node = var_node
        self.type_node = type_node
        self.token = self.op = op
        self.right = right
        
# class Cond_stmt(AST):
#     def __init__(self, leftexpr, comp_op, rightexpr):
#         self.leftexpr = leftexpr
#         self.comp_op = comp_op
#         self.rightexpr = rightexpr


class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Program(AST):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class Bool(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.op = Token(None, 'None')

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class If_stmt(AST):
    def __init__(self, condition, body, else_block):
        self.condition = condition
        self.body = body
        self.else_block = else_block


class Do_stmt(AST):
    def __init__(self, while_condition, do_body):
        self.condition = while_condition
        self.do_body = do_body


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def skip(self):
        self.current_token = self.lexer.get_next_token()

    def program(self):

        """program : OBJECT variable '{' stmt_list '}' """

        self.eat(OBJECT)
        var_node = self.id()
        prog_name = var_node.value
        # print(prog_name)
        # print(self.current_token)
        self.eat(LCURL)
        body_node = self.body()
        self.eat(RCURL)
        program_node = Program(prog_name, body_node)

        return program_node

    def body(self):
        """body :  { statement_list }"""
        # print("body")
        
       # ___________________in-built lines
        self.eat(DEF)
        self.eat(MAIN)
        self.eat(LPAREN)
        self.eat(ARGS)
        self.eat(COLON)
        self.eat(ARRAY)
        self.eat(LBRACE)
        self.eat(STRING)
        self.eat(RBRACE)
        self.eat(RPAREN)
        #_____________________
        
        
        
        self.eat(LCURL)
        nodes = self.stmt_list()
        self.eat(RCURL)
        root = Body()
        for node in nodes:
           root.children.append(node)
        return root

    def stmt_list(self):
        """stmt_list : stmt [[SEMI] stmt_list]"""
        # print("stmtlist")
        node = self.stmt()
        results = [node]
        while self.current_token.type != RCURL and self.current_token.type != EOF:
            results.append(self.stmt())
        return results

    def stmt(self):
        """
        statement : assign_stmt
                    | stmt1
                    | empty
        """
        # print("stmt")
        if self.current_token.type == ID:
            node = self.assign_stmt()
        elif self.current_token.type == VAR:
            node = self.decl_stmt()
        else:
            node = self.stmt1()
        if (self.current_token.type == SEMI):
            self.eat(SEMI)

        return node

    def assign_stmt(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        # print("assign_stmt")
        left = self.id()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign_stmt(left, token, right)

        return node
    
    def decl_stmt(self):
        
        # print("decleration stmt")
        self.eat(VAR)
        var_node = self.current_token
        self.eat(ID)
        self.eat(COLON)
        type_node = INTEGER
        self.eat(INT)
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        
        decl = Declaration(var_node, type_node,token,right)
        
        return decl
    
    def type_spec(self):
        """type_spec : INTEGER
                    | REAL
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        node = Type(token)
        return node

    def id(self):
        """
        variable : ID | const
        """
        # print("id")
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        # print("expr")
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*"""
        # print("term")
        node = self.factor()
        while self.current_token.type in (MUL, DIV, REM):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == REM:
                self.eat(REM)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """factor : PLUS factor
                  | MINUS factor
                  | LPAREN expr RPAREN
                  | variable
        """
        # print("factor")
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == TRUE:
            self.eat(TRUE)
            return Bool(token)
        elif token.type == FALSE:
            self.eat(FALSE)
            return Bool(token)
        else:
            node = self.id()
            return node

    def stmt1(self):
        """stmt1: 'if' '(' con_stmt ')' stmt_list [[semi] 'else' expr]  (cond_stmt)
                | 'do' Expr [semi] `while' `(' Expr ')'  (do_stmt)"""
        # print("stmt1")
        if self.current_token.type == IF:
            node = self.if_stmt()
        elif self.current_token.type == DO:
            node = self.do_stmt()
        else:
            node = self.empty()
        return node

    def if_stmt(self):
        # print("ifstmt")
        self.eat(IF)
        self.eat(LPAREN)
        condition = self.cond_stmt()
        self.eat(RPAREN)
        while self.current_token.type == 'EOL':
            self.advance()
        body = self.stmt_list()
        while self.current_token.type == 'EOL':
            self.advance()
        if (self.current_token.type == 'ELSE'):
            self.eat(ELSE)
            else_block = self.stmt_list()
        else:
            else_block = self.empty()

        node = If_stmt(condition, body, else_block)

        return node

    def do_stmt(self):
        # print("dostmt")
        self.eat(DO)
        if (self.current_token.type == 'LCURL'):
            self.eat(LCURL)
            statement = self.stmt_list()
            self.eat(RCURL)
        else:
            statement = self.stmt_list()
        self.eat(WHILE)
        self.eat(LPAREN)
        cond = self.cond_stmt()
        self.eat(RPAREN)
        node = Do_stmt(cond, statement)

        return node
    
    def cond_stmt(self):
        # print("cond_stmt")
        node = self.expr()
        if self.current_token.type in ('LEQUAL', 'DEQUAL', 'GEQUAL', 'LESSTHAN', 'GREATHAN' ):
            token = self.current_token
            self.eat(token.type)
        right = self.expr()
        node = BinOp(node,token,right)
        return node

    def parse(self):
        # print("parse")
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node