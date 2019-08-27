# write a program which will read in the documents from the file "doc-text" from the cranfield collection and output the following:
#       For each document in the collection print
#             1. its id number
#             2. the number of unique terms in the document
#             3. for each unique term, print the term and its term frequency
#             4. sort the terms alphabetically
# ignore case, stemmed with the porter stemmer, remove stopwords

# create an inverted file of the collection
# store the inverted file in an external file (basically a big hash)
# ex HASH = {
#   word1 = [1, [[x, y]]]
#   word2 = [3, [[x, y]], [[x, y]], [[x, y]]]
# }

import json
import sys
import PorterStemmer

p = PorterStemmer.PorterStemmer()
output = ""
terms = {}
docs = {}

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
         "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]


termsPerDoc = {}
totalTermsPerDoc = {}

with open ("./cran.all.1400", 'r') as infile:

    while 1:
        output = ''
        word = ''
        line = infile.readline()
        if '.I' in line:
            docNum = int(line.split(' ')[1])
            docs[docNum] = []
            termsPerDoc[int(docNum)] = {}
            totalTermsPerDoc[int(docNum)] = 0
            while '.W' not in line:
                line = infile.readline()
        if line == '':
            break
        for c in line:
            if c.isalpha():
                word += c.lower()
            else:
                if word:
                    if word in stopwords:
                        break
                    word = p.stem(word, 0, len(word)-1)
                    output += p.stem(word, 0,len(word)-1)
                    if word not in terms:
                        terms[word] = 1
                    else:
                        terms[word] += 1
                    if word not in termsPerDoc[docNum]:
                        termsPerDoc[docNum][word] = 1
                    else:
                        termsPerDoc[docNum][word] += 1
                    if word not in docs[docNum]:
                        docs[docNum].append(word)
                    word = ''
                    totalTermsPerDoc[int(docNum)] += 1
                output += c.lower()
appearsIn = {}

for key in sorted(terms.iterkeys()):
    appearsIn[key] = []
    for key2 in sorted(docs.iterkeys()):
        if key in docs[key2]:
            appearsIn[key].append(key2)
            
inverseHash = {}
for key in sorted(appearsIn.iterkeys()):
    inverseHash[key] = []
    inverseHash[key].append(len(appearsIn[key]))
    inverseHash[key].append(appearsIn[key])

with open('./INV_FILE_HASH.txt', 'w') as outFile:
    done = 0
    outFile.write('{\n')
    for key in sorted(inverseHash.iterkeys()):
        outFile.write('     "' + key + '": ' + '{"total": "' + str(inverseHash[key][0]) + '", "docs": ["' + str(inverseHash[key][1][0]))
        for i in inverseHash[key][1][1:]:
            outFile.write('","' + str(i))
        done += 1
        if done < len(terms):
            outFile.write('"]},\n')
        else:
            outFile.write('"]}\n')
    outFile.write('}')
    
    
print len(terms), "unique terms"

with open('./TF_HASH.txt', 'w') as outFile:
    json.dump(termsPerDoc, outFile)

with open('./TOTAL_TERMS.txt', 'w') as outFile:
    json.dump(totalTermsPerDoc, outFile)
