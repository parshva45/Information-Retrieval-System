import pickle
import math
import collections

with open("inverted_list_unigram_Stemming_encoded.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("DocumentID_DocLen_Stemming_encoded.txt", 'rb') as f:
    docID_doclen = pickle.loads(f.read())

stemmed_queries = []        #Conatins all the queries required
with open('cacm_stem.query.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
stemmed_queries.extend(l)

#idf = log(N/df)

final_score = {}     # dictionary of docID, bm25-score
i = 1                #counter for counting query ids

def tf_idf(tf,df):

    N = 3204
    idf = math.log(N/df+1)
    score = tf * idf

    return score

def calc_score(q):
    final_score = {}
    terms = q.split()
    for term in terms:
        if term in inverted_index:
            for doc in inverted_index[term]:
                if doc[0] not in final_score.keys():
                    final_score[doc[0]] = tf_idf(doc[1],len(inverted_index[term]))
                else:
                    final_score[doc[0]] += tf_idf(doc[1],len(inverted_index[term]))

    return final_score

f=open('Top_100_pages_for_queries_using_tf_idf_model_Stemming.txt', 'w')
for query in stemmed_queries:
    c = 1                          #the variable c denotes rank
    tf_idf_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(tf_idf_score.items(), key = lambda s : s[1], reverse = True))
    f.write('\nFor query : %s\n\n' %query)
    for id in final_score1:
        if (c < 100):
            f.write('%d Q0 %s %d %s tfidf_StemNoStop\n' %(i,id,c,final_score1[id]))             #format-> query_id Q0 doc_id rank BM25_score system_name
            c += 1
    i += 1
f.close()
