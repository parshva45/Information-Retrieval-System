import pickle
import os
from collections import OrderedDict

path = r'C:\Users\virat\PycharmProjects\Project\Top_100_docs_using_tf-idf_normalized_encoded'
queryID_top100Docs = {}
for file in os.listdir(path):
    doc_tf_idfScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Top_100_documents_using_tf-idf_normalized_model_for_query_")
    id = string[1].split("_")[0]
    with open(current_file, 'rb') as f:
        doc_tf_idfScore = pickle.loads(f.read())
    all_docs = list(doc_tf_idfScore.keys())
    top_100_docs = all_docs[:100]
    queryID_top100Docs[id] = top_100_docs

queryID_top100Docs_sorted = OrderedDict(sorted(queryID_top100Docs.items(), key=lambda x: x,reverse=False))

print(queryID_top100Docs_sorted)
output = open('QueryID_Top100Docs_by_TF-IDF_Normalized_encoded.txt' , 'wb')
pickle.dump(queryID_top100Docs_sorted , output)
output.close()
