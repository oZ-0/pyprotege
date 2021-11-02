"""
File defining Object property classes.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET
from .entity import Entity


class ObjectProperty(Entity):
    """Class which represents an object property. Derives from the Entity virtual class. """

    def __init__(self, name: str, domains: str, ranges: str):
        """Basic contructor for object properties.

        Args:
            name (str): The name of the property
            domains (str): The classes which can hold this property
            ranges (str): The types of possible values of the property
        """
        super().__init__(name)
        self.tag = 'owl:ObjectProperty'
        self.subproperty_of = None
        self.inverse_of = None
        self.domains = domains
        self.ranges = ranges
        self.symmetric = False

    def set_symmetric(self, val: bool = True):
        """State that this property is symmetric.

        Args:
            name (str): The name of the superproperty.
        """
        self.symmetric = val

    def as_subproperty_of(self, name: str):
        """State that it is a subproperty of a property called name. Its existence is not checked.

        Args:
            name (str): The name of the superproperty.
        """
        self.subproperty_of = name

    def as_inverse_of(self, name: str):
        """State that this 

        Args:
            name (str): The name of the superproperty.
        """
        self.inverse_of = name

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
                'rdf:resource', "http://www.w3.org/2002/07/owl#topObjectProperty")
        if self.inverse_of is not None:
            inverse_of_xml = ET.SubElement(subelement, 'rdfs:inverseOf')
            inverse_of_xml.set('rdf:resource', ontology_name +
                               "#"+self.inverse_of)
        if self.symmetric:
            type_xml = ET.SubElement(subelement, 'rdf:type')
            type_xml.set('rdf:resource',
                         "http://www.w3.org/2002/07/owl#SymmetricProperty")
        domain_xml = ET.SubElement(subelement, 'rdfs:domain')
        domain_xml.set('rdf:resource', ontology_name +
                       "#"+self.domains)
        range_of_xml = ET.SubElement(subelement, 'rdfs:range')
        range_of_xml.set('rdf:resource', ontology_name +
                         "#"+self.ranges)
        return subelement
