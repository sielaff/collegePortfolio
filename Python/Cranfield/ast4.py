import sys
import PorterStemmer

p = PorterStemmer.PorterStemmer()
import math
import numpy as np
output = ""
terms = {}
docs = {}
import json

stopwords =  ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
         "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
         "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
         "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how",
         "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's",
         "me", "more", "most", "my", "myself", "nor", "not", "of", "on", "once", "only", "or", "other", "ought", "our", "ours",
         "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such",
         "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
         "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
         "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's",
         "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd",
         "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

queries = []

with open ("./cran_qry.txt", 'r') as infile:
    while 1:
        word = ''
        line = infile.readline()
        if '.I' in line:
            query = []
            infile.readline()
        if line == '':
            break
        for c in line:
            if c.isalpha():
                word += c.lower()
            else:
                if word:
                    if word not in stopwords:
                        word = p.stem(word, 0, len(word)-1)
                        query.append(word)
                    word = ''
        queries.append(query)

final = []
for q in queries:
    if q not in final:
        final.append(q)

with open('TF_HASH.txt', 'r') as inFile:
    frequency = json.load(inFile)

with open('TOTAL_TERMS.txt', 'r') as inFile:
    totals = json.load(inFile)

with open('INV_FILE_HASH.txt', 'r') as inFile:
    inverse = json.load(inFile)
    
# tf = ln(1 + frequency/total)
# idf = ln(1 + docs containing term/total number of docs)

tfidf = {}

for i in range (0, len(final)):           # for each query
    query = final[i]
    tfidf[i] = {}                            # set up tfidf hash for that query
    for word in query:                       # for each word in that query
          # find tf * idf for that word in every document
        for docNum in range(1, 1400):             # for every document
            if word in frequency[str(docNum)]:
                freq = float(frequency[str(docNum)][word])
            else: freq = 0
            # freq now has term frequency of word in docNum
            total = float(totals[str(docNum)])
            tf = np.log(float(freq/total) + 1)
            # now have tf, calculate idf
            if word in inverse:
                contains = float(inverse[word]['total'])
            else:
                contains = 0
            idf = np.log(float(contains/1400) + 1)
            # have tf and idf, multiply
            tfidf[i][word] = tf * idf

print tfidf
            
