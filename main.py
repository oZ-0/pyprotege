# import pandas as pd

# data = pd.read_csv('deputes-active.csv')
# print(data.head())

from pyprotege.ontology import Ontology
from pyprotege.ontology_class import OntologyClass
from pyprotege.data_property import DataProperty
from pyprotege.object_property import ObjectProperty
from pyprotege.individual import Individual


ONTOLOGY_NAME = "test"

test = Ontology("Test")

person = OntologyClass("Person")
test.add_class(person)

man = OntologyClass("Man")
man.as_subclass_of("Person")
test.add_class(man)

parent = OntologyClass("Parent")
parent.as_subclass_of("Person")
test.add_class(parent)

woman = OntologyClass("Woman")
woman.as_subclass_of("Person")
woman.as_disjoint_with("Man")
test.add_class(woman)

father = OntologyClass("Father")
father.as_subclass_of("Parent")
test.add_class(father)

ischild = ObjectProperty("IsChildOf", "Person", "Person")
ischild.as_inverse_of("isParentOf")
test.add_object_property(ischild)

isfriend = ObjectProperty("isFriendOf", "Person", "Person")
test.add_object_property(isfriend)

isparent = ObjectProperty("isParentOf", "Person", "Person")
isparent.as_inverse_of("isChildOf")
test.add_object_property(isparent)

isfather = ObjectProperty("isFatherOf", "Man", "Person")
isfather.as_subproperty_of("isParentOf")
test.add_object_property(isfather)

age = DataProperty("age", "Person", "integer")
test.add_data_property(age)

john_params = {
    'type': 'Man',
    'age': {
        "type": "integer",
        "text": "30"
    }
}
john = Individual("John", john_params)
test.add_individual(john)

lea_params = {
    "type": "Woman",
    'isFriendOf': 'John',
    'age': {
        "type": "integer",
        "text": "31"
    }
}
lea = Individual("Lea", lea_params)
test.add_individual(lea)

tom_params = {
    'type': 'Man',
    'isChildOf': 'John',
    'isChildOf#2': 'Lea',
    'age': {
        "type": "integer",
        "text": "5"
    }
}
tom = Individual("Tom", tom_params)
test.add_individual(tom)

test.write_xml("test.xml")
