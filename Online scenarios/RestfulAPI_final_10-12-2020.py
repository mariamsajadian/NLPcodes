" this codes for query over online metadata"
from SPARQLWrapper import SPARQLWrapper, JSON

# API address
sparql = SPARQLWrapper('https://api.labs.kadaster.nl/datasets/pdok/metadata/services/metadata/sparql')
# create folder
# txt file contains keywords in the questions that is replaced in the SPARQL query as object
with open("KeywordExtension.txt") as Dutch:
    Save_keywords = Dutch.read()

Input_Keyword = Save_keywords.split('\n')

# you can search by: keywords, about, dateIssued, name  (here should be key)
for k in Input_Keyword:
    print(k)
    sparql.setQuery(""" PREFIX sdo: <https://schema.org/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT "dataset" ?resource ?keyword WHERE {
          VALUES (?type ?class) {
          ("dataset" sdo:Dataset)
        ("service" sdo:WebAPI)
       }
        ?resource <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?class;
        (sdo:about|sdo:keywords|sdo:name|sdo:dateIssued|sdo:identifier) ?keyword.
         FILTER(CONTAINS(LCASE(STR(?keyword)), LCASE(STR(""" + k + """))))
       }
        ORDER BY ("dataset") (?resource) (?keyword) """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    lineList = []
    for result in results["results"]["bindings"]:
        listOfDictionary = (result['resource'])
        URI = (listOfDictionary['value'])
        # concatenate browser search engine to URLs
        metadata = "https://data.labs.kadaster.nl/pdok/metadata/browser?resource=" + URI
        # print(metadata)
        # append the lists in the loop(mutable and Immutable and initialize strings and data structure
        lineList.append(metadata)
        # print(len(lineList))
    mylist = list(dict.fromkeys(lineList))
    # print the number of list
    number = (len(mylist))
    number = str(number)
    print(number)
for my in mylist:
    print(my)