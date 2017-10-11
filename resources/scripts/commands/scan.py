import urllib.parse
import xml.etree.ElementTree as ET
from multiprocessing import Process
from os.path import abspath, basename, dirname, isdir, isfile, join
from urllib.request import urlopen

import requests
import webstruct
from ..support.articleDateExtractor import *
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
from pkg_resources import resource_filename
from webstruct.feature_extraction import HtmlFeatureExtractor

from ..support.data_handler import DataHandler
from .command import Command


class Scan(Command):
    def __init__(self, args):
        """ Constructor of the Scan object. Initialize the parent Command object, check and
            catch errors and initialize variables.
        """
        # Call the Command constructor
        args["Command"] = "Scan"
        super(Scan, self).__init__(args)
        # Check for potential errors
        if args["--in"] and isfile(args["--in"]):
            # Use settings file as pointed to by the user
            self.scan_settings = DataHandler(data_file=args["--in"])
        elif args["--in"]:
            # User settings file not found.
            self.error("File not found: {}".format(args["--in"]), fatal=True)
        else:
            # Use default settings file
            self.scan_settings = DataHandler(data_file=\
                                             join(resource_filename("resources.data", "app_data"),
                                                  "default_scan_settings.xml"))
        self.log("Initialized")

    def run(self):
        self.log("Running")
        scan_processes = []
        for site in self.scan_settings.get_all("site"):
            process = ScanProcess(self, site, self.scan_settings)
            process.start()
            scan_processes.append(process)
            #break
        self.wait_for_processes(scan_processes, name="scanning")
        self.log("Terminating")

class ScanProcess(Process):
    def __init__(self, parent, site, scan_settings):
        super(ScanProcess, self).__init__()
        self.parent = parent
        self.site = site
        self.settings = scan_settings

    def run(self):
        """ Start the scanning process
        """
        self.parent.log("Scanning {}".format(self.site.attrib["name"]))
        companies = [company.attrib["name"].lower() for company in self.settings.get_all("company")]
        with urlopen(self.site.find('url').text) as response:
            for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
                if link.has_attr('href'):
                    for company in companies:
                        if company in link["href"]:
                            self.analyse_article(link['href'], company)

    def analyse_article(self, url, company):
        """ Look closer at the article and append it to the database.
        """
        # Merge relative urls to absolute
        url = urllib.parse.urljoin(self.site.find('url').text, url)
        # Check if this article has been seen before
        if any(url == saved_url.text for saved_url in self.settings.root.\
               findall(".//*[@name='{}']*/url".format(company))):
            return
        # Create a new "sighting" post
        company_element = self.settings.root.find(".//*[@name='{}']".format(company))
        sighting_element = ET.SubElement(company_element, "sighting")

        datetime_obj = extractArticlePublishedDate(url)
        date = "{}-{}-{}".format(datetime_obj.year, datetime_obj.month, datetime_obj.day)
        time = "{:02d}:{:02d}:{:02d}".format(datetime_obj.hour, datetime_obj.minute,
                                             datetime_obj.second)

        date_element = ET.SubElement(sighting_element, "date")
        date_element.text = date
        time_element = ET.SubElement(sighting_element, "time")
        time_element.text = time
        site_element = ET.SubElement(sighting_element, "site")
        site_element.text = self.site.attrib["name"]
        url_element = ET.SubElement(sighting_element, "url")
        url_element.text = url
        self.settings.save()
