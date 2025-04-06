import numpy as np
from node import Node

class DecisionTreeClassifier():
    def __init__(self, min_samples_split=2, max_depth=4, n_features=None, feat_idxs=None):
        # quantidade minima de amostras necessarias para dividir, profundidade maxima da arvore
        
        self.root = None
        
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_features = n_features
        self.feat_idxs = feat_idxs
     
    def build_tree(self, dataset, current_depth=0):
        ''' metodo recursivo para construir a arvore '''
        
        # talvez de erro por causa da primeira linha do arquivo txt
        X, Y = dataset[:,:-1], dataset[:,-1] #X recebe todos features, Y recebe classificacao
        num_samples, total_num_features = np.shape(X)
        num_labels = len(np.unique(Y))
            
        # dividir ate encontrar as condicoes de parada
        if (num_samples>=self.min_samples_split and current_depth<=self.max_depth and num_labels>1):
            
            # procura pela melhor divisao
            best_split = self.get_best_split(dataset, num_samples)
            
            # confere se o ganho de informacao e positivo
            if best_split["info_gain"] > 0:
                
                #chama recursivamente este metodo para continuar as ramificacoes
                left_subtree = self.build_tree(best_split["dataset_left"], current_depth + 1)
                right_subtree = self.build_tree(best_split["dataset_right"], current_depth + 1)
                
                #retorna o no de decisao
                return Node(best_split["feature_index"], best_split["threshold"],
                            left_subtree, right_subtree, best_split["info_gain"])
                
        #retorna no folha
        leaf_value = self.calculate_leaf_value(Y)
        return Node(value=leaf_value)            
            
            
    def get_best_split(self, dataset, num_samples):
        '''' metodo para encontrar a melhor divisao '''
        
        # dicionario para armazenar a melhor divisao
        best_split = {}
        max_info_gain = -float("inf")
        
        # loop sobre todas as features
        for feature_index in self.feat_idxs:
            
            feature_values = dataset[:, feature_index]
            possible_thresholds = np.unique(feature_values)
            
            # loop sobre todos os valores da feature
            for threshold in possible_thresholds:
                
                # get current split
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                
                # confere se os filhos nao sao nulos
                if len(dataset_left)>0 and len(dataset_right)>0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    
                    # calcula o ganho de informacao
                    current_info_gain = self.information_gain(y, left_y, right_y, "gini")
                    
                    # atualiza a melhor divisao se necessario
                    if current_info_gain>max_info_gain:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = current_info_gain
                        max_info_gain = current_info_gain
                        
        # return best split
        return best_split
    
    def split(self, dataset, feature_index, threshold):
        ''' metodo para dividir a informacao '''
        
        dataset_left = np.array([row for row in dataset if row[feature_index]<=threshold])
        dataset_right = np.array([row for row in dataset if row[feature_index]>threshold])
        return dataset_left, dataset_right
    
    def information_gain(self, parent, l_child, r_child, mode="entropy"):
        ''' metodo para calcular o ganho de informacao '''
        
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        if mode=="gini":
            gain = self.gini_index(parent) - (weight_l*self.gini_index(l_child) + weight_r*self.gini_index(r_child))
        else:
            gain = self.entropy(parent) - (weight_l*self.entropy(l_child) + weight_r*self.entropy(r_child))
        return gain
    
    def entropy(self, y):
        ''' metodo para calcular a entropy '''
        
        class_labels = np.unique(y)
        entropy = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            entropy += -p_cls * np.log2(p_cls)
        return entropy
    
    def gini_index(self, y):
        ''' metodo para calcular o gini index '''
        
        class_labels = np.unique(y)
        gini = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            gini += p_cls**2
        return 1 - gini
    
    def calculate_leaf_value(self, Y):
        ''' metodo para calcular o no folha '''
        
        Y = list(Y)
        return max(Y, key=Y.count) #retorna o valor de maior incidencia, caso nao foi feita divisao exata
        
    def print_tree(self, tree=None, indent=" "):
        ''' metodo para printar a arvore '''
        
        if not tree:
            tree = self.root

        if tree.value is not None:
            print(tree.value)

        else:
            print("X_"+str(tree.feature_index), "<=", tree.threshold, "?", tree.info_gain)
            print("%sleft:" % (indent), end="")
            self.print_tree(tree.left, indent + indent)
            print("%sright:" % (indent), end="")
            self.print_tree(tree.right, indent + indent)
    
    def fit(self, X, Y):
        ''' metodo para criar a arvore, a partir de informacao '''
        
        total_num_features = np.shape(X)[1]
        
        # distincao entre modelo decision tree e random forest. Modelo random forest, atualiza
        # essa variavel automaticamente
        if self.n_features is None:
            self.n_features = total_num_features
        
        #seleciona features que serao usados. Todos no algoritmo Decision Tree Classifier, porem
        #apenas alguns no algoritmo Random Forest Classifier
        self.feat_idxs = np.random.choice(total_num_features, self.n_features, replace=False)
        
        dataset = np.concatenate((X, Y), axis=1)
        self.root = self.build_tree(dataset)
    
    def predict(self, X):
        ''' metodo para prever um novo dataset '''
        
        preditions = [self.make_prediction(x, self.root) for x in X]
        return preditions
    
    def make_prediction(self, x, tree):
        ''' metodo para prever um unico data point'''
        
        if tree.value!=None: return tree.value
        feature_val = x[tree.feature_index]
        if feature_val<=tree.threshold:
            return self.make_prediction(x, tree.left)
        else:
            return self.make_prediction(x, tree.right)
    
    def get_feat_idxs(self):
        return self.feat_idxs
    
        