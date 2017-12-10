import re
import os
from bs4 import BeautifulSoup

# This script is used to tokenize by de-punctuation and case-folding of the
# raw HTML text of the cacm corpus to get the cleaned up text files to be
# input to the inverted indexer

# variable to store document length
documentLen = 0

# dictionary with key as docID and value as corresponding document length
docID_documentLen = {}

# create new directory for output
newpath = 'Tokenizer Output/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

# input path of corpus of raw cacm html
path = os.path.dirname(os.path.realpath(__file__)) + "/../../../Raw HTML/"

for file in os.listdir(path):
    print("Tokenizing: " + file)
    current_file = os.path.join(path, file)
    page_content = open(current_file, 'r').read()
    soup = BeautifulSoup(page_content,"html.parser")
    for req_content in soup.find_all("html"):
        req_content_text = req_content.text
        req_content_text = re.sub(r"[^0-9A-Za-z,-\.:\\$]", " ", req_content_text)   # retain alpha-numeric text along with ',',':' and '.'
        result_text = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", req_content_text, 0)   # retain '.', '-' or ',' between digits
        result_text = result_text.split()
        for rt in result_text:                                                      # remove minus and not hyphens
            if rt.startswith('-'):
                rt.replace(rt, rt.split('-')[1])
            if rt.endswith('-'):
                rt.replace(rt, rt.split('-')[0])
            else:
                continue
        result_text = ' '.join(result_text)
        result_text = result_text.lower()       # convert everything to lower case
        index_of_am = result_text.rfind("am")   # contains the last index of the term "am"
        index_of_pm = result_text.rfind("pm")   # contains the last index of the term "pm"

        # retain the text content until am or pm in the corpus documents

        if index_of_am > index_of_pm:
            greater_index = index_of_am
        else:
            greater_index = index_of_pm
        result_text = result_text[:(greater_index + 2)]

        f = open(newpath + file[:-5] + '.txt', 'w', encoding='utf-8')
        result_text = result_text.lower()                                           # convert everything to lower case
        f.write(result_text.strip())
        f.close()

print("\n\nTokenizing Process DONE")