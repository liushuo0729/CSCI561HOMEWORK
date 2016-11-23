import sys
import ply.yacc as yacc
import ply.lex as lex


class TreeNode(object):
    def __init__(self):
        self.flag = True
        self.relation = None
        self.left = None
        self.right = None
        self.predicate = None
        self.parameter = None

    def __eq__(self,other):
        if type(other) != type(self):
            return False
        return self.flag == other.flag and self.predicate == other.predicate and self.parameter== other.parameter


RELATION = {
    1:'OR',
    2:'AND',
    3:'IMPLY'
}

def printTree(root,layer):
    tmp = " "*layer
    print (tmp+"Flag:"+str(root.flag))
    if root.relation:
        print (tmp+"Relation:"+str(root.relation))
    if root.predicate:
        print (tmp+"Predicate Name:"+str(root.predicate))
    if root.parameter:
        print (tmp+"parameter:"+str(root.parameter))
    if root.left:
        printTree(root.left,layer+1)
    if root.right:
        printTree(root.right,layer+1)

def eliminateImpl(root):
    if root.relation == 'IMPLY':
        root.left.flag = not root.left.flag
        root.relation = RELATION[1]
    if root.left:
        eliminateImpl(root.left)
    if root.right:
        eliminateImpl(root.right)

def moveInward(root):
    if root.left:
        if not root.flag:
            root.flag = True
            if root.relation=='OR':
                root.relation = 'AND'
            elif root.relation=='AND':
                root.relation = 'OR'
            root.left.flag = not root.left.flag
            root.right.flag = not root.right.flag
        moveInward(root.left)
        moveInward(root.right)

def distribute(root):
    result = []
    if not root.left:
        result.append(root)
    else:
        if root.relation == 'AND':
            result = distribute(root.left)+distribute(root.right)
        elif root.relation == 'OR':
            resultLeft = distribute(root.left)
            resultRight = distribute(root.right)
            for leftElement in resultLeft:
                for rightElement in resultRight:
                    tmp = TreeNode()
                    tmp.relation = 'OR'
                    tmp.left = leftElement
                    tmp.right = rightElement
                    result.append(tmp)
    return result

def generateKB(root):
    result = []
    if not root.left:
        result.append(root)
    else:
        result+=generateKB(root.left)
        result+=generateKB(root.right)
    return result

def contradiction(target,known):
    if target.predicate==known.predicate and (target.flag != known.flag):
        for i in range(len(target.parameter)):
            if (not isVariable(target.parameter[i])) and (not isVariable(known.parameter[i])):
                if target.parameter[i] != known.parameter[i]:
                    return False
        return True
    else:
        return False



def isVariable(para):
    if len(para)==1:
        if para>='a' and para<='z':
            return True
    return False


def unification(target,known,sentence):
    result = []
    table = {}

    for i in range(len(target.parameter)):
        if not isVariable(target.parameter[i]) and isVariable(known.parameter[i]):
            table[known.parameter[i]] = target.parameter[i]

    for item in sentence:
        if item!=known:
            newItem = TreeNode()
            newItem.flag = item.flag
            newItem.predicate = item.predicate
            newItem.parameter = item.parameter[:]
            for i in range(len(newItem.parameter)):
                if newItem.parameter[i] in table:
                    newItem.parameter[i] = table[newItem.parameter[i]]
            result.append(newItem)
    return result






def printKB(CNF):
    result = ""
    for item in CNF:
        if not item.flag:
            result+='~'
        result+=item.predicate
        result+='('
        for parameter in item.parameter:
            result+=parameter
            result+=','
        result+=')'
        result+='|'
    print (result)

if sys.version_info[0] >= 3:  
    raw_input = input  
  
tokens = (  
    'NAME','VARIABLE','IMPLY'  
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

t_IMPLY = r'=>'
    
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
    ('left','IMPLY'),  
    ('left','|','&'),   
    ('right','~'),  
    )  
  
# dictionary of names  
names = { }  

kb = []
root = TreeNode()


def p_statement(p):
    'statement : sentence'
    root = p[1]
    #printTree(root,0)
    eliminateImpl(root)
    #printTree(root,0)
    moveInward(root)
    #printTree(root,0)
    global kb
    kb+=distribute(root)
    # for s in kb:
    #     print ("SENTENCE-------------------")
    #     printTree(s,0)

def p_sentence_assign(p):  
    '''sentence : atomsentence
                | complexsentence'''
    p[0] = p[1]

def p_complexsentence(p):  
    '''complexsentence : '(' sentence ')'
                  | '~' sentence 
                  | sentence '|' sentence 
                  | sentence '&' sentence
                  | sentence IMPLY sentence'''
    if p[1] == '(':
        p[0] = p[2]
    elif p[1] == '~': 
        p[2].flag= not p[2].flag
        p[0] = p[2] 
    elif p[2] == '|':
        p[0] = TreeNode()
        p[0].left = p[1]
        p[0].right = p[3]
        p[0].relation = RELATION[1]
    elif p[2] == '&':
        p[0] = TreeNode()
        p[0].left = p[1]
        p[0].right = p[3]
        p[0].relation = RELATION[2]
    else:
        p[0] = TreeNode()
        p[0].left = p[1]
        p[0].right = p[3]
        p[0].relation = RELATION[3]

def p_predicate(p):
    "predicate : NAME"
    p[0] = p[1]

def p_atomsentence(p):
    "atomsentence : predicate '(' terms ')'"
    p[0] = TreeNode()
    p[0].predicate = p[1]
    p[0].parameter = p[3]
 

def p_terms(p):
    '''terms : term
            | term ',' terms'''
    p[0] = []
    p[0].append(p[1])
    if(len(p)>2):
        p[0] += p[3]

def p_term(p):
    '''term : constant
            | VARIABLE'''
    p[0] = p[1]
    # if (p[1][0]>='a' and p[1][0]<='z'):
    #     print ("Variable:"+p[1])
    # else:
    #     print ("CONSTANT:"+p[1])           
def p_constant(p):
    "constant : NAME"
    p[0] = p[1]  
  
def p_error(p):  
    if p:  
        print("Syntax error at '%s'" % p.value)  
    else:  
        print("Syntax error at EOF")  
   
yacc.yacc()  

KB = []
hashTable = {}

def inference(history,query):
    global KB
    global hashTable

    if history:
        for item in history:
            if item==query:
                return False

    for i in hashTable[query.predicate]:
        for item in KB[i]:
            if contradiction(query,item):
                newQueries = unification(query,item,KB[i])
                if not newQueries:
                    return True
                else:
                    boolean = True
                    for newQuery in newQueries:
                        newHistory = history
                        newHistory.append(query)
                        if not inference(newHistory,newQuery):
                            boolean = False
                            break
                    if boolean:
                        return True
                break
    return False

read = open("input.txt")
output = open("output.txt",'w')
x = int(read.readline())
for i in range(x):
    yacc.parse(read.readline().rstrip('\n'))
queries = kb
#for query in queries:
    #printTree(query,0)
kb = []
y = int(read.readline())
for i in range(y):
    s = read.readline().rstrip('\n')
    yacc.parse(s)
for sentence in kb:
    KB.append(generateKB(sentence))
    #printTree(sentence,0)
for i in range(len(KB)):
    for item in KB[i]:
        if item.predicate not in hashTable:
            hashTable[item.predicate] = list()
        hashTable[item.predicate].append(i)
    #printKB(KB[i])
#print (hashTable)

history = []

for query in queries:
    query.flag = not query.flag
    if(inference(history,query)):
        output.write("TRUE\n")
    else:
        output.write("FALSE\n")

# history = []
# print (history) 
# print (inference(history,queries[1]))

# for query in queries:
#     printTree(query,0)
#     history = []
#     print (inference(history,query))
#     printTree(query,0)
#     print ('-----------------')



# while 1:  
#     try:  
#         s = raw_input('calc > ')  
#     except EOFError:  
#         break  
#     if not s: continue  
#     yacc.parse(s)  