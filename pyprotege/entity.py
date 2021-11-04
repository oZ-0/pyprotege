"""
File defining the virtual Entity class.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET


class Entity:
    """ Entity virtual class containaing the necessary arguments and methods. """

    def __init__(self, name: str):
        """Basic constructor for the entity class.

        Args:
            name (str): The name of the ontology.
        """
        self.name = name
        self.disjoint_with = []

    def as_disjoint_with(self, name: str):
        """State that it is disjoint with the class called name. Its existence is not checked.

        Args:
            name (str): The name of the disjoint class.
        """
        self.disjoint_with.append(name)

    def to_xml(self, subelement: ET.Element, ontology_name: str) -> ET.Element:
        """Converts the class to an xml element.

        Args:
            subelement (ET.Element): The subelement in which to convert the class.
            ontology_name (str): The name of the Ontology.

        Returns:
            ET.SubElement: The modified subelement.
        """
        raise NotImplementedError
