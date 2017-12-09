import pickle
import math
import collections

with open("../../Encoded Data Structures (Stemmed)/Encoded-Stemmed_Inverted_List.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("../../Encoded Data Structures (Stemmed)/Encoded-Stemmed_DocumentID_DocLen.txt", 'rb') as f:
    docID_documentLen = pickle.loads(f.read())

stemmed_queries = []        # Contains all the queries required
with open('../cacm_stem.query.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
stemmed_queries.extend(l)

#BM25 FORMULA : ((k2 + 1)q)/((k2 + q)) * ((k1 + 1)f)/((K + f)) * log((r + 0.5)(N − n − R + r + 0.5))/((n − r + 0.5)(R − r + 0.5))
#where: K = k1(bL + (1 − b))

#f = term frequency in that document
#n = total number of documents in which the term appears,i.e., len(docIds)
#L = doc length / avg doc length

final_score = {}     # dictionary of docID, bm25-score
avg_doc_len = sum(docID_documentLen.values()) / len(docID_documentLen.keys())  # gives the average document length for the given corpus
i = 1                # counter for counting query ids


def bm25(f, n, L, R, r):

    k1 = 1.2
    k2 = 100
    b = 0.75
    N = len(docID_documentLen.keys())   # 3204
    q = 1

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
            for doc in inverted_index[term]:
                if doc[0] not in final_score.keys():
                    final_score[doc[0]] = bm25(doc[1], len(inverted_index[term]) , (docID_documentLen[doc[0]] / avg_doc_len), 0, 0)
                else:
                    final_score[doc[0]] += bm25(doc[1], len(inverted_index[term]) , (docID_documentLen[doc[0]] / avg_doc_len), 0, 0)

    return final_score


f = open('Stemmed_BM25_NoRelevance_Top100_Pages.txt', 'w')
for query in stemmed_queries:
    c = 1                          # the variable c denotes rank
    print("Calculating BM25 Score with Stemming for query: " + query)
    bm25_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(bm25_score.items(), key=lambda s : s[1], reverse=True))
    f.write('\nFor query : %s\n\n' % query)
    for id in final_score1:
        if c < 100:
            # format-> query_id Q0 doc_id rank BM25_score system_name
            f.write('%d Q0 %s %d %s BM25ModelStemNoStop\n' %(i,id,c,final_score1[id]))
            c += 1
    i += 1
f.close()
