from .tree import DecisionTreeClassifier
from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import numpy as np
import pandas as pd

def execute_model(data):

    print("\niniciando execução do modelo...\n")

    # divisao treino-teste (20% teste e 80% treino)
    print("dividindo informação entre treino e teste de predição...")
    X = data.iloc[:, :-1].values
    Y = data.iloc[:, -1].values.reshape(-1,1)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2, random_state=3)
    print("informação dividida com sucesso!")

    # criando a arvore a partir da informacao dada
    print("\ncriando as árvores de decisão a partir da informação de treino...")
    classifier = RandomForest(n_trees=5, max_depth=4, min_samples_split=3)
    classifier.fit(X_train,Y_train)
    classifier.print_trees()
    print("\nrandom forest criada com sucesso!\n")

    # testando a precisao da arvore criada
    print("testando a precisão de predição da floresta criada...\n")
    Y_pred = classifier.predict(X_test)
    print("teste realizado com sucesso!")
    print("Precisão: " + str(accuracy_score(Y_test, Y_pred)))
    print("\nfinalizando execução...\n")
    
    return

class RandomForest():
    
    def __init__(self, n_trees=5, max_depth=5, min_samples_split=3, total_features=None):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.total_features = total_features
        self.trees = []
        
    def fit(self, X, Y):
        '''' metodo para criar as arvores da florest, conforme informacao oferecida '''
        
        self.total_features = X.shape[1]      
        n_optmized_features = int(np.sqrt(self.total_features))
        
        for _ in range(self.n_trees):
            tree = DecisionTreeClassifier(min_samples_split=self.min_samples_split,
                                          max_depth=self.max_depth, n_features=n_optmized_features)
            X_sample, Y_sample = self.bootstrap_samples(X, Y)
            tree.fit(X_sample, Y_sample)
            self.trees.append(tree)
    
    def bootstrap_samples(self, X, Y):
        ''' metodo para randomizar escolha das features de divisao em cada arvore '''
        n_samples = np.shape(X)[0]
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], Y[idxs]
    
    def most_commom_label(self, Y):
        ''' metodo para selecionar valor de maior incidencia de retorno de cada arvore para certo 
            sample de predição '''
        counter = Counter(Y)
        most_commom = counter.most_common(1)[0][0]
        return most_commom
    
    def predict(self, X):
        ''' metodo para prever novo dataset '''
        predictions = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(predictions, 0, 1)      
        predictions = np.array([self.most_commom_label(pred) for pred in tree_preds])
        return predictions
    
    def print_trees(self):
        for i in range(self.n_trees):
            tree = self.trees[i]
            
            idx_list = tree.get_feat_idxs()
            
            text = (", ".join(map(str, idx_list)))
            
            print("\nÁrvore " + str(i + 1))
            print("\nfeatures randomicamente selecionados: " + text + "\n")
            tree.print_tree()
