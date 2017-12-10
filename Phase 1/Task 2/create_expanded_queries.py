import pickle

with open("Encoded-Queries_With_Their_Expansion_Terms.txt", 'rb') as f:
    query_expansionterms = pickle.loads(f.read())

with open("../Task 1/Encoded Data Structures/Encoded-QueryID_RelevantDocs.txt", 'rb') as f:
    queryID_relevantDocs = pickle.loads(f.read())

query = list(query_expansionterms.keys())  #contains all the unexpanded, depunctuated queries
query_terms = []                           #contains the terms of the query
for q in query:
    query_terms.append(q.split())

expansion_terms = list(query_expansionterms.values())  #contains the terms needed for query expansion

answer = []                                #contains all the terms in the expanded query, joining these terms
                                           #will give us the final resulted expanded query
i = 0
while i<len(query_terms):
     # answer.append(list(set(query_terms[i] + expansion_terms[i])))

     c_answer = (query_terms[i] + expansion_terms[i])
     new_answer = []                      #contains all the terms for the query under consideration,
                                          # to be joined which would result in the final query

     # remove duplicate terms from the term list
     for x in c_answer:
         if x not in new_answer:
             new_answer.append(x)
     answer.append(new_answer)
     i += 1

print(answer)

final_query = {}   #dictionary having query id as key and expanded query as it's corresponding value
'''
for i, list in enumerate(answer,1):
    
    final_query[i] = expanded_query
'''
ids = list(queryID_relevantDocs.keys())

i = 0
for list in answer:
    expanded_query = ' '.join(list)
    final_query[ids[i]] = expanded_query
    i += 1

output = open('Encoded-Expanded_Queries.txt','wb')
pickle.dump(final_query, output)
output.close()
