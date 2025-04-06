class Node():
    
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        #caracteristica de divisao, valor/limiar da divisao, acesso aos nos fihlos, ganho de info, valor
        
        #decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain
        
        #leaf node
        self.value = value
