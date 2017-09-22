import csv
from multiprocessing import Process
from os.path import dirname

import numpy as np
from pkg_resources import resource_filename
from sklearn.externals import joblib

from ..commands.command import Command
from ..support.data_handler import DataHandler


class Model(Process):
    STOP_CHARS = [".", ",", ";", ":", "@"]
    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self.model_data = DataHandler(data_file=kwargs["model_file"])
        self.model = None
        if self.model_data.has("model_file"):
            self.model = joblib.load(self.model_data.get("model_file"))
        self.trn_do = False
        self.tst_do = False
        self.prd_do = False
        self.data = None

    def run(self):
        if self.prd_do:
            pass
        elif self.tst_do:
            self.test_process()
            self.model_data.save()
        elif self.trn_do:
            self.train_process()
            self.model_data.save()
    
    def train(self, trn_data):
        """ Initialize a training process.
        """
        self.data = trn_data
        self.trn_do = True
        self.tst_do = False
        self.prd_do = False

    def test(self, tst_data):
        """ Initialize a testing process.
        """
        self.data = tst_data
        self.trn_do = False
        self.tst_do = True
        self.prd_do = False

    def format_data(self, data):
        for stop_char in self.STOP_CHARS:
            data = data.replace(stop_char, "")
        data = data.lower()
        data = data.split(" ")
        data = [word.strip() for word in data if len(word) > 0]
        return data

    def get_XY_columns(self, x_col, terms):
        y_col = np.zeros((len(x_col),), dtype=np.int)
        for i, data_string in enumerate(x_col):
            for term in terms:
                if term in data_string:
                    y_col[i] = 1
                    break
        x_col = self.string_encode_int(x_col)
        return np.column_stack([y_col, x_col])

    def string_encode_int(self, string_list):
        """ Encode the string list to an int list using a dictionary.
        """
        int_list = []
        word_dictionary = self.read_word_dictionary()
        keys = word_dictionary.keys()
        for string in string_list:
            if string in keys:
                int_list.append(word_dictionary[string])
            else:
                word_dictionary[string] = len(keys)
                int_list.append(len(keys))
                keys = word_dictionary.keys()
        self.write_word_dictionary(word_dictionary)
        return np.array(int_list, dtype=int)

    def read_word_dictionary(self):
        """ Read and return the dictionary file.
        """
        word_dictionary = {}
        with open(resource_filename("resources.data.app_data", "dictionary.csv")) as dict_file:
            reader = csv.reader(dict_file)
            for row in reader:
                word_dictionary[row[0]] = row[1]
        return word_dictionary

    def write_word_dictionary(self, word_dictionary):
        """ Write the dictionary file.
        """
        with open(resource_filename("resources.data.app_data", "dictionary.csv"), 'w') as dict_file:
            writer = csv.writer(dict_file)
            writer.writerows([[key, value] for key, value in word_dictionary.items()])
    
    def save_model(self, model):
        """ Save a model using joblib dump.
        """
        # Does the model allready have a model_file, if so this should be overwriten
        if self.model_data.has("model_file"):
            model_file_name = self.model_data.get("model_file")
        # ... it doesn't we create a new path and save it in the model data
        else:
            cmd = Command({"-v":False, "-l":False, "Command":""})
            model_file_name = cmd.get_next_file(dirname(self.model_data.data_file),
                                                "hmm_model", "pkl")
            self.model_data.set_text("model_file", model_file_name)
        # And write the file
        joblib.dump(model, model_file_name)
