'''
A syntax analyzer that takes in tokens to determine if syntax errors exist in your programming language based off of rules provided.
'''
class Parser: 
    
    #constructor for Parser
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_ind = -1
        self.current_tok = None
        self.syn_errors = []

    #function to move to next token in the list
    def to_next_tok(self):
        self.tok_ind += 1
        if self.tok_ind >= 0 and self.tok_ind < len(self.tokens):
            self.current_tok = self.tokens[self.tok_ind].type
        else:
            print(self.current_tok)
            print("Error: no more tokens")
            exit() 
        return self.current_tok


    #Starts checking the token list for syntax errors, calls statement_list to get started
    def check_syntax(self):
        if self.to_next_tok() == 'BEGIN':
            result = self.Statement_list()
            if not result:          
                return self.syn_errors
        else:
            self.syn_errors.append("SyntaxError: Read in tokens before BEGIN")

    #Recursively check all statements in the program (text file)
    def Statement_list(self):
        next = self.to_next_tok()
        self.tok_ind -= 1
        if next == "END":
            return True       
        elif self.Statement():
            if self.Statement_list():
                return True
            else:
                self.syn_errors.append("SyntaxError: END not found")
                return False
        else: 
            return False
    

    #classify the current statement so the correct function will check its syntax 
    def Statement(self):
        key = self.to_next_tok()

        if key == 'int_key':
            if self.Var_decl() == True:
                return True
        elif key == 'id':
            if self.Var_assign() == True:
                return True
        elif key == 'case_key':
            if self.Case() == True:
                return True
        elif key == 'itr_key':
             if self.Itr() == True:
                return True
        else:
            return False

    
    #Checks if variable declaration statement has correct syntax
    def Var_decl(self):
        var = self.to_next_tok()
        stop = self.to_next_tok()
        if var == 'id' and stop == 'end_stmt':
            return True
        else:
            return "Bad"
    

    #Checks if variable assignment/initialization statement has correct syntax
    def Var_assign(self):
        operator = self.to_next_tok()
        if operator == 'assign':           
            status = self.Math_expr()
            if status == True:
                stop = self.to_next_tok()
                if stop == 'end_stmt':
                    return True
                else:
                    print('Error: expecting "."')               
                    return "Bad"
        else:
            print('Error: expecting "="')               
            return "Bad"
    

    #Checks if case statement has correct syntax
    def Case(self):
        if self.Boolean_expr() == True:
            next = self.to_next_tok()
            if next == "L_bracket":            
                if self.If_true() == True:              
                    next = self.to_next_tok()
                    if next == 'other_key':
                        next = self.to_next_tok()
                        if next == "L_bracket":
                            if self.If_false() == True:
                                if self.to_next_tok() == 'end_stmt':
                                    return True
                                else:
                                    self.tok_ind -= 1
                                    print('Syntax error: Expecting "."')
                                    return 'Bad'
                        else:
                            self.tok_ind -= 1                       
                            return 'Bad'                                    
                    elif next == 'end_stmt':                    
                        return True
                    else:
                        self.tok_ind -= 1
                        print('Syntax error: Expecting "."') 
                        return 'Bad' 
            else:
                self.tok_ind -= 1
                print('Expecting "["')
                return 'Bad'      
        else: 
            return 'Bad'          
    

    #Checks if Boolean expression has correct syntax
    def Boolean_expr(self):
        rela_op = ["EQ", "NEQ", "LT", "GT", "LTE", "GTE"]
        next = self.to_next_tok()
        if next == 'L_paren':
            if self.Number() == True:
                if self.to_next_tok() in rela_op:
                    if self.Number() == True:
                        if self.to_next_tok() == 'R_paren':
                            return True
                        else:
                            self.tok_ind -= 1
                            return 'bad'
                else:
                    self.tok_ind -= 1 
                    return 'bad'
        else:
            self.tok_ind -= 1
            return "Bad"

        return 'Bad'


    #Recursively CHecks all statments in case's (if statment) execution block for syntax errors
    def If_true(self):
        next = self.to_next_tok()
        if next == "R_bracket":         
            return True
        self.tok_ind -= 1
        if self.Statement() == True:                             
            if self.If_true() == True:
                return True        
        
        print('Syntax error at If_true')
        return 'Bad'
    

    #Recursively CHecks all statments in other's (else statment) execution block for syntax errors 
    def If_false(self):
        next = self.to_next_tok()
        if next == "R_bracket":         
            return True
        self.tok_ind -= 1
        if self.Statement() == True:                             
            if self.If_false() == True:
                return True 
        print('Syntax error in if_false execution block')             
        return 'Bad'
        
    
    
    #Checks grammar of itr (for loop) statement
    def Itr(self):
        if self.Number() == True:
            if self.to_next_tok() == 'times_key':
                next = self.to_next_tok()
                if next == 'L_bracket':
                    if self.To_repeat() == True:
                        if self.to_next_tok() == 'end_stmt':
                            return True
                        else:                
                            self.tok_ind -= 1
                            print('Syntax error: "." expected')
                            return 'Bad'
                else:                
                    self.tok_ind -= 1
                    print('Syntax error: "[" expected')
                    return 'Bad'
            else:                
                self.tok_ind -= 1
                print('Syntax error: "times" expected')
                return 'Bad'
        return 'Syntax error at Itr'
    

    #Recursively Checks all statements in itr's execution block for syntax errors
    def To_repeat(self):
        next = self.to_next_tok()
        if next == "R_bracket":         
            return True
        self.tok_ind -= 1
        if self.Statement() == True:                             
            if self.To_repeat() == True:
                return True                        
        print('Syntax error at To_repeat')
        return 'Bad'
    

    #Checks if mathmetical expression's syntax is correct
    def Math_expr(self):
        operator = ["add", "subtract", "multiply", "divide", "module"]
        if self.Term() == True:
            if self.to_next_tok() in operator:
                if self.Math_expr() == True:
                    return True
            self.tok_ind -= 1
            return True
            
        return 'Bad'


    #Checks if term's syntax is correct ()
    def Term(self):
        operator = ["add", "subtract", "multiply", "divide", "module"]
        if self.Factor() == True:
            return True
        elif self.to_next_tok() in operator:
            if self.Factor() == True:
                return True 
        self.tok_ind -= 1          
        return 'Bad'


    #Checks the operand's syntax (number, expression in parentheses)
    def Factor(self):
        if self.Number() == True:
            return True
        elif self.to_next_tok() == 'L_paren':
            if self.Math_expr() == True:
                if self.to_next_tok() == 'R_paren':                    
                    return True
                self.tok_ind -= 1
        self.tok_ind -= 1
        return 'Bad'


    #Check if the next token is a number (literal + variable)
    def Number(self):
        nums = [
            'lit_int8b', 
            'lit_int4b', 
            'lit_int2b', 
            'lit_int1b', 
            'id'
        ]
        next = self.to_next_tok()
        if next in nums :
            return True
        self.tok_ind -= 1
        return 'bad'


#--------------------------------------------------------------------------#
#                            Run time code                                 #
#--------------------------------------------------------------------------#