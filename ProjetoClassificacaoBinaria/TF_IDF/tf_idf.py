''' Term Frequency - Inverse Document Frequency '''

import re
from typing import Dict, List

import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None) 

path = "/home/beckerpedro/Documentos/Ceos/ProjetoClassificacaoBinaria/Extractor/dataset/dataset_79_100.txt"

# Retorna lista de documentos (texto de cada publicacao tokenizado)
def data_to_documents_list(path):
    docs = []
    with open(path, "r") as file:
        linha = file.readline() # linha recebe uma linha de classificação
        linha = file.readline() # linha recebe um texto
        while linha != "":
            docs.append(tokenize(linha))
            for _ in range(3):
                linha = file.readline() # pula para próximo texto
    return docs

# Retorna lista de dicionários com contagem (value) de cada palavra (key) de cada documento
def docs_process(docs): 
    documents_word_counts = []
    for doc in docs:
        documents_word_counts.append(calculate_word_frequencies(doc))
    return documents_word_counts

# Retorna texto tokenizado  
def tokenize(text: str) -> List[str]:
    ''' Divide o texto em palavras singulares (tokens) '''
    
    # Remove espaços desnecessários
    cleaned_text = text.strip()

    # Remove pontuacao 
    cleaned_text = re.sub(r"[^\w\s]", "", cleaned_text)
    
    # Divide o texto limpo em tokens
    tokens = cleaned_text.lower().split()

    #filtra por palavras sem valor como numeros
    return tokens

# Retorna dicionário com
def calculate_word_frequencies(document: List[str]) -> Dict[str, int]:
    ''' Calcula a frequência de cada palavra em um documento '''
    
    frequencies = {}
    for word in document:
        frequencies[word] = frequencies.get(word, 0) + 1
    
    return frequencies


def calculate_tf(word_counts: Dict[str, int], document_length: int) -> Dict[str, float]:
    '''  Calcula a frequência de termos de cada palavra em um documento  '''
    
    tf_dict = {word: count / float(document_length) for word, count in word_counts.items()}
    
    return tf_dict


def calculate_idf(documents_word_counts: List[Dict[str, int]]) -> Dict[str, float]:
    ''' Calcula a frequencia inversa do documento para cada palavra em todos documentos '''
    
    N = len(documents_word_counts)
    idf_dict = {}
    unique_words = set(word for doc in documents_word_counts for word in doc)
    
    for word in unique_words:
        #conta o numero de documentos que contem a palavra
        doc_containing_word = sum(word in document for document in documents_word_counts)
    
        idf_dict[word] = np.log10((N + 1) / (doc_containing_word + 1))
        
    return idf_dict


def calculate_tfidf(tf_dict: Dict[str, float], idf_dict: Dict[str, float]) -> Dict[str, float]:
    ''' Calcula o TF-IDF de cada palavra em um documento '''
    
    tfidf_dict = {word: tf_val * idf_dict[word] for word, tf_val in tf_dict.items()}
    
    return tfidf_dict


def main():
    
    documents = data_to_documents_list(path)        # lista com listas de tokens
    
    documents_word_counts = docs_process(documents) # lista de dicionarios com frequencia de cada palavra
    
    idf_dict = calculate_idf(documents_word_counts) # dicionario

    tfidfs = []
    for doc, doc_word_counts in zip(documents, documents_word_counts):
        tf_dict = calculate_tf(doc_word_counts, len(doc))
        tfidf_dict = calculate_tfidf(tf_dict, idf_dict)
        tfidfs.append(tfidf_dict)

    return tfidfs
    
if __name__ == "__main__":
    main()