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

def generate_ngrams(words_list, n):                           #Function to generate n-grams
    ngrams_list = []

    for num in range(0, len(words_list)):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)

    return ngrams_list

query_docNamedocScore = {}

for q in query_dict:
    document_docScore = {}
    query_score = 0
    query = query_dict[q]
    query_terms = query.split()
    bigrams = generate_ngrams(query_terms,2)
    #print(bigrams)
    for term in query_terms:
        docList = []
        doc_list = []
        if term in inverted_index:
            queryTerm_Position[term] = inverted_index[term]
            for i in range (0,len(queryTerm_Position[term])):
                docList.append(inverted_index[term][i])
            for doc in docList:
                doc_list += [doc[0]]
        queryTerm_docList[term] = doc_list
    for term in bigrams:
        terms_under_consideration = term.split()
        if len(term.split()) == 2:
            #print(terms_under_consideration)
            #print(queryTerm_docList[terms_under_consideration[0]])
            #print(len(queryTerm_docList[terms_under_consideration[0]]))
            #print(queryTerm_docList[terms_under_consideration[1]])
            #print(len(queryTerm_docList[terms_under_consideration[1]]))
            #print("-----------------------------------------------")
        #print(list(set(queryTerm_docList[terms_under_consideration[0]] + queryTerm_docList[terms_under_consideration[1]])))
            common_docs = [val for val in queryTerm_docList[terms_under_consideration[0]] if val in queryTerm_docList[terms_under_consideration[1]]]
            #print(common_docs)
            #print("-----------------------------------------------")
            for doc in common_docs:
                positionListOfTerm1 = []
                positionListOfTerm2 = []
                value_part_of_term_1 = inverted_index[terms_under_consideration[0]]
                value_part_of_term_2 = inverted_index[terms_under_consideration[1]]
                for i in range(0,len(value_part_of_term_1)):
                    #print(value_part[i])
                    if value_part_of_term_1[i][0] == doc:
                        #print("aaya")
                        positionListOfTerm1 = value_part_of_term_1[i][1]
                #print("positionListOfTerm1")
                #print(positionListOfTerm1)
                #print("----------------------")
                for i in range(0,len(value_part_of_term_2)):
                    #print(value_part[i])
                    if value_part_of_term_2[i][0] == doc:
                        #print("aaya")
                        positionListOfTerm2 = value_part_of_term_2[i][1]
                #print("positionListOfTerm2")
                #print(positionListOfTerm2)
                #print("----------------------")
                score = 0
                for element1 in positionListOfTerm1:
                    for element2 in positionListOfTerm2:
                        if ( (element1-element2) >= -4) and ( (element1 - element2) <= 0):
                            score += 1
                if doc not in document_docScore:
                    document_docScore[doc] = score
                else:
                    document_docScore[doc] += score
    query_docNamedocScore[q] = document_docScore

#print(query_docNamedocScore)
for key,value in query_docNamedocScore.items():
    v = query_docNamedocScore[key]
    query_docNamedocScore_sorted = collections.OrderedDict(sorted(v.items(), key=lambda x: x[1], reverse=True)) #sort the inverted index
    query_docNamedocScore[key] = query_docNamedocScore_sorted

print(query_docNamedocScore)









'''    
f = open("Query_PositionInfo.txt",'w')
f.write(str(query_positionInfo))
f.close()

f = open("QueryTerm_DocList.txt", 'w')
f.write(str(queryTerm_docList))
f.close()
'''