"""RestFul API query"""
""" This code is the  final semantic keyword matcher updated 05-2-2021 """
"""Data_answer_first.csv is keywords collected from metadata. 
KeywordsEnglish.txt is for user keywords. metadata_pdok_all_removed.ttl is metadata collected 17-1-2017.
You can find new metadata here: https://data.labs.kadaster.nl/pdok/metadata/graphs or https://data.labs.kadaster.nl/pdok/metadata/."""
"""Developer: Mariam Sajjadian"""
import nltk
from nltk.corpus import wordnet
from google_trans_new import google_translator
import csv # this library is used for setting output in CSV format
from pattern.en import pluralize, singularize # to deal with the plural noun of a singular noun
from SPARQLWrapper import SPARQLWrapper, JSON # for query over online metadata
from timeit import default_timer as timer
from datetime import timedelta

start = timer()
#### setting inputs
Path_input = "C:\\0000Pythoncodes\\API\\final\\input\\"
#### input user keyword
with open(Path_input + "KeywordsEnglish.txt") as User_keyword_English:
    User_keyword = User_keyword_English.read()
    User_keyword = User_keyword.replace(" ", "_")
    name = User_keyword.split('\n')
    # print(User_keyword)
#### input keywords extracted from the RDF metadata
with open(Path_input + "Data_answer_first.csv") as English:
    metadataEnglish = English.read()
    key_list_Meta = metadataEnglish.split('\n')

#### this function is used for providing output similarity links
def outputsimilarity(similarity,path_output):
    #### write a URI to a file a csv file
    with open(path_output + User_keyword + ".csv", "w", newline='') as w:
        wr = csv.writer(w, quoting=csv.QUOTE_ALL)
        for word in similarity:
            if not word.strip(): continue
            wr.writerow([word])

#### this functtion returns keywords to the root
def lemmatize_keywords(words):
    lemmatizer = nltk.WordNetLemmatizer()
    lemmatized_keyword = (lemmatizer.lemmatize(words))
    return lemmatized_keyword

#### synonyms_synsets() function calculate synonyms and lemmas for the user keyword
#### print(synonyms_synsets(setAList)) to check the function
setAList = [lemmatize_keywords(User_keyword)]
def synonyms_synsets(AList):
    synonyms = []
    for TheList in AList:
        for syn in wordnet.synsets(TheList):
            for l in syn.lemmas():
                synStr = l.name()
                SynStrlemma = lemmatize_keywords(synStr) # return synonyms to their roots
                SynStrlemmaLower = SynStrlemma.lower()
                synonyms.append(SynStrlemmaLower)
                semanticKeywords = list(synonyms) # List of synonyms
                semanticKeywordsUnique = list(dict.fromkeys(semanticKeywords))[0:4] # remove duplicates from a List
    return semanticKeywordsUnique

#### hyponyms() function returns the list hyponyms for user inputs
#### print(hyponyms(setAList)) to check the function
def hyponyms(AList):
    for root in AList:
        hypoHyper = wordnet.synset(root + '.n.01')
        hypo_hyponyms = lambda s: s.hyponyms() # function and output is a code(<function <lambda> at 0x000001FF883E3598>)
        # the make 'Synset' object iterable, I need a closure
        # Compute transitive closures of synsets regarding a relation via breadth-first search
        list(hypoHyper.closure(hypo_hyponyms)) == hypoHyper.hyponyms()
        hyo_hypo_hyponyms_list = list(hypoHyper.closure(hypo_hyponyms))
        #### compute hyponyms
        hyponyms_list = []
        # if is for error when keywords do not have any hyponyms
        if len(hyo_hypo_hyponyms_list) > 0:
            for hyponym in hyo_hypo_hyponyms_list:
                hyponymStr = hyponym.name()
                hyponymStrSpl = hyponymStr.split('.')[0] ## clean name
                hyponyms_list.append(hyponymStrSpl)
                hyponyms_list_final = list(hyponyms_list)
        else:
            hyponyms_list_final = ['none'] # if the list is empty

    return hyponyms_list_final

#### hypernyms() function returns the list hypernyms for user inputs
##### print(hypernyms(setAList)) to check the function
def hypernyms(AList):
    for root in AList:
        hypoHyper = wordnet.synset(root + '.n.01')
        hyper_hypernyms = lambda s: s.hypernyms()
        # the make 'Synset' object iterable, I need a closure
        # Compute transitive closures of synsets regarding a relation via breadth-first search
        list(hypoHyper.closure(hyper_hypernyms)) == hypoHyper.hypernyms()
        hye_hyper_hypernyms_list = list(hypoHyper.closure(hyper_hypernyms))
        #### compute hypernym or superordinate
        hypernyms_list = []
        if len(hye_hyper_hypernyms_list) > 0:
            for hyp in hye_hyper_hypernyms_list:
                hyeStr = hyp.name()
                hyeStrSpl = hyeStr.split('.')[0]
                hypernyms_list.append(hyeStrSpl)
                hypernyms_list_final = list(hypernyms_list)
        else:
            hypernyms_list_final = ['none']
    return hypernyms_list_final

### Set A
Final_list_synsets_SetA = synonyms_synsets(setAList)
Final_list_synsets_SetA.extend(hyponyms(setAList))
Final_list_synsets_SetA.extend(hypernyms(setAList))
"""the below function compute relatedness"""
####this function compute set B and the output is the result of  A ∩ B
####print(metadata_synset_lists(key_list_Meta, Final_list_synsets_SetA))
def metadata_synset_lists(Meta, synsets_SetA):
    synonyms_semantic_final_AB = []
    final = []
    for TheList in Meta:
        synonyms_meta = []
        for syn in wordnet.synsets(TheList):
            for l in syn.lemmas():
                synStr_meta = l.name()
        # print("this is my new test:",synonyms)
                SynStrlemma_meta = lemmatize_keywords(synStr_meta)  # return synonyms to their roots
                SynStrlemmaLower_meta = SynStrlemma_meta.lower()
                synonyms_meta.append(SynStrlemmaLower_meta)
                semanticKeywords = list(synonyms_meta)  # List of synonyms
                semanticKeywordsUnique_meta_setB = list(dict.fromkeys(semanticKeywords))[0:4]
        intersection_keyword_AB = list(set.intersection(set(synsets_SetA), set(semanticKeywordsUnique_meta_setB)))
        if len(intersection_keyword_AB) >= 1:
            for intersectionAB in intersection_keyword_AB:
                if len(intersectionAB) > 2:
                    synonyms_semantic_final_AB.append(intersectionAB)
            final.append(synonyms_semantic_final_AB)
    flat_list = [item for sublist in final for item in sublist]
    synonyms_semantic_final_meta_setAandB = list(dict.fromkeys(flat_list))


    return synonyms_semantic_final_meta_setAandB

"""this is smilarity function"""
### set C
#### the similarity_score function checks distance between the user keyword with metadata keywords
#### print(similarity_score(User_keyword, key_list_Meta))
def similarity_score(keyword, Meta):
    lookup_keyword = wordnet.synset(lemmatize_keywords(keyword) + '.n.01')
    syn_answer_list = []
    answer_scores_list = []
    score_similarity = []

    for syn_answer in Meta:
        syn_answer = lemmatize_keywords(syn_answer)
        lookup_meta = wordnet.synset(syn_answer + '.n.01')
        syn_scores = str(round(lookup_keyword.wup_similarity(lookup_meta), 2))
        syn_answer_split = syn_answer.split(',')
        syn_answer_list.append(syn_answer_split)
        answer_scores_split = syn_scores.split(',')
        answer_scores_list.append(answer_scores_split)
        concatenate_list = [x + y for x, y in zip(syn_answer_list, answer_scores_list)] # Making a list by concatenating items in parallel

        for con in concatenate_list:
            itemTofloat = float(con[1])
            if itemTofloat > 0.69:

                concatenate_list_strings_str = con[0]
                score_similarity.append(concatenate_list_strings_str)
                concatenate_list_strings = score_similarity
                # print(concatenate_list_strings)
            # else:
            #     concatenate_list_strings = []
                # print("2",concatenate_list_strings)
                # concatenate_list_sort = (sorted(concatenate_list_strings, key=operator.itemgetter(1), reverse=True))  # Reverse Sort and select the first 5 items
                # metalist_final_score_setC = [item[0] for item in concatenate_list_sort] # Extract first item of each sublist
    return(concatenate_list_strings)

setAandB = metadata_synset_lists(key_list_Meta, Final_list_synsets_SetA)
print(setAandB)
setC = similarity_score(User_keyword, key_list_Meta)[0:3]
print(setC)

setAandB.extend(setC)
setAandB = setAandB
for AB in setAandB :
   setAandBandC_p = pluralize(AB)
   setAandBandC_p= setAandBandC_p.split('\n')

setAandB.extend(setAandBandC_p)
setAandB.extend(name)
setAandBandC = setAandB
setAandBandC_final = list(dict.fromkeys(setAandBandC))
print("semantic keywords in English:", setAandBandC_final)

key_list = []
for name in setAandBandC_final:
    name = name.replace("_", " ")
    # print(name)
    translator = google_translator()
    translate_text = translator.translate(name,lang_tgt='nl')[0:-1]
    # print(" the output api:", translate_text)
    key_list.append(translate_text)
key = key_list
print("semantic keywords in Dutch:", key)
sparql = SPARQLWrapper('https://api.labs.kadaster.nl/datasets/pdok/metadata/services/metadata/sparql')
##### Run a Query
lineList1 = []
for k in key:
    k = "'" + k + "'"
    # print(k)
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
