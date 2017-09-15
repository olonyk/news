#!/usr/bin/env python3.5
""" ##  ##        ######           ##     ##             #####
    ### ##        ##               ##     ##            ##
    ######        ####             ##  #  ##             #####
    ## ###        ##                #######                  ##
    ##  ## EURAL  ###### STIMATOR    #   # EB CRAWLING   ##### URVEILLANCE

    Usage:
        news Train [-vl] --type=MODEL_TYPE [--file=DATA_FILE] [--out=OUTPUT_FILE]
        news Download [-vl] --in=URL_FILE --out=OUTPUT_FILE
        news TrainTest [-vl] --in=DOWNLOAD_FILE [--nr_runs=NR_RUNS]
    
    Example:
        python3.5 news.py Download -v --in=resources/data/tmp_data/dl.csv --out=data
"""
from docopt import docopt

from resources.scripts.commands.download import Download
from resources.scripts.commands.train_test import TrainTest

if __name__ == "__main__":
    args = docopt(__doc__)
    COMMAND = None
    if args["Download"]:
        COMMAND = Download(args)
    if args["TrainTest"]:
        COMMAND = TrainTest(args)
    if COMMAND:
        COMMAND.run()