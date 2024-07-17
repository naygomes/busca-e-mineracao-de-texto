# IMPLEMENTAÇÃO DE UM SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL

Esta é a primeira atividade individual da disciplina **COS738 - Busca e Mineração de Texto**, ministrada pelo professor Geraldo Xexéo em 2024.1.

O objetivo desta tarefa é fazer um sistema de recuperação da informação divido em módulos especificados.

## PRÉ-REQUISITOS

- [Python 3](https://www.python.org/downloads/)
- [Anaconda](https://www.anaconda.com/download)
  - nltk
  - numpy
  - pandas
  - matplot
  - Jupyter Notebook

## COMO RODAR O CÓDIGO??

1. Primeiro, clone o repositório do projeto:

```
git clone https://github.com/naygomes/busca-e-mineracao-de-texto.git
```

2. Agora, acesse a pasta "task1" pelo terminal:

```
cd busca-e-mineracao-de-texto/task1
```

3. instale todas as dependências:

```
pip3 install -r requirements.txt
```

4. Por fim, basta rodar o arquivo:

```
python3 src/main.py
```

#### OBS:

Caso dê algum erro de certificado no _stopwords_ ou no _word_tokenize_, rode os seguintes comandos no terminal:

- **stopwords:**

```
python3 -m nltk.downloader stopwords
```

- **word_tokenize:**

```
python3 -m nltk.downloader punkt
```

## STEMMER VS NOSTEMMER

Nos arquivos **BUSCA.CFG**,**GLI.CFG** e **PC.CFG** que estão na pasta _config_, há uma linha referente ao Stemmer (primeira linha).

Para **ativar** a técnica, basta colocar a linha com valor **STEMMER**.

Para **desativar**, basta colocar a linha com valor **NOSTEMMER**.

Após isso, basta rodar o código do passo 4 para que os arquivos sejam gerados.

## AVALIAÇÃO DOS RESULTADOS

Para executado o arquivo que calcula as métricas presentes no [RELATORIO.MD](https://github.com/naygomes/busca-e-mineracao-de-texto/blob/main/task1/avalia/RELATORIO.MD), basta executar o seguinte comando dentro da pasta **task1**:

```
jupyter notebook
```

Um link local (http://localhost:8888/tree/src) se abrirá com o ambiente de desenvolvimento Jupyter. O arquivo de avaliação está dentro da pasta _src_ (src/evaluator.ipynb).
