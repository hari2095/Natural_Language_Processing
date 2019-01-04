#!/usr/bin/env python
import os
import re

"""
###CODE PLAYGROUND
def conditional_to_upper(name,ref_str):
    if ref_str.isupper():
        return (name.upper())
    return name

ghost_capture = []
def replace_name(match):
    #print match.group(0)
    #print match.group(1)
    #print match.group()
    ghost_capture.append(match.group(1)) 
    split_name = match.group(0).split(match.group(1))    
    
    first_name = "John"
    last_name  = "Smith"

    first_name = conditional_to_upper(first_name,split_name[0])    
    last_name  = conditional_to_upper(last_name ,split_name[1])    

    replacement_str = first_name + match.group(1) + last_name
    #print replacement_str
    return replacement_str

names_file = open("names.txt","r")
names = names_file.read().splitlines()

sentence = "Sarah-Milstein John Gosden Patricio Martinez Gregory Ford Monica Bellucci -STEVE-MADDEN- Miguel Tejada Richard Sloat Nadja Swarovski Alfred Taubman Bob Aberamson Calvin Schaefer Harry Brattin Sarah Milstein "

#print names
for name in names:
    #print name
    split_name = name.split()
    name_regex = re.compile(re.escape(split_name[0]) + r'(?P<mid>[^a-zA-Z])' + re.escape(split_name[1]),flags=re.I) 
    #r'(?P<prechar>[^a-zA-Z])'

    #print surname_regex.pattern

    #sentence = surname_regex.sub('John\g<mid>Smith',sentence)
    sentence = re.sub(name_regex,replace_name,sentence)
    #print sentence
print ghost_capture
print sentence

###CODE PLAYGROUND

"""

def conditional_to_upper(name,ref_str):
    if ref_str.isupper():
        return (name.upper())
    return name

def replace_name(match):
    split_name = match.group(0).split(match.group(1))    
    
    first_name = "John"
    last_name  = "Smith"

    first_name = conditional_to_upper(first_name,split_name[0])    
    last_name  = conditional_to_upper(last_name ,split_name[1])    

    replacement_str = first_name + match.group(1) + last_name
    #print replacement_str
    return replacement_str

#1. Fetch all names to be eliminated from names.txt
names_file = open("names.txt","r")
names = names_file.read().splitlines()
names_file.close()

input_folder  = "nyt"
output_folder = "nytmodified"

if not os.path.isdir(output_folder):
    os.mkdir(output_folder,0755)

#2 Iterate over each file
for file_no in range(1000):
    input_file_name  = input_folder  + "/file" + str(file_no) + ".txt"
    input_file  = open( input_file_name,"r")

    #2.1 For each file, create a corresponding output file in the nytmodified directory
    output_file_name = output_folder + "/file" + str(file_no) + ".txt"
    output_file = open(output_file_name,"w")

    input_txt = input_file.read()

    found_names = []
    for name in names:
        match = re.search(name,input_txt)
        #2.2 If a name-to-be-eliminated is found, redact all occurences of the full
        #    name and add this name to a temporary list for this file
        if match:
            found_names.append(match.group())
        split_name = name.split()
        name_regex = re.compile(re.escape(split_name[0]) + r'(?P<mid>(\s))' + re.escape(split_name[1])) 
        input_txt = re.sub(name_regex,replace_name,input_txt)
                

    #2.3 Then proceed to remove only those surnames that have been 
    #    seen so far. Use regex - non-letterSurnamenon-letter
    for name in found_names:
        surname = name.split()[1]
        surname_regex = re.compile(re.escape(surname) + r'(?P<postchar>[^a-zA-Z])') 
        #print surname_regex.pattern

        input_txt = surname_regex.sub('Smith\g<postchar>',input_txt)
    
    output_file.write(input_txt)

    input_file.close()
    output_file.close()


