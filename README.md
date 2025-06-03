# MedAI_ArchitectureKG
This repository contains the code and data for the bachelor thesis project: "Formalizing Boxology: An Ontology-Driven Approach for Representing Neuro-Symbolic Medical AI Architectures". The project focuses on transforming unstructured medical AI system diagrams into structured, queryable knowledge graphs using semantic technologies.

## Repository Structure
- Phase1_DataCleaning.ipynb: Jupyter Notebook for cleaning and preprocessing raw data extracted from publications.
- Phase2_OntologyCreation.py: Python script to define and create the ontology framework representing AI system components and their relationships.
- Phase3_Boxology_DOT: Directory containing DOT files representing Boxology diagrams of AI systems.
- Phase3_Boxology_RDF: Directory containing RDF files converted from DOT representations.
- Phase4_ParsingDOT_CreatingRDF.py: Python script to parse DOT files and generate corresponding RDF triples based on the ontology.
- OntologyFramework.owl: The OWL file defining the ontology used for structuring the AI system components and their interrelations.
- RawData.xlsx: Excel file containing the initial raw data.
- ProcessedData.xlsx: Excel file containing the cleaned and processed data without boxologies formalized

## Usage
- Data Cleaning: Open and run Phase1_DataCleaning.ipynb to clean and preprocess the raw data from RawData.xlsx. The cleaned data will be saved as ProcessedData.xlsx.
- Ontology Creation: Run Phase2_OntologyCreation.py to define and create the ontology framework. This will generate OntologyFramework.owl.
- DOT File Generation: Using the processed data, manually or programmatically create DOT files representing each Boxology diagrams. Save these files in the Phase3_Boxology_DOT/ directory. With name as DOT_publicationID
- RDF Conversion: Run Phase4_ParsingDOT_CreatingRDF.py to parse the DOT files and generate corresponding RDF files. The output will be saved in the Phase3_Boxology_RDF/ directory.
- Semantic Querying: Load OntologyFramework.owl and the RDF files into a semantic triple store like GraphDB. Use SPARQL queries to explore and analyze the structured AI system architectures.

For visualizing the DOT file paste the dot code onto: [Graphviz]([url](https://dreampuf.github.io/GraphvizOnline/?engine=dot#digraph%20G%20%7B%0A%0A%20%20subgraph%20cluster_0%20%7B%0A%20%20%20%20style%3Dfilled%3B%0A%20%20%20%20color%3Dlightgrey%3B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%2Ccolor%3Dwhite%5D%3B%0A%20%20%20%20a0%20-%3E%20a1%20-%3E%20a2%20-%3E%20a3%3B%0A%20%20%20%20label%20%3D%20%22process%20%231%22%3B%0A%20%20%7D%0A%0A%20%20subgraph%20cluster_1%20%7B%0A%20%20%20%20node%20%5Bstyle%3Dfilled%5D%3B%0A%20%20%20%20b0%20-%3E%20b1%20-%3E%20b2%20-%3E%20b3%3B%0A%20%20%20%20label%20%3D%20%22process%20%232%22%3B%0A%20%20%20%20color%3Dblue%0A%20%20%7D%0A%20%20start%20-%3E%20a0%3B%0A%20%20start%20-%3E%20b0%3B%0A%20%20a1%20-%3E%20b3%3B%0A%20%20b2%20-%3E%20a3%3B%0A%20%20a3%20-%3E%20a0%3B%0A%20%20a3%20-%3E%20end%3B%0A%20%20b3%20-%3E%20end%3B%0A%0A%20%20start%20%5Bshape%3DMdiamond%5D%3B%0A%20%20end%20%5Bshape%3DMsquare%5D%3B%0A%7D))
