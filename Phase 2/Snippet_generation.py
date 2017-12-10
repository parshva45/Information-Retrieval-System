import re
import os
from bs4 import BeautifulSoup
import pickle

# this variable stores length of document
doclen = 0

# dictionary which has key as docID and value as doc length
docID_doclen = {}

# dictionary which has key as docID and value as list of sentences
ID_CleanedSentence = {}

# list of all sentences
all_sentences = []

# dictionary with query as key and documents as value
dict_query_doc = {}

# dictionary with query as input and documentID, sentences as value
master_dict = {}

# stopped inverted list
ret_dict = {}

# list of words in the sentence
word_vectors = []


path1 = os.path.dirname(os.path.realpath(__file__)) + "/../Phase 1/Task 1/Encoded Data Structures/Encoded-Cleaned_Queries.txt"
path2 = os.path.dirname(os.path.realpath(__file__)) + "/../Raw HTML/"
path4 = os.path.dirname(os.path.realpath(__file__)) + "/../Phase 1/Task 3/Part A/Encoded Data Structures (Stopped)/Encoded-Stopped_Inverted_List.txt"

# list of common words
common_words = []
with open('common_words.txt','r') as f:
   l = f.readlines()
l = [x.strip() for x in l]
common_words.extend(l)

with open(path4, 'rb') as file:
    ret_dict = pickle.loads(file.read())

with open(path1, 'rb') as file:
    query_dict = pickle.loads(file.read())

# this function maps sentences with scores and sorts them in decreasing order of scores
def highestThree(sentence_list,score_list):
    highThree = sorted(zip(score_list, sentence_list), reverse=True)[:3]
    return highThree

# this function calculates significance factor for the sentence
def calc_significant_words(words, doc, num_of_sentences):
    global ret_dict
    global word_vectors
    if num_of_sentences < 25:
        threshold = 4 - 0.1 * (25 - num_of_sentences)
    elif num_of_sentences <= 40:
        threshold = 4
    else:
        threshold = 4 + 0.1 * (num_of_sentences - 40)
    word_vectors = []
    significant_words = []
    for word in words:
        if word.lower() not in common_words:
            val = ret_dict[word.lower()]
            for tup in val:
                if doc == tup[0]:
                    if tup[1] >= threshold:
                        word_vectors.append(1)
                        if word not in significant_words:
                            significant_words.append(word)
                    else:
                        word_vectors.append(0)
        else:
            word_vectors.append(0)
    if 1 in word_vectors:
        start = word_vectors.index(1)
        end = len(word_vectors) - word_vectors[::-1].index(1) - 1
        numberof1 = word_vectors.count(1)
        total_bracketed = end - start + 1
        significance_factor = (numberof1 ** 2)/total_bracketed
        return significance_factor
    else:
        return 0

# this function generates snippets for each of the models
def generate_snippet(filepath, writepath):
    global path2
    global path4
    global path1
    for file in os.listdir(path2):
        print("Generating Snippets for File: " + file)
        i = 1
        current_file = os.path.join(path2,file)
        page_content = open(current_file,'r').read()
        soup = BeautifulSoup(page_content,"html.parser")
        for req_content in soup.find_all("html"):
            req_content_text = req_content.text
            result_text = req_content_text.split('\n')
            for element in result_text:
                if element is "":
                    result_text.remove(element)

            result_text = '\n'.join(result_text)
            index_of_am = result_text.rfind("AM")                         # contains the last index of the term "AM"
            index_of_pm = result_text.rfind("PM")                         # contains the last index of the term "PM"

            # retain the text content uptil AM or PM in the corpus documents

            if index_of_am > index_of_pm:
                greater_index = index_of_am
            else:
                greater_index = index_of_pm
            result_text = result_text[:(greater_index+2)]

            # retain alpha-numeric text along with ',',':' and '.'
            result_text = re.sub(r"[^0-9A-Za-z,-\.:\\$]", " ", result_text)

            # retain '.', '-' or ',' between digits
            result_text = re.sub(r"(?!\d)[$,%,:.,-](?!\d)"," ", result_text, 0)

            result_text = re.sub(r' +', ' ', result_text).strip()             # remove spaces

            list_of_words = result_text.split()
            i = 0
            j = 0
            each = []
            for element in list_of_words:
                if i == 0:
                    each.append([])
                    each[j].append(element)
                    i += 1
                elif i < 10:
                    each[j].append(element)
                    i += 1
                else:
                    j += 1
                    each.append([])
                    each[j].append(element)
                    i = 1

            sentences = []
            for e in each:
                s = ""
                for element in e:
                    s += " " + str(element)
                sentences.append(s.strip())
            ID_CleanedSentence[file[:-5]] = sentences

    with open(filepath, 'r') as file:
        ret = file.read().split()

    for k, v in ID_CleanedSentence.items():
        for sentence in v:
            all_sentences.append(sentence)

    j = 0
    for i in range(0,  int(len(ret)/5)):
        list_doc = [ret[j], ret[j+1], ret[j+2], ret[j+3], ret[j+4]]
        dict_query_doc[i+1] = list_doc
        j += 5

    f = open(writepath, 'w')
    for quid, docs in dict_query_doc.items():
        master_dict[quid] = []
        for doc in docs:
            master_dict[quid].append((doc, ID_CleanedSentence[doc]))

    for quid, doclist in master_dict.items():
        quid_str = str(quid)
        f.write("-----------------------------------------------------------------\n")
        f.write("For Query " + str(quid) + " : "+query_dict[quid_str]+"\n\nTop 5 documents are:\n\n")
        i = 0
        for doc in doclist:
            i += 1
            s_factor_list = []
            for sentence in doc[1]:
                words = sentence.split(" ")
                s_factor = calc_significant_words(words, doc[0], len(doc[1]))
                s_factor_list.append(s_factor)

            f.write(str(i)+") "+doc[0]+"\n\n")
            factor_sentences = highestThree(doc[1], s_factor_list)
            significance_factors = []
            sentences = []
            for factor_sentence in factor_sentences:
                significance_factors.append(factor_sentence[0])
                sentences.append(factor_sentence[1])
            f.write("\n"+ str(significance_factors)+ "\n")
            highlighted_sentences = []
            query_terms = query_dict[quid_str].split(" ")
            for sentence in sentences:
                highlighted_sentence_terms = []
                for term in sentence.split(" "):
                    if term.lower() in query_terms and term.lower() not in common_words:
                        highlighted_sentence_terms.append("<b>"+term+"</b>")
                    else:
                        highlighted_sentence_terms.append(term)
                highlighted_sentences.append(" ".join(highlighted_sentence_terms).replace("</b> <b>"," "))

            for highlighted_sentence in highlighted_sentences:
                f.write(highlighted_sentence+"\n")
            f.write("\n")


filepath_list = []
writepath_list = []

filepath_list.append(os.path.dirname(os.path.realpath(__file__)) + "/../Phase 1/Task 3/Part A/Step 4/Lucene (Stopped)/Stopped_Lucene_Top5_Docs.txt")
filepath_list.append(os.path.dirname(os.path.realpath(__file__)) + "/../Phase 1/Task 3/Part A/Step 4/BM25 (Stopped)/Stopped_BM25_NoRelevance_Top5_Docs.txt")
filepath_list.append(os.path.dirname(os.path.realpath(__file__)) + "/../Phase 1/Task 3/Part A/Step 4/QLM (Stopped)/Stopped_QLM_Top5_Docs.txt")
filepath_list.append(os.path.dirname(os.path.realpath(__file__)) + "/../Phase 1/Task 3/Part A/Step 4/TF-IDF (Stopped)/Stopped_TF_IDF_Normalized_Top5_Docs.txt")


writepath_list.append(r'Snippets_Stopped_Lucene.txt')
writepath_list.append(r'Snippets_Stopped_BM25_NoRelevance.txt')
writepath_list.append(r'Snippets_Stopped_QLM.txt')
writepath_list.append(r'Snippets_Stopped_TF_IDF_Normalized.txt')

for i in range(0, len(filepath_list)):
    print("\nDONE\n\n")
    generate_snippet(filepath_list[i], writepath_list[i])
