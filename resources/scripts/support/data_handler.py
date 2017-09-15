import xml.etree.ElementTree as ET
from os.path import isfile
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
        content = """<?xml version="1.0"?>
        <data>
        </data>"""
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
