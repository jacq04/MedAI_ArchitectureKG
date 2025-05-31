import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD
from rdflib.namespace import NamespaceManager

df = pd.read_excel("THESIS_DEMO\ProcessedData.xlsx")

df.columns = df.columns.str.strip()  

g = Graph()

#NAMESPACES
EX = Namespace("http://example.org/publication#")
BOX = Namespace("http://example.org/boxology#")
ML = Namespace("http://example.org/ml#")
RB = Namespace("http://example.org/rb#")
GEO = Namespace("http://example.org/geo#")

g.bind("ex", EX)
g.bind("box", BOX)
g.bind("ml", ML)
g.bind("rb", RB)
g.bind("geo", GEO)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)

namespace_manager = g.namespace_manager
namespace_manager.bind('box', BOX, override=True)

#CLASSES
g.add((EX.Publication, RDF.type, RDFS.Class))
g.add((BOX.Boxology, RDF.type, RDFS.Class))
g.add((BOX.Architecture, RDF.type, RDFS.Class))
g.add((ML.MLMethod, RDF.type, RDFS.Class))
g.add((RB.RBMethod, RDF.type, RDFS.Class))
g.add((GEO.Country, RDF.type, RDFS.Class))


#looping through each row and building triples
for _, row in df.iterrows():
    id = int(row["Index"]) 
    pub_uri = URIRef(EX + f"Publication_{id}")
    g.add((pub_uri, RDF.type, EX.Publication)) #clarifying x is a publication

    boxology_uri = URIRef(f"http://example.org/boxology#Boxology_{id}")
    g.add((pub_uri, EX.hasBoxology, boxology_uri))
    g.add((boxology_uri, RDF.type, BOX.Boxology))
    
    #DATA PROPERTIES
    def is_valid_year(value):
        '''
        To check if the year is a valid 4 digit value.
        '''
        return isinstance(value, (int, float)) and 1000 <= int(value) <= 9999
    if pd.notna(row.get("Index")):
        g.add((pub_uri, EX["index"], Literal(int(row["Index"]), datatype=XSD.integer)))
    if pd.notna(row.get("Title")):
        g.add((pub_uri, EX.title, Literal(row["Title"])))
    if pd.notna(row.get("Author")):
        g.add((pub_uri, EX.author, Literal(row["Author"])))
    if pd.notna(row.get("Description and Clinical application")):
        g.add((pub_uri, EX.description, Literal(row["Description and Clinical application"])))
    if pd.notna(row.get("Primary motivation")):
        g.add((pub_uri, EX.primaryMotivation, Literal(row["Primary motivation"])))
    if pd.notna(row.get("Secondary motivation")):
        g.add((pub_uri, EX.secondaryMotivation, Literal(row["Secondary motivation"])))
    if pd.notna(row.get("Succes")):
        g.add((pub_uri, EX.success, Literal(row["Succes"])))
    if pd.notna(row.get("Limiting")):
        g.add((pub_uri, EX.limitation, Literal(row["Limiting"])))
    if pd.notna(row.get("Reference")):
        g.add((pub_uri, EX.bibliographicReference, Literal(row["Reference"])))
    
    #some year values are not 4 digits causing errors
    if pd.notna(row.get("Year of publication")) and is_valid_year(row["Year of publication"]):
        g.add((pub_uri, EX.year, Literal(str(int(row["Year of publication"])), datatype=XSD.gYear)))

    #OBJECT PROPERTIES
    if pd.notna(row.get("Type of architecture")):
        arch_uri = URIRef(BOX + row["Type of architecture"].strip().replace(" ", "_"))
        g.add((pub_uri, EX.hasArchitecture, arch_uri))
        g.add((arch_uri, RDF.type, BOX.Architecture)) 

    if pd.notna(row.get("ML method")):
        ml_uri = URIRef(ML + row["ML method"].strip().replace(" ", "_"))
        g.add((pub_uri, EX.usesMLMethod, ml_uri))
        g.add((ml_uri, RDF.type, ML.MLMethod)) 

    if pd.notna(row.get("Rule-based method")):
        rb_uri = URIRef(RB + row["Rule-based method"].strip().replace(" ", "_"))
        g.add((pub_uri, EX.usesRBMethod, rb_uri))
        g.add((rb_uri, RDF.type, RB.RBMethod))

    if pd.notna(row.get("Country of publication")):
        country_uri = URIRef(GEO + row["Country of publication"].strip().replace(" ", "_"))
        g.add((pub_uri, EX.hasCountry, country_uri))
        g.add((country_uri, RDF.type, GEO.Country))

    

#SAVING RESULTS
g.serialize(destination="OntologyFramework.owl", format="xml")
print("ONTOLOGY SAVED")

