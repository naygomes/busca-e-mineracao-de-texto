import re
import logging
from xml.etree import ElementTree as ET
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import *

from utils import read_config, get_stemmer

stemmer = PorterStemmer()

logger = logging.getLogger(__name__)

def parse_record(record, use_stemmer):
    record_number = record.find('RECORDNUM').text.replace(' ', '')
    
    abstract = record.find('ABSTRACT')
    if abstract is None:
        abstract = record.find('EXTRACT')

    if abstract is None:
        print('Erro ao abrir ' + record_number + ': ABSTRACT e EXTRACT inexistentes')
        abstract = ' '
    else:
        abstract = abstract.text

    if use_stemmer:
        logger.info("Usando stemmer para a geração da lista invertida")
        abstract = ' '.join([stemmer.stem(word) for word in abstract.split()])
    
    abstract = re.sub(r'[^a-zA-Z\s]', ' ', abstract.replace('\n', ' ')).upper()

    return record_number, abstract

def generate_inverted_list(config_path):
    record_list = []

    logger.info("Lendo arquivo de configuração")

    config_file = read_config(config_path)

    logger.info("Arquivo de configuração lido com sucesso")

    leia_path = config_file['LEIA']
    escreva_path = config_file['ESCREVA'][0]
    use_stemmer = get_stemmer(config_file)
       
    logger.info("Lendo os arquivos de dados")

    for file in leia_path:
        doc = ET.parse(file).getroot()
        for record in doc.findall('RECORD'):
            record_number, abstract = parse_record(record, use_stemmer)
            record_list.append((record_number, abstract))
    
    logger.info("Arquivo de dados lido com sucesso")

    logger.info("Gerando palavras de parada")

    stop_words = set(stopwords.words('english'))
    inverted_list = {}

    logger.info("Palavras de parada geradas com sucesso")

    logger.info("Gerando lista invertida")

    for record_number, abstract in record_list:
        word_tokens = word_tokenize(abstract)
        filtered_list = [word for word in word_tokens if not word.lower() in stop_words and len(word) > 2]
        for word in filtered_list:
            if word not in inverted_list:
                inverted_list[word] = []
            inverted_list[word].append(record_number)
    
    logger.info("Lista invertida gerada com sucesso")

    logger.info("Gerando saída em um arquivo csv")

    with open(escreva_path, 'w', encoding='utf-8') as file:
        file.write('Word;DocumentsList\n')
        for word, documentsList in inverted_list.items():
            file.write(word + ';' + str(documentsList) + '\n')
    
    logger.info("Saída gerada com sucesso")
