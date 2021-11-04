"""
File defining Datatype property classes.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET
from .entity import Entity


class DataProperty(Entity):
    """Class which represents a datatype property. Derives from the Entity virtual class. """

    def __init__(self, name: str, domains: str, ranges: str):
        """Basic contructor for data properties.

        Args:
            name (str): The name of the property
            domains (str): The classes which can hold this property
            ranges (str): The type of possible values of the property
        """
        super().__init__(name)
        self.tag = 'owl:DatatypeProperty'
        self.subproperty_of = None
        self.domains = domains
        if ranges in ["integer", "decimal", "boolean", "string"]:
            self.ranges = 'http://www.w3.org/2001/XMLSchema#'+ranges
        else:
            ValueError(
                "ranges must be one of 'integer', 'decimal', 'boolean', 'string'")

    def as_subproperty_of(self, name: str):
        """State that it is a subproperty of a property called name. Its existence is not checked.

        Args:
            name (str): The name of the superproperty.
        """
        self.subproperty_of = name

    def to_xml(self, subelement: ET.Element, ontology_name: str) -> ET.Element:
        """Converts the class to an xml element.

        Args:
            subelement (ET.Element): The subelement in which to convert the class.
            ontology_name (str): The name of the Ontology.

        Returns:
            ET.SubElement: The modified subelement.
        """
        subelement.set('rdf:about', ontology_name+"#"+self.name)
        if self.subproperty_of is not None:
            subproperty_xml = ET.SubElement(subelement, 'rdfs:subPropertyOf')
            subproperty_xml.set('rdf:resource', ontology_name +
                                "#"+self.subproperty_of)
        else:
            subproperty_xml = ET.SubElement(subelement, 'rdfs:subPropertyOf')
            subproperty_xml.set(
                'rdf:resource', "http://www.w3.org/2002/07/owl#topDataProperty")

        domain_xml = ET.SubElement(subelement, 'rdfs:domain')
        domain_xml.set('rdf:resource', ontology_name +
                       "#"+self.domains)
        range_xml = ET.SubElement(subelement, 'rdfs:range')
        range_xml.set('rdf:resource', self.ranges)
        return subelement
