import pandas as pd
from pyprotege.ontology import Ontology
from pyprotege.ontology_class import OntologyClass
from pyprotege.data_property import DataProperty
from pyprotege.object_property import ObjectProperty
from pyprotege.individual import Individual


ONTOLOGY_NAME = "politique"
ontology = Ontology("Politique")

parti = OntologyClass("Parti")
ontology.add_class(parti)

groupe = OntologyClass("Groupe")
groupe.as_subclass_of("Parti")
ontology.add_class(groupe)

votant = OntologyClass("Votant")
ontology.add_class(votant)

elu = OntologyClass("Elu")
elu.as_subclass_of("Votant")
ontology.add_class(elu)

nonElu = OntologyClass("nonElu")
nonElu.as_subclass_of("Votant")
ontology.add_class(nonElu)

depute = OntologyClass("Depute")
depute.as_subclass_of("Elu")
ontology.add_class(depute)

senateur = OntologyClass("Senateur")
senateur.as_subclass_of("Elu")
senateur.as_disjoint_with("Depute")
ontology.add_class(senateur)

maire = OntologyClass("Maire")
maire.as_subclass_of("Elu")
ontology.add_class(maire)

lieuDeFonction = OntologyClass("LieuDeFonction")
ontology.add_class(lieuDeFonction)


estAllie = ObjectProperty("EstAllie", "Parti", "Parti")
estAllie.set_symmetric()
ontology.add_object_property(estAllie)

aVotePour = ObjectProperty("aVotePour", "Votant", "Parti")
ontology.add_object_property(aVotePour)

sympathisantDe = ObjectProperty("sympathisantDe", "Votant", "Parti")
ontology.add_object_property(sympathisantDe)

incluantElu = ObjectProperty("incluantElu", "Parti", "Elu")
ontology.add_object_property(incluantElu)

appartientAGroupe = ObjectProperty("appartientAGroupe", "Elu", "Groupe")
appartientAGroupe.as_inverse_of("incluantElu")
ontology.add_object_property(appartientAGroupe)

travailleA = ObjectProperty("travailleA", "Votant", "LieuDeFonction")
ontology.add_object_property(travailleA)

heberge = ObjectProperty("heberge", "LieuDeFonction", "Votant")
heberge.as_inverse_of("travailleA")
ontology.add_object_property(heberge)


nom_votant = DataProperty("nomVotant", "Votant", "string")
ontology.add_data_property(nom_votant)

nom_groupe = DataProperty("nomGroupe", "Votant", "string")
ontology.add_data_property(nom_groupe)

prenom = DataProperty("prenom", "Votant", "string")
ontology.add_data_property(prenom)

age = DataProperty("age", "Votant", "integer")
ontology.add_data_property(age)

genre = DataProperty("genre", "Votant", "boolean")
ontology.add_data_property(genre)

tauxVote = DataProperty("tauxVote", "Votant", "decimal")
ontology.add_data_property(tauxVote)

loyaute = DataProperty("loyaute", "Votant", "decimal")
ontology.add_data_property(loyaute)

votePourMajorite = DataProperty("votePourMajorite", "Votant", "decimal")
ontology.add_data_property(votePourMajorite)

voteSpecialite = DataProperty("voteSpecialite", "Votant", "decimal")
ontology.add_data_property(voteSpecialite)

departement = DataProperty("departement", "Votant", "string")
ontology.add_data_property(departement)

experience = DataProperty("experience", "Votant", "integer")
ontology.add_data_property(experience)

# lieu = DataProperty("lieu", "Votant", "LieuDeFonction")
# ontology.add_data_property(lieu)


# ----------------------------------------------------------------


df = pd.read_csv('deputes-active.csv')
df.replace({'M.': True, 'Mme': False}, inplace=True)
df['nom'] = df['nom'].apply(lambda x: x.lower().replace(" ", ""))
df['prenom'] = df['prenom'].apply(lambda x: x.lower())
df['groupe'] = df['groupe'].apply(lambda x: x.lower().replace(" ", ""))
df['experienceDepute'] = df['experienceDepute'].apply(
    lambda x: x.lower().replace("mois", "ans"))  # create biais but simplest fix
df['scoreParticipationSpecialite'] = df['scoreParticipationSpecialite'].fillna(
    0)
df['scoreLoyaute'] = df['scoreLoyaute'].fillna(0)
df = df.astype(str)

# def remplissage(df,ontologie):
for index, row in df.iterrows():
    param = {
        'type': 'Depute',
        'nomVotant': {
            "type": "string",
            "text": str(row['nom'])
        },
        'prenom': {
            "type": "string",
            "text": row['prenom']
        },
        'age': {
            "type": "integer",
            "text": str(int(row['age']))
        },
        'genre': {
            "type": "boolean",
            "text": str(row['civ']).lower()
        },
        'tauxVote': {
            "type": "decimal",
            "text": str(float(row['scoreParticipation']))
        },
        'loyaute': {
            "type": "decimal",
            "text": str(float(row['scoreLoyaute']))
        },
        'votePourMajorite': {
            "type": "decimal",
            "text": str(float(row['scoreMajorite']))
        },
        'voteSpecialite': {
            "type": "decimal",
            "text": str(float(row['scoreParticipationSpecialite']))
        },
        'departement': {
            "type": "string",
            "text": row['departementNom']
        },
        'experience': {
            "type": "integer",
            "text": str(int(row['experienceDepute'][:-3]))
        },
        "appartientAGroupe": row['groupe'],
        "travailleA": "assembleenationale"

    }
    ontology.add_individual(Individual(str(row['nom']), param))

groupes = df['groupe'].unique()
for grp in groupes:
    param = {
        'type': 'Groupe',
        'nomGroupe': {
            "type": "string",
            "text": grp
        }
    }
    ontology.add_individual(Individual(grp, param))

ontology.add_individual(Individual("assembleenationale", {'type': 'LieuDeFonction'}))

# rne-maires.csv et rne-sen.csv ne marchent pas


ontology.write_xml("main.xml")
