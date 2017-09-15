from multiprocessing import Process
import numpy as np
import hashlib

class Model(Process):
    STOP_CHARS = [".", ",", ";", ":", "@"]
    def __init__(self):
        super(Model, self).__init__()
        self.trn_do = False
        self.tst_do = False
        self.prd_do = False
        self.trn_data = None
        self.tst_data = None
        self.prd_data = None

    def run(self):
        if self.prd_do:
            pass
        elif self.tst_do:
            pass
        elif self.trn_do:
            self.train_process()
    
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
        return np.column_stack([x_col, y_col])

    def string_encode_int(self, string_list):
        int_list = []
        m = hashlib.md5()
        for string in string_list:
            m.update(string)
            
        return np.array(int_list, dtype=int)