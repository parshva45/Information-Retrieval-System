import pickle
import collections
import os

d1 = {}                                                      #dictionary to store term, term frequency
#docID = 0                                                    #gives the document ID for a particular document
doc_name = []                                                #list to store all the document names obtained
docID_doclen = {}                                            #dictionary to store the document length of a particular document
docID_docName = {}

def generate_ngrams(words_list, n):                           #Function to generate n-grams
    ngrams_list = []

    for num in range(0, len(words_list)):
        ngram = ' '.join(words_list[num:num + n])
        ngrams_list.append(ngram)

    return ngrams_list


def inverted_index(file):                                     #Function to generate inverted index
    #c = 1
    d1 = {}
    inv_index_unigram = {}
    current_file = os.path.join(path,file)
    terms = open(current_file,'r').read()
    term_list = terms.split()
    #docID_doclen[file[:-4]] = len(term_list)
    for i, term in enumerate(term_list,1):
        if term in d1:
            d1[term].append(i)
        else:
            #position = []
            d1[term] = []
            d1[term].append(i)
        tuple = file[:-4],d1[term]
        inv_index_unigram[term] = tuple
        #c += 1
    return inv_index_unigram

parent_inverted_list = {}
path = r'../Phase 1/Task 1/Step 1/Tokenizer Output'
for file in os.listdir(path):
    child_inverted_list = inverted_index(file)
    for term in child_inverted_list:

        if term in parent_inverted_list:

            parent_inverted_list[term].append(child_inverted_list[term])              #append the (docID,tf) for the term if the same term appears in another document

        else:

            parent_inverted_list[term] = [child_inverted_list[term]]

inv_list_unigram = collections.OrderedDict(sorted(parent_inverted_list.items()))      #sort the inverted index

output = open('inverted_list_unigram_position.txt', 'w+', encoding = 'utf-8')
for term in inv_list_unigram:
    output.write("%s -> %s\n" %(term , inv_list_unigram[term]))
output.close()

output = open('inverted_list_unigram_position_encoded.txt' , 'wb')
pickle.dump(inv_list_unigram , output)
output.close()

#print(inv_list_unigram['for'])

for val in inv_list_unigram['and']:
    if val[0] == 'CACM-0405':
        print(val)

'''
f = open("DocumentID-DocLen.txt", 'w', encoding = 'utf-8')
f.write(str(docID_doclen))
f.close()

output = open('DocumentID-DocLen-encoded.txt' , 'wb')
pickle.dump(docID_doclen , output)
output.close()
'''
