''' Term Frequency - Inverse Document Frequency '''

import re
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
#from sklearn.feature_extraction.text import TfidfVectorizer -> alternativa para simplificacao
    
    
def tokenize(text: str) -> List[str]:
    ''' Divide o texto em palavras singulares (tokens) '''
    
    # Remove pontuacao 
    cleaned_text = re.sub(r"[^\w\s]", "", text)
    
    # Divide o texto limpo em tokens
    tokens = cleaned_text.lower().split()
    return tokens


def calculate_word_frequencies(document: List[str]) -> Dict[str, int]:
    ''' Calcula a frequencia de cada palavra em um documento '''
    
    frequencies = {}
    for word in document:
        frequencies[word] = frequencies.get(word, 0) + 1
    
    return frequencies


def calculate_tf(word_counts: Dict[str, int], document_length: int) -> Dict[str, float]:
    '''  Calcula a frequencia de termos de cada palavra em um documento  '''
    
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


def visualize_tfidf(tfidf_matrix: pd.DataFrame):
    """Visualize the TF-IDF matrix using a heatmap."""
    plt.figure(figsize=(10, 10))
    sns.heatmap(tfidf_matrix, annot=True, cmap="YlGnBu")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def main():
    
    sentences = ["Life, if well lived, is long enough.",
                 "Your time is limited, so don't waste it living someone else's life."]
    
    documents = [tokenize(sentence) for sentence in sentences]
    #print(documents)
    
    documents_word_counts = [calculate_word_frequencies(doc) for doc in documents]
    #print(documents_word_counts)
    
    idf_dict = calculate_idf(documents_word_counts)
    #print(idf_dict)

    tfidfs = []
    for doc, doc_word_counts in zip(documents, documents_word_counts):
        tf_dict = calculate_tf(doc_word_counts, len(doc))
        tfidf_dict = calculate_tfidf(tf_dict, idf_dict)
        tfidfs.append(tfidf_dict)
        
    tfidf_matrix = pd.DataFrame(tfidfs, index=["Document A", "Document B"]).T
    print(tfidf_matrix)
    visualize_tfidf(tfidf_matrix) 
    
    
if __name__ == "__main__":
    main()