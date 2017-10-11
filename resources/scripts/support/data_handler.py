import xml.etree.ElementTree as ET
from os.path import isfile
from collections import Counter
import random

class DataHandler(object):
    """ The data handler class handles data and in xml format.
    """
    def __init__(self, **kwargs):
        """ The data handler class is initialized with one conditional argument, data_file. If the
            file in the data_file path exists then this file is read into the ET tree, if the file
            does not exist then a new empty xml document is initialized.
        """
        self.data_file = kwargs["data_file"]
        self.parent = None
        if "parent" in kwargs.keys():
            self.parent = kwargs["parent"]
        if isfile(self.data_file):
            tree = ET.parse(kwargs["data_file"])
            self.root = tree.getroot()
        else:
            self.root = self.initialize()

    def initialize(self):
        """ Define and initialize an empty xml document and return the root node.
        """
        content = """<?xml version="1.0"?><data></data>"""
        return ET.fromstring(content)

    def add_document(self, tag="post", name="1", args={}):
        """ Add a new post in the xml data base.
        """
        element = ET.SubElement(self.root, tag, attrib={"name":name})
        for key, value in args.items():
            sub_element = ET.SubElement(element, key)
            sub_element.text = str(value)

    def add_element(self, element):
        """ Add an element at the root.
        """
        self.root.append(element)

    def save(self):
        """ Save the current tree.
        """
        ET.ElementTree(self.root).write(self.data_file)
    
    def divide_random(self, quota=0.5):
        """ Divides the data tree into two parts where the first part has quota part of the posts.
            The return value is a tuple of two new data handlers. These data handlers can not be
            saved as they have no file value.
        """
        elements = list(self.root)
        cut_index = int(len(elements)*quota)
        random.shuffle(elements)
        elements_1 = elements[:cut_index]
        elements_2 = elements[cut_index:]
        tree_1 = DataHandler(data_file="")
        tree_2 = DataHandler(data_file="")
        [tree_1.add_element(element) for element in elements_1]
        [tree_2.add_element(element) for element in elements_2]
        return (tree_1, tree_2)

    def print_tree(self, element=None, indent=0):
        if not element:
            element = self.root
        print_str = " ".join("{}: {}".format(key, value) for key, value in element.attrib.items())
        print_str = "tag: {} {}".format(element.tag, print_str)
        print("{}{}".format("\t"*indent, print_str))
        for elem in element:
            if elem:
                self.print_tree(element=elem, indent=indent+1)

    def get_file_data(self):
        """ Search for all nodes called file_name and use their text to read files
        """
        text_data = ""
        for file_name in self.root.findall(".//file_name"):
            text_data += self.read_file(file_name.text)
        return text_data

    def get_submodels(self):
        """ Return a list of all files noted in the data
        """
        files = [file_name.text for file_name in self.root.findall(".//file_name")]
        classes = [model_class.text for model_class in self.root.findall(".//model_class")]
        return [(model_file, model_class) for model_file, model_class in zip(files, classes)]

    def get_terms(self):
        """ Return the terms associated with each data. This function will be updated in the future.
        """
        terms = []
        for term in self.root.findall(".//ftg"):
            terms.append(term.text)
        return list(set(terms))

    def read_file(self, file_name):
        """ Read and return the file_name
        """
        ret = []
        with open(file_name) as data_file:
            ret = " ".join([row for row in data_file.readlines()])
        return ret

    def has(self, name):
        """ Test if name is in the data
        """
        return len(self.root.findall(name)) > 0

    def get(self, name):
        """ Find and return the value of name.
        """
        return self.root.find(name).text

    def set_text(self, name, text):
        """ Set the text of name.
        """
        element = self.root.find(name)
        if element:
            element.text = str(text)
        else:
            element=ET.Element(name)
            element.text=text
            self.root.append(element)
    
    def get_all(self, name):
        """ Find and return the value of name.
        """
        return self.root.findall(name)

    def print_sites(self):
        """ mscan specific!
        Print all the sites in the data
        """
        site_elements = self.root.findall(".site")
        if len(site_elements) < 1:
            print("No sites in data")
            return
        print("{:<18}URL".format("Name"))
        for site_element in site_elements:
            print("{:<18}{}".format(site_element.attrib["name"], site_element.find("url").text))
        print()
    
    def print_companies(self):
        """ mscan specific!
        Print all the companies in the data
        """
        comp_elements = self.root.findall(".company")
        if len(comp_elements) < 1:
            print("No sites in data")
            return
        print("{:<18}#sightings".format("Name"))
        for comp_element in comp_elements:
            print("{:<18}{}".format(comp_element.attrib["name"], len(comp_element.getchildren())))
        print()
    
    def get_company_data(self):
        """ mscan specific!
        Return company data
        """
        comp_elements = self.root.findall(".company")
        comp_data = []
        for comp_element in comp_elements:
            dates = sorted([date.text for date in comp_element.findall("*//date")])
            last = dates[0]
            first = dates[-1]
            dates = Counter(dates)
            tickers = [ticker.text for ticker in comp_element.findall("*//ticker")]
            comp_data.append({"name":comp_element.attrib["name"], "dates":dates, "first":first,
                              "last":last, "tickers":tickers})
        return comp_data