from .model import Model
import time

class HiddenMarkovModel(Model):
    def __init__(self):
        super(HiddenMarkovModel, self).__init__()

    def train(self, trn_data):
        self.trn_data = trn_data
        self.trn_do = True
        self.tst_do = False
        self.prd_do = False
    
    def train_process(self):
        time.sleep(5)