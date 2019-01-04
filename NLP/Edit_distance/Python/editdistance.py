#!/usr/bin/env python3
import sys
from collections import defaultdict

def ins_cost(ch):
    return int(1)

def del_cost(ch):
    return int(1)

def subs_cost(ch1,ch2):
    if (ch1 == ch2):
        return int(0)
    return int(1)
def min_bounds_check(i,j,min_edits):
    if (i >min_edits and j >  min_edits):
        return True
    return False

def vanilla_levenstein(source, dest,min_edits):
    n = len(dest)
    m = len(source)
    distance = [[float("inf")]*(m+1) for _ in range(n+1)]
    distance[0][0] = 0
    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + ins_cost(dest[i-1])
    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + del_cost(source[j-1])
    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j] +ins_cost(dest[i-1]), distance[i][j-1] + del_cost(source[j-1]) , distance[i-1][j-1] + subs_cost(source[j-1],dest[i-1]))
            #check if we can abort the search if distance is already greater than the current min distance found.
            if ( min_bounds_check(i,j,min_edits) and distance[i][j] > min_edits):
                return float("inf")
    return distance[n][m]

def is_swap_possible(a,b,i,j):
    return (a[j] == b[i-1] and a[j-1] == b[i]) 

def osa(source, dest,min_edits):
    n = len(dest)
    m = len(source)
    #print (source)
    #print (dest)
    #print (min_edits)
    distance = [[float("inf")]*(m+1) for _ in range(n+1)]
    distance[0][0] = 0
    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + ins_cost(dest[i-1])
    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + del_cost(source[j-1])
    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j] +ins_cost(dest[i-1]), distance[i][j-1] + del_cost(source[j-1]) , distance[i-1][j-1] + subs_cost(source[j-1],dest[i-1]))
            if (i > 1 and j > 1 and is_swap_possible(source,dest,i-1,j-1) ):
                distance[i][j] = min(distance[i][j],distance[i-2][j-2]+1)
            #check if we can abort the search if distance is already greater than the current min distance found.
            if (min_bounds_check(i,j,min_edits) and distance[i][j] > min_edits):
                return float("inf")
    return distance[n][m]
    
LEVENSTEIN = 1
OSA = 2
DL = 3
TRIE = 4

mode = int(sys.argv[1])
inp_file_name = sys.argv[2]
dict_file_name = sys.argv[3]
op_file_name = sys.argv[4]

ip_file = open(inp_file_name,'r')
dict_file = open(dict_file_name,'r')
op_file = open(op_file_name, 'w+')

ip_list = ip_file.readlines()
vocab = dict_file.readlines()

ip_list = [element.rstrip("\n") for element in ip_list]

vocab = sorted(vocab,key=len)
vocab = [element.rstrip("\n") for element in vocab]

scratch1 = open("scratchfile1.txt",'w+')
scratch2 = open("scratchfile2.txt",'w+')

correct = 0
i = 0
corrections = []
scratch1dict = {}
scratch2dict = {}
word_in_dict = 0
dict_in_word = 0

dict_set = set(vocab)

for word in ip_list:
    #Words not misspelt will be caught here
    if word in vocab:
        correct += 1
        op_file.write(word+' 0\n')
    #Else form a list of possible words that the misspelt word might map to
    else:
        wlen = len(word)
        #limit candidates to twice the length of the current word
        #since the string (misspelt) could just as easily be formed from scratch
        #or by replacing the each of the characters of a similar sized word  
        #from the dictionary
        max_len   = 2*wlen
        min_edits = wlen
        target_candidate = None
        for target in vocab:
            dist = min_edits
            if (word in target):
                word_in_dict += 1
                if (len(target) - len(word) <= 2):
                    if (LEVENSTEIN == mode):
                        dist = vanilla_levenstein(word,target,min_edits)
                    elif (OSA == mode):
                        dist = osa(word,target,min_edits)
            else:
                word_chars = set(list(word))
                target_chars = set(list(target))
        
                #if (len(word_chars^target_chars) <=5): 
                if (LEVENSTEIN == mode):
                    dist = vanilla_levenstein(word,target,min_edits)
                elif (OSA == mode):
                    dist = osa(word,target,min_edits)
                #print ("minedits:",min_edits)
            if (min_edits > dist):
                min_edits = dist
                target_candidate = target
                if (1 == min_edits):
                    break
        i += 1
        corrections.append((word,target_candidate,min_edits))
        op_file.write(target_candidate+" "+str(min_edits)+"\n")
