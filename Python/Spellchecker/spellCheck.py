def find_max(list):
    "A function to find the max of a given list [essentially obsolete with max(list)]"
    max = 0
    index = 0
    return_list = []
    j = 0
    for x in list:
        if x > max:
            max = x
            j = index
        index += 1
    return_list.append(max)
    return_list.append(j)
    return return_list
    
import numpy as np
import random

# hash table for what characters might be corrupted to

D = {}
D['a'] = ['z', 's', 'q']
D['b'] = ['v', 'g', 'h', 'n']
D['c'] = ['x', 'd', 'f', 'v']
D['d'] = ['s', 'e', 'f', 'c', 'x']
D['e'] = ['w', 'r', 'd']
D['f'] = ['d', 'r', 'g', 'v', 'c']
D['g'] = ['f', 't', 'h', 'b', 'v']
D['h'] = ['g', 'y', 'j', 'n', 'b']
D['i'] = ['u', 'o', 'k', 'j']
D['j'] = ['h', 'u', 'i', 'k', 'm', 'n']
D['k'] = ['j', 'i', 'o', 'l', 'm']
D['l'] = ['k', 'o', 'p']
D['m'] = ['n', 'j', 'k']
D['n'] = ['b', 'h', 'j', 'm']
D['o'] = ['i', 'p', 'l', 'k']
D['p'] = ['o']
D['q'] = ['w', 'a']
D['r'] = ['e', 't', 'f']
D['s'] = ['a', 'w', 'd', 'x', 'z']
D['t'] = ['r', 'y', 'g', 'f']
D['u'] = ['y', 'i', 'j', 'h']
D['v'] = ['c', 'f', 'g', 'b']
D['w'] = ['q', 'e', 's']
D['x'] = ['z', 's', 'd', 'c']
D['y'] = ['t', 'u', 'h', 'g']
D['z'] = ['a', 's', 'x']

# do it for capital letters

for c in  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
    D[c] = []
    for ch in D[c.lower()]:
        D[c].append(ch.upper())
        
# list for characters found, hash for times each character was found
        
chars_found = []
times_found = {}
first_letter = {}
word_count = 0

# separate test and train documents

lines = []
char_count = 0
for line in open("text.txt"):
    newstring = []
    if char_count >= 160000:
        break
    for c in line:
        char_count += 1
        newstring.append(c)
        if c in chars_found:
            times_found[c] += 1
        else:
            if ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')):
                chars_found.append(c)
                times_found[c] = 1
    lines.append(''.join(newstring))

for c in chars_found:
    first_letter[c] = 0

# find likelihood that a letter is the first letter in a word
    
flag = True
for line in lines:
    for c in line:
        if flag and D.get(c):
            word_count += 1
            first_letter[c] += 1
            flag = False
        if c == ' ' or c == '\n' or c == '"':
            flag = True

for c in chars_found:
    if D.get(c):
        first_letter[c] = (float)(first_letter[c])/(float)(word_count)
            
f = open("train.txt", 'w')
for line in lines:
    f.write(line)

# corrupt the test document at 10%

productions = {}
for c in chars_found:
    if c in D:
        productions[c] = {}
        productions[c][c] = 0
        for ch in D:
            productions[c][ch] = 0
        for ch in D[c]:
            productions[c][ch] = 0
            
lines = []
count = 0
for line in open("text.txt"):
    newstring = []
    for c in line:
        count += 1
        if count > 160000:
            num = random.randint(0, 100)
            if num < 10 and D.get(c):                      # change 10 in this line to 20 to change corruption rate
                new_c = D[c][random.randint(0, len(D[c])-1)]
                productions[c][new_c] += 1
                c = new_c
            else:
                if D.get(c):
                    productions[c][c] += 1
            newstring.append(c)
    lines.append(''.join(newstring))

# write the corrupted text to the test file
    
f = open("test.txt", 'w')
for line in lines:
    f.write(line)
    
states = {}

# states is hash of hashes, number of times one character was followed by another

for c in chars_found:
    if (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
        states[c] = {}
        for i in range(0, len(chars_found)):
            states[c][chars_found[i]] = 0

for line in open("train.txt"):
    for i in range(0, len(line)):
        if i < len(line)-1 and states.get(line[i]) and states.get(line[i+1]):
            states[line[i]][line[i+1]] += 1

for c in chars_found:
    for i in chars_found:
        if ((c >= 'A' and c <= 'Z')or(c >= 'a' and c <= 'z'))and((i >= 'A' and i <= 'Z')or(i >= 'a' and i <= 'z')):
            states[c][i] = (float)(states[c][i])/(float)(times_found[c])

# go through productions and fix error where a letter that doesn't appear has a 0% chance to corrupt to itself

for c in productions:
    if productions[c][c] == 0:
        productions[c][c] = 1
        
# find percentage of times letter was found and percentage of productions

total_prods = {}
for c in chars_found:
    if D.get(c) and productions.get(c):
        total_prods[c] = 0
        for ch in productions[c]:
            total_prods[c] += productions[c][ch]
        if total_prods[c] != 0:
            for ch in productions[c]:
                productions[c][ch] = (float)(productions[c][ch])/(float)(total_prods[c])

# generate 2d array of states -- transition matrix
# also generate 2d array of productions

for c in chars_found:
    if c >= ' ' and c < '~':
        if not states.get(c):
            states[c] = {}
        for ch in chars_found:
            if c >= ' ' and c < '~':
                if not states[c].get(ch):
                    states[c][ch] = 0

l_to_n = {}
n_to_l = {}
n_to_l_p = {}
l_to_n_p = {}
count = 0
transition = []
prods = []

for c in states:
    if c >= ' ' and c < '~':
        transition.append([])
        l_to_n[c] = count
        n_to_l[count] = c
        count += 1
count = 0
for c in productions:
    if D.get(c):
        prods.append([])
        l_to_n_p[c] = count
        n_to_l_p[count] = c
        count += 1

for i in range(0, len(transition)):
    for j in range(0, len(n_to_l)):
        transition[i].append(states[n_to_l[i]][n_to_l[j]])
        
for i in range(0, len(prods)):
    for j in range(0, len(n_to_l_p)):
        prods[i].append(productions[n_to_l_p[i]][n_to_l_p[j]])        
        
# now:
# states has a hash of the state transitions from letter to letter
# productions has a hash of the corruption likelihood
# transitions is a 2d array with the transitions at [i][j]
# l_to_n is a hash that maps a letter to its index in the transitions array
# n_to_l is a hash that maps an index in the transitions array to a letter

f = open("test.txt", 'r')

buffer = []
words = []
for w in f:
    for c in w:
        if c != ' ' and c!= '\n':
            if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
                buffer.append(c)
        else:
            words.append(''.join(buffer))
            buffer = []
    
max_val = 0
max_index = 0

for word in words:
    print word, 'corrected to', 
    i = 0
    ptr_ary = np.zeros((len(n_to_l),len(word)), dtype=int)
    hmm_ary = np.zeros((len(n_to_l),len(word)))
    correct_string = ''
    correct_states = []
    if len(word) >= 1:
        for y in word:
            for z in range(0, len(l_to_n)):
                max_list = []
                if productions.get(y):
                    if i == 0:
                        hmm_ary[z][0] = first_letter[n_to_l[z]] * prods[z][l_to_n_p[y]]
                    else:
                        for w in range(0, len(l_to_n)):
                            max_list.append(hmm_ary[w][i-1] * transition[w][z] * prods[l_to_n_p[n_to_l[z]]][l_to_n_p[y]])
                        value = find_max(max_list)
                        hmm_ary[z][i] = value[0]
                        ptr_ary[z][i] = value[1]
                        
            i += 1
        max_list = []
        for u in range(0, len(l_to_n_p)):
            max_list.append(hmm_ary[u][len(word)-1])
        value = find_max(max_list)
        max_index = value[1]
        for u in range(0, len(word))[::-1]:
            correct_states.append(max_index)
            max_index = ptr_ary[max_index][u]
        for u in correct_states[::-1]:
            correct_string += n_to_l_p[u]
        word = correct_string
        print correct_string
            
f = open("corrected.txt", 'w')

for word in words:
    f.write(word)
    f.write(' ')
                                 
