from .model import Model
import time
from hmmlearn.hmm import GaussianHMM
import numpy as np

class HiddenMarkovModel(Model):
    def __init__(self):
        super(HiddenMarkovModel, self).__init__()

    def train(self, trn_data):
        self.trn_data = trn_data
        self.trn_do = True
        self.tst_do = False
        self.prd_do = False
    
    def train_process(self):
        # Read and parse the training data
        data = self.trn_data.get_file_data()
        data = self.format_data(data)
        terms = self.trn_data.get_terms()
        data = self.get_XY_columns(data, terms)
        model = GaussianHMM(n_components=4, covariance_type="diag", n_iter=1000).fit(data)

        print(terms)
        print(data)
