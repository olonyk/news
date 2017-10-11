import sys
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from multiprocessing import Process
from os.path import abspath, basename, dirname, isdir, isfile, join
from urllib.request import urlopen

import requests
import webstruct
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
from pkg_resources import resource_filename
from webstruct.feature_extraction import HtmlFeatureExtractor

from ..support.articleDateExtractor import *
from ..support.data_handler import DataHandler
from .command import Command

try:
    from matplotlib.finance import quotes_historical_yahoo_ochl
except ImportError:
    # For Matplotlib prior to 1.5.
    from matplotlib.finance import quotes_historical_yahoo as quotes_historical_yahoo_ochl

class ModifyScan(Command):
    def __init__(self, args):
        """ Constructor of the Scan object. Initialize the parent Command object, check and
            catch errors and initialize variables.
        """
        # Call the Command constructor
        args["Command"] = "Scan"
        super(ModifyScan, self).__init__(args)
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
        functions = [self.quit, self.print_sites, self.print_companies, self.add_site, self.add_company, self.plot_all]
        while True:
            print("Choose action")
            for i, function in enumerate(functions):
                print("{:_<18}{}".format(i, function.__doc__))
            response = input(">")
            try:
                functions[int(response)]()
            except ValueError:
                pass
        self.log("Terminating")
    
    def quit(self):
        """Quit"""
        sys.exit()

    def print_sites(self):
        """Print sites in settings"""
        self.scan_settings.print_sites()

    def print_companies(self):
        """Print sites in settings"""
        self.scan_settings.print_companies()
    
    def add_site(self):
        """Add site"""
        site_name = input("site name: ")
        site_url = input("site url: ")
        print("Confirm that {} with url {} will be added to data".format(site_name, site_url))
        confirm = input("[Y/n]: ")
        if not confirm.lower() == "y":
            return
        new_site = ET.SubElement(self.scan_settings.root, "site", {"name":site_name})
        ET.SubElement(new_site, "url").text = site_url
        self.scan_settings.save()
    
    def add_company(self):
        """Add company"""
        company_name = input("company name: ")
        tickers = []
        while True:
            ticker = input("ticker symbol (optional): ")
            if ticker == "" or len(tickers) > 4:
                break
            else:
                tickers.append(ticker)
        print("Confirm that {} will be added to data".format(company_name))
        confirm = input("[Y/n]: ")
        if not confirm.lower() == "y":
            return
        new_company = ET.SubElement(self.scan_settings.root, "company", {"name":company_name})
        for ticker in tickers:
            ET.SubElement(new_company, "ticker").text = ticker
        self.scan_settings.save()
    
    def plot_all(self):
        """Plot all companies"""
        comp_data = self.scan_settings.get_company_data()
        for comp in comp_data:
            quotes = quotes_historical_yahoo_ochl("INTC", datetime.strptime(comp["first"], '%Y-%m-%d'), datetime.strptime(comp["last"], '%Y-%m-%d'))
            print(quotes)
