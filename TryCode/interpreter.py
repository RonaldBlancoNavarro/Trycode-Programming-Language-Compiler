from tkinter import END

class TryCodeExecute:
    def __init__(self, tree, env, txtOutput):
        self.txtOutput = txtOutput
        self.env = env
        result = self.walkTree(tree)
        #mostrar resultado en output
        if result is not None and result == "True" or result == "False":
           self.txtOutput.insert(END,result)
        if result is not None and isinstance(result, int):
            self.txtOutput.insert(END,result)
        if result is not None and isinstance(result, float):
            self.txtOutput.insert(END,result)
        if isinstance(result, str) and result[0] == '"':
            self.txtOutput.insert(END,result)
            self.txtOutput.insert(END,"\n")
        if result is not None  and isinstance(result, bool): 
            self.txtOutput.insert(END,result)

    def walkTree(self, node): #recorrer arbol

        if node == "TRUE":
            return "True"
        if node == "FALSE":
            return "False"
        if node == "NULL":
            return None
        
        #tipos de datos
        if isinstance(node, int):
            return node
        if isinstance(node, float):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == "program":
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        #tipos de datos
        if node[0] == "num":
            return node[1]

        if node[0] == "float":
            return node[1]

        if node[0] == "str":
            return node[1]
        
        if node[0] == "bool":
            return node[2]

        if node[0] == "print":
            self.txtOutput.insert(END,"\n")
            return node[1]

        if node[0] == "if_stmt": #if
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == "condition_eqeq":
            return self.walkTree(node[1]) == self.walkTree(node[2])
        if node[0] == "condition_noeq":
            return self.walkTree(node[1]) != self.walkTree(node[2])   
        if node[0] == "condition_lteq":
            return self.walkTree(node[1]) <= self.walkTree(node[2])    
        if node[0] == "condition_gteq":
            return self.walkTree(node[1]) >= self.walkTree(node[2])   
        if node[0] == "condition_lt":
            return self.walkTree(node[1]) < self.walkTree(node[2])   
        if node[0] == "condition_gt":
            return self.walkTree(node[1]) > self.walkTree(node[2])    
        if node[0] == "condition_and":
           return self.walkTree(node[1]) and self.walkTree(node[2])
        if node[0] == "condition_or":
           return self.walkTree(node[1]) or self.walkTree(node[2])
        if node[0] == "condition_not":
            return not self.walkTree(node[1])                                  

        if node[0] == "fun_def": #funcion
            self.env[node[1]] = node[2]

        if node[0] == "fun_call":#llamada a funcion
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                self.txtOutput.insert(END,"Undefined function '%s'" % node[1])
                return 0

        #operaciones aritmeticas
        if node[0] == "add":
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == "sub":
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == "mul":
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == "neg":
            return -1 * self.walkTree(node[1])            
        elif node[0] == "div":
            return self.walkTree(node[1]) / self.walkTree(node[2])

        #asignacion de variables
        if node[0] == "var_assign":
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == "var":
            try:
                return self.env[node[1]]
            except LookupError:
                self.txtOutput.insert(END,"Undefined variable '" + node[1] + "' found!")
                return 0
        
        if node[0] == "bool_assign":
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == "null_assign":
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        #for
        if node[0] == "for_loop":
            if node[1][0] == "for_loop_setup":
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        self.txtOutput.insert(END,res)
                        self.txtOutput.insert(END, '\n')
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == "for_loop_setup":
            return (self.walkTree(node[1]), self.walkTree(node[2]))

        #while
        if node[0] == "while_loop":
            if node[2][0] == "while_loop_statements":

                while self.walkTree(node[1]):
                    res = self.walkTree(node[2][1])
                    if res is not None:
                        self.txtOutput.insert(END,res)
                        self.txtOutput.insert(END, '\n')
                    self.walkTree(node[2][2])
