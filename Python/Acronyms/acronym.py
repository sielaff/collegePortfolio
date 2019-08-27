stopwords = ["a", "about", "above", "after", "again", "against", "all",
             "am", "an", "and", "any", "are", "as", "at", "be", "because",
             "been", "before", "being", "below", "between", "both", "but",
             "by", "could", "did", "do", "does", "doing", "down", "during",
             "each", "few", "for", "from", "further", "had", "has", "have",
             "having", "he", "hed", "hell", "hes", "her", "here", "heres",
             "hers", "herself", "him", "himself", "his", "how", "hows", "i",
             "id", "ill", "im", "ive", "if", "in", "into", "is", "it",
             "its", "its", "itself", "lets", "me", "more", "most", "my",
             "myself", "nor", "of", "on", "once", "only", "or", "other",
             "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
             "she", "shed", "shell", "shes", "should", "so", "some", "such",
             "than", "that", "thats", "the", "their", "theirs", "them", "themselves",
             "then", "there", "theres", "these", "they", "theyd", "theyll",
             "theyre", "theyve", "this", "those", "through", "to", "too",
             "under", "until", "up", "very", "was", "we", "wed", "well",
             "were", "weve", "were", "what", "whats", "when", "whens",
             "where", "wheres", "which", "while", "who", "whos", "whom",
             "why", "whys", "with", "would", "you", "youd", "youll", "youre",
             "youve", "your", "yours", "yourself", "yourselves"]

# list of stopwords found online
# option -- could generate list of reject words to improve performance
#     might add this later if performance is noticeably bad

# TODO -- maybe remove hell, shell, well from this list -- without apostrophe
#         meaning is abstracted and could mistake a non-stopword for one

# array declarations

acronyms = []
acro_count = [1 for x in range(1000)]
definitions = []
specialChars = ['!', '@', '#', '$', '%', '^', '&', '*', '(',
                ')', '_', '+', '=', '`', '~', ',', '<', '.',
                '>', '[', '{', ']', '}', '/', '?', '\'', '|',
                '\n', '"', ' ', '', ';', ':']

# function definitions

def remove_special_chars(words):
    "Function used to remove special characters from a list of words."
    for i in range(0, len(words)):                            
        newWord = []
        for j in range(0, len(words[i])):                          # keep buffer of characters in the word
            if not words[i][j] in specialChars:                    # don't add to buffer if it's a special character
                newWord.append(words[i][j])
        words[i] = "".join(newWord)                                # word gets whatever's in the buffer
    return words                                                   # join to get 'word' and not ['w', 'o', 'r', 'd']
 
def split_hyphens(words):
    "Function used to separate hyphenated words into separate words."
    hyphen = True                                                  # flag to check if a word has been changed
    while hyphen:                                                  # we want to iterate thru until we know 
        hyphen = False                                             #      there's no more words to split
        hyphen_index = []                                          # index stores index where we need to add word
        hyphen_word = []                                           # word stores the word to insert at index
        for i in range (0, len(words)): 
            newWord = []
            for j in range(0, len(words[i])):                    
                if words[i][j] != '-':                             # keep word the same if you don't come across -
                    newWord.append(words[i][j])
                else:                                              # otherwise set flag, add _, update index and word
                    hyphen = True
                    newWord.append('_')
                    hyphen_word.append(words[i].split('-', 1))     # word gets whatever immediately follows the -
                    hyphen_index.append(i+1)
                    break                                          # break out of the for loop
            words[i] = "".join(newWord)                            # update the word (shorten it if there was a -)
        hyphen_count = 0                                           # need this if inserting multiple words at once
        for i in range(0, len(hyphen_index)):                      # ie. if we came across multiple hyphenated words
            words.insert(hyphen_index[i]+hyphen_count, hyphen_word[i][1])
            hyphen_count += 1                                      # insert the proper word at the index
    return words                                                  

# TODO -- make this less janky -- try using split

def get_word_type(line, index):
    "Function used to fill the 'types' array based on types of words."
    if index != 0 and line[index-1][len(line[index-1])-1] == '_':
        return 'h'
    if line[index].lower() in stopwords:
        return 's'
    if line[index] in acronyms:
        return 'a'
    if line[index][len(line[index])-1] == '_':
        return 'H'
    else:
        return 'w'

def gen_leader_type(words, i, pre_lead, pre_type, post_lead, post_type, pre_win, post_win):
    "Function to generate leader and type arrays for an acronym candidate."
    win_length = 2 * len(words[i])                        # size of pre-window and post-window is 2*word length
    if i <= win_length:                                   # if we don't have enough words to fill pre-window
        for j in range(0, i):
            if words[j] != '' and words[j] != ' ':
                pre_leader.append(words[j][0].lower())
                pre_type.append(get_word_type(words, j))
                pre_win.append(words[j])
    else:                                                 # if there are enough words to fill pre-window
        for j in range(i-win_length, i):
            if words[j] != '' and words[j] != ' ':
                pre_leader.append(words[j][0].lower())
                pre_type.append(get_word_type(words, j))
                pre_win.append(words[j])
    if len(words)-i <= win_length:
        for j in range(i+1, len(candidates)):
            if words[j] != '' and words[j] != ' ':
                post_leader.append(words[j][0].lower())
                post_type.append(get_word_type(words, j))
                post_win.append(words[j])
    else:                                                 # same process for post-window
        for j in range(i+1, i+win_length+1):
            if words[j] != '' and words[j] != ' ':
                post_leader.append(words[j][0].lower())
                post_type.append(get_word_type(words, j))
                post_win.append(words[j])

def build_lcs_matrix(x, y):
    "Function to generate the matrix of largest common subsequences."
    m = len(x)
    n = len(y)
    c = [[0 for u in range(0, n+1)] for v in range(0, m+1)]
    b = [['' for u in range(0, n+1)] for v in range(0, m+1)]
    for i in range(0, m+1):
        c[i][0] = 0
    for i in range(0, n+1):
        c[0][i] = 0
    for i in range(1, m+1):
        for j in range(1, n+1):
            if x[i-1] == y[j-1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = '<^'
            elif c[i-1][j] >= c[i][j-1]:
                c[i][j] = c[i-1][j]
                b[i][j] = '^'
            else:
                c[i][j] = c[i][j-1]
                b[i][j] = '<'
    return (b, c, c[m][n])

def parse_lcs_matrix(b, start_i, start_j, m, n, lcs_length, stk, vector_list):
    "Function to parse the LCS matrix to find every LCS."
    for i in range(start_i, m+1):
        for j in range(start_j, n+1):
            if b[i][j] == '<^':
                stk.append([j, i])
                if lcs_length == 1:
                    v = build_vector(stk, n)
                    vector_list.append(v)
                else:
                    parse_lcs_matrix(b, i+1, j+1, m, n, lcs_length-1, stk, vector_list)
                del stk[-1]
    return

def build_vector(stk, n):
    "Function to build a vector for the parse function."
    v = []
    for s in stk:
        v.append(s)
    return v

def convert_vector(v, size):
    "Function to convert vector to a single list mapping leaders to acronym letters."
    vec = [0 for u in range(size)]
    for i in range(0, size):
        for j in v:
            if j[1] == i+1:
                vec[i] = j[0]
    return vec

def vector_values(v, types):
    "Function to determine misses, stopcount, distance, and size of a given vector."
    stopcount = 0
    misses = 0
    for i in range(0, len(v)):
        if v[i] != 0:
            break
    first = i
    for i in range(len(v)-1, -1, -1):
        if v[i] != 0:
            break
    last = i
    size = last - first
    distance = len(v) - last
    for i in range(first, last):
        if v[i] > 0 and types[i] == 's':
            stopcount = stopcount + 1
        elif v[i] == 0 and types[i] != 's' and types[i] != 'h':
            misses = misses + 1
    return (stopcount, misses, size, distance)

def compare_vectors(a, b, word_type):
    "Function to compare vector values to determine acronym candidate."
    stopA = 99
    missA = 99
    sizeA = 99
    distA = 99
    (stopA, missA, sizeA, distA) = vector_values(v, word_type)
    stopB = 99
    missB = 99
    sizeB = 99
    distB = 99
    (stopB, missB, sizeB, distB) = vector_values(v, word_type)
    if missA > missB:
        return b
    elif missA < missB:
        return a
    if stopA > stopB:
        return b
    elif stopA < stopB:
        return a
    if distA > distB:
        return b
    elif distA < distB:
        return a
    if sizeA > sizeB:
        return b
    elif sizeA < sizeA:
        return a
    return a

# now we read the text file

import sys
if len(sys.argv) != 2:
    print "Usage: python acronym.py <file_name>"
    sys.exit(1)

filename = sys.argv[1]
try:
    f = open(filename, 'r')
except IOError:
    print "Error reading file."

# copy lines in text file to array and remove headings
#     these are lines that are entirely uppercase
# also remove lines that are just whitespace

lines = f.readlines()
f.close()
for i in range (0, len(lines)):
    if lines[i].isupper() or lines[i] == '\n':
        lines[i] = ' '
lines2 = []
for i in lines:
    if i != ' ':
        lines2.append(i)
lines = lines2

# now we begin the big loop

for line in lines:                                                # for every line of our file
    words = line.split(' ')                                       # split into words
    words = remove_special_chars(words)                           # remove special characters from the line
    words = split_hyphens(words)                                  # all-hyphenated-words become all_ hyphenated_ words
    candidates = []                                               # array, 1 = word is acronym candidate, 0 otherwise
    for word in words:                                            # candidate is all uppercase, btwn 3 and 10 chars
        if word.isupper() and len(word) >= 3 and len(word) <= 10:
            candidates.append(1)
        else:
            candidates.append(0)
    for i in range(0, len(candidates)):
        if candidates[i] == 1:
            pre_leader = []                                       # initialize arrays for each acronym candidate
            post_leader = []
            pre_type = []
            post_type = []
            pre_length = 0
            post_length = 0
            pre_win = []
            post_win = []
        
            gen_leader_type(words, i, pre_leader, pre_type, post_leader, post_type, pre_win, post_win)

            x = ''.join(pre_leader)                               # build the lcs matrix for the pre and post window
            y = words[i].lower()                                  # lcs is longest common subsequence btwn two words
            if x != '':
                (pre_b, pre_c, pre_length) = build_lcs_matrix(x, y)

            x = ''.join(post_leader)
            if x != '':
                (post_b, post_c, post_length) = build_lcs_matrix(x, y)
                                                                  # now we have the length of the lcs
            
	    if  ((float(pre_length)/float(len(y)))+0.2) >= 1 or ((float(post_length)/float(len(y)))+0.2) >= 1:
                                                                  # if both are below confidence level, stop
                pre_vector_list = []                              # more array declarations
                post_vector_list = []
                pre_vector = []
                post_vector = []
                stk = []
                
                if (float(pre_length)/float(len(y)))+0.2 >= 1:    # generate vectors for each lcs matrix
                    parse_lcs_matrix(pre_b, 0, 0, len(''.join(pre_leader)), len(y), pre_length, stk,  pre_vector_list)
                    for v in pre_vector_list:
                        pre_vector.append(convert_vector(v, len(''.join(pre_leader))))
		if (float(post_length)/float(len(y)))+0.2 >= 1:
                    parse_lcs_matrix(post_b, 0, 0, len(''.join(post_leader)), len(y), post_length, stk, post_vector_list)
                    for v in post_vector_list:
                        post_vector.append(convert_vector(v, len(''.join(post_leader))))

                use_pre = False                                    # denote whether we use pre-window or post-window
                use_post = False
                if pre_vector != []:
                    if len(pre_vector) > 1:                        # if we have multiple vectors, determine which to use
                        while len(pre_vector) >= 2:
		           to_del =  compare_vectors(pre_vector[0], pre_vector[1], pre_type)
                           pre_vector.remove(to_del)
                        defn = pre_vector[0]
                    else:
                        defn = pre_vector[0]
                    use_pre = True
						
                if post_vector != []:
                    if len(post_vector) > 1:
                        while len(post_vector) >= 2:
		            to_del =  compare_vectors(post_vector[0], post_vector[1], post_type)
                            post_vector.remove(to_del)
                        defn = post_vector[0]
                    else:
                        defn = post_vector[0]
                    use_post = True
                        
                if y != ' ' and not y.upper() in acronyms:          # add our acronyms to the acronym list
                    acronyms.append(y.upper())
                    def_string = []                                 # generate the string for the definition and add it
                    for i in range(0, len(defn)):
                        if defn[i] != 0:
                            if use_pre:
                                for j in range(i, len(defn)):
                                    def_string.append(pre_win[j])
                                    if defn[j] == len(y):
                                        break
                                break
                            elif use_post:
                                for j in range(i, len(defn)):
                                    def_string.append(post_win[j])
                                    if defn[j] == len(y):
                                        break
                                break
                    for j in range(0, len(def_string)):             # capitalize first letter of non-stopwords
                        if not def_string[j] in stopwords:
                            newS = []
                            for i in range(0, len(def_string[j])):
                                if i == 0:
                                    newS.append((def_string[j][i]).upper())
                                else:
                                    newS.append(def_string[j][i])
                            def_string[j] = ''.join(newS)
                    definitions.append(' '.join(def_string))
                elif y.upper() in acronyms:                         # increment count for acronym
                    acro_count[acronyms.index(y.upper())] += 1

print '%10s' % 'Acronyms', '%11s' % 'Appearances', '%10s' % 'Definitions'                  
for i in range(0, len(acronyms)):
    print '%10s' % acronyms[i], '%11s' % acro_count[i],  '%10s' % definitions[i]
