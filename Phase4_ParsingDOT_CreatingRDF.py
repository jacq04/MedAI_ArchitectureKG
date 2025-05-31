import os
import re
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS
from rdflib.namespace import NamespaceManager

dot_folder = "FINAL_THESIS/Phase3_Boxology_DOT"
ttl_folder = "FINAL_THESIS/Phase3_Boxology_RDF"

os.makedirs(ttl_folder, exist_ok=True)
EX = Namespace("http://example.org/publication#") 
BOX = Namespace("http://example.org/boxology#") 


def process_dot_file(dot_file_path):
    '''
    XYZ
    '''
    pub_id = os.path.basename(dot_file_path).split("_")[1]  #DOT_9 → "9" later used for URI generation later on 
    with open(dot_file_path, "r") as f:
        dot = f.read()

    g = Graph()
    
    namespace_manager = g.namespace_manager
    namespace_manager.bind('box', BOX, override=True)
    namespace_manager.bind('rdfs', RDFS)

    g.bind("ex", EX) #shortening namespaces for ttl file 
    g.bind("box", BOX)

    pub_uri = EX[f"Publication_{pub_id}"]
    box_uri = BOX[f"Boxology_{pub_id}"]
    g.add((pub_uri, EX.hasBoxology, box_uri)) #publicationX has boxologyX

    subgraphs = re.findall(r'subgraph\s+cluster_\d+\s*{(.*?)}', dot, re.DOTALL) #collecting all subgraphs and extracting content inside the curly bracket, converts to string and puts in a list
    for index, block in enumerate(subgraphs, 1): #index: 4 subgraphs, each subgraph which is a string in list subgraph
        step_uri = BOX[f"Steps_{pub_id}_{index}"] #step's URI - Steps_9_1
        g.add((step_uri, RDF.type, BOX.Step)) #step is of type step
        g.add((box_uri, BOX.includesStep, step_uri)) # boxology has step step_uri

        label_match = re.search(r'label\s*=\s*"([^"]+)"', block) 
        #only set rdfs:label if it hasn't been added already
        if label_match:
            label_text = label_match.group(1).strip()
            if (step_uri, RDFS.label, None) not in g:
                g.add((step_uri, RDFS.label, Literal(label_text)))

        #match all inputs (input, input1, input2...), outputs, and process
        for prop, predicate in [("input", BOX.hasInput), ("output", BOX.hasOutput)]:
            # Find all input1, input2, input etc.
            matches = re.findall(fr'{prop}\d*\s*=\s*"([^"]+)"', block)
            for val in matches:
                val_clean = val.strip()
                node_label = val_clean.replace(" ", "_").replace(":", "_")
                node_uri = BOX[node_label]
                g.add((step_uri, predicate, node_uri))
                if (node_uri, RDFS.label, None) not in g:
                    g.add((node_uri, RDFS.label, Literal(val_clean)))


    # Only one process per step is assumed
        process_match = re.search(r'process\s*=\s*"([^"]+)"', block)
        if process_match:
            val_clean = process_match.group(1).strip()
            node_label = val_clean.replace(" ", "_").replace(":", "_")
            node_uri = BOX[node_label]
            g.add((step_uri, BOX.hasProcess, node_uri))
            if (node_uri, RDFS.label, None) not in g:
                g.add((node_uri, RDFS.label, Literal(val_clean)))



    #save TTL - create as a seperate funciton??
    ttl_path = os.path.join(ttl_folder, f"TTL_{pub_id}.ttl")
    g.serialize(destination=ttl_path, format="turtle")
    print(f"created TTL for Publication {pub_id}: {ttl_path}")

#create a seperate function?? #to run over each file in the folder #STARTS HERE 
for file in os.listdir(dot_folder):
    if file.startswith("DOT_") and os.path.isfile(os.path.join(dot_folder, file)):
        process_dot_file(os.path.join(dot_folder, file)) #dot foler path + the specific dot file's path, eg Boxology_dots\DOT_9
                                                        #better do it this way for automation 
    

