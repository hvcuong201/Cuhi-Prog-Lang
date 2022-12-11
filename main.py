from Lexer import *
from Parser import *
import pprint

if __name__ == "__main__":
    mylex = Lexer()

    #token list created
    mytokens, lex_stat = mylex.tokenize("no_error_test1.txt")

    if lex_stat == 'No':
        myParse = Parser(mytokens)
        #yes if there is a syntax error, no if there are no errors
        syntax_stat = myParse.check_syntax()
        print ('Lexical error: ',lex_stat)
        print ('Syntax error: ', syntax_stat)
        if syntax_stat == 'Yes':
            exit()
        print('\ntoken list: \n')
        pprint.pprint(mytokens)