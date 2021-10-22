"""RestFul API query"""
""" This code is the  final semantic keyword matcher updated 05-2-2021 """
"""Data_answer_first.csv is keywords collected from metadata. 
KeywordsEnglish.txt is for user keywords. metadata_pdok_all_removed.ttl is metadata collected 17-1-2017.
You can find new metadata here: https://data.labs.kadaster.nl/pdok/metadata/graphs or https://data.labs.kadaster.nl/pdok/metadata/."""
"""Developer: Mariam Sajjadian"""
from SPARQLWrapper import SPARQLWrapper, JSON # for query over online metadata
from timeit import default_timer as timer
from datetime import timedelta

start = timer()
sparql = SPARQLWrapper('https://api.labs.kadaster.nl/datasets/pdok/metadata/services/metadata/sparql')

#### setting inputs
Path_input = "C:\\0000Pythoncodes\\API\\final\\input\\"

#### input user keyword
with open(Path_input + "baseline.txt") as User_keyword_English:
    User_keyword = User_keyword_English.read()
    User_keyword = User_keyword.replace(" ", "_")
    name = User_keyword.split('\n')

lineList1 = []
k = User_keyword
print(k)
k = "'" + k + "'"
print(len(k))
sparql.setQuery(""" PREFIX sdo: <https://schema.org/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT "dataset" ?resource ?keyword WHERE {
          VALUES (?type ?class) {
          ("dataset" sdo:Dataset)
        ("service" sdo:WebAPI)
       }
        ?resource <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?class;
        (sdo:about|sdo:keywords|sdo:name|sdo:dateIssued|sdo:description) ?keyword.
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
# print(lineList)
if len(lineList) > 0:
    for lineList in lineList:
        # print(lineList)
        lineList1.append(lineList)

mylist = list(dict.fromkeys(lineList1))
number = len(mylist)

for URLs in mylist:
    print(URLs)
# print(len(lineList1))
print("number of links are:", number)
end = timer()
print(timedelta(seconds=end-start))
""" Some keywords may retrieve metadata using Google API,
you can add the Google translate code if the keyword would not find in WordNet. """
