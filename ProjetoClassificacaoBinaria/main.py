import pandas as pd
import numpy as np

from TF_IDF import tf_idf
from RandomForest import randomforest

def init_y():
    Y = []
    for _ in range(100):
        Y.append(1)
    for _ in range(79):
        Y.append(0)
    return Y

def init_data():
    tfidfs = tf_idf.main()

    data = pd.DataFrame(tfidfs)
    data = data.fillna(0)
    data['classe'] = init_y()

    return data

def main():

    data = init_data()

    randomforest.execute_model(data)


    print("\nMatriz usada pelo modelo:\n")
    print(data)

    # Precisao esta ruim pois os features sao randomicamente escolhidos. Como a maioria dos features sao NaN, muitas features não
    # tem valor para a floresta


if __name__ == "__main__":
    main()