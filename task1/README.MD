# IMPLEMENTAÇÃO DE UM SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL

Esta é a primeira atividade individual da disciplina **COS738 - Busca e Mineração de Texto**, ministrada pelo professor Geraldo Xexéo em 2024.1.

O objetivo desta tarefa é fazer um sistema de recuperação da informação divido em módulos especificados.

## COMO RODAR??

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

## OBS:

Caso dê algum erro de certificado no _stopwords_ ou no _word_tokenize_, rode os seguintes comandos no terminal:

- **stopwords:**

```
python3 -m nltk.downloader stopwords
```

- **word_tokenize:**

```
python3 -m nltk.downloader punkt
```
