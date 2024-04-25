import json
import re
import math
from nltk.tokenize import word_tokenize
from utils import read_config
from indexer import calculate_tf, calculate_idf, generate_tf


def generate_queries(consultas_path):
    with open(consultas_path, 'r', encoding='utf-8') as file:
        queries = {}
        for i, line in enumerate(file):
            if i == 0:
                continue

            query_number, query_text = line.strip('\n').partition(';')[0], line.strip('\n').partition(';')[2]
            queries[query_number] = query_text
    return queries

def process_text(text):
    return re.sub(r'[^a-zA-Z\s]', ' ', text.replace('\n', ' ')).upper()

def create_tf_idf(file):
    queries = generate_queries(file)
    inverted_list = {}

    for number, text in queries.items():
            processed_text = process_text(text)
            word_tokens = word_tokenize(processed_text)
            print(word_tokens)
            for word in word_tokens:
                if (word not in inverted_list):
                    inverted_list[word] = []
                
                inverted_list[word] = inverted_list[word].append(number)

    tf = calculate_tf(inverted_list)
   