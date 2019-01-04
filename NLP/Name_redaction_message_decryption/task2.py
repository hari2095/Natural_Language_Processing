#!/usr/bin/env python
import collections

alphabet = "abcdefghijklmnopqrstuvwxyz"

def init_dict(given_dict):
    for letter in alphabet:
        given_dict[letter] = 0
    return given_dict

def combine_dicts (dict_1,dict_2):
    for letter in alphabet:
        dict_1[letter] += dict_2[letter]
    return dict_1

def frequency_analysis(text):
    return_dict = {}
    return_dict = init_dict(return_dict)
    for letter in alphabet:
        return_dict[letter] = text.count(letter)        
    return return_dict



corpus_folder  = "nyt"

corpus_dict    = {}
encrypted_dict = {}
corpus_dict    = init_dict(corpus_dict)

#1 Iterate over each file in the corpus
for file_no in range(1000):
    corpus_file_name  = corpus_folder  + "/file" + str(file_no) + ".txt"
    corpus_file  = open(corpus_file_name,"r")

    text = corpus_file.read()

    recv_dict = frequency_analysis(text)
    corpus_dict = combine_dicts(recv_dict,corpus_dict)

    corpus_file.close()

#2 Perform frequency analysis for the encrypted file
encrypted_file = open("mit.txt","r")
text = encrypted_file.read()

encrypted_dict = frequency_analysis(text)

#Save both dictionaries in descending order of counts
sorted_corpus = collections.OrderedDict(sorted(corpus_dict.items(), key=lambda item:item[1],reverse=True))
sorted_edict  = collections.OrderedDict(sorted(encrypted_dict.items(), key=lambda item:item[1],reverse=True))    

#Store a mapping from the corpus character to the message character
mapping = {}



for (k1,v1),(k2,v2) in zip(sorted_corpus.iteritems(),sorted_edict.iteritems()):
    mapping[k2] = k1
    #print "{" + k1 + ":" + str(v1) +"||" + k2 + str(v2) + "}" 

mapping['v'] = 'a'
mapping['y'] = 'b'
mapping['o'] = 'd'
mapping['m'] = 'f'
mapping['x'] = 'g'
mapping['c'] = 'i'
mapping['h'] = 'j'
mapping['z'] = 'l'
mapping['p'] = 'n'
mapping['t'] = 'o'
mapping['l'] = 'p'
mapping['u'] = 'q'
mapping['w'] = 'u'
mapping['a'] = 'v'
mapping['f'] = 'w'
mapping['b'] = 'y'
mapping['g'] = 'z'

#print mapping

decoded_file = open("decoded.txt","w")

decrypted_text = ""
for ch in text:
    if ch.isalpha():
        if ch.isupper():
            decrypted_text += mapping[ch.lower()].upper()
        else:    
            decrypted_text += mapping[ch]
    else:
        decrypted_text += ch
    
decoded_file.write(decrypted_text)
decoded_file.close()
