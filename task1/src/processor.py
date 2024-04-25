import logging
from unidecode import unidecode
from xml.etree import ElementTree as ET
from utils import read_config

logger = logging.getLogger(__name__)

def process_text(text):
    processed_text = unidecode(text.replace(';', '').upper()).replace('\n', '')
    processed_text = ' '.join(processed_text.split())
    return processed_text

def sum_votes(votes):
    count = sum(1 for vote in votes if vote != '0')
    return str(count)

def generate_consultas(config_path):
    logger.info("Gerando consultas")

    query_list = []

    logger.info("Lendo arquivo de configuração")

    config_file = read_config(config_path)

    logger.info("Arquivo de configuração lido com sucesso")

    leia_path = config_file['LEIA'][0]
    consultas_path = config_file['CONSULTAS'][0]

    logger.info("Lendo arquivo de dados")

    with open(leia_path, 'r', encoding='utf-8') as file:
            doc = ET.parse(leia_path).getroot()
            for query in doc.findall('QUERY'):
                query_number = query.find('QueryNumber').text
                query_text = query.find('QueryText').text
                query_text_processed = process_text(query_text)
                query_list.append((query_number, query_text_processed))
    
    logger.info("Arquivo de dados lido com sucesso")

    logger.info("Gerando saída em um arquivo csv")

    with open(consultas_path, 'w', encoding='utf-8') as file:
        file.write('QueryNumber;QueryText\n')
        for query_number, query_text in query_list:
            file.write(query_number + ';' + query_text + '\n')
    
    logger.info("Saída gerada com sucesso")

def generate_esperados(config_path):
    query_list = []

    logger.info("Lendo arquivo de configuração")
   
    config_file = read_config(config_path)

    logger.info("Arquivo de configuração lido com sucesso")
    
    leia_path = config_file['LEIA'][0]
    esperados_path = config_file['ESPERADOS'][0]
    
    logger.info("Lendo arquivo de dados")

    with open(leia_path, 'r', encoding='utf-8') as file:
        doc = ET.parse(leia_path).getroot()
        for query in doc.findall('QUERY'):
            query_number = query.find('QueryNumber').text
            records = {}
            for i in query.iter('Item'):
                records[i.text] = i.get('score')
            query_list.append((query_number, records))
    
    logger.info("Arquivo de dados lido com sucesso")

    logger.info("Gerando saída em um arquivo csv")

    with open(esperados_path, 'w', encoding='utf-8') as file:
        file.write('QueryNumber;DocNumber;DocVotes\n')
        for query_number, records in query_list:
            for document, votes in records.items():
                file.write(query_number + ';' + document + ';' + sum_votes(votes) + '\n')
    
    logger.info("Saída gerada com sucesso")


