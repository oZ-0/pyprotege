import xml.etree.ElementTree as ET


class Ontology:
    def __init__(self, name: str):
        self.name = name
        self.classes = []
        self.object_properties = []
        self.data_properties = []
        self.individuals = []

    def add_object_property(self, name: str):
        self.object_properties.append(name)

    def add_data_property(self, name: str):
        self.data_properties.append(name)

    def add_class(self, ontology_class):
        self.classes.append(ontology_class)

    def add_individual(self, individual):
        -1

    def start_xml(self):
        xml_document = ET.Element("rdf:RDF")
        xml_document.set('xmlns', self.name+"#")
        xml_document.set('xml:base', self.name)
        xml_document.set('xmlns:owl', "http://www.w3.org/2002/07/owl#")
        xml_document.set(
            'xmlns:rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        xml_document.set('xmlns:xml', "http://www.w3.org/XML/1998/namespace")
        xml_document.set('xmlns:xsd', "http://www.w3.org/2001/XMLSchema#")
        xml_document.set('xmlns:rdfs', "http://www.w3.org/2000/01/rdf-schema#")
        xml_document.set('xmlns:'+self.name, self.name+"#")

        ontology = ET.SubElement(xml_document, 'owl:Ontology')
        ontology.set('rdf:about', self.name)
        return xml_document

    def to_xml(self):
        xml_document_string = """<?xml version="1.0"?>"""
        xml_document = self.start_xml()

        for ontology_class in self.classes:
            subelement = ET.SubElement(xml_document, ontology_class.tag)
            ontology_class.to_xml(subelement, self.name)

        for object_property in self.object_properties:
            subelement = ET.SubElement(xml_document, object_property.tag)
            object_property.to_xml(subelement, self.name)

        for data_property in self.data_properties:
            subelement = ET.SubElement(xml_document, data_property.tag)
            data_property.to_xml(subelement, self.name)

        for individual in self.individuals:
            subelement = ET.SubElement(xml_document, individual.tag)
            individual.to_xml(subelement, self.name)

        xml_document_string += ET.tostring(xml_document).decode("utf-8")
        return xml_document_string

    def write_xml(self, name):
        with open(name, 'w') as file:
            file.write(self.to_xml())
