'''
Convenience classes for using scikit-learn classifiers with pandas DataFrames
'''
import sunekutools as st
import pickle

from sklearn.linear_model import LogisticRegressionCV
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


TEXT_MODELS = [MultinomialNB, SGDClassifier]



# Convenience functions

def get_practice_data(verbose=True):
    '''
    Package the Fisher iris dataset from scikit-learn as a DataFrame
    OUTPUTS
      Data      DataFrame with numeric predictors and categorical target
    '''

    # sklearn stores the dataset as "Bunch" object.
    # This is somewhat like a dictionary.
    from sklearn.datasets import load_iris
    iris = load_iris()

    # Show detailed explanation?
    if verbose:
        print( iris['DESCR'] )

    # Load predictors and convert to a DataFrame
    Data = st.pd.DataFrame(iris.data,columns=iris.feature_names)
    Data.index.name = 'FlowerId'

    # Change the column names to names I like better

    def short_name(long_name):
    
        # Drop the ' (cm)' from each name
        short_name = long_name[:-5]
        
        # Capitalize both words
        short_name = short_name.title()
        
        # Remove space between words
        short_name = short_name.replace(' ','')
        
        return short_name

    Data.columns = [ short_name(x) for x in Data.columns ]

    # Target column is an array of 0's, 1's, and 2's.
    # Make it a categorical variable instead.
    category_labels = st.pd.Series(iris.target_names).str.capitalize()
    Target = st.pd.Series(iris.target)
    Target = Target.map(category_labels).astype('category')

    # Attach the target column to [Data]
    Data['Type'] = Target

    return Data



# Custom classes

class Classifier():
    '''
    Generic classifier template not intended for actual use.
    Each type of classifier has its own class derived from this one.
    '''


    # Utility methods

    def __init__(self,
        data,
        target,
        predictors  = [],
        model       = None,
        text_mode   = False,
        params      = dict() ):
        '''
        INPUTS
            data        DataFrame: one target column and one or more predictor columns
            target      string: which column of [data] to use as target?
            predictor   optional list: columns of data to use as predictors
            text_mode   optional bool: use text predictors?
            model       sklearn classifier model
            params      dict: parameters to pass to model
        NOTES
            If no [predictors] input, then all columns except target_name will be used as predictors.
            Columns of [data] will be ordered like this: target, then sorted(predictors)
            Before initializing, consider defining indicator variables, standardizing inputs, etc.
        '''

        # If no predictor_names, then use all columns as predictors
        if len(predictors) == 0:
            predictors = [ x for x in data.columns if x != target ]

        # Pass parameters to model
        model = model(**params)

        # Enforce sort order (this is important!)
        categories  = sorted(data[target].unique())
        predictors  = sorted(predictors)
        data        = data[ [target] + predictors ]

        if text_mode:

            assert len(predictors) == 1, \
                "Text must be stored as a single column."

            assert any([ isinstance(model,x) for x in TEXT_MODELS ]), \
                "Text mode has not been tested with this model:\n%s" % model

            # Extract word count and weight by TF-IDF score to create features.
            # See http://scikit-learn.org/stable/modules/feature_extraction.html
            steps = [
                ( 'vectorize',  CountVectorizer() ),
                ( 'tfidf',      TfidfTransformer() ),
                ( 'classify',   model ) ]
            model = Pipeline(steps)

        self.model      = model
        self.data       = data
        self.target     = target
        self.categories = categories
        self.predictors = predictors
        self.text_mode  = text_mode

    def __repr__(self):
        ''' Human-readable description of Classifer object '''

        msg = "Classifier object with %s samples\n" % len(self.data)
        if self.text_mode:
            msg += "Text mode is enabled\n"
        msg += "\n"
        
        msg += "Target:\n  "
        msg += self.target + "\n\n"

        msg += "Categories:\n  "
        msg += "\n  ".join(self.categories) + "\n\n"

        msg += "Predictors:\n  "
        msg += "\n  ".join(self.predictors) + "\n\n"

        if isinstance(self.model,Pipeline):
            msg += "Pipeline:\n  "
            msg += "\n  ".join( x[0] for x in self.model.steps ) + "\n\n"         
            msg += "Model:\n  "
            msg += str(self.model.steps[-1][1])
        else:
            msg += "Model:\n  "
            msg += str(self.model)

        return msg

    def _unpack(self,data=None):
        '''
        Separate target column and predictor columns from data.
        If no data input, then use all of [self.data]
        INPUTS
          data          optional chunk of [self.data] or similar DataFrame
        OUTPUTS
          Predictors    column(s) of [self.data] to use as predictors
          Target        column to be predicted
          Cats          sorted categories of target
        '''

        if data is None:
            data = self.data

        Target      = data[self.target]
        Cats        = self.categories
        Predictors  = data[self.predictors]

        return Target, Cats, Predictors


    # User methods

    def reset(self,params):
        '''
        Reset the model with new parameters
        INPUTS
          params    dict of parameters for whatever sklearn model we're using
        Caution: modifies self.Model
        ''' 
        self.model.__init__(**params)

    def target_freq(self,data=None):
        '''
        How often does each category appear in target column of data?
        If no data input, then use all of self.data.
        INPUTS
          data      optional chunk of [self.data] or similar DataFrame
        OUTPUTS
          Freq      human-readable Series of category frequencies
        '''

        if data is None:
            data = self.data

        Target, Cats, Predictors = self._unpack(data)
        Freq = Target.value_counts().sort_index() / len(Target)

        return Freq

    def pairplot(self,data=None):
        '''
        Show histograms of predictors colored by target type.
        Show scatterplots of all pairs of predictors.
        If no data input, then use all of self.data.
        INPUTS
          data      optional chunk of [self.data] or similar DataFrame
        CAUTION: This can be slow!
        '''

        if data is None:
            data = self.data

        st.seaborn.pairplot(data,hue=self.target)
      
    def partition(self,nSamples=None,fTraining=None):
        '''
        Partition [self.data] into [Training] and [Testing].
        If no input given, then return 2 copies of [self.data].
        INPUTS
            fData       optional bool aligned with [self.data]: use only these rows for training
            nSamples    optional int: randomly choose this many samples for training
        OUTPUTS
            [Training]  portion of [self.data] to use for training
            [Testing]   portion of [self.data] to use for testing
        NOTE
            If both [fData] and nSamples are input, then [Training] rows are chosen
            randomly from rows for which [fData]==True. All other rows are in [Testing].
        '''

        data = self.data

        if (nSamples is None) & (fTraining is None):
            print( "Using all %s rows for training and testing" % len(data) )
            return data.copy(), data.copy()

        if fTraining is None:
            fTraining = st.pd.Series(True,index=data.index)

        if nSamples is not None:
            training_rows   = st.np.random.choice(data.index[fTraining],size=nSamples,replace=False)
            fTraining       = data.index.isin(training_rows)

        Training    = data.loc[fTraining].copy()
        Testing     = data.loc[~fTraining].copy()

        return Training, Testing

    def train(self,data=None):
        '''
        Use data to train model. If no data input, then use all of self.Data.
        INPUTS
          data   optional chunk of [self.data] or similar DataFrame
        OUTPUTS
           *** Modifies self.Model
        '''

        Target, Cats, Predictors = self._unpack(data)
        print( "Training classifier with %s samples" % len(Target) )
        self.model.fit(Predictors,Target)

    def classify(self,predictors):
        '''
        Attempt to classify each row of new_predictors.
        INPUTS
          predictors    DataFrame: predictor columns
        OUTPUTS
          Result        DataFrame: predictions (and their probabilities, if available)
        '''

        model                       = self.model
        Target, Cats, OldPredictors = self._unpack()

        # Force new [predictors] to have same column order as [self.data]
        predictors = predictors.sort_index(axis=1)

        print( "Classifying %s samples" % len(predictors) )
        Result              = st.pd.DataFrame(index=predictors.index)
        Result[Target.name] = model.predict(predictors)

        return Result


    # Methods for testing

    def test(self,training,testing,verbose=True):
        '''
        Test classifier on data with known categories.
        INPUTS:
          training  data to use for training
          testing   data to use for testing
        OUTPUTS:
          Result        DataFrame of predicted and true classifications with probabilities
          *** Modifies self.Model
        '''

        model                               = self.model
        TestTarget, Cats, TestPredictors    = self._unpack(testing)

        # Fit model to training data
        self.train(training)

        # Attempt to classify each row of [TestPredictors]
        Result = self.classify(TestPredictors)

        # Compare prediction to known results
        Result = Result.rename(columns={TestTarget.name:'Model'})
        Result.insert(0,'Reality',TestTarget)
        Result['IsCorrect'] = Result['Model']==Result['Reality']

        return Result

    def null_test(self,training,testing):
        '''
        Test a very naive classifier on data with known categories.
        INPUTS:
          training  chunk of [Data] matrix to use for training
          testing   chunk of [Data] matrix to use for testing
        OUTPUTS:
          Result    DataFrame of predicted and true classifications with probabilities
        '''

        TestTarget, Cats, TestPredictors = self._unpack(testing)

        # Calculate how often each class appears in training_data
        Freqs = self.target_freq(training)

        # Classify test_data randomly based on [Freqs]
        Result              = st.pd.DataFrame(index=testing.index)
        Result['Reality']   = TestTarget
        Result['Model']     = st.np.random.choice(Cats,size=len(TestTarget),p=Freqs)
        Result['IsCorrect'] = Result['Model']==Result['Reality']

        return Result

    def confusion(self,result):
        '''
        Package "confusion matrix" as a human-readable DataFrame
        INPUTS:
          test_result   output of self.test() or self.null_test()
        OUTPUTS:
          Confusion     human-readable DataFrame
        '''

        if self.text_mode:
            raise NotImplementedError("confusion() method does not work in text mode yet")

        categories = sorted(result['Reality'].unique())

        Confusion           = metrics.confusion_matrix(result['Reality'],result['Model'])
        Confusion           = st.pd.DataFrame(Confusion)
        Confusion.columns   = categories
        Confusion.index     = [ 'Actually ' + str(cat) for cat in categories ]

        # Tell user how we did
        nCorrect    = Confusion.values.diagonal().sum()
        nSamples    = len(result)
        CorrectPct  = round( (100.0 * nCorrect) / nSamples, 2 )
        print( "%s of %s (%s%%) classifications were correct" % (nCorrect,nSamples,CorrectPct) )

        return Confusion


    # Methods for saving/loading

    def save(self,filename):
        ''' Save model as pickle file '''

        with open(filename,'wb') as f:
            pickle.dump(self,f)

    @staticmethod
    def load(filename):
        ''' Unpickle a previously-saved model '''

        with open(filename,'rb') as f:
            return pickle.load(f)



class LogisticClassifier(Classifier):
    '''
    Classify using scikit-learn LogisticRegressionCV or similar
    Predictor columns should be floating-point numbers.
    (Indicator variables restricted to [0,1] are OK.) 
    '''

    def __init__(self,*args,**kwargs):

        if 'model' not in kwargs.keys():
            kwargs['model'] = LogisticRegressionCV

        Classifier.__init__(self,*args,**kwargs)

    def classify(self,predictors):
        ''' Logistic classifiers predict category probabilities, not just categories '''

        model       = self.model
        categories  = self.categories

        Result  = Classifier.classify(self,predictors)

        # Estimate probabilities for each classification
        probs       = model.predict_proba(predictors)
        p_names     = [ 'p'+str(cat) for cat in categories ]
        for k in range(len(p_names)):
            col_name = p_names[k]
            Result[col_name] = probs[:,k]
            Result[col_name] = Result[col_name].round(3)

        return Result      
        
    def coefs(self):
        '''
        Show regression coefficients x100.
        NOTE: Run self.train() first, or these will be meaningless.
        '''

        Target, Cats, Predictors    = self._unpack()
        Coefs                       = self.model.coef_

        # Pacakge [Coefs] as a human-readable DataFrame
        if len(Cats) > 2:
            index = Cats
        else:
            index = ['True']
        Coefs = st.pd.DataFrame(Coefs,index=index,columns=Predictors.columns)

        # Multiply and round for easier reading
        Coefs = (100*Coefs).round()

        return Coefs
