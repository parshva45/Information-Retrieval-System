import pickle
import collections

with open("../../Encoded Data Structures (Stemmed)/Encoded-Stemmed_Inverted_List.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("../../Encoded Data Structures (Stemmed)/Encoded-Stemmed_DocumentID_DocLen.txt", 'rb') as f:
    docID_documentLen = pickle.loads(f.read())

query_dict = {}

stemmed_queries = []        #Conatins all the queries required
with open('../cacm_stem.query.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
stemmed_queries.extend(l)

#idf = log(N/df)

final_score = {}     # dictionary of docID, bm25-score
corpus_len = sum(docID_documentLen.values())  #gives |C|
i = 1                #counter for counting query ids


def ql(tf,D,lamb,C):
    a = (1 - lamb) * (tf/D)
    b = lamb * (tf/C)
    score = a+b

    return score


def calc_score(q):
    final_score = {}
    terms = q.split()
    for term in terms:
        if term in inverted_index:
            for doc in inverted_index[term]:
                if doc[0] not in final_score.keys():
                    final_score[doc[0]] = ql(doc[1],docID_documentLen[doc[0]],0.35,corpus_len)
                else:
                    final_score[doc[0]] += ql(doc[1],docID_documentLen[doc[0]],0.35,corpus_len)

    return final_score


f1 = open('Stemmed_QLM_Top100_Pages.txt', 'w')
for query in stemmed_queries:
    c = 1                          # the variable c denotes rank
    ql_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(ql_score.items(), key = lambda s : s[1], reverse = True))
    f1.write('\nFor query : %s\n\n' % query)
    for id in final_score1:
        if c <= 100:
            f1.write('%d Q0 %s %d %s QueryLikelihoodModelStemNoStop\n' %(i,id,c,final_score1[id]))             #format-> query_id Q0 doc_id rank BM25_score system_name
        c += 1
    i += 1
f.close()

