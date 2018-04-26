import numpy as np
import math
from collections import defaultdict

#get the queries from the text document
def getQueries():
    with open("set2\queries.txt", "r") as doc:
        queries = doc.readlines()
        queries = [line.strip() for line in queries]
    return queries

#create the dictionary
def createDictionary(doc):
    dictList = []
    #with open("set2\docs.txt", "r") as doc: #for efficiency, pass docs as an argument
    for line in doc:
        for word in line.split():
            dictList.append(word)
    dictList = list(set(dictList)) 
                #if word not in dictList: #alternative, ignore duplicates, pass into set then list
                    #dictList.append(word)
    return dictList

def getRelevantDocs(relevantList):
    relevantDocStrings = []
    with open("set2\docs.txt", "r") as doc:
        for i,line in enumerate(doc):
            for j in relevantList: 
                if (i+1) == j:
                    relevantDocStrings.append(line)
        return relevantDocStrings

def populateIndex():
    with open("set2\docs.txt", "r") as doc:
        index = defaultdict(list)
        for i, line in enumerate(doc):
            for word in line.split():
                if (i+1) not in index[word]:
                    index[word].append(i+1)
    return dict(index)

def queryIndex(index, query):
    documentList = []
    queryFound = False
    for key,value in index.items():
        for queryItem in query.split():
            if key == queryItem:
                queryFound = True
                documentList.append(value)
                queryset = map(set, documentList)
    if queryFound == True:
        relevantDoc = set.intersection(*queryset)
        return list(relevantDoc)

def createVector(doc, query, dict):
    query = query.split()
    doc = doc.split()

    queryVec = np.empty(len(dict), int) 
    docVec = np.empty(len(dict), int)
    for i,word in enumerate(dict):
        queryVec[i] = query.count(word)
        docVec[i] = doc.count(word)
    dot = np.dot(queryVec,np.array(docVec))
    normQuery = np.linalg.norm(queryVec)
    normDoc = np.linalg.norm(docVec)
    cos = (dot / (normQuery*normDoc))
    degrees = np.degrees(np.arccos(cos))
    vector = round(degrees, 5)

    return vector
    
def main():
    queries = getQueries()
    lineList = []
    with open("set2\docs.txt", "r") as doc:
        dictList = createDictionary(doc)

    with open("set2\docs.txt", "r") as doc:
        for line in doc.readlines():
            lineList.append(line.strip("\n"))
    index = populateIndex()
  
    print("Words in dictionary: " , len(dictList))
    for query in range(0, len(queries)):
        print("Query: ", queries[query])
        relevantList = queryIndex(index, queries[query])
        relevantList = sorted(relevantList)
        relevantDocStrings = getRelevantDocs(relevantList)
        vecDict = {}
        #find intersection of line and dictList
        for i,line in enumerate(relevantDocStrings):
            querydict = list((set(line.split()) & set(dictList)) | set(queries[query].split()))
            vecDict[relevantList[i]] = createVector(line, queries[query], querydict)
        print("Relevant documents: ", end ="")
        print(" ".join(str(x) for x in relevantList))
        vecsorted = sorted(vecDict, key=vecDict.get)
        for vec in vecsorted:
            print(vec, "{:.5f}".format(vecDict[vec]))              
main()


