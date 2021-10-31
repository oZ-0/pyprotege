import xml.etree.ElementTree as ET
from .entity import Entity


class DataProperty(Entity):
    def __init__(self, name: str, domains: str, ranges: str):
        super().__init__(name)
        self.tag = 'owl:DatatypeProperty'
        self.subproperty_of = None
        self.domains = domains
        if ranges in ['int', 'float', 'string', 'boolean']:
            self.ranges = 'http://www.w3.org/2001/XMLSchema#'+ranges
        else:
            ValueError(
                "ranges must be one of 'int', 'float', 'string', 'boolean'")

    def add_subproperty(self, name: str):
        self.subproperty_of = name

    def to_xml(self, subelement, ontology_name: str):
        subelement.set('rdf:about', ontology_name+"#"+self.name)
        if self.subproperty_of is not None:
            subproperty_xml = ET.SubElement(subelement, 'rdfs:subPropertyOf')
            subproperty_xml.set('rdf:resource', ontology_name +
                                "#"+self.subproperty_of)
        else:
            subproperty_xml = ET.SubElement(subelement, 'rdfs:subPropertyOf')
            subproperty_xml.set('rdf:resource', "http://www.w3.org/2002/07/owl#topDataProperty")

        domain_xml = ET.SubElement(subelement, 'rdfs:domain')
        domain_xml.set('rdf:resource', ontology_name +
                       "#"+self.domains)
        range_xml = ET.SubElement(subelement, 'rdfs:range')
        range_xml.set('rdf:resource', ontology_name +
                      "#"+self.ranges)
        return subelement
