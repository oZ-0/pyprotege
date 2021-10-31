import xml.etree.ElementTree as ET
from .entity import Entity


class ObjectProperty(Entity):
    def __init__(self, name: str, domains: str, ranges: str):
        super().__init__(name)
        self.tag = 'owl:ObjectProperty'
        self.subproperty_of = None
        self.inverse_of = None
        self.domains = domains
        self.ranges = ranges

    def as_subproperty_of(self, name: str):
        self.subproperty_of = name

    def as_inverse_of(self, name: str):
        self.inverse_of = name

    def to_xml(self, subelement, ontology_name: str):
        subelement.set('rdf:about', ontology_name+"#"+self.name)
        if self.subproperty_of is not None:
            subproperty_xml = ET.SubElement(subelement, 'rdfs:subPropertyOf')
            subproperty_xml.set('rdf:resource', ontology_name +
                             "#"+self.subproperty_of)
        else:
            subproperty_xml = ET.SubElement(subelement, 'rdfs:subPropertyOf')
            subproperty_xml.set('rdf:resource', "http://www.w3.org/2002/07/owl#topObjectProperty")
        if self.inverse_of is not None:
            inverse_of_xml = ET.SubElement(subelement, 'rdfs:inverseOf')
            inverse_of_xml.set('rdf:resource', ontology_name +
                             "#"+self.inverse_of)
        domain_xml = ET.SubElement(subelement, 'rdfs:domain')
        domain_xml.set('rdf:resource', ontology_name +
                             "#"+self.domains)
        range_of_xml = ET.SubElement(subelement, 'rdfs:range')
        range_of_xml.set('rdf:resource', ontology_name +
                             "#"+self.ranges)
        return subelement
