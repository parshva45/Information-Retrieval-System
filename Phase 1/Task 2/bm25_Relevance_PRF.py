import pickle
import math
import collections
import os

with open("../Task 1/Encoded Data Structures/Encoded-Inverted_List.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("../Task 1/Encoded Data Structures/Encoded-DocumentID_DocLen.txt", 'rb') as f:
    docID_doclen = pickle.loads(f.read())

with open("Encoded-Expanded_Queries.txt", 'rb') as f:
    query_dict = pickle.loads(f.read())

with open("../Task 1/Encoded Data Structures/Encoded-QueryID_RelevantDocs.txt", 'rb') as f:
    queryID_relevantDocs = pickle.loads(f.read())

queryID_noofrelevantdocs = {}
for string in queryID_relevantDocs:
    queryID_noofrelevantdocs[string] = len(queryID_relevantDocs[string])

#print(queryID_relevantDocs)
#print(queryID_noofrelevantdocs)

query_list = list(query_dict.values())    #Conatins all the queries required

#BM25 FORMULA : ((k2 + 1)q)/((k2 + q)) * ((k1 + 1)f)/((K + f)) * log((r + 0.5)(N − n − R + r + 0.5))/((n − r + 0.5)(R − r + 0.5))
#where: K = k1(bL + (1 − b))

#f = term frequency in that document
#n = total number of documents in which the term appears,i.e., len(docIds)
#L = doc length / avg doc length

final_score = {}     # dictionary of docID, bm25-score
avg_doc_len = sum(docID_doclen.values()) / len(docID_doclen.keys())  #gives the average document length for the given corpus
i = 1                #counter for counting query ids

def bm25(f, n, L, R, r):

    k1 = 1.2
    k2 = 100
    b = 0.75
    N = len(docID_doclen.keys())
    q = 1

    K = k1 * ((b * L) + (1 - b))
    a = (k2 + 1) * q / (k2 + q)
    b = (k1 + 1) * f / (K + f)
    c = (r + 0.5) * (N - n - R + r + 0.5)
    d = (n - r + 0.5) * (R - r + 0.5)

    score = a * b * math.log(c/d)

    return score


def compute_r(term,id):
    r = 0

    relevant_doc_list = queryID_relevantDocs[str(id)]
    for doc in relevant_doc_list:
        f = open('../Task 1/Step 1/Tokenizer Output/' + doc + '.txt', 'r')
        file_content = f.read()
        file_content_terms = file_content.split()
        if term in file_content_terms:
            r += 1
    return r


def calc_score(q,R,id):
    final_score = {}
    terms = q.split()
    if str(id) in queryID_relevantDocs.keys():
        for term in terms:
            if term in inverted_index:
                r = compute_r(term,id)

                for doc in inverted_index[term]:
                    if doc[0] not in final_score.keys():
                        final_score[doc[0]] = bm25(doc[1], len(inverted_index[term]) , (docID_doclen[doc[0]] / avg_doc_len), R, r)
                    else:
                        final_score[doc[0]] += bm25(doc[1], len(inverted_index[term]) , (docID_doclen[doc[0]] / avg_doc_len), R, r)

    return final_score

f = open('BM25_Relevance_PRF_Top100_Pages.txt', 'w')
for qID in query_dict:
    c = 1                          # the variable c denotes rank
    # if qID in queryID_relevantDocs.keys():
    #     try:
    #         R = queryID_noofrelevantdocs[qID]
    #     except ValueError:
    #         R = 0
    R = queryID_noofrelevantdocs[qID]
    bm25_score = calc_score(query_dict[qID],R,qID)
    final_score1 = collections.OrderedDict(sorted(bm25_score.items(), key = lambda s : s[1], reverse = True))
    f.write('\nFor query : %s\n\n' %query_dict[qID])
    for id in final_score1:
        if (c < 100):
            f.write('%d Q0 %s %d %s BM25_model\n' %(int(qID),id,c,final_score1[id]))             #format-> query_id Q0 doc_id rank BM25_score system_name
            c += 1
    newpath = r'Encoded Data Structures (PRF)/Encoded-BM25-Relevance-PRF-Top100Docs-perQuery/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    #if qID in queryID_relevantDocs.keys():
    output = open(newpath + 'Encoded-Top100Docs-BM25-Relevance-PRF' + '_%d' %int(qID) + '.txt', 'wb')
    pickle.dump(final_score1, output)
    output.close()
    #i += 1
f.close()
