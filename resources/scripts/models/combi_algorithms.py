
class CombiAlgorithm(object):
    def __init__(self, **kwargs):
        self.model_data = DataHandler(data_file=kwargs["model_file"])

class HardVoting(CombiAlgorithm):
    def __init__(self, **kwargs):
        super(HardVoting, self).__init__(**kwargs)
