from multiprocessing import Process

class Model(Process):
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