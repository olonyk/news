from multiprocessing import Manager

from .hidden_markov_model import HiddenMarkovModel
from .model_set import ModelSet


class InformationExtractionModel(ModelSet):
    def __init__(self, args):
        self.model_algorithms = [HiddenMarkovModel]
        self.model_class = "InformationExtractionModel"
        super(InformationExtractionModel, self).__init__(args)

        #self.model_list = Manager().list([None] * len(self.model_algorithms))
        #self.model_set = [model_alg(model_list=self.model_list, model_index=i) for i, model_alg in\
        #                  enumerate(self.model_algorithms)]

    #def reset(self):
    #    self.model_set = [model_alg(model_list=self.model_list, model_index=i) for i, model_alg in\
    #                      enumerate(self.model_algorithms)]
