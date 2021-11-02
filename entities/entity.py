"""
File defining the virtual Entity class.
Designed for Protégé - IA301.
"""

class Entity:
    def __init__(self, name:str):
        self.name = name
        self.disjoint_with = []

    def add_disjoint(self, name:str):
        self.disjoint_with.append(name)

    def to_xml(self):
        raise NotImplementedError