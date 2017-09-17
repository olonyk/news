import time
import warnings

from hmmlearn.hmm import GaussianHMM

import numpy as np

from .model import Model


class HiddenMarkovModel(Model):
    def __init__(self, **kwargs):
        print(kwargs)
        super(HiddenMarkovModel, self).__init__(**kwargs)
    
    def train_process(self):
        # Read and parse the training data
        data = self.data.get_file_data()
        data = self.format_data(data)
        terms = self.data.get_terms()
        data = self.get_XY_columns(data, terms)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        model = GaussianHMM(n_components=2, covariance_type="diag", n_iter=1000).fit(data)
        warnings.simplefilter("always")
        self.model_list[self.model_index] = model
    
    def test_process(self):
        data = self.data.get_file_data()
        data = self.format_data(data)
        terms = self.data.get_terms()
        data = self.get_XY_columns(data, terms)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        results = self.model_list[self.model_index].predict(data)
        warnings.simplefilter("always")
        
        #np.set_printoptions(threshold=np.nan)
        #data = np.column_stack([data, results])
        print("Means and vars of each hidden state")
        for i in range(self.model_list[self.model_index].n_components):
            print("{0}th hidden state".format(i))
            corr = np.sum(np.logical_and(results == i, data[:,0] == 1))
            tott = np.sum(data[:,0])
            print("accuracy = {:.04}".format(corr/tott))
            print()