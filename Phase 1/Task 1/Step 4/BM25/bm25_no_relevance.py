import pickle
import math
import collections
import os

# This script implements the BM25 model for ranking the documents for every query
# and retrieving the top 100 documents from the ranked documents

# Access Encoded Data Structures

# load the dictionary while contains all inverted list of the corpus
with open("../../Encoded Data Structures/Encoded-Inverted_List.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

# load the dictionary which contains the docID and documentLen for all the
# document in the
with open("../../Encoded Data Structures/Encoded-DocumentID_DocLen.txt", 'rb') as f:
    docID_documentLen = pickle.loads(f.read())

# load the cleaned queries dictionary to calculate document scores for each of these queries
with open("../../Encoded Data Structures/Encoded-Cleaned_Queries.txt", 'rb') as f:
    query_dict = pickle.loads(f.read())

query_list = list(query_dict.values())    # Contains all the queries required

# BM25 FORMULA :
# ((k2 + 1)q)/((k2 + q)) * ((k1 + 1)f)/((K + f)) * log((r + 0.5)(N − n − R + r + 0.5))/((n − r + 0.5)(R − r + 0.5))
# where: K = k1(bL + (1 − b))

# f = term frequency in that document
# n = total number of documents in which the term appears,i.e., len(docIds)
# L = doc length / avg doc length

final_score = {}     # dictionary of docID, bm25-score

# gives the average document length for the given corpus
avg_doc_len = sum(docID_documentLen.values()) / len(docID_documentLen.keys())

i = 1                # counter for counting query ids
top_5 = {}           # dictionary which wil store information of top 5 pages by BM25 score


# this function implements the above mathematical formula to calculate a return score
# based on the given arguments
def bm25(f, n, L, R, r, q):

    k1 = 1.2
    k2 = 100
    b = 0.75
    N = len(docID_documentLen.keys())   # 3204 documents
    # q = 1

    K = k1 * ((b * L) + (1 - b))
    a = (k2 + 1) * q / (k2 + q)
    b = (k1 + 1) * f / (K + f)
    c = (r + 0.5) * (N - n - R + r + 0.5)
    d = (n - r + 0.5) * (R - r + 0.5)
    score = a * b * math.log(c / d)

    return score


def calc_score(q):
    final_score = {}
    terms = q.split()
    for term in terms:
        if term in inverted_index:
            qf = terms.count(term)  # count the occurrences of query term in the query
            for doc in inverted_index[term]:
                if doc[0] not in final_score.keys():
                    final_score[doc[0]] = bm25(doc[1], len(inverted_index[term]), (docID_documentLen[doc[0]] / avg_doc_len), 0, 0, qf)
                else:
                    final_score[doc[0]] += bm25(doc[1], len(inverted_index[term]), (docID_documentLen[doc[0]] / avg_doc_len), 0, 0, qf)

    return final_score


f = open('BM25_NonRelevance_Top100_Pages.txt', 'w')

f.write('Ranking (Top 100) for the queries in Cleaned_Queries.txt in the format:' + "\n")
f.write('query_id Q0 doc_id rank BM25_NoRelevance_score system_name' + "\n\n")

for query in query_dict.values():
    c = 1                                      # the variable c denotes rank
    print("Calculating BM25 Score with no relevance for query: " + query)
    bm25_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(bm25_score.items(), key=lambda s: s[1], reverse=True))
    f.write('\nFor query : %s\n\n' % query)
    for quid in final_score1:
        if c < 100:
            # format-> query_id Q0 doc_id rank BM25_score system_name
            f.write('%d Q0 %s %d %s BM25_model_NoRelevance\n' % (i, quid, c, final_score1[quid]))
        if c <= 5:
            if query not in top_5.keys():
                top_5[query] = [quid]
            else:
                top_5[query].append(quid)
        c += 1
    newpath = r'../../Encoded Data Structures/Encoded-BM25-NoRelevance-Top100Docs-perQuery/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    output = open(
        newpath + 'Encoded-Top100Docs-BM25-NoRelevance' + '_%d' % i + '.txt', 'wb')
    pickle.dump(final_score1, output)
    output.close()
    i += 1
f.close()

top_5_docs = list(top_5.values())
list_output = open('BM25_NoRelevance_Top5_Docs.txt', 'w')
for doc in top_5_docs:
    for i in doc:
        list_output.write(i + "\n")
list_output.close()

print("\n\nBM25 Scoring with No Relevance Process DONE")
output = open('BM25_NoRelevance_Top5_Query_Pages.txt', 'w')
output.write(str(top_5))
output.close()
encoded_output = open('../../Encoded Data Structures/Encoded-BM25_NoRelevance_Top5_Query_Pages.txt', 'wb')
pickle.dump(top_5, encoded_output)
encoded_output.close()