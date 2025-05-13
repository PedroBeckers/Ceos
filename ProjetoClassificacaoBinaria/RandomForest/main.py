""" Modelo: https://github.com/AssemblyAI-Community/Machine-Learning-From-Scratch/tree/main/05%20Random%20Forests """

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from RandomForest import randomforest

def new_step(text):
    print("\n" + "*" * (len(text) + 4))
    print("  " + text)
    print("*" * (len(text) + 4) + "\n")

# coletando informacao
new_step("coletando informação...")
data = pd.read_csv(r"/home/beckerpedro/Documentos/Ceos/ClassifierAlgorithms/GenericDatasets/breast_cancer_data.csv")

# ajuste para todas colunas serem exibidas
pd.options.display.max_columns = 6
pd.options.display.max_rows = 10
pd.options.display.width = 90

# exibindo previa da tabela
print(data)
print("\ninformação coletada com sucesso!")

# divisao treino-teste (20% teste e 80% treino)
print("\ndividindo informação entre treino e teste de predição...")
X = data.iloc[:, :-1].values
Y = data.iloc[:, -1].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2, random_state=41)
print("informação dividida com sucesso!")

# criando a arvore a partir da informacao dada
new_step("criando a árvore de decisão a partir da informação de treino...")
classifier = randomforest.RandomForest(n_trees=10, max_depth=2, min_samples_split=3)
classifier.fit(X_train,Y_train)
classifier.print_trees()
print("\nárvore de decisão criada com sucesso!")

# testando a precisao da arvore criada
new_step("testando a precisão de predição da árvore criada...")
Y_pred = classifier.predict(X_test)
print("teste realizado com sucesso!")
print("Precisão: " + str(accuracy_score(Y_test, Y_pred)))
print("\nfinalizando execução...")
 