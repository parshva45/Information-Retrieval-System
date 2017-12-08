import pickle
import math
import collections
import os

# Access Encoded Data Structures
with open("../../Encoded Data Structures (Stopped)/Encoded-Stopped_Inverted_List.txt", 'rb') as f:
    inverted_index = pickle.loads(f.read())

with open("../../Encoded Data Structures (Stopped)/Encoded-Stopped_DocumentID_DocLen.txt", 'rb') as f:
    docID_documentLen = pickle.loads(f.read())

with open("../../Encoded Data Structures (Stopped)/Encoded-Cleaned_Queries_Stopped.txt", 'rb') as f:
    query_dict = pickle.loads(f.read())

query_list = list(query_dict.values())    #Contains all the queries required

#idf = log(N/df)

final_score = {}     # dictionary of docID, bm25-score
i = 1                #counter for counting query ids
top_5 = {}


def tf_idf(tf, df, D):

    N = len(docID_documentLen.keys())
    idf = math.log(N/df+1)
    normalized_tf = tf/D
    score = normalized_tf * idf

    return score


def calc_score(q):
    final_score = {}
    terms = q.split()
    for term in terms:
        if term in inverted_index:
            for doc in inverted_index[term]:
                if doc[0] not in final_score.keys():
                    final_score[doc[0]] = tf_idf(doc[1],len(inverted_index[term]), docID_documentLen[doc[0]])
                else:
                    final_score[doc[0]] += tf_idf(doc[1],len(inverted_index[term]), docID_documentLen[doc[0]])

    return final_score


f = open('Stopped_TF_IDF_Normalized_Top100_Pages.txt', 'w')
for query in query_list:
    c = 1                          # the variable c denotes rank
    print("Calculating TF-IDF Score with Stopping for query: " + query)
    tf_idf_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(tf_idf_score.items(), key=lambda s: s[1], reverse=True))
    f.write('\nFor query : %s\n\n' %query)
    for quid in final_score1:
        if c < 100:
            f.write('%d Q0 %s %d %s tf_idf_model_StopNoStem\n' % (i, quid, c, final_score1[quid]))           # format-> query_id Q0 doc_id rank BM25_score system_name
        if c <= 5:
            if query not in top_5.keys():
                top_5[query] = [quid]
            else:
                top_5[query].append(quid)
        c += 1
    newpath = r'../../Encoded Data Structures (Stopped)/Encoded-Stopped_TF-IDF-Normalized-Top100Docs-perQuery/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    output = open(
        newpath + 'Encoded-Top100Docs-Stopped_TF-IDF-Normalized' + '_%d' % i + '.txt', 'wb')
    pickle.dump(final_score1, output)
    output.close()
    i += 1
f.close()

top_5_docs = list(top_5.values())
list_output = open('Stopped_TF_IDF_Normalized_Top5_Docs.txt', 'w')
for doc in top_5_docs:
    for i in doc:
        list_output.write(i + "\n")
list_output.close()

print("\n\nTF-IDF Scoring with Stopping Process DONE")
output = open('Stopped_TF_IDF_Normalized_Top5_Query_Pages.txt', 'w')
output.write(str(top_5))
output.close()
encoded_output = open('../../Encoded Data Structures (Stopped)/Encoded-Stopped_TF_IDF_Normalized_Top5_Query_Pages.txt', 'wb')
pickle.dump(top_5, encoded_output)
encoded_output.close()