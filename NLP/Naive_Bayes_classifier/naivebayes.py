#!/usr/bin/env python
import sys
import math
import re
from collections import Counter 

def tokenize(text):
    text = re.sub(r'\s+'," ",text)
    tokens = text.split(" ")
    return tokens

def extract_data(data_file):
    #read the entire text in one shot
    text = data_file.read()
    #split the text into lines
    lines = text.split("\n")
    #split the labels and the speeches
    YnX = [e.split("\t") for e in lines]
    #Extract labels
    Y = [e[0] for e in YnX]
    #Extract speeches
    X = [e[1] for e in YnX]
    #Tokenize the speeches
    tokens = [tokenize(speech) for speech in X]
    #Form dictionary using unique tokens
    dictionary = set().union(*tokens)
    return Y,tokens,dictionary

def get_class_probs(Y):
    #Get counts of all classes
    class_counts = Counter(Y) 
    #Get the total number of examples
    total_class_counts = len(Y)

    P_class = {}
    for clas in class_counts.keys():
        P_class[clas] = -math.log((float(class_counts[clas]))/total_class_counts)
    return P_class

def get_term_counts_per_class(Y,tokens):
    #Get count for each term occuring in each of the speeches
    term_counts = Counter(element for speech in tokens for element in speech)

    counts_dict = {}
    #iterate over each of the speeches
    for i in range(len(Y)):
        speech = Y[i]
        terms = Counter(tokens[i])
        if speech in counts_dict.keys():
            curr_terms = counts_dict[speech]
            curr_terms += terms
            counts_dict[speech] = curr_terms
        else:
            counts_dict[speech] = terms
    #print (counts_dict['RED']['THE'])
    #print (sum(counts_dict['RED'].values()))
    return counts_dict

def get_term_probs_per_class(Y,tokens,dictionary):
    termcounts_class = get_term_counts_per_class(Y,tokens)
    #print (len(dictionary))
    probs_dict = {}
            
    for key,terms in termcounts_class.items():
        #make a copy so that we don't modify 
        #the original dictionary while performing 
        #add-one smoothing
        temp_counts = terms.copy()
        for term in temp_counts.keys():
            temp_counts[term] += 1
        denom = sum(terms.values()) + len(dictionary)
        for term in temp_counts.keys():
            temp_counts[term] /= float(denom)
            temp_counts[term] = -math.log(temp_counts[term])
        probs_dict[key] = temp_counts
    #print (probs_dict['RED']['THE'])
    return probs_dict    

def train(Y,tokens,dictionary):
    class_probs = get_class_probs(Y)
    prob_terms_class = get_term_probs_per_class(Y,tokens,dictionary)
    return class_probs,prob_terms_class

def get_prob_labelgivenspeech(label,speech,classprob,prob_tokens):
    prob_label = classprob
    product_termprobs  = sum([prob_tokens[token] for token in speech])
    prob_label += product_termprobs
    return prob_label

def calc_metrics(unique_labels,results,op_file):
    metrics_dict = {}
    relevance_measures = ["tp","fn","fp"]
    right = 0
    wrong = 0

    #accuracy  = (float(right))/(right+wrong)
    for label in unique_labels:
        metrics_dict[label] = {}
        for measure in relevance_measures:
            metrics_dict[label][measure] = 0
        
    for result in results:
        predicted = result[0]
        gold      = result[1]
        if predicted == gold:
            right += 1
            metrics_dict[predicted]["tp"] += 1
        else:
            wrong += 1
            metrics_dict[predicted]["fp"] += 1
            for label in unique_labels:
                if (label != predicted):
                    metrics_dict[label]["fn"] += 1
    for label in unique_labels:
        tp = metrics_dict[label]["tp"]
        fn = metrics_dict[label]["fn"]
        fp = metrics_dict[label]["fp"]
        metrics_dict[label]["precision"] = tp/float(tp+fp)
        metrics_dict[label]["recall"]    = tp/float(tp+fn)
    accuracy = right/float(right+wrong)
    op_str  = "overall accuracy\n" + str(accuracy) +"\n"
    op_str += "precision for red\n"
    op_str += str(metrics_dict['RED']['precision']) + "\n"
    op_str += "recall for red\n"
    op_str += str(metrics_dict['RED']['recall']) + "\n"
    op_str += "precision for blue\n"
    op_str += str(metrics_dict['BLUE']['precision']) + "\n"
    op_str += "recall for blue\n"
    op_str += str(metrics_dict['BLUE']['recall']) + "\n"
    op_str += "\n"
    op_file.write(op_str) 
    print ("\n\n")
    #print (results)
    #print (metrics_dict)

def test(Y,Y_test,tokens_test,class_probs,prob_terms_class,op_file):
    unique_labels = set(Y)
    results = []
    for (speech,test_label) in zip(tokens_test,Y_test):
        max_label = ""
        maximum = float("-inf")
        for label in unique_labels:
            temp = get_prob_labelgivenspeech(label,speech,class_probs[label],prob_terms_class[label])
            print (maximum,temp,label)
            if maximum < temp:
                maximum = temp
                max_label = label
        #print (math.exp(maximum))
        if (max_label != "" and max_label != test_label):
            print ("\n",maximum,max_label,test_label)
        results.append((max_label,test_label))
    calc_metrics(unique_labels,results,op_file) 

train1_filename = sys.argv[1]
test1_filename  = sys.argv[2]
train2_filename = sys.argv[3]
test2_filename  = sys.argv[4]

train1_file = open(train1_filename,"r")
test1_file  = open(test1_filename,"r")
train2_file = open(train2_filename,"r")
test2_file  = open(test2_filename,"r")
op_file     = open("task1.txt",'w+')

Y,tokens,dictionary = extract_data(train1_file)
class_probs,prob_terms_class = train(Y,tokens,dictionary)

Y_test,tokens_test,dictionary_test = extract_data(test1_file)
test(Y,Y_test,tokens_test,class_probs,prob_terms_class,op_file) 

Y,tokens,dictionary = extract_data(train2_file)
class_probs,prob_terms_class = train(Y,tokens,dictionary)

Y_test,tokens_test,dictionary_test = extract_data(test2_file)
test(Y,Y_test,tokens_test,class_probs,prob_terms_class,op_file) 

op_file.close()
