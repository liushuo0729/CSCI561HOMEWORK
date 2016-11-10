import sys
import ply.yacc as yacc
import ply.lex as lex

if sys.version_info[0] >= 3:  
    raw_input = input  
  
tokens = (  
    'NAME','VARIABLE','ENTAIL'  
    )  
  
literals = ['|','&','~','(',')',',']  
  
# Tokens  
  
def t_NAME(t):
    r'[A-Z][a-zA-Z0-9_]*'
    t.value = str(t.value)
    return t

def t_VARIABLE(t):
    r'[a-z]'
    t.value = str(t.value)
    return t

t_ENTAIL = r'=>'
    
t_ignore = " \t"  
  
def t_newline(t):  
    r'\n+'  
    t.lexer.lineno += t.value.count("\n")  
      
def t_error(t):  
    print("Illegal character '%s'" % t.value[0])  
    t.lexer.skip(1)  
      
lex.lex()  
  
# Parsing rules  
  
precedence = (
    ('left','ENTAIL'),  
    ('left','|','&'),   
    ('right','~'),  
    )  
  
# dictionary of names  
names = { }  
  
def p_sentence_assign(p):  
    '''sentence : atomsentence
                | complexsentence'''
    p[0] = p[1]  
  
def p_complexsentence(p):  
    '''complexsentence : '(' sentence ')'
                  | '~' sentence 
                  | sentence '|' sentence 
                  | sentence '&' sentence
                  | sentence ENTAIL sentence'''
    tmp = ""
    for i in range(1,len(p)):
        tmp+=p[i]
    p[0] = tmp  
    if p[1] == '('  :
        print ("Closure"+p[2])  
    elif p[1] == '~': 
        print ("Not"+p[2]) 
    elif p[2] == '|':
        print (p[1]+"OR"+p[3]) 
    elif p[2] == '&':
        print (p[1]+"AND"+p[3])
    else:
        print (p[1]+"ENTAIL"+p[3])

def p_predicate(p):
    "predicate : NAME"
    p[0] = p[1]

def p_atomsentence(p):
    "atomsentence : predicate '(' terms ')'"
    p[0] = p[1] + p[2] + p[3] + p[4]
    print ("Predicate name:"+p[1]) 

def p_terms(p):
    '''terms : term
            | term ',' terms'''
    tmp = ""
    for i in range(1,len(p)):
        tmp+=p[i]
    p[0] = tmp 
def p_term(p):
    '''term : constant
            | VARIABLE'''
    p[0] = p[1]
    if (p[1][0]>='a' and p[1][0]<='z'):
        print ("Variable:"+p[1])
    else:
        print ("CONSTANT:"+p[1])           
def p_constant(p):
    "constant : NAME"
    p[0] = p[1]  
  
def p_error(p):  
    if p:  
        print("Syntax error at '%s'" % p.value)  
    else:  
        print("Syntax error at EOF")  
   
yacc.yacc()  
  
while 1:  
    try:  
        s = raw_input('calc > ')  
    except EOFError:  
        break  
    if not s: continue  
    yacc.parse(s)  