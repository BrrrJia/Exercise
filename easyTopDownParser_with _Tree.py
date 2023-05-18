# top_down_skeleton.py
# Jonas Kuhn, University of Stuttgart, 2020-23
# course "Parsing"

from nltk import CFG
from nltk import Tree

grammar = """
S -> NP VP
NP -> Det N
VP -> V | V NP
Det -> 'the' | 'an' | 'my' | 'most'
N -> 'elephant' | 'elephants' | 'mouse' | 'mice'
V -> 'sneezed' | 'giggled' | 'trumpeted' | 'tickled'
"""

def load_grammar(grammar):
    G = {}
    cfg = CFG.fromstring(grammar)
    for P in cfg.productions():
        if f'{P.lhs()}' not in G: # if the left-hand side of the production not in the G
            if P.is_nonlexical(): # if no terminal exists at the right-hand side of production 
                R = [] # initial one empty possible right side list
                for item in P.rhs(): # for each item in the right hand of production
                    R.append(f'{item}') # the right side list append the item in production
                R.reverse() # make one right side list reversed
                G[f'{P.lhs()}'] = [R] # add one possible right side as value into the dictionary
            else: # if at least one terminal exists at the right-hand side of production 
                R = []
                for item in P.rhs():
                    R.append(f'{item}')
                G[f'{P.lhs()}'] = [R]
        else: # if the left-hand side of the production already exists in the G
            if P.is_nonlexical():
                R = []
                for item in P.rhs():
                    R.append(f'{item}')
                R.reverse()
                G[f'{P.lhs()}'].append(R)
            else:
                R = []
                for item in P.rhs():
                    R.append(f'{item}')
                G[f'{P.lhs()}'].append(R)
    return G

def build_tree(seq):
    if not seq:
        return []
    else:
        (A,n) = seq[0]
        seq = seq[1:]
        subtrees = []
        for i in range(n):
            (ST, seq) = build_tree(seq)
            subtrees.append(ST)
        return (Tree(A,subtrees), seq)

# Boolean variable for switching tracing info on and off  
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
interactive = True # False

# internal format of cfg production rules with reversed right-hand sides (!)
G = {'S': [['VP', 'NP']], 
     'NP': [['N', 'Det']], 
     'VP': [['V']], 'Det': [['my'], ['the'], ['an'], ['most']], 
     'N': [['mice'],['elephant'], ['elephants'], ['mouse']], 
     'V': [['giggled'], ['sneezed'], ['trumpeted']]}

# main procedure:
def parse(G, tokens):
    # G:      dict with list of reversed rhs's for each non-terminal
    # tokens: list of input tokens

    if trace: print("parsing ", tokens, "...")

    # initialize data structures:
    stack    = ['S'] #initialize the stack as list and add the start symbol
    inbuffer = tokens # make token list as the initialized inbuffer
    detrive = [] # record the used productions and the arity

    # main loop:
    while len(inbuffer) > 0:
        if trace: print('           {:<40}{:>40}'.format(str(stack),str(inbuffer)))

        # expand
        if stack[-1] in G: # if the top item in the stack is the key in the Grammar dictionary       
            RHS = G[stack[-1]][0]
    
            if trace: print(" >expand ...")
            for elem in G[stack[-1]]:
                if elem[0] == inbuffer[0]:
                    RHS = elem
                    break
            
            detrive += [(stack[-1], len(RHS))]
            stack    = stack[:-1] + RHS# pop out the top item and add the value of the key to the stack
            inbuffer = inbuffer # inbuffer isn't changed
            


         # match
        elif stack[-1] == inbuffer[0]: # if the top item of stack is equal as the first item of inbuffer
            if trace: print(" >match ...")
            detrive += [(stack[-1], 0)]
            stack    = stack[:-1] # then the top item of stack is poped out
            inbuffer = inbuffer[1:] # the first item of inbuffer is also popped out
            
        # no match:
        else: 
            if trace: print(" >dead end!")
            break        
                

    if trace: print('           {:<40}{:>40}'.format(str(stack),str(inbuffer)))

    # termination
    if len(stack) == 0 and len(inbuffer) == 0: # if the stack and inbuffer lists are empty
        print("success!\n")
        Parsetree, seq = build_tree(detrive)
        Parsetree.draw()
    else:
        print("failure!\n")

# Later we will take the grammar in some other format, so we will have
# to convert it to our internal dict format:
# G =  load_grammar(grammar)

def demo():
    # show internal representation of grammar
    G = load_grammar(grammar)

    if trace: print("Internal grammar representation:\n",G)

    if interactive:
        # interactive way of running the parser in user input:
        while True:
        # The following could possibly be embedded in a loop to allow for trying out several inputs:
            sentence = input('Type sentence: ') # user can input the string to be parsed
            if sentence == 'q': # if the input string is 'q'
                break # the outside while-loop ends up
            tokens = sentence.split()  # split up string in tokens (using the default separator, i.e. space)
            # call actual parsing procedure:
            parse(G, tokens)
    else:
        tokens = "the elephant sneezed".split() 
        parse(G, tokens)
        tokens = "my mouse giggled".split() 
        parse(G, tokens)


demo()


