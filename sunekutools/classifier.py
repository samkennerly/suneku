"""
Example scikit-learn classifier.
"""
from pandas import Categorical, DataFrame
from sklearn.datasets import load_iris

def iris_data():
    """
    DataFrame: Fisher's iris dataset from scikit-learn.
    Target column is 'species' as a Categorical.
    """
    iris = load_iris()
    cats = Categorical.from_codes(iris.target,iris.target_names)
    cols = iris.feature_names
    data = iris.data

    return DataFrame(data,columns=cols).assign(species=cats)



