#!/usr/bin/env python3
import sys
import re
from collections import Counter,defaultdict
import math
import string

def train_bigram(tokens, word_freq):
    bigram_counts = defaultdict(int)
    bigram_probs  = defaultdict(float)
    N = len(tokens)
    window = 10
    for i in range(1,N):
        bigram_counts[(tokens[i-1],tokens[i])] += 1
    for k,v in bigram_counts.items():
        w1 = k[0]
        bigram_probs[k] = float(v)/word_freq[w1]
    print(Counter(bigram_counts).most_common(10))
    print("")
    return (bigram_probs,bigram_counts)

def train_trigram(tokens, bigram_counts):
    trigram_counts = defaultdict(int)
    trigram_probs  = defaultdict(float)
    N = len(tokens)
    for i in range(2,N):
        trigram_counts[tokens[i-2],tokens[i-1],tokens[i]] += 1
    for k,v in trigram_counts.items():
        w1 = k[0]
        w2 = k[1]
        bigram_count = bigram_counts[w1,w2]
        trigram_probs[k] = float(v)/bigram_count
    print(Counter(trigram_counts).most_common(10))
    print("")
    return (trigram_probs, trigram_counts)
     
lambda0 = float(sys.argv[1])
lambda1 = float(sys.argv[2])
lambda2 = float(sys.argv[3])
lambda3 = float(sys.argv[4])

train_file_name  = sys.argv[5]
test_file_name = sys.argv[6]

output_file_name = "result.txt"

train_file = open(train_file_name,'r')
test_file  = open(test_file_name ,'r')

train_text = train_file.read()
train_file.close()

train_text = re.sub(r'\s+',r' ',train_text)
#Make all punctuations space separated
train_text = re.sub(r'([^\w\s])',r" \1 ",train_text)

tokens = train_text.split(" ")
tokens = [token for token in tokens if token != '']
unsmoothed_word_freq = Counter(tokens) 
#print (unsmoothed_word_freq.most_common())
word_freq = {}
word_freq['UNKNOWNWORD'] = 0

discard_list = []

train_text += " "
for k,v in unsmoothed_word_freq.items():
    if v < 5:
        discard_list.append(k)
        word_freq['UNKNOWNWORD'] += 1
    else:
        if k in word_freq.keys():
            word_freq[k] += 1
        else:
            word_freq[k] = v
set_diff = set(tokens) - set(discard_list)
smoothed_tokens = []
for token in tokens:
    if token in set_diff:
        smoothed_tokens.append(token)
    else:
        smoothed_tokens.append('UNKNOWNWORD')
tokens = smoothed_tokens
N = len(tokens)
vocab_size = len(word_freq)
uniform_prob = 1/vocab_size
uniform_interpol = float(lambda0) * uniform_prob

unigram_probs = {key:float(value)/N for (key,value) in word_freq.items() }

print ("unigram types count:")
print (len(word_freq))
print(Counter(word_freq).most_common(10))
print("")

print ("bigram types count:")
bigram_probs,bigram_counts = train_bigram(tokens,word_freq)
print (len(bigram_counts))

print ("trigram_probs:")
trigram_probs,trigram_counts = train_trigram(tokens,bigram_counts)
print (len(trigram_counts))

test_text = test_file.read()
test_file.close()
test_tokens = test_text.split(" ")
test_tokens = [token for token in test_tokens if token != '']

#find the list of tokens in the test set but not the training set
diff_list = list(set(test_tokens)-set(tokens))


set_diff = set(test_tokens) - set(diff_list)
smoothed_test_tokens = []
for token in test_tokens:
    if token in set_diff:
       smoothed_test_tokens.append(token)
    else:
       smoothed_test_tokens.append('UNKNOWNWORD') 
test_tokens = smoothed_test_tokens

N_test = len(test_tokens)
unigrams = unigram_probs.keys()
bigrams  =  bigram_probs.keys()
trigrams = trigram_probs.keys()

log_sum = float(0.0)
for i in range(2,N_test):
    w1 = test_tokens[i-2]
    w2 = test_tokens[i-1]
    w3 = test_tokens[i]

    #At the very minimum, the probability will be equal to the uniform distribution's probability
    prob = uniform_interpol
    #prob1 = 0.0
    #prob2 = 0.0
    #prob3 = 0.0
    #If unigram exists, use unigram_probability
    if (w1 in unigrams):
        #print (type(lambda1))
        #print (type(unigram_probs[w1]))
        #prob1= math.log(unigram_probs[w1])
        prob += lambda1*unigram_probs[w1]
    #If bigram exists, use that too
    if ((w1,w2) in bigrams):
        #prob2 = math.log(bigram_probs[(w1,w2)])
        prob += lambda2*bigram_probs[(w1,w2)]
    #If trigram exists, use that too
    if ((w1,w2,w3) in trigrams):
        #prob3 = math.log(trigram_probs[(w1,w2,w3)])
        prob += lambda3*trigram_probs[(w1,w2,w3)]
    #log_sum += (prob + lambda1*prob1 + lambda2*prob2 + lambda3*prob3)
    log_sum += math.log(prob)

print ("log_sum:"+str(log_sum))
log_sum *= float(-1)/N_test

perplexity = math.exp(log_sum)

print ("perplexity: ",perplexity)

op_file = open(output_file_name,'w+')
op_file.write(str(perplexity))
op_file.close()
