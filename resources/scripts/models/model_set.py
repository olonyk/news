from ..commands import Command
from ..support.data_handler import DataHandler
from pkg_resources import resource_filename
from os.path import join, dirname
from . import *
import sys
import inspect

class ModelSet(Command):
    def __init__(self, args):
        super(ModelSet, self).__init__(args)
        if "model_file" in args.keys():
            # Load a saved model
            model_file = DataHandler(data_file=args["model_file"])
        else:
            # Create a new model set
            model_file = join(resource_filename("resources.data.app_data", "app_data"), "model_set.xml")
            self.model_data = DataHandler(data_file=model_file)
            for model_alg in self.model_algorithms:
                sub_model_file = join(dirname(model_file), "model.xml")
                self.model_data.add_document(tag="sub_model", args={"file_name":sub_model_file,
                                                                    "model_class":str(model_alg)})
        self.reset()

    def reset(self):
        sub_models = self.model_data.get_submodels()
        self.model_set = []
        for (sub_model_file, sub_model_class) in sub_models:
            for class_name, class_obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
                if str(class_obj) == str(sub_model_class):
                    self.model_set.append(class_obj(model_file=sub_model_file))
                    break

    def train(self, **kwargs):
        trn_data = kwargs["trn_data"]
        for sub_model in self.model_set:
            sub_model.train(trn_data)
            sub_model.start()
        self.wait_for_processes(self.model_set, name="Training")
        self.reset()
    
    def test(self, **kwargs):
        tst_data = kwargs["tst_data"]
        for sub_model in self.model_set:
            sub_model.test(tst_data)
            sub_model.start()
        self.wait_for_processes(self.model_set, name="Testing")
        self.reset()