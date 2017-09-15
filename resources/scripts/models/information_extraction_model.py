from .model_set import ModelSet
from .hidden_markov_model import HiddenMarkovModel

class InformationExtractionModel(ModelSet):
    def __init__(self, args):
        super(InformationExtractionModel, self).__init__(args)
        self.model_set = [HiddenMarkovModel(), HiddenMarkovModel()]
    
    