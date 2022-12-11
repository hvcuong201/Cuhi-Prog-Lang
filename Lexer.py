'''
Lexical Analyzer takes in a source file ( extension for your language optional ) and tokenizes all lexemes that fit in your created language

    Identifiers
    Key words
    operators
    literals
        string
        integer
        real
        Boolean


'''
import re

#--------------------------------------------------------------------------#
#                            List of TOKENS                                #
#--------------------------------------------------------------------------# 
TOKENS = [
    (r'BEGIN',                      'BEGIN'),
    (r'END',                        'END'),
    (r'if',                         'if_key'),
    (r'for',                        'for_key'),
    (r'else',                       'else_key'),
    (r'times',                      'times_key'),
    (r'int',                        'int_key'),
    (r'real',                       'real_key'),
    (r'str',                        'string_key'),
    (r'bool',                       'boolean_key'),
    (r'".*"',                       'lit_string'),
    (r'TRUE',                       'lit_bool'),
    (r'FALSE',                      'lit_bool'),
    (r'0|-?[1-9][0-9]*',            'lit_int4b'),
    (r'-?\d+\.\d+',                 'lit_real'),
    (r'[a-zA-Z_]{1,7}',             'id'),
    (r'\;',                         'end_stmt'),
    (r'\+',                         'add'),
    (r'-',                          'subtract'),
    (r'\*',                         'multiply'),
    (r'/',                          'divide'),
    (r'%',                          'module'),
    (r'=',                          'assign'),
    (r'==',                         'EQ'),
    (r'!=',                         'NEQ'),
    (r'<',                          'LT'),
    (r'>',                          'GT'),
    (r'<=',                         'LTE'),
    (r'>=',                         'GTE'),
    (r'\(',                         'L_paren'),
    (r'\)',                         'R_paren'),
    (r'\{',                         'L_bracket'),
    (r'\}',                         'R_bracket'), 
]

BYTE_SPECIFIC_INT = [
    r'0|[1-9][0-9]*_b8',
    r'0|[1-9][0-9]*_b4',
    r'0|[1-9][0-9]*_b2',
    r'0|[1-9][0-9]*_b1'
]


#--------------------------------------------------------------------------#
#                            TOKEN                                         #
#--------------------------------------------------------------------------# 
class Token:
	def __init__(self, type, value=None):
		self.type = type
		self.value = value
        
	def __repr__(self):
		if self.value: return f'{self.value}:{self.type}'
		return f'{self.type}'

#--------------------------------------------------------------------------#
#                            LEXER                                         #
#--------------------------------------------------------------------------#
class Lexer:
    #read program (text file) and create a list of tokens   
    def tokenize(self, file):
        tokens = []
        
        with open (file, "r") as f:
            code = f.read()  
            print(code)
            start = re.search(r'BEGIN',code).span()[0]
            end = re.search(r'END',code).span()[1]
            #cut the text that's above BEGIN and below END
            code = code[start:end]
            #Create the list of tokens
            raw_tokens = code.split()                  
            print()

        #matches the tokens to its type using regular expressions
        for tok in raw_tokens:
            before = len(tokens)
            for pattern, type in TOKENS:
                if re.fullmatch(pattern,tok):
                    if pattern in BYTE_SPECIFIC_INT:
                        num = tok[0:len(tok)-3]
                        tokens.append(Token(type, num))
                    else:
                        tokens.append(Token(type, tok))
                    break   
            after = len(tokens)
            #Checks for tokens not added to tokens list
            if after == before:
                print('Lexical error: ',tok,' at index: ', raw_tokens.index(tok),' (invalid lexeme)')
                return None, 'Yes'
                
        return tokens, 'No'