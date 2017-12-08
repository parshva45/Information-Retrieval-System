import pickle
import collections

with open("../Task 1/Encoded Data Structures/Encoded-Cleaned_Queries.txt", 'rb') as f:
    qID_query = pickle.loads(f.read())

d1 = {}                                                      # dictionary to store term, term frequency
docID = 0                                                    # gives the document ID for a particular document
doc_name = []                                                # list to store all the document names obtained
docID_documentLen = {}                                       # dictionary storing the document length of a particular document

common_words = []
with open('common_words.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
common_words.extend(l)

docs = []
with open('../Task 1/Step 4/QLM/QLM_Top5_Docs.txt', 'r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
docs.extend(l)

alltop5words = []
for doc in docs:
    top5words = []
    filename = '../Task 1/Step 1/Tokenizer Output/' + doc + '.txt'
    doc_terms = []
    f = open(filename , 'r').read()
    content = f.split(" ")
    term_tf = {}
    for term in content:
        if term not in common_words:
            if term in term_tf:
                term_tf[term] += 1
            else:
                term_tf[term] = 1
    term_tf = collections.OrderedDict(sorted(term_tf.items(), key=lambda x: x[1], reverse=True))
    c = 0
    for term in term_tf:
        if c < 5:
            top5words.append(term)
        c += 1
    alltop5words.append(top5words)

final_top5words_array = []

i = 0
while i < len(alltop5words):

   merged_array = alltop5words[i] + alltop5words[i+1] + alltop5words[i+2] + alltop5words[i+3] + alltop5words[i+4]
   final_top5words_array.append(merged_array)
   i += 5

query_name = list(qID_query.values())

query_expansionterms = dict(zip(query_name,final_top5words_array))

print(query_expansionterms)

output = open('Queries_with_their_expansion_terms.txt','wb')
pickle.dump(query_expansionterms, output)
output.close()
