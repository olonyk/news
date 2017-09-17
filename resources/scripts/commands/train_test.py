from os.path import isfile

from .command import Command
from ..support.data_handler import DataHandler
from ..models.information_extraction_model import InformationExtractionModel as IEM

class TrainTest(Command):
    """ The TrainTest command trains an information extraction model and tests it.
    """
    def __init__(self, args):
        """ Constructor of the TrainTest object. Initialize the parent Command object, check and
            catch errors and initialize variables.
        """
        # Call the Command constructor 
        args["Command"] = "TrainTest"
        super(TrainTest, self).__init__(args)
        # Check for potential errors
        if isfile(args["--in"]):
            self.data_handler = DataHandler(parent=self, data_file=args["--in"])
        else:
            self.error("File not found: {}".format(args["--in"]), fatal=True)
        self.nr_runs = 1
        if args["--nr_runs"]:
            self.nr_runs = args["--nr_runs"]
        self.log("TrainTest is initialized")
    
    def run(self):
        for i in range(self.nr_runs):
            (trn_data, tst_data) = self.data_handler.divide_random(quota=0.5)
            model = IEM({"-v":self.verbose, "-l":self.logging, "Command":"IEM"})
            model.train(trn_data=trn_data)
            result = model.test(tst_data=tst_data)