from urllib.request import urlopen
from multiprocessing import Process
from os.path import isfile, join, dirname, abspath, basename, isdir
import os
from bs4 import BeautifulSoup
from bs4.element import Comment

import requests

from .command import Command
from ..support.data_handler import DataHandler


class Download(Command):
    """ The downloading class is used to download web pages and saving them to files.
    """
    def __init__(self, args):
        """ Constructor of the Download object. Initialize the parent Command object, check and
            catch errors and initialize variables.
        """
        # Call the Command constructor 
        args["Command"] = "Download"
        super(Download, self).__init__(args)
        # Check for potential errors
        if isfile(args["--in"]):
            self.urls = self.read_file(args["--in"])
        else:
            self.error("File not found: {}".format(args["--in"]), fatal=True)
        if isfile(args["--out"]):
            os.remove(args["--out"])
        self.dir_name = join(dirname(abspath(args["--out"])), "downloads")
        if not isdir(self.dir_name):
            os.mkdir(self.dir_name)
        self.data_handler = DataHandler(parent=self, data_file=args["--out"])
        self.log("Download is initialized")

    def run(self):
        self.log("Download is running")
        head = self.urls.pop(0)
        download_processes = []
        for url in self.urls:
            file_name = join(self.dir_name, "download_{}.txt".format(len(download_processes)))
            data_dict = {key: value for key, value in zip(head, url)}
            data_dict["file_name"] = file_name
            self.data_handler.add_document(tag="download", name=basename(file_name), args=data_dict)
            process = DownloadProcess(self, url[head.index("url")], file_name)
            process.start()
            download_processes.append(process)
        self.wait_for_processes(download_processes, name="download")
        self.data_handler.save()
        

class DownloadProcess(Process):
    def __init__(self, parent, url, file_name):
        super(DownloadProcess, self).__init__()
        self.parent = parent
        self.url = url
        self.file_name = file_name

    def run(self):
        """ Start the downloading process
        """
        self.parent.log("Downloading {} to file {}".format(self.url, self.file_name))
        with urlopen(self.url) as url:
            soup = BeautifulSoup(url.read(), "html.parser")
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        text = " ".join(t.strip() for t in visible_texts)
        self.parent.write_file(self.file_name, text)

    def tag_visible(self, element):
        """ Filter visable dom elements
        """
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
"""
<company name="Volvo">
        <sighting>
            <date>2017-10-01</date>
            <time>00:00:00</time>
            <site>DN ekonomi</site>
            <url>https://www.dn.se/ekonomi/</url>
        </sighting>
    </company>
"""