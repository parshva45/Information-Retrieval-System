import collections
import os
import pickle

d1 = {}                                              # dictionary to store term, term frequency
doc_name = []                                        # list to store all the document names obtained
docID_documentLen = {}                               # dictionary to store the document length of a particular document
docID_docName = {}

encoded_dir = r'../Encoded Data Structures (Stopped)/'
if not os.path.exists(encoded_dir):
    os.makedirs(encoded_dir)


def inverted_index(filename):                                     # Function to generate inverted index
    inv_index_unigram = {}
    current_file = os.path.join(path, filename)
    terms = open(current_file, 'r').read()
    term_list = terms.split()
    docID_documentLen[file[:-4]] = len(term_list)
    for term in term_list:
        if terms.count(term) == 0:
            continue
        else:
            d1[term] = terms.count(term)
        tup = file[:-4], d1[term]
        inv_index_unigram[term] = tup
    return inv_index_unigram


parent_inverted_list = {}
path = r'../Step 1/Stopped Tokenizer Output'
for file in os.listdir(path):
    child_inverted_list = inverted_index(file)
    for term in child_inverted_list:

        if term in parent_inverted_list:

            parent_inverted_list[term].append(child_inverted_list[term])        # append the (docID,tf) for the term if the same term appears in another document

        else:

            parent_inverted_list[term] = [child_inverted_list[term]]

inv_list_unigram = collections.OrderedDict(sorted(parent_inverted_list.items()))      #sort the inverted index

output = open('Stopped_Inverted_List.txt', 'w+', encoding='utf-8')
for term in inv_list_unigram:
    output.write("%s -> %s\n" % (term, inv_list_unigram[term]))
output.close()

f = open("Stopped_DocumentID_DocLen.txt", 'w', encoding='utf-8')
f.write(str(docID_documentLen))
f.close()

output = open(encoded_dir + 'Encoded-Stopped_Inverted_List.txt', 'wb')
pickle.dump(inv_list_unigram, output)
output.close()

output = open(encoded_dir + 'Encoded-Stopped_DocumentID_DocLen.txt', 'wb')
pickle.dump(docID_documentLen, output)
output.close()

