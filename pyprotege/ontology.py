"""
File defining the main Ontology class.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET
from .object_property import ObjectProperty
from .data_property import DataProperty
from .ontology_class import OntologyClass
from .individual import Individual


class Ontology:
    """ The main Ontology class. """

    def __init__(self, name: str):
        """Basic constructor for the main Ontology class.

        Args:
            name (str): The name of the ontology.
        """
        self.name = name
        self.url = "http://www.semanticweb.org/"
        self.classes = []
        self.object_properties = []
        self.data_properties = []
        self.individuals = []

    def add_object_property(self, object_property: ObjectProperty):
        """Add an object property to the Ontology.

        Args:
            object_property (str): The object property to be added to the ontology.
        """
        self.object_properties.append(object_property)

    def add_data_property(self, data_property: DataProperty):
        """Add a datatype property to the Ontology.

        Args:
            data_property (str): The data property to be added to the ontology.
        """
        self.data_properties.append(data_property)

    def add_class(self, ontology_class: OntologyClass):
        """Add an object class to the Ontology.

        Args:
            ontology_class (OntologyClass): The class to be added to the ontology.
        """
        self.classes.append(ontology_class)

    def add_individual(self, individual: Individual):
        """Add an individual to the Ontology.

        Args:
            individual (Individual): The individual to be added to the ontology.
        """
        self.individuals.append(individual)

    def start_xml(self) -> ET.Element:
        """Generate the beginning of the XML Element.

        Returns:
            ET.Element: The beginning of the XML Element.
        """
        xml_document = ET.Element("rdf:RDF")
        xml_document.set('xmlns', self.url+self.name+"#")
        xml_document.set('xml:base', self.url+self.name)
        xml_document.set('xmlns:owl', "http://www.w3.org/2002/07/owl#")
        xml_document.set(
            'xmlns:rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        xml_document.set('xmlns:xml', "http://www.w3.org/XML/1998/namespace")
        xml_document.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema#")
        xml_document.set('xmlns:rdfs', "http://www.w3.org/2000/01/rdf-schema#")
        xml_document.set('xmlns:'+self.name, self.url+self.name+"#")

        ontology = ET.SubElement(xml_document, 'owl:Ontology')
        ontology.set('rdf:about', self.name)
        return xml_document

    def to_xml(self) -> str:
        """Converts the ontology to an XML string.

        Returns:
            str: the ontology as a XML string.
        """
        xml_document_string = """<?xml version="1.0"?>"""
        xml_document = self.start_xml()

        for ontology_class in self.classes:
            subelement = ET.SubElement(xml_document, ontology_class.tag)
            ontology_class.to_xml(subelement, self.url+self.name)

        for object_property in self.object_properties:
            subelement = ET.SubElement(xml_document, object_property.tag)
            object_property.to_xml(subelement, self.url+self.name)

        for data_property in self.data_properties:
            subelement = ET.SubElement(xml_document, data_property.tag)
            data_property.to_xml(subelement, self.url+self.name)

        for individual in self.individuals:
            subelement = ET.SubElement(xml_document, individual.tag)
            individual.to_xml(subelement, self.url+self.name)

        xml_document_string += ET.tostring(xml_document).decode("utf-8")
        return xml_document_string

    def write_xml(self, name: str):
        """Write the ontology on the disk as an XML document.

        Args:
            name (str): The name of the file.
        """
        with open(name, 'w') as file:
            file.write(self.to_xml())
