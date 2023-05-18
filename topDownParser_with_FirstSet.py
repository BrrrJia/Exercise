# top_down_reference.py
# Jonas Kuhn, University of Stuttgart, 2023
# course "Parsing"

from nltk import CFG

# Boolean variable for switching tracing info on and off  
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
interactive = True # False

# string format used in nltk.CFG class:
# our test grammar:
grammar = """
S -> NP VP
NP -> DET N
VP -> V
DET -> 'the' | 'an' | 'my' | 'most'
N -> 'elephant' | 'elephants' | 'mouse' | 'mice'
V -> 'sneezed' | 'giggled' | 'trumpeted'
"""

grammar2 = """
S    -> '(' S Op S ')' | Num
Num  -> Sign Num | '1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'0'
Op   -> '+' | '-' | '*' | '/'
Sign -> '-'
"""

grammar3 = """
S -> NP VP
NP -> DET N | DET N PP | 'I'
VP -> V | V NP | V NP PP
PP -> P NP
DET -> 'the' | 'an' | 'my' | 'most'
P -> 'in'
N -> 'elephant' | 'elephants' | 'mouse' | 'mice' | 'pajamas'
V -> 'sneezed' | 'giggled' | 'trumpeted' | 'saw' | 'shot'
"""

# conversion procedure for grammar:
def load_grammar(grammar_string):
    cfg = CFG.fromstring(grammar_string)
    grammar = {}
    for prod in cfg.productions():
        nt = str(prod.lhs())
        rrhs = [str(a) for a in reversed(prod.rhs())]
        if nt not in grammar:
            grammar[nt] = [rrhs]
        else:
            grammar[nt].append(rrhs)
    return grammar

G = load_grammar(grammar2)

# get grob first sets
def get_first_dict(grammar=G):
    # grammar: the grammar used in parser

    first_dict = {}
    for key, value in grammar.items():
        first_dict[key]= []
        for prod in value:
            first_dict[key].append(prod[-1])
    return first_dict

first_dict = get_first_dict(G)

# get the first set for one non-terminal
def first_set(nonterminal: str, frist_dictionary=first_dict):
    # nonterminal: one non-terminal
    # frist_dictionary: dict of the grob first sets

    remove_list = []
    add_list = []
    for count, elem in enumerate(frist_dictionary[nonterminal]):
        if elem in frist_dictionary:
            remove_list.append(elem)
            add_list.extend(first_set(elem)[1])
    for elem in remove_list:
        frist_dictionary[nonterminal].remove(elem)
    frist_dictionary[nonterminal].extend(add_list)
    return frist_dictionary, frist_dictionary[nonterminal]

# get the first set for all the non-terminal
def get_all_first_set(frist_dictionary=first_dict):
    # frist_dictionary: dict of the grob first sets
    
    for key,value in frist_dictionary.items():
        first_set(key)
    for key,value in frist_dictionary.items():
        frist_dictionary[key] = set(value)
    return frist_dictionary

# main procedure:
def parse(G, tokens):
    # G:      dict with list of reversed rhs's for each non-terminal
    # tokens: list of input tokens

    if trace: print("parsing ", tokens, "...")

    # (preprocessing) get the first set
    First = get_all_first_set()
    print(First)

    # initialize data structures:
    stack    = ["S"]
    inbuffer = tokens

    # main loop:
    while len(inbuffer) > 0:
        if trace: print('           {:<40}{:>40}'.format(str(stack),str(inbuffer)))

        # expand
        if stack[-1] in G:  # there must be a non-terminal on top of the stack
            rrhs = G[stack[-1]][0]

            # to avoid being completely blind, choose a different production
            # in case it starts with the terminal that's next in the inbuffer:
            for Prod in G[stack[-1]]:
                if inbuffer[0] == Prod[-1]:
                    rrhs = Prod
                    break # keep the one for which there is a match, discard other productions
                # with considering the first set, if the top one of buffer in 
                # the first set of the leftmost in the production, then choose this
                elif Prod[-1] in First: # if the leftmost is a non-terminal
                    if inbuffer[0] in First[Prod[-1]]:
                        rrhs = Prod
                        break # keep the one for which there is a match, discard other productions
            
            if trace: print(" >expand: ", stack[-1], " -R-> ", rrhs)

            # the reversed rhs from the chosen production replaces NT on the stack
            stack = stack[:-1] + rrhs

            # leave variable inbuffer unchanged

        # match
        elif stack[-1] == inbuffer[0]:  # terminal on top of the stack matches next input symbol
            if trace: print(" >match:  ", stack[-1])
            stack = stack[:-1]  # pop top element from the stack
            inbuffer = inbuffer[1:]  # consume first element from input buffer

        # no match:
        else:  # terminal on top of the stack doesn't match next input symbol
            if trace: print(" >dead end!")
            break  # since we cannot backtrack, we have to discard this attempt
                   # (without having reached a termination condition)

    if trace: print('           {:<40}{:>40}'.format(str(stack),str(inbuffer)))

    # termination
    if not (len(stack) > 0 or len(inbuffer) > 0):
        print("success!\n")
    else:
        print("failure!\n")


def demo():
    # show internal representation of grammar
    if trace: print("Internal grammar representation:\n",G)

    if interactive:
        # interactive way of running the parser in user input:
        
        # The following could possibly be embedded in a loop to allow for trying out several inputs:
        sentence = input('Type sentence: ') # user can input the string to be parsed
        tokens = sentence.split()  # split up string in tokens (using the default separator, i.e. space)

        # call actual parsing procedure:
        parse(G, tokens)
    else:
        tokens = "the elephant sneezed".split() 
        parse(G, tokens)
        tokens = "my mouse giggled".split() 
        parse(G, tokens)


demo()


