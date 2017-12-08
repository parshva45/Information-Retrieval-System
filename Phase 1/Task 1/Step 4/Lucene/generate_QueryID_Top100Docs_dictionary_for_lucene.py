import pickle

queryID_Top100Docs = {}
queryID_Top5Docs = {}
top_100_docs = []
with open("Top_100_docNames_for_queries_using_lucene_model.txt", 'r', encoding='utf-8') as f:
   l = f.readlines()
l = [x.strip() for x in l]
top_100_docs.extend(l)

i = 1
c = 0
for doc in top_100_docs:
    if c < 100:
        if i not in queryID_Top100Docs:
            queryID_Top100Docs[i] = []
            queryID_Top5Docs[i] = []
        queryID_Top100Docs[i].append(doc)
        if c < 5:
            queryID_Top5Docs[i].append(doc)
        c += 1
        continue
    i += 1
    queryID_Top100Docs[i] = []
    queryID_Top100Docs[i].append(doc)
    queryID_Top5Docs[i] = []
    queryID_Top5Docs[i].append(doc)
    c = 1

output = open('QueryID_Top100Docs_by_lucene_encoded.txt', 'wb')
pickle.dump(queryID_Top100Docs, output)
output.close()

top_5_docs = list(queryID_Top5Docs.values())
list_output = open('Lucene_Top5_Docs.txt', 'w')
for doc in top_5_docs:
    for i in doc:
        list_output.write(i + "\n")
list_output.close()

output = open('QueryID_Top5Docs_by_lucene_encoded.txt', 'wb')
pickle.dump(queryID_Top5Docs, output)
output.close()
