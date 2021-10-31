import xml.etree.ElementTree as ET
from .entity import Entity


class Individual(Entity):
    def __init__(self, name: str, params: dict):
        super().__init__(name)
        self.tag = "owl:NamedIndividual"
        self.params = params

    def to_xml(self, subelement, ontology_name: str):
        subelement.set('rdf:about', ontology_name+"#"+self.name)
        for (key, val) in self.params.items():
            if key == "type":
                param_xml = ET.SubElement(subelement, 'rdf:'+key)
            else:
                param_xml = ET.SubElement(subelement, key)
            if not isinstance(val,dict):
                param_xml.set('rdf:resource', ontology_name +
                          "#"+val)
            else:
                param_xml.set(val['refkey'], val['refval'])
                if val.get("text"):
                    param_xml.text = val["text"]
        return subelement
