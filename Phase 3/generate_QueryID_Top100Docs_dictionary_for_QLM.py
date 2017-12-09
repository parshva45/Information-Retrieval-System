import pickle
import os
from collections import OrderedDict

path = r'C:\Users\virat\PycharmProjects\Project\Top_100_docs_using_ql_encoded'
queryID_top100Docs = {}
for file in os.listdir(path):
    doc_qlmScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Top_100_documents_using_qlm_model_for_query_")
    id = string[1].split("_")[0]
    with open(current_file, 'rb') as f:
        doc_qlmScore = pickle.loads(f.read())
    all_docs = list(doc_qlmScore.keys())
    top_100_docs = all_docs[:100]
    queryID_top100Docs[id] = top_100_docs

queryID_top100Docs_sorted = OrderedDict(sorted(queryID_top100Docs.items(), key=lambda x: x,reverse=False))

print(queryID_top100Docs_sorted)
output = open('QueryID_Top100Docs_by_QLM_encoded.txt' , 'wb')
pickle.dump(queryID_top100Docs_sorted , output)
output.close()
