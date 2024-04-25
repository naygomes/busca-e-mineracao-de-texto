import logging
import copy
import math
from utils import read_config

logger = logging.getLogger(__name__)


def parse_dict(leia_path):
    inverted_list = {}

    with open(leia_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            word = line.partition(';')[0].rstrip()
            docs = line.partition(';')[2].replace('\n', '').split(";")

            if len(word) > 2:
                inverted_list[word] = docs
            
    return inverted_list

def generate_tf(leia_path):
    inverted_list = parse_dict(leia_path)

    tf_dict = {}

    for word, docs in list(inverted_list.items()):
        for doc in eval(docs[0]):    
        
            if doc not in tf_dict:
                tf_dict[doc] = {}

            if word not in tf_dict[doc]:
                tf_dict[doc][word] = 1
            else: 
                tf_dict[doc][word] += 1

    return tf_dict

def calculate_tf(tf_dict):
    tf_result = copy.deepcopy(tf_dict)
    for doc, words in list(tf_dict.items()):
        for word, occurrences in list(words.items()):
            tf_result[doc][word] = occurrences/len(words)

    return tf_result

def calculate_idf(leia_path):
    idf_dict = {}
    total_docs = len(generate_tf(leia_path))
    tf_dict = parse_dict(leia_path)

    for word, docs in list(tf_dict.items()):
        new_list = list(set(eval(docs[0])))
        number_docs_with_word = len(new_list)
        idf_dict[word] = math.log(total_docs / (1 + number_docs_with_word))
    return idf_dict

def calculate_tf_idf(tf, idf):
    tf_idf = {}
    for doc, words in list(tf.items()):
        for word in words:   

            if doc not in tf_idf:
                tf_idf[doc] = {}
            if word not in tf_idf[doc]:
                tf_idf[doc][word] = tf[doc][word] * idf[word]
    return tf_idf

def indexer(config_path):
    logger.info("Gerando consultas")
    config_file = read_config(config_path)
    logger.info("Arquivo de configuração lido com sucesso")

    leia_path = config_file['LEIA'][0]
    escreva_path = config_file['ESCREVA'][0]

    logger.info("Calculando tf")
    tf_dict= generate_tf(leia_path)
    tf = calculate_tf(tf_dict)
    logger.info("Tf calculado com sucesso")

    logger.info("Calculando idf")
    idf = calculate_idf(leia_path)
    logger.info("Idf calculado com sucesso")

    logger.info("Calculando tf_idf")
    tf_idf = calculate_tf_idf(tf, idf)
    logger.info("Tf_idf calculado com sucesso")


    logger.info("Gerando saída em um arquivo csv")

    with open(escreva_path, 'w', encoding='utf-8') as file:
        file.write('Document;TfIdfWords\n')
        for doc, wordsList in tf_idf.items():
            file.write(doc + ';' + str(wordsList) + '\n')
    
    logger.info("Saída gerada com sucesso")
