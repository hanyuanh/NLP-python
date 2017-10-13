#suppose i have rules from q1
#implement CKY parser with Viterbi algo
#For a time I took the highest prob of "TOP" in the table as the root of the tree, but in fact the root has to be the
#upperright most angle of the table
import re
import math
import copy
import tree
    #first part regex: [^ ][ ]+
# sentence = "Which is last ?".split()
sentence = "Show me ground transportation in Westchester County .".split()
# sentence = "On Thursday .".split()
class Rule(object):
    def __init__(self, root, nodes, prob):
        #head is str
        #children is list of strs
        self.root = root
        self.nodes = nodes
        self.prob = prob

def getGrammar(filename):
    #The grammar file comes from q1, the format
    #ADVP -> ADVP_RB PP  # 0.285714285714
    #root nodes prob
    try:
        grammar_text = open(filename, 'r')
    except:
        print "Error"
    grammar = {}
    #key:   root:str
    #value: spans
    #           --listNodes
    #           --prob
    for line in grammar_text:
        ltmp = re.split(' -> | # ', line)
        root = ltmp[0]  # root
        listNode = ltmp[1].split()  # list of nodes
        log_prob = math.log10(float(ltmp[2][:-1])) #prob, -1 to cut the carriage
        if root not in grammar:
            grammar[root] = [[listNode, log_prob]]
        else:
            grammar[root].append([listNode, log_prob])
    return grammar

def cky(grammar, sentence):
    n = len(sentence)
    table = [[{} for i in range(n + 1)] for j in range(n + 1)]
    backpointers = [[{} for i in range(n + 1)] for j in range(n + 1)]
    #init: should be constant time to find out the tags of a word
    unkdict = {}
    unk_backpointers = {}
    #save unk as dict and backpointer before init
    for root in grammar:
        for span in grammar[root]:
            if "<unk>" in span[0]:
                unkdict[root] = span[1]
                unk_backpointers[root] = [span[0], None]
    #init:
    for j in range(1, n+1):
        bHasFound = False
        for ruleroot in grammar:
            # if ruleroot == "DT":
            #     print "DT"
            if ruleroot == "WHNP_WP":
                print "bp"
            for span in grammar[ruleroot]:
                if sentence[j - 1] in span[0]:
                    table[j - 1][j][ruleroot] = span[1]
                    backpointers[j-1][j][ruleroot] = [span[0], None]
                    bHasFound = True
        if bHasFound == False:
            table[j - 1][j] = copy.deepcopy(unkdict)
            for key in unk_backpointers:
                backpointers[j-1][j][key] = [[sentence[j-1]], None]
    # the following loops have problems
    for j in range(1, n+1):
        for i in reversed(range(0, j-1)):
            print "in list[{0}][{1}]".format(i, j)
            if i == 1 and j == 4 :
                print "breakp"
            for k in range(i+1, j):
                # table[i][j] += {A if A -> B C \in gram,
                # 				  B \in table[i][k]
                #				  C \in table[k][j]}
                for root in grammar:
                    for span in grammar[root]:
                        #span[0] is list of nodes
                        #span[1] is prob
                        if len(span[0]) == 2:
                            B = span[0][0]
                            C = span[0][1]
                            if B in table[i][k] and C in table[k][j]:
                                if root == "TOP":
                                    print "bp"
                                if root not in table[i][j]:
                                    table[i][j][root] = table[i][k][B] + table[k][j][C] + span[1]
                                    backpointers[i][j][root] = [span[0], k]
                                else:
                                    #they are logs! add them up
                                    log_prop = table[i][k][B] + table[k][j][C] + span[1]
                                    if log_prop > table[i][j][root]:
                                        table[i][j][root] = log_prop
                                        # rule = Rule(root, span[0], span[1])
                                        backpointers[i][j][root] = [span[0], k]
    # print table
    return table, backpointers
backpointers = []
def createTree(i, j, tag):
    #leaf or not?
    if backpointers[i][j][tag][1] != None:
        k = backpointers[i][j][tag][1]
        #tag
        #pos?
        children = []
        child = createTree(i, k)
        while child != None:
            children.append(child)
            #pos += length
            child = Tree


def main():
    grammar = getGrammar("q1_ans.data")
    table, backpointers = cky(grammar, sentence)
    #the func return a tree
    result = createTree(backpointers, 0, len(sentence))
if __name__ == '__main__':
    main()
