from entities.ontology import Ontology
from entities.ontology_class import OntologyClass
from entities.data_property import DataProperty
from entities.object_property import ObjectProperty
from entities.individual import Individual


ONTOLOGY_NAME = "politique"
test = Ontology("Politique")

parti = OntologyClass("Parti")
test.add_class(parti)

groupe = OntologyClass("Groupe")
groupe.as_subclass_of("Parti")
test.add_class(groupe)

votant = OntologyClass("Votant")
test.add_class(votant)

elu = OntologyClass("Elu")
elu.as_subclass_of("Votant")
test.add_class(elu)

nonElu = OntologyClass("nonElu")
nonElu.as_subclass_of("Votant")
test.add_class(nonElu)

depute = OntologyClass("Depute")
depute.as_subclass_of("Elu")
test.add_class(depute)

senateur = OntologyClass("Senateur")
senateur.as_subclass_of("Elu")
senateur.as_disjoint_with("Depute")
test.add_class(senateur)

maire = OntologyClass("Maire")
maire.as_subclass_of("Elu")
test.add_class(maire)

lieuDeFonction = OntologyClass("LieuDeFonction")
test.add_class(lieuDeFonction)


estAllie = ObjectProperty("EstAllie","Parti","Parti")
estAllie.set_symmetric()
test.add_object_property(estAllie)

aVotePour = ObjectProperty("aVotePour","Votant","Parti")
test.add_object_property(aVotePour)

sympathisantDe = ObjectProperty("sympathisantDe","Votant","Parti")
test.add_object_property(sympathisantDe)

appartientAParti = ObjectProperty("appartientAParti","Elu","Parti")
test.add_object_property(appartientAParti)

appartientAGroupe = ObjectProperty("appartientAGroupe","Elu","Groupe")
appartientAGroupe.as_subproperty_of("appartientAParti")
test.add_object_property(appartientAGroupe)

travailleA = ObjectProperty("travailleA","Votant","LieuDeFonction")
test.add_object_property(lieuDeFonction)


nom = DataProperty("nom", "Votant", "string")
test.add_data_property(nom)

prenom = DataProperty("prenom", "Votant", "string")
test.add_data_property(prenom)

age = DataProperty("age", "Votant", "int")
test.add_data_property(age)

genre = DataProperty("genre", "Votant", "boolean")
test.add_data_property(genre)

tauxVote = DataProperty("tauxVote", "Votant", "int")
test.add_data_property(tauxVote)

loyaute = DataProperty("loyaute", "Votant", "int")
test.add_data_property(loyaute)

votePourMajorite =  DataProperty("votePourMajorite", "Votant", "int")
test.add_data_property(votePourMajorite)

voteSpecialite =  DataProperty("voteSpecialite", "Votant", "int")
test.add_data_property(voteSpecialite)

departement =  DataProperty("departement", "Votant", "string")
test.add_data_property(departement)

experience =  DataProperty("experience", "Votant", "int")
test.add_data_property(experience)

lieu =  DataProperty("lieu", "LieuDeFonction", "string")
test.add_data_property(lieu)


# ----------------------------------------------------------------


import pandas as pd

df = pd.read_csv('deputes-active.csv')
df.replace({'M.':True,'Mme':False},inplace=True)
df['nom'] = df['nom'].apply(lambda x: x.replace(" ",""))
df = df.astype(str)

# def remplissage(df,ontologie):
for index, row in df.iterrows():
    param ={ 
        'type': 'Depute',
        'nom': {
        "type": "string",
        "text": str(row['nom'])
    }
    ,
        'prenom': {
        "type": "string",
        "text": row['prenom']
    },
        'age': {
        "type": "int",
        "text": row['age']
    },
        'genre': {
        "type": "boolean",
        "text": row['civ']
    },
        'tauxVote':{
        "type": "int",
        "text": row['scoreParticipation']
    }, 
        'loyaute': {
        "type": "int",
        "text": row['scoreLoyaute']
    },
        'votePourMajorite': {
        "type": "int",
        "text": row['scoreMajorite']
    },
        'voteSpecialite': {
        "type": "int",
        "text": row['scoreParticipationSpecialite']
    },
        'departement': {
        "type": "string",
        "text": row['departementNom']
    },
        'experience': {
        "type": "int",
        "text": row['experienceDepute'][:-3]
    }

    }
    test.add_individual(Individual(str(row['nom']), param))

#rne-maires.csv et rne-sen.csv ne marchent pas


test.write_xml("main.xml")
