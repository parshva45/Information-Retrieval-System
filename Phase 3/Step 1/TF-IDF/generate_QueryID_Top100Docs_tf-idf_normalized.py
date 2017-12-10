# This code generates a dictionary with the query id as it's key and it's top 100 documents
# generated by tf-idf model, as it's corresponding value

import pickle
import os

# make the directory if it doesn't exist already
newpath = r'../../Encoded Data Structures (Phase 3)/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

path = r'../../../Phase 1/Task 1/Encoded Data Structures/Encoded-TF-IDF-Normalized-Top100Docs-perQuery'
queryID_top100Docs = {}                          # dictionary to store query id as key and it's corresponding
                                                 # top 100 documents as it's value
for file in os.listdir(path):
    doc_tf_idfScore = {}
    current_file = os.path.join(path,file)
    string = current_file.split("Encoded-Top100Docs-TF-IDF-Normalized_")
    id = string[1].split(".")[0]                 # gives the query id, example: id =1, id = 2, etc.
    with open(current_file, 'rb') as f:
        doc_tf_idfScore = pickle.loads(f.read())
    all_docs = list(doc_tf_idfScore.keys())
    top_100_docs = all_docs[:100]                # gets the top 100 documents
    queryID_top100Docs[id] = top_100_docs

# write the dictionary to a file, in encoded format using pickle library of python
output = open(newpath + 'Encoded-QueryID_Top100Docs_tf-idf_normalized.txt', 'wb')
pickle.dump(queryID_top100Docs , output)
output.close()
