import pickle

queryID_Top100Docs = {}
top_100_docs = []
with open("Top_100_docNames_for_queries_using_lucene_SA_model.txt", 'r', encoding = 'utf-8') as f:
   l = f.readlines()
l = [x.strip() for x in l]
top_100_docs.extend(l)

print(len(top_100_docs))

i = 1
c = 0
for doc in top_100_docs:
    if(c < 100):
        if i not in queryID_Top100Docs:
            queryID_Top100Docs[i] = []
        queryID_Top100Docs[i].append(doc)
        c += 1
        continue
    i += 1
    queryID_Top100Docs[i] = []
    queryID_Top100Docs[i].append(doc)
    c = 1

print(queryID_Top100Docs)

for id in queryID_Top100Docs:
    print(queryID_Top100Docs[id])
    print(len(queryID_Top100Docs[id]))
    print("---------------------------")

print(queryID_Top100Docs)

output = open('QueryID_Top100Docs_by_lucene_SA_encoded.txt' , 'wb')
pickle.dump(queryID_Top100Docs , output)
output.close()
