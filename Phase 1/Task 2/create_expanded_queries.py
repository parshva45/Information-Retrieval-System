import pickle

with open("Queries_with_their_expansion_terms_encoded.txt", 'rb') as f:
    query_expansionterms = pickle.loads(f.read())

query = list(query_expansionterms.keys())  #contains all the unexpanded, depunctuated queries
query_terms = []                           #contains the terms of the query
for q in query:
    query_terms.append(q.split())

expansion_terms = list(query_expansionterms.values())  #contains the terms needed for query expansion

answer = []                                #contains all the terms in the expanded query, joining these terms
                                           #will give us the final resulted expanded query
i = 0
while(i<len(query_terms)):
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

final_query = {}   #dictionary having query id as key and expanded query as it's corresponding value

for i,list in enumerate(answer,1):
    expanded_query = ' '.join(list)
    final_query[i] = expanded_query

print(final_query)

output = open('Resulting_Expanded_Queries_encoded.txt','wb')
pickle.dump(final_query, output)
output.close()