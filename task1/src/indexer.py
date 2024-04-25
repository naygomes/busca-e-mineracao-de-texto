from operator import invert
import copy
import os
import math
import json
from utils import read_config


def invert_tf(tf):
    inverted_tf = {}
    for word, docs in tf.items():
        for word in words:
            if word not in inverted_tf:
                inverted_tf[word] = {}
            # if doc not in inverted_tf[word]:
                # inverted_tf[word][doc] = tf[doc][word]
    return inverted_tf

def generate_tf(leia_path):
    inverted_list = {}

    with open(leia_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            word = line.partition(';')[0].rstrip()
            docs = line.partition(';')[2].replace('\n', '').split(";")

            if len(word) > 2:
                inverted_list[word] = docs
            
    tf_dict = {}

    for word, docs in list(inverted_list.items()):
        for doc in eval(docs[0]):    
        
            if doc not in tf_dict:
                tf_dict[doc] = {}

            if word not in tf_dict[doc]:
                tf_dict[doc][word] = 1
            else: 
                tf_dict[doc][word] += 1

    tf_result = copy.deepcopy(tf_dict)
    for doc, words in list(tf_dict.items()):
        for word, occurrences in list(words.items()):
            tf_result[doc][word] = occurrences/len(words)
    return tf_result


def generate_idf(tf):
    idf = {}
    itf = invert_tf(tf)
    for word in itf:
        idf[word] = math.log(len(tf) / len(itf[word]))
    return idf

# def tf_idf(tf, idf):


def indexer(config_path):
    config_file = read_config(config_path)

    leia_path = config_file['LEIA'][0]
    escreva_path = config_file['ESCREVA'][0]
    tf = generate_tf(leia_path)
    
indexer('config/INDEX.CFG')