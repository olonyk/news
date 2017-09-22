import time
import warnings

from hmmlearn.hmm import GaussianHMM

import numpy as np
from .model import Model


class HiddenMarkovModel(Model):
    def __init__(self, **kwargs):
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
        # Calculate which component is associated with the target
        results = model.predict(data)
        best_acc = 0
        for i in range(model.n_components):
            acc = np.sum(np.logical_and(results == i, data[:,0] == 1)) / np.sum(data[:,0])
            if acc > best_acc:
                best_acc = acc
                best_com = i
        warnings.simplefilter("always")
        self.save_model(model)
        self.model_data.set_text("target_comp", best_com)


    def test_process(self):
        data = self.data.get_file_data()
        data = self.format_data(data)
        terms = self.data.get_terms()
        data = self.get_XY_columns(data, terms)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        results = self.model.predict(data)
        warnings.simplefilter("always")
        
        target_comp = int(self.model_data.get("target_comp"))
        for i in range(self.model.n_components):
            if target_comp == i:
                acc = np.sum(np.logical_and(results == i, data[:,0] == 1)) / np.sum(data[:,0])
                print("Target component: {}".format(acc))
            else:
                acc = np.sum(np.logical_and(results == i, data[:,0] != 1)) / np.sum(np.logical_not(data[:,0]))
                print("Background component: {}".format(acc))