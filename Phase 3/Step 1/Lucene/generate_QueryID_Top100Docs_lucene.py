import pickle
import os

newpath = r'../../Encoded Data Structures (Phase 3)/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

queryID_Top100Docs = {}
top_100_docs = []
with open("../../../Phase 1/Task 1/Step 4/Lucene/Lucene_Top100_Docs.txt", 'r', encoding='utf-8') as f:
   l = f.readlines()
l = [x.strip() for x in l]
top_100_docs.extend(l)

i = 1
c = 0
for doc in top_100_docs:
    if c < 100:
        if i not in queryID_Top100Docs:
            queryID_Top100Docs[i] = []
        queryID_Top100Docs[i].append(doc)
        c += 1
        continue
    i += 1
    queryID_Top100Docs[i] = []
    queryID_Top100Docs[i].append(doc)
    c = 1

output = open(newpath + 'Encoded-QueryID_Top100Docs_Lucene.txt', 'wb')
pickle.dump(queryID_Top100Docs , output)
output.close()
