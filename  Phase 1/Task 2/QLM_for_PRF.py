import pickle
import collections

with open("inverted_list_unigram_encoded.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("DocumentID-DocLen-encoded.txt", 'rb') as f:
    docID_doclen = pickle.loads(f.read())

with open("Resulting_expanded_queries_encoded.txt", 'rb') as f:
    query_dict = pickle.loads(f.read())

query_list = list(query_dict.values())    #Conatins all the queries required

# idf = log(N/df)

final_score = {}     # dictionary of docID, bm25-score
corpus_len = sum(docID_doclen.values())  #gives |C|
i = 1                #counter for counting query ids
top_5 = {}


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
                    final_score[doc[0]] = ql(doc[1],docID_doclen[doc[0]],0.35,corpus_len)
                else:
                    final_score[doc[0]] += ql(doc[1],docID_doclen[doc[0]],0.35,corpus_len)

    return final_score


f1=open('Top_100_pages_for_queries_using_ql_model_after_expansion.txt', 'w')
for query in query_list:
    c = 1                          # the variable c denotes rank
    ql_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(ql_score.items(), key = lambda s : s[1], reverse = True))
    f1.write('\nFor query : %s\n\n' %query)
    for id in final_score1:
        if (c <= 100):
            f1.write('%d Q0 %s %d %s Query_Likelihood_model_after_expansion\n' %(i,id,c,final_score1[id]))             #format-> query_id Q0 doc_id rank BM25_score system_name
        c += 1
    i += 1
f.close()