#George Browning
#C1769600
import numpy as np
import math
from collections import defaultdict

#get the queries from the text document
def getQueries():
    with open("set1\queries.txt", "r") as doc:
        queries = doc.readlines()
        queries = [line.strip() for line in queries]
    return queries

#create the dictionary
def createDictionary(doc):
    dictList = []
    for line in doc:
        for word in line.split():
            #append every word in the document to the dictionary
            dictList.append(word)
    #to remove duplicates efficiently, pass the dictionary into a set and back into a list again
    dictList = list(set(dictList)) 
    return dictList

def getRelevantDocs(relevantList):
    relevantDocStrings = []
    #returns a list of all lines that have the relevant document numbers
    with open("set1\docs.txt", "r") as doc:
        for i,line in enumerate(doc):
            for j in relevantList: 
                if (i+1) == j:
                    relevantDocStrings.append(line)
        return relevantDocStrings

def populateIndex():
    with open("set1\docs.txt", "r") as doc:
        #defaultdict provides a default value for keys that have not yet been initialised
        index = defaultdict(list)
        #for every word in the document, check what documents it's in and add those document numbers to the dictionary entry for that word
        for i, line in enumerate(doc):
            for word in line.split():
                if (i+1) not in index[word]:
                    index[word].append(i+1)
    return dict(index)

def queryIndex(index, query):
    documentList = []
    queryFound = False
    #search each item in the index for that query
    for key,value in index.items():
        for queryItem in query.split():
            if key == queryItem:
                queryFound = True
                documentList.append(value)
                queryset = map(set, documentList)
    #if the words in the query have been found, the intersection of the words' relevant documents are the relevant documents for the whole query
    if queryFound == True:
        relevantDoc = set.intersection(*queryset)
        return list(relevantDoc)

def createVector(doc, query, dict):
    query = query.split()
    doc = doc.split()

    queryVec = np.empty(len(dict), int) 
    docVec = np.empty(len(dict), int)
    #creates the query vector and the document vector
    for i,word in enumerate(dict):
        queryVec[i] = query.count(word)
        docVec[i] = doc.count(word)
    #work out the angle between the 2
    dot = np.dot(queryVec,np.array(docVec))
    normQuery = np.linalg.norm(queryVec)
    normDoc = np.linalg.norm(docVec)
    cos = (dot / (normQuery*normDoc))
    degrees = np.degrees(np.arccos(cos))
    #round it to 5 decimal places
    vector = round(degrees, 5)

    return vector
    
def main():
    queries = getQueries()
    lineList = []
    with open("set1\docs.txt", "r") as doc:
        #create the dictionary
        dictList = createDictionary(doc)

    with open("set1\docs.txt", "r") as doc:
        #get list of lines in the document
        for line in doc.readlines():
            lineList.append(line.strip("\n"))
    #build the inverted index
    index = populateIndex()
  
    print("Words in dictionary: " , len(dictList))
    for query in range(0, len(queries)):
        print("Query: ", queries[query])
        #get the relevant document numbers by querying the index for that query
        relevantList = queryIndex(index, queries[query])
        relevantList = sorted(relevantList)
        #find the strings belonging to the relevant document numbers
        relevantDocStrings = getRelevantDocs(relevantList)
        vecDict = {}
        #instead of creating a vector using the entire dictionary, it is much faster to create to create a vector
        # using only the words that are either in the query or in the specific line the vector is being calculated for
        # eg: (words in the line ∩ dictionary) ∪ words in the query
        for i,line in enumerate(relevantDocStrings):
            querydict = list((set(line.split()) & set(dictList)) | set(queries[query].split()))
            vecDict[relevantList[i]] = createVector(line, queries[query], querydict)
        print("Relevant documents: ", end ="")
        print(" ".join(str(x) for x in relevantList))
        #sort the angles in ascending order
        vecsorted = sorted(vecDict, key=vecDict.get)
        for vec in vecsorted:
            #print the angle, include trailing zeroes if there are fewer than 5 decimal places (eg. 45.10000)
            print(vec, "{:.5f}".format(vecDict[vec]))              
main()