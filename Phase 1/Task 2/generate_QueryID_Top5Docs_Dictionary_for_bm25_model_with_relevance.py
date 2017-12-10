import pickle
import os
from collections import OrderedDict

path = r'../Task 1/Encoded Data Structures/Encoded-BM25-Relevance-Top5Docs-perQuery/'
queryID_top5Docs = {}
for file in os.listdir(path):
    doc_bm25_withRelevanceScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Encoded-Top5Docs-BM25-Relevance_")
    id = string[1].split('.')[0]
    with open(current_file, 'rb') as f:
        doc_bm25_withRelevanceScore = pickle.loads(f.read())
    all_docs = list(doc_bm25_withRelevanceScore.keys())
    top_5_docs = all_docs[:5]
    queryID_top5Docs[id] = top_5_docs

queryID_top5Docs_sorted = OrderedDict(sorted(queryID_top5Docs.items(), key=lambda x: x,reverse=False))

print(queryID_top5Docs_sorted)
output = open('Encoded-QueryID_Top5Docs_BM25_Relevance.txt', 'wb')
pickle.dump(queryID_top5Docs_sorted , output)
output.close()
