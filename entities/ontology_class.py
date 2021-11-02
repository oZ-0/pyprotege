"""
File defining Classes of objects.
Designed for Protégé - IA301.
"""

import xml.etree.ElementTree as ET
from .entity import Entity


class OntologyClass(Entity):
    def __init__(self, name: str):
        super().__init__(name)
        self.subclass_of = None
        self.tag = "owl:Class"
        self.disjoint_with = []

    def as_subclass_of(self, name: str):
        self.subclass_of = name

    def as_disjoint_with(self, name: str):
        self.disjoint_with.append(name)

    def to_xml(self, subelement, ontology_name: str):
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
