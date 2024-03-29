from sly import Parser
from lexer import TryCodeLexer
_='_'

class TryCodeParser(Parser):
    tokens = TryCodeLexer.tokens

    precedence = (
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "UMINUS"),
    )

    def __init__(self):
        self.env = {}

    #Reglas de arbol de sintaxis

    @_("")
    def statement(self, p):
        pass

    @_("WHILE condition THEN \n statement \n  statement")
    def statement(self, p):
        return ("while_loop", p.condition,("while_loop_statements", p.statement0, p.statement1) )   

    @_("FOR var_assign TO expr THEN statement")
    def statement(self, p):
        return ("for_loop", ("for_loop_setup", p.var_assign, p.expr), p.statement)

    @_("IF condition THEN \n statement ELSE \n statement")
    def statement(self, p):
        return ("if_stmt", p.condition, ("branch", p.statement0, p.statement1))

    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ("fun_def", p.NAME, p.statement)
    
    @_('PRINT "(" STRING ")"')
    def print(self, p):
        return ("print", p.STRING)
    
    @_('PRINT "(" NAME ")"')
    def expr(self, p):
        return ("var", p.NAME)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ("fun_call", p.NAME)

    @_("condition AND condition")
    def condition(self, p):
        return ("condition_and", p.condition0, p.condition1)

    @_("condition OR condition")
    def condition(self, p):
        return ("condition_or", p.condition0, p.condition1)

    @_("NOT condition")
    def condition(self, p):
        return ("condition_not", p.condition)        

    @_("expr EQEQ expr")
    def condition(self, p):
        return ("condition_eqeq", p.expr0, p.expr1)

    @_("expr NOEQ expr")
    def condition(self, p):
        return ("condition_noeq", p.expr0, p.expr1)        

    @_("expr LTEQ expr")
    def condition(self, p):
        return ("condition_lteq", p.expr0, p.expr1) 

    @_("expr GTEQ expr")
    def condition(self, p):
        return ("condition_gteq", p.expr0, p.expr1)   

    @_("expr LT expr")
    def condition(self, p):
        return ("condition_lt", p.expr0, p.expr1)   

    @_("expr GT expr")
    def condition(self, p):
        return ("condition_gt", p.expr0, p.expr1)                  

    @_("var_assign")
    def statement(self, p):
        return p.var_assign
    
    @_("bool_assign")
    def statement(self, p):
        return p.bool_assign
    
    @_("null_assign")
    def statement(self, p):
        return p.null_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ("var_assign", p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ("var_assign", p.NAME, p.STRING)
    
    @_('NAME "=" TRUE')
    def bool_assign(self, p):
        return ("bool_assign", p.NAME, p.TRUE)

    @_('NAME "=" FALSE')
    def bool_assign(self, p):
        return ("bool_assign", p.NAME, p.FALSE)

    @_('NAME "=" NULL')
    def null_assign(self, p):
        return ("null_assign", p.NAME, p.NULL)        

    @_("expr")
    def statement(self, p):
        return p.expr

    @_("print")
    def statement(self, p):
        return p.print
    
    @_('expr "+" expr')
    def expr(self, p):
        return ("add", p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ("sub", p.expr0, p.expr1)
      
    @_('expr "*" expr')
    def expr(self, p):
        return ("mul", p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ("div", p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ("neg", p.expr) 

    @_("NAME")
    def expr(self, p):
        return ("var", p.NAME)

    @_("NUMBER")
    def expr(self, p):
        return ("num", p.NUMBER)

    @_("FLOAT")
    def expr(self, p):
        return ("float", p.FLOAT)