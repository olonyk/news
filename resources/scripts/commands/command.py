import csv
import sys
from datetime import datetime
from os.path import isfile, join
import shutil


class Command(object):
    """ The Command object holds commonly used methods inherited by all other commands such as
        Download and Train. The Command object holds functionalities such as logging, printouts and
        file handling.
    """
    def __init__(self, args):
        self.verbose = args["-v"]
        self.logging = args["-l"]
        self.command = args["Command"]

    def log(self, msg):
        """ Handles the logging and printouts.
        """
        if self.verbose or self.log:
            msg = "{}   {}   {}".format(str(datetime.now()), self.command, msg)
        if self.verbose:
            cols = shutil.get_terminal_size().columns
            if len(msg) > cols:
                print(msg[:cols])
            else:
                print(msg)
        if self.logging:
            print("logging not implemented yet")

    def error(self, msg, fatal=False):
        """ Handles error messages, exits the system is fatal is True.
        """
        msg = "{}\t{}\tERROR\t{}".format(str(datetime.now()), self.command, msg)
        print(msg)
        if self.logging:
            print("logging not implemented yet")
        if fatal:
            sys.exit(1)

    def read_file(self, file_name):
        """ Handles reading of files.
        """
        ret = []
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            ret = [row for row in reader]
        return ret

    def write_file(self, file_name, content):
        """ Write content to file.
        """
        with open(file_name, "w") as out:
            out.write(content)

    def wait_for_processes(self, processes, name="Unknown"):
        """ Handles the waiting for a list of processes.
        """
        while len(processes) > 0:
            self.log("Waiting for {} processes, {} left".format(name, len(processes)))
            process = processes[0]
            process.join()
            processes = [proc for proc in processes if proc.is_alive()]
        self.log("Waiting for {} processes, done".format(name))

    def get_next_file(self, directory, name, suffix):
        """ Returns the next avaiable file name in directory.
        """
        tmp_name = join(directory, "{}.{}".format(name, suffix))
        counter = 1
        while True:
            if isfile(tmp_name):
                tmp_name = join(directory, "{}_{}.{}".format(name, counter, suffix))
                counter += 1
            else:
                return tmp_name
