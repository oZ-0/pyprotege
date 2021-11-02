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
            name (str): The name of the property.
            params (dict): The parameters of the individual. If params contains a datatype
                property, it is best to indicate its type using the type attribute. You can also
                provide the full XML line using keyref and valref attributes.
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
                    ref_url = "http://www.w3.org/2001/XMLSchema#"
                    if val_type in ["int", "long", "float", "double", "boolean"]:
                        param_xml.set("rdf:datatype", ref_url+val_type)
                        param_xml.text = val["text"]
                    else:
                        raise NotImplementedError(
                            "The type "+val_type+" has not yet been implemented...")
                else:
                    param_xml.set(val['refkey'], val['refval'])
                    if val.get("text"):
                        param_xml.text = val["text"]
        return subelement
