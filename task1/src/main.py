from processor import generate_consultas, generate_esperados
from generator import generate_inverted_list
from indexer import indexer
from searcher import searcher


processor_consultas = generate_consultas('config/PC.CFG')
processor_esperados = generate_esperados('config/PC.CFG')

generator_inverted_list = generate_inverted_list('config/GLI.CFG')

model_tf_idf = indexer('config/INDEX.CFG')

searcher_results = searcher('config/BUSCA.CFG')

