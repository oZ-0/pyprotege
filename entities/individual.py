"""
File defining the Individual class which helps creating NamedIndividuals.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET
from .entity import Entity


class Individual(Entity):
    """Class which represents an individual. Derives from the Entity virtual class."""

    def __init__(self, name: str, params: dict):
        """Basic contructor for the individual. 

        Args:
            name (str): The name of the property
            params (dict): The parameters of the individual
        """
        super().__init__(name)
        self.tag = "owl:NamedIndividual"
        self.params = params

    def to_xml(self, subelement: ET.Element, ontology_name: str) -> ET.Element:
        """Converts the class to an xml element.

        Args:
            subelement (ET.Element): The subelement in which to convert the class.
            ontology_name (str): The name of the Ontology.

        Returns:
            ET.SubElement: The modified subelement.
        """
        subelement.set('rdf:about', ontology_name+"#"+self.name)
        for (key, val) in self.params.items():
            if key == "type":
                param_xml = ET.SubElement(subelement, 'rdf:'+key)
            else:
                param_xml = ET.SubElement(subelement, key)
            if not isinstance(val, dict):
                param_xml.set('rdf:resource', ontology_name +
                              "#"+val)
            else:
                val_type = val.get('type')
                if val_type is not None:
                    if val_type == "int":
                        param_xml.set(
                            "rdf:datatype", "http://www.w3.org/2001/XMLSchema#integer")
                    elif val_type == "float":
                        param_xml.set(
                            "rdf:datatype", "http://www.w3.org/2001/XMLSchema#float")
                    elif val_type == "bool":
                        param_xml.set(
                            "rdf:datatype", "http://www.w3.org/2001/XMLSchema#boolean")
                    else:
                        raise NotImplementedError(
                            "The type "+val_type+" has not been implemented. Contact the maintainer.")
                    param_xml.text = val["text"]
                else:
                    param_xml.set(val['refkey'], val['refval'])
                    if val.get("text"):
                        param_xml.text = val["text"]
        return subelement
