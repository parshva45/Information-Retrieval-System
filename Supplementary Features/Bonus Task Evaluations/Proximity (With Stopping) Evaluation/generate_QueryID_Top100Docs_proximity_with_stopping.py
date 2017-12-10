import pickle
import os
from collections import OrderedDict

path = r'../../Encoded Data Structures (Bonus)/Encoded-Top100-Docs-Proximity-Stopping'
queryID_top100Docs = {}
for file in os.listdir(path):
    doc_pScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Encoded-Top100Docs-Proximity-Stopping_")
    id = string[1].split(".")[0]
    with open(current_file, 'rb') as f:
        doc_pScore = pickle.loads(f.read())
    all_docs = list(doc_pScore.keys())
    top_100_docs = all_docs[:100]
    queryID_top100Docs[id] = top_100_docs

queryID_top100Docs_sorted = OrderedDict(sorted(queryID_top100Docs.items(), key=lambda x: x,reverse=False))


output = open('../../Encoded Data Structures (Bonus)/Encoded-QueryID_Top100Docs_Proximity_with_stopping.txt', 'wb')
pickle.dump(queryID_top100Docs_sorted , output)
output.close()
