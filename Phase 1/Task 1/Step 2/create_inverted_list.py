import collections
import os
import pickle

# This script is used to generate the inverted index of every term/word in the
# text obtained after tokenizing the raw HTML. The generated inverted index contains
# key as the term and value as tuple of documentID and term frequency

d1 = {}                                               # dictionary to store term, term frequency
doc_name = []                                         # list to store all the document names obtained

# dictionary with key as docID and value as corresponding document lengthdocID_documentLen = {}
docID_docName = {}

# create new directory for encoded output files that can be used later on
# to import data structures
encoded_dir = r'../Encoded Data Structures/'
if not os.path.exists(encoded_dir):
    os.makedirs(encoded_dir)

# dictionary that stores key as docID and value as corresponding document length
docID_documentLen = {}


# this function generates inverted index for each word in the tokenizer output text
def inverted_index(filename):
    inv_index_unigram = {}
    current_file = os.path.join(path, filename)
    terms = open(current_file,'r').read()
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
path = r'../Step 1/Tokenizer Output'
for file in os.listdir(path):
    child_inverted_list = inverted_index(file)
    print("Generating inverted list for: " + str(file))
    for term in child_inverted_list:
        if term in parent_inverted_list:
            # append the (docID,tf) for the term if the same term appears in another document
            parent_inverted_list[term].append(child_inverted_list[term])
        else:
            parent_inverted_list[term] = [child_inverted_list[term]]

inv_list_unigram = collections.OrderedDict(sorted(parent_inverted_list.items()))      # sort the inverted index


# write output file
output = open('Inverted_List.txt', 'w+', encoding='utf-8')
for term in inv_list_unigram:
    output.write("%s -> %s\n" %(term , inv_list_unigram[term]))
output.close()

f = open("DocumentID_DocLen.txt", 'w', encoding='utf-8')
f.write(str(docID_documentLen))
f.close()


# dump encoded files using pickle to be used later on as same data structure for
# any other file
output = open(encoded_dir + 'Encoded-Inverted_List.txt', 'wb')
pickle.dump(inv_list_unigram, output)
output.close()

output = open(encoded_dir + 'Encoded-DocumentID_DocLen.txt', 'wb')
pickle.dump(docID_documentLen, output)
output.close()

