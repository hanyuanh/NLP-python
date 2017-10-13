# input trees binarized
import tree
import sys, fileinput
from collections import Counter
import re

#f = open("train.trees", 'r')
#f = open("train.trees.pre", 'r')
f = open("train.trees.pre.unk", 'r')
rules = Counter()

class Rule(object):
    #rules like S -> PP NP
    def __init__(self, head, children):
        #head is str
        #children is list of strs
        self.head = head
        self.children = children
        self.count = 0
        self.prob = 0.0

    def __str__(self):
        str = self.head + ' -> '
        for c in self.children:
            str += c + ' '
        str = str[:-1]
        return str

def _count_rules(s):
    result = tree.Tree.interior_node.match(s)
    if result != None:
        label = result.group(1)
        pos = result.end()
        children = []
        (child, length) = _count_rules(s[pos:])
        while child != None:
            children.append(child)
            pos += length
            (child, length) = _count_rules(s[pos:])
        result = tree.Tree.close_brace.match(s[pos:])
        if result != None:
            pos += result.end()
            #str = str(label + "->" children[0] + children[1])
            #rules = Counter()
            #rules.add()
            if len(children) > 0:
                str = label + " -> "
                for i in range(len(children)):
                    str += children[i].label + " "
                str = str[:-1]
                rules[str] += 1
            return tree.Node(label, children), pos
        else:
            return (None, 0)
    else:
        result = tree.Tree.leaf_node.match(s)
        if result != None:
            pos = result.end()
            label = result.group(1)
            if label == "Is":
                print label
            #label = label.replace("-LRB-", "(")
            #label = label.replace("-RRB-", ")")
            return (tree.Node(label,[]), pos)
        else:
            return (None, 0)

for line in f:
    t = tree.Tree.from_str(line)
    '''
    root = t.root
    tempnode = root
    if tempnode has children:
        record this node and its children as a tree
        input it into Counter()(like hash it)
    else:
        return 0
    '''
    _count_rules(line)
    # print t
    # traversal of binary tree
listRules = []
for item in rules.items():
    listRule = list(item)
    listRule.insert(0, listRule[0].split(' ')[0])
    listRules.append(listRule)
tags = Counter()
for rule in listRules:
    tags[rule[0]] += rule[2]
for rule in listRules:
    print "tags[rule[0]]: {0}".format;(tags[rule[0]])
    print "rule[2]: {0}".format(rule[2])
    print rule[2] / tags[rule[0]]
    rule.append(float(rule[2])/tags[rule[0]])
INT_MIN = -99999
prob = INT_MIN
most_freq_rule = ""
n_times = INT_MIN
for rule in listRules:
    if rule[2] > n_times:
        most_freq_rule = rule[1]
        n_times = rule[2]
print "'s' sum: {0}".format(sum);
print "ANS:\n"
print "How many rules? : {0}".format(listRules.__len__())
print "Most freq rule: {0} It occurs {1} times".format(most_freq_rule, n_times)
'''
for item i rules
'''
listStr = []
for rule in listRules:
    listStr.append("{0} # {1}\n".format(rule[1], rule[3]))
listStr.sort()
fo = open("q1_ans.data", 'w')
for rule in listStr:
    fo.write(rule)