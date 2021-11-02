"""
File defining Classes of objects.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET
from .entity import Entity


class OntologyClass(Entity):
    """ Class which represents an ontology class. Derives from the Entity virtual class. """

    def __init__(self, name: str):
        """Basic contructor for classes.

        Args:
            name (str): The name of the property
        """
        super().__init__(name)
        self.subclass_of = None
        self.tag = "owl:Class"
        self.disjoint_with = []

    def as_subclass_of(self, name: str):
        """State that it is a subclass of a classs called name. Its existence is not checked.

        Args:
            name (str): The name of the superclass.
        """
        self.subclass_of = name

    def to_xml(self, subelement: ET.Element, ontology_name: str):
        """Converts the class to an xml element.

        Args:
            subelement (ET.Element): The subelement in which to convert the class.
            ontology_name (str): The name of the Ontology.

        Returns:
            ET.SubElement: The modified subelement.
        """
        subelement.set('rdf:about', ontology_name+"#"+self.name)
        if self.subclass_of is not None:
            subclass_xml = ET.SubElement(subelement, 'rdfs:subClassOf')
            subclass_xml.set('rdf:resource', ontology_name +
                             "#"+self.subclass_of)
        if self.disjoint_with:
            for el in self.disjoint_with:
                disjoint_xml = ET.SubElement(subelement, 'rdfs:disjointWith')
                disjoint_xml.set('rdf:resource', ontology_name +
                                 "#"+el)
        return subelement
