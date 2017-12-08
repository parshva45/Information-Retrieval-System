import pickle
import math
import collections

with open("inverted_list_unigram_position_encoded.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("DocumentID-DocLen-encoded.txt", 'rb') as f:
    docID_doclen = pickle.loads(f.read())

with open("Cleaned_queries_encoded.txt", 'rb') as f:
    query_dict = pickle.loads(f.read())

queryTerm_Position = {}
queryTerm_docList = {}
query_positionInfo = {}

for q in query_dict:
    docList = []
    query = query_dict[q]
    print(query)
    query_terms = query.split()
    print(query_terms)
    #print(len(query_terms))
    for term in query_terms:
        if term in inverted_index:
            queryTerm_Position[term] = inverted_index[term]
            for i in range (0,len(queryTerm_Position[term])):
                docList.append(inverted_index[term][i])
            queryTerm_docList[term] = docList
        query_positionInfo[query] = queryTerm_Position

#print(queryTerm_Position)
#print(queryTerm_docList)
print(query_positionInfo)

#for query in queryTerm_docList:
f = open("Query_PositionInfo.txt",'w')
f.write(str(query_positionInfo))
f.close()


