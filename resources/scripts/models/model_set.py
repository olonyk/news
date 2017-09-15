from ..commands import Command

class ModelSet(Command):
    def __init__(self, args):
        super(ModelSet, self).__init__(args)

    def train(self, **kwargs):
        trn_data = kwargs["trn_data"]
        for sub_model in self.model_set:
            sub_model.train(trn_data)
            sub_model.start()
        self.wait_for_processes(self.model_set, name="Training")