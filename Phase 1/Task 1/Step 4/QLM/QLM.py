import pickle
import collections
import os

# This script implements the Query Likelihood Model for ranking the documents for every query
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

final_score = {}                                # dictionary of docID, bm25-score
corpus_len = sum(docID_documentLen.values())    # gives |C|
i = 1                                           # counter for counting query ids
top_5 = {}                                      # dictionary which wil store information of top 5 pages by BM25 score


# this function returns the ql score for the given parameters
def ql(tf, D, lamb, C):
    a = (1 - lamb) * (tf/D)
    b = lamb * (tf/C)
    score = a+b

    return score


# this function calculates the score and call the ql function
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


f = open('QLM_Top100_Pages.txt', 'w')

f.write('Ranking (Top 100) for the queries in Cleaned_Queries.txt in the format:' + "\n")
f.write('query_id Q0 doc_id rank QLM_score system_name' + "\n\n")

for query in query_list:
    c = 1                          # the variable c denotes rank
    print("Calculating QLM Score for query: " + query)
    ql_score = calc_score(query)
    final_score1 = collections.OrderedDict(sorted(ql_score.items(), key=lambda s: s[1], reverse=True))
    f.write('\nFor query : %s\n\n' %query)
    for quid in final_score1:
        if c <= 100:
            # format-> query_id Q0 doc_id rank BM25_score system_name
            f.write('%d Q0 %s %d %s Query_Likelihood_Model\n' % (i, quid, c, final_score1[quid]))

        if c <= 5:
            if query not in top_5.keys():
                top_5[query] = [quid]
            else:
                top_5[query].append(quid)
        c += 1
    newpath = r'../../Encoded Data Structures/Encoded-QLM-Top100Docs-perQuery/'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    output = open(
        newpath + 'Encoded-Top100Docs-QLM' + '_%d' % i + '.txt', 'wb')
    pickle.dump(final_score1, output)
    output.close()
    i += 1
f.close()

top_5_docs = list(top_5.values())
list_output = open('QLM_Top5_Docs.txt', 'w')
for doc in top_5_docs:
    for i in doc:
        list_output.write(i + "\n")
list_output.close()

print("\n\nQuery Likelihood Model Scoring Process DONE")

# write the dictionary containing the query as key and a list of top 5 relevant document by
# QLM scores as its corresponding values
output = open('QLM_Top5_Query_Pages.txt', 'w')
output.write(str(top_5))
output.close()
encoded_output = open('../../Encoded Data Structures/Encoded-QLM_Top5_Query_Pages.txt', 'wb')
pickle.dump(top_5, encoded_output)
encoded_output.close()

