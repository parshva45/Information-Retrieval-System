import pickle
import os
from collections import OrderedDict

newpath = r'../../Encoded Data Structures (Phase 3)/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

path = r'../../../Phase 1/Task 1/Encoded Data Structures/Encoded-TF-IDF-Normalized-Top100Docs-perQuery'
queryID_top100Docs = {}
for file in os.listdir(path):
    doc_tf_idfScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Encoded-Top100Docs-TF-IDF-Normalized_")
    id = string[1].split(".")[0]
    with open(current_file, 'rb') as f:
        doc_tf_idfScore = pickle.loads(f.read())
    all_docs = list(doc_tf_idfScore.keys())
    top_100_docs = all_docs[:100]
    queryID_top100Docs[id] = top_100_docs

queryID_top100Docs_sorted = OrderedDict(sorted(queryID_top100Docs.items(), key=lambda x: x,reverse=False))

output = open(newpath + 'Encoded-QueryID_Top100Docs_tf-idf_normalized.txt', 'wb')
pickle.dump(queryID_top100Docs_sorted , output)
output.close()
