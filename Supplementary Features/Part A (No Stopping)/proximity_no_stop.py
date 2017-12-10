import pickle
import collections
import os

newpath = '../Encoded Data Structures (Bonus)/Encoded-Top100-Docs-Proximity-NoStopping/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

with open("../Encoded Data Structures (Bonus)/Encoded-Inverted_List_Position_No_Stopping.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("../../Phase 1/Task 1/Encoded Data Structures/Encoded-DocumentID_DocLen.txt", 'rb') as f:
    all_docs = pickle.loads(f.read()).keys()

with open("../../Phase 1/Task 1/Encoded Data Structures/Encoded-Cleaned_Queries.txt", 'rb') as f:
    query_dict = pickle.loads(f.read())

queryTerm_Position = {}
queryTerm_docList = {}
query_positionInfo = {}
i = 1


def generate_ngrams(words_list, n):                           #Function to generate n-grams
    ngrams_list = []

    for num in range(0, len(words_list)):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)

    return ngrams_list


query_docNamedocScore = {}


def calc_score(query):
    document_docScore = {}
    query_terms = query.split()
    bigrams = generate_ngrams(query_terms,2)
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
            common_docs = [val for val in queryTerm_docList[terms_under_consideration[0]] if val in queryTerm_docList[terms_under_consideration[1]]]
            for doc in common_docs:
                positionListOfTerm1 = []
                positionListOfTerm2 = []
                value_part_of_term_1 = inverted_index[terms_under_consideration[0]]
                value_part_of_term_2 = inverted_index[terms_under_consideration[1]]
                for i in range(0,len(value_part_of_term_1)):
                    if value_part_of_term_1[i][0] == doc:
                        positionListOfTerm1 = value_part_of_term_1[i][1]
                for i in range(0,len(value_part_of_term_2)):
                    if value_part_of_term_2[i][0] == doc:
                        positionListOfTerm2 = value_part_of_term_2[i][1]
                score = 0
                for element1 in positionListOfTerm1:
                    for element2 in positionListOfTerm2:
                        if ((element1-element2) >= -4) and ((element1 - element2) <= 0):
                            score += 1
                if doc not in document_docScore:
                    document_docScore[doc] = score
                else:
                    document_docScore[doc] += score
    return document_docScore


f = open('Proximity_NoStopping_Top100_Pages.txt', 'w')
for query in query_dict.values():
    c = 1                          # the variable c denotes rank
    proximity_score = calc_score(query)
    for doc in all_docs:
        if doc not in proximity_score:
            proximity_score[doc] = 0
    final_score1 = collections.OrderedDict(sorted(proximity_score.items(), key=lambda s: s[1], reverse=True))
    f.write('\nFor query : %s\n\n' %query)
    for id in final_score1:
        if c <= 100:
            f.write('%d Q0 %s %d %s ProximityNoStopNoStem\n' %(i,id,c,final_score1[id]))             #format-> query_id Q0 doc_id rank BM25_score system_name
            c += 1
    output = open(newpath + 'Encoded-Top100Docs-Proximity-NoStopping' + '_%d' %i + '.txt', 'wb')
    pickle.dump(final_score1, output)
    output.close()
    i += 1
f.close()