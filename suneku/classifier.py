"""
Classify data into categories with scikit-learn and pandas.
"""
from numpy import log2
from numpy.random import choice
from pandas import Categorical, DataFrame, Series, crosstab
from seaborn import pairplot
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegressionCV

def qrange(data,qbig=0.84,qsmall=0.16):
    """
    Series: Inter-quantile range for each column of a DataFrame.
    Close to standard deviation for normal input with default parameters.
    """
    return (data.quantile(qbig) - data.quantile(qsmall)) / 2

def traintest(data,trainfrac=0.25):
    """ 2-tuple: Training and testing views of a DataFrame. """
    data = DataFrame(data)

    nrows = len(data)
    nkeep = int(trainfrac * nrows)
    train = Series(False,index=range(nrows))
    train[choice(train.index,size=nkeep,replace=False)] = True
    print("Train with {:,} of {:,} rows".format(nkeep,nrows))

    return data.loc[train], data.loc[~train]

class LogisticClassifier:
    """
    Classify rows of a matrix into one of several categories.
    Return a DataFrame with category and probability for each row.

    Initialize using training data with known categories.
    Call with new data to classify each row.

    Input
        data    any valid DataFrame input: Training data.
        target  string or int: Name of column with known classes.
        **kwargs are passed to scikit-learn model.
    """

    def __init__(self,data,target,**kwargs):
        data = DataFrame(data,copy=True)
        training = data[data.columns.drop(target)]
        data[target] = data[target].astype('category')

        self.data = data
        self.model = LogisticRegressionCV(**kwargs)
        self.offset = training.median()
        self.scalar = qrange(training)
        self.target = target

        self.learn()

    classes = property(lambda self: self.data[self.target].cat.categories)
    features = property(lambda self: self.data.columns.drop(self.target))

    def __call__(self,data):
        """ DataFrame: Class prediction and confidence for each row. """
        features,probs = self.features, self.probs

        data = probs(DataFrame(data,columns=features))
        cats = DataFrame(index=data.index)
        cats['class'] = data.idxmax(axis=1).astype('category')
        cats['p_class'] = data.max(axis=1)

        return cats

    def __str__(self):
        """ str: Human-readable summary. """
        indent = "  {}".format
        keyval = "{:<8}: {}".format

        def lines():
            yield type(self).__name__
            yield keyval('target',self.target)
            yield keyval('samples',len(self.data))
            yield keyval('model',type(self.model).__name__)
            yield from ('features:',*map(indent,self.features))
            yield from ('classes :',*map(indent,self.classes))

        return '\n'.join(lines())

    def coefs(self):
        """ DataFrame: Fitted coefficients for each (class,feature). """
        classes,features,model = self.classes,self.features,self.model

        return DataFrame(model.coef_,index=classes,columns=features)

    @classmethod
    def demo(cls):
        """
        LogisticClassifier: Example with pre-loaded data.
        Uses Fisher's iris dataset from scikit-learn.
        """
        iris = load_iris()
        cats = Categorical.from_codes(iris.target,iris.target_names)
        data = DataFrame(iris.data,columns=iris.feature_names)
        data.insert(0,'species',cats)

        return cls(data,'species')

    def learn(self,**kwargs):
        """ None: Re-train model with new parameters. """
        data,rescaled,target = self.data,self.rescaled,self.target

        self.model.set_params(**kwargs)
        self.model.fit(rescaled(data),data[target])

    def probs(self,data):
        """ DataFrame: Class probabilities for each row in input. """
        classes,model,rescaled = self.classes,self.model,self.rescaled

        data = rescaled(data)
        probs = model.predict_proba(data)

        return DataFrame(probs,index=data.index,columns=classes)

    def quantile(self,q):
        """ Series: Value at quantile 'q' for each feature. """
        return self.data[self.features].quantile(q)

    def rescaled(self,data):
        """ DataFrame: Adjust offset and scale of input data. """
        return (DataFrame(data)[self.features] - self.offset) / self.scalar

    def show(self,**kwargs):
        """ seaborn PairGrid: Show pairwise relationships. """
        return pairplot(self.data,hue=self.target,**kwargs)

    def test(self,data):
        """ DataFrame: Compare predictions to known results. """
        target = self.target

        data = DataFrame(data)
        modeled = self(data)
        reality = data[target].astype('category')
        correct = modeled['class'] == reality

        # Calculate self-information in bits.
        surprise = modeled['p_class'].copy()
        surprise[~correct] = 1 - surprise[~correct]
        surprise = -log2(surprise)

        # Show percent correct and confusion matrix.
        print("{:.1%} correct".format(correct.mean()))
        print("\n{}\n".format(crosstab(reality,modeled['class'])))

        return ( modeled
                .assign(correct=correct)
                .assign(reality=reality)
                .assign(surprise=surprise)
                .sort_index(axis=1) )



