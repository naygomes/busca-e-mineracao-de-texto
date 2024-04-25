from unidecode import unidecode
from xml.etree import ElementTree as ET
from utils import read_config

def process_text(text):
    processed_text = unidecode(text.replace(';', '').upper())
    return processed_text

def sum_votes(votes):
    count = sum(1 for vote in votes if vote != '0')
    return str(count)

def generate_consultas(config_path):
    query_list = []

    config_file = read_config(config_path)
    leia_path = config_file['LEIA'][0]
    consultas_path = config_file['CONSULTAS'][0]

    with open(leia_path, 'r', encoding='utf-8') as file:
            doc = ET.parse(leia_path).getroot()
            for query in doc.findall('QUERY'):
                query_number = query.find('QueryNumber').text
                query_text = query.find('QueryText').text
                query_text_processed = process_text(query_text)
                query_list.append((query_number, query_text_processed))

    with open(consultas_path, 'w', encoding='utf-8') as file:
        file.write('QueryNumber;QueryText\n')
        for query_number, query_text in query_list:
            file.write(query_number + ';' + query_text + '\n')

def generate_esperados(config_path):
    query_list = []
    
    config_file = read_config(config_path)
    leia_path = config_file['LEIA'][0]
    esperados_path = config_file['ESPERADOS'][0]
    
    with open(leia_path, 'r', encoding='utf-8') as file:
        doc = ET.parse(leia_path).getroot()
        for query in doc.findall('QUERY'):
            query_number = query.find('QueryNumber').text
            records = {}
            for i in query.iter('Item'):
                records[i.text] = i.get('score')
            query_list.append((query_number, records))

    with open(esperados_path, 'w', encoding='utf-8') as file:
        file.write('QueryNumber;DocNumber;DocVotes\n')
        for query_number, records in query_list:
            for document, votes in records.items():
                file.write(query_number + ';' + document + ';' + sum_votes(votes) + '\n')

