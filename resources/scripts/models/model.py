from multiprocessing import Process
from pkg_resources import resource_filename
from ..support.data_handler import DataHandler

import numpy as np
import csv


class Model(Process):
    STOP_CHARS = [".", ",", ";", ":", "@"]
    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self.model_data = DataHandler(data_file=kwargs["model_file"])
        if self.model_data.has(""):
            self.model
        self.trn_do = False
        self.tst_do = False
        self.prd_do = False
        self.data = None

    def run(self):
        if self.prd_do:
            pass
        elif self.tst_do:
            self.test_process()
        elif self.trn_do:
            self.train_process()
    
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
