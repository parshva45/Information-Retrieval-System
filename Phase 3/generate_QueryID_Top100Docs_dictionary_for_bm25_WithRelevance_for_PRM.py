import pickle
import os
from collections import OrderedDict

path = r'C:\Users\virat\PycharmProjects\Project\Top_100_docs_using_bm25_with_relevance_for_PRM_encoded'
queryID_top100Docs = {}
for file in os.listdir(path):
    doc_bm25_withRelevanceScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Top_100_documents_using_bm25_model_with_relevance_for_PRM_for_query_")
    id = string[1].split("_")[0]
    with open(current_file, 'rb') as f:
        doc_bm25_withRelevanceScore = pickle.loads(f.read())
    all_docs = list(doc_bm25_withRelevanceScore.keys())
    top_100_docs = all_docs[:100]
    queryID_top100Docs[id] = top_100_docs

queryID_top100Docs_sorted = OrderedDict(sorted(queryID_top100Docs.items(), key=lambda x: x,reverse=False))

print(queryID_top100Docs_sorted)
output = open('QueryID_Top100Docs_by_BM25_WithRelevance_for_PRM_encoded.txt' , 'wb')
pickle.dump(queryID_top100Docs_sorted , output)
output.close()
