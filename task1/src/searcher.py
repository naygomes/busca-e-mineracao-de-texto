import re
import math
import logging
from nltk.tokenize import word_tokenize
from utils import read_config, get_stemmer
from indexer import calculate_tf, calculate_tf_idf

logger = logging.getLogger(__name__)

def generate_queries(consultas_path):
    logger.info("Lendo os arquivos de dados")

    with open(consultas_path, 'r', encoding='utf-8') as file:
        queries = {}
        for i, line in enumerate(file):
            if i == 0:
                continue
    
            query_number, query_text = line.strip('\n').partition(';')[0], line.strip('\n').partition(';')[2]
            queries[query_number] = query_text
    
    logger.info("Arquivo de dados lido com sucesso")

    return queries

def process_text(text):
    return re.sub(r'[^a-zA-Z\s]', ' ', text.replace('\n', ' ')).upper()

def create_queries_tf_idf(consultas_path):
    queries = generate_queries(consultas_path)
    inverted_list = {}

    for number, text in list(queries.items()):
        processed_text = process_text(text)
        word_tokens = word_tokenize(processed_text)
        for word in word_tokens:
            if (word not in inverted_list):
                inverted_list[word] = []
            inverted_list[word] = inverted_list[word] + [number]

    tf_dict = {}
    for word, documents in inverted_list.items():
        for doc in documents:
            if (doc not in tf_dict):
                tf_dict[doc] = {}
            try:
                tf_dict[doc][word] += 1
            except:
                tf_dict[doc][word] = 1
    
    tf = calculate_tf(tf_dict)
    idf = {}
    total_docs = len(tf_dict)
    inverted_tf = {}

    for doc, words in tf.items():
        for word in words:
            if word not in inverted_tf:
                inverted_tf[word] = [doc]
            else:
                inverted_tf[word].append(doc)

    for word, docs in list(inverted_tf.items()):
        new_list = list(set(docs))
        number_docs_with_word = len(new_list)
        idf[word] = math.log(total_docs / (1 + number_docs_with_word))

    tf_idf = calculate_tf_idf(tf, idf)
    return tf_idf

def similarity(vector1, vector2):
    dot_product = 0
    for word in vector1:
        if word in vector2:
            dot_product += vector1[word] * vector2[word]
    magnitude1 = math.sqrt(sum(vector1[word] ** 2 for word in vector1))
    magnitude2 = math.sqrt(sum(vector2[word] ** 2 for word in vector2))
    try:
        return dot_product / (magnitude1 * magnitude2)
    except ZeroDivisionError:
        return 0

def searcher(config_path):

    logger.info("Lendo arquivo de configuração")

    config_file = read_config(config_path)

    logger.info("Arquivo de configuração lido com sucesso")

    modelo_path = config_file['MODELO'][0]
    consultas_path = config_file['CONSULTAS'][0]
    resultados_path = config_file['RESULTADOS'][0]

    use_stemmer = get_stemmer(config_file)

    resultados_path = resultados_path.rpartition('.')[0] + ('-stemmer.csv' if use_stemmer else '-nostemmer.csv')

    logger.info("Gerando tf_idf das consultas")

    query_tf_idf = create_queries_tf_idf(consultas_path)
    
    logger.info("Tf_idf das consultas gerado com sucesso")

    model_tf_idf = {}

    logger.info("Lendo arquivo de modelo")
    logger.info("Gerando tf_idf do modelo")

    with open(modelo_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            doc = line.partition(';')[0].rstrip()
            words = line.partition(';')[2].replace('\n', '').split(";")

            model_tf_idf[doc] = eval(words[0])
    logger.info("Arquivo de modelo lido com sucesso")
    logger.info("Tf_idf do modelo gerado com sucesso")

    searches = {}
    
    logger.info("Calculando similaridade")

    for query in query_tf_idf:
        searches[query] = {}
        for doc in model_tf_idf:
            searches[query][doc] = similarity(query_tf_idf[query], model_tf_idf[doc])
    
    logger.info("Similaridade calculada com sucesso")

    logger.info("Gerando dicionário de buscas ordenado por similaridade")

    searches_list = {}
    for query, docs in searches.items():
        searches_list[query] = dict(sorted(docs.items(), key=lambda item: item[1], reverse=True))
    
    logger.info("Dicionário de buscas gerado com sucesso")

    logger.info("Gerando saída em um arquivo csv")

    with open(resultados_path, 'w', encoding='utf-8') as file:
        file.write('QueryId;ResultList\n')
        for query, docs in searches_list.items():
            rank = 1
            for doc_number in docs:
                ordered_list = [rank, doc_number, searches_list[query][doc_number]]
                file.write(f'{query};{ordered_list}\n')
                rank += 1
    
    logger.info("Saída gerada com sucesso")
