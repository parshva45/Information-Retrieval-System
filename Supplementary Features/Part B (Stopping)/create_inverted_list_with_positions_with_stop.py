import pickle
import collections
import os

common_words = []
with open('../../Phase 1/Task 3/Part A/common_words.txt', 'r') as f:
    line = f.readlines()
line = [x.strip() for x in line]
common_words.extend(line)

d1 = {}                                                      #dictionary to store term, term frequency
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
    d1 = {}
    inv_index_unigram = {}
    current_file = os.path.join(path,file)
    terms = open(current_file,'r').read()
    term_list = terms.split()
    for i, term in enumerate(term_list,1):
        if term not in common_words:
            if term in d1:
                d1[term].append(i)
            else:
                d1[term] = []
                d1[term].append(i)
            tuple = file[:-4],d1[term]
            inv_index_unigram[term] = tuple
    return inv_index_unigram

parent_inverted_list = {}
path = r'../../Phase 1/Task 3/Part A/Step 1/Stopped Tokenizer Output'
for file in os.listdir(path):
    child_inverted_list = inverted_index(file)
    for term in child_inverted_list:

        if term in parent_inverted_list:

            parent_inverted_list[term].append(child_inverted_list[term])              #append the (docID,tf) for the term if the same term appears in another document

        else:

            parent_inverted_list[term] = [child_inverted_list[term]]

inv_list_unigram = collections.OrderedDict(sorted(parent_inverted_list.items()))      #sort the inverted index

output = open('Inverted_List_With_Positions_With_Stopping.txt', 'w+', encoding='utf-8')
for term in inv_list_unigram:
    output.write("%s -> %s\n" %(term, inv_list_unigram[term]))
output.close()

newpath = r'../Encoded Data Structures (Bonus)/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

output = open(newpath + 'Encoded-Inverted_List_Position_With_Stopping.txt', 'wb')
pickle.dump(inv_list_unigram , output)
output.close()