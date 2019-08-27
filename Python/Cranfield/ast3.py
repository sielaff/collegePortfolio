# build a program which will interactively read in a boolean string query and return all the documents in the inverted file which match it
# output should be a list of document ids for a given query
# stem and remove stopwords from queries
# treat 'AND 'OR 'NOT' and () as special operators
# order of precedence: () -> NOT -> AND, OR

import json
import sys
import PorterStemmer
p = PorterStemmer.PorterStemmer()

stopwords =  ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
              "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
              "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
              "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
              "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's",
              "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours",
              "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such",
              "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
              "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
              "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's",
              "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd",
              "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "not"]


q = raw_input("Query: ")
q = q.split()
qry = []
for w in q:
    w = w.replace("(", "( ")
    w = w.replace(")", " )")
    w = w.split()
    for c in w:
        qry.append(c)

# qry is now a list with parentheses separate

query = []
word = ''
for w in qry:
    if w == '(' or w == ')':
        word = w
    else:
        for c in w:
            if c.isalpha():
                word += c.lower()
        if word not in stopwords:
            word = p.stem(word, 0, len(word) - 1)
    query.append(word)
    word = ''

# now ready to check query; words are stemmed and stopwords are removed; parentheses still intact
# check parentheses
parens = 0
for i in query:
    if parens < 0: print "Query poorly formed, please check parentheses."; exit()
    if i == '(': parens += 1
    elif i == ')':  parens -= 1
if parens != 0: print "Query poorly formed, please check parentheses."; exit()

with open ('INV_FILE_HASH.txt', 'r') as inFile:
    invHash = json.load(inFile)

# invHash is inverted hash imported as json

nums = []
for i in range(1, 1401):
    nums.append(i)

# list of numbers for not-ing
    
docs = {}
    
for word in query:
    if word not in stopwords and word != '(' and word != ')':
        docs[word] = []
        for i in invHash[word]['docs']:
            docs[word].append(int(i))
        docs['!' + word] = [x for x in nums if x not in invHash[word]['docs']]

# docs that words appear in and docs they don't
        
changed = True
while changed:
    changed = False
    for i in range(0, len(query)):
        if query[i] == 'not' and query[i+1] != '(':
            changed = True
            w = query[i+1]
            del query[i+1]
            query.insert(i+1, "!" + w)
            del query[i]
            break
        
# dealt with nots that are directly before a word
        
print query

while ('(' in query):
    start = 0
    end = len(query)

    for (i, c) in enumerate(query):
        if c == '(':
            start = i
        if c == ')':
            end = i + 1
            break
    replace = []
    for j in query[start + 1:end - 1]:
        replace.append(j)
    del query[start:end]
    query.insert(start, replace)

def evaluate(w1, w2, op):
    sol = []
    if op == 'or':
        sol = w1 + w2
    elif op == 'and':
        for i in w1:
            if i in w2:
                sol.append(i)
    return sol
    
def eval_query(q):
    w1, op, w2 = q
    if isinstance(w1, list):
        w1 = eval_query(w1)
    else: w1 = docs[w1]
    if isinstance(w2, list):
        w2 = eval_query(w2)
    else: w2 = docs[w2]
    return evaluate(w1, w2, op)

print eval_query(query)
