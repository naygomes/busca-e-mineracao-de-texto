import re
from xml.etree import ElementTree as ET
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from utils import read_config

def parse_record(record):
    record_number = record.find('RECORDNUM').text.replace(' ', '')
    
    abstract = record.find('ABSTRACT')
    if abstract is None:
        abstract = record.find('EXTRACT')

    if abstract is None:
        print('Erro ao abrir ' + record_number + ': ABSTRACT e EXTRACT inexistentes')
        abstract = ' '
    else:
        abstract = abstract.text

    abstract = re.sub(r'[^a-zA-Z\s]', ' ', abstract.replace('\n', ' ')).upper()
    return record_number, abstract

def generate_inverted_list(config_path):
    record_list = []

    config_file = read_config(config_path)
    leia_path = config_file['LEIA']
    escreva_path = config_file['ESCREVA'][0]

    for file in leia_path:
        doc = ET.parse(file).getroot()
        for record in doc.findall('RECORD'):
            record_number, abstract = parse_record(record)
            record_list.append((record_number, abstract))

    stop_words = set(stopwords.words('english'))
    inverted_list = {}

    for record_number, abstract in record_list:
        word_tokens = word_tokenize(abstract)
        filtered_list = [word for word in word_tokens if not word.lower() in stop_words and len(word) > 2]
        for word in filtered_list:
            if word not in inverted_list:
                inverted_list[word] = []
            inverted_list[word].append(record_number)

    with open(escreva_path, 'w', encoding='utf-8') as file:
        file.write('Word;DocumentsList\n')
        for word, documentsList in inverted_list.items():
            file.write(word + ';' + str(documentsList) + '\n')
