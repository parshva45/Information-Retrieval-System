import re
import os
from bs4 import BeautifulSoup

documentLen = 0
docID_documentLen = {}

newpath = 'Tokenizer Output/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

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
        result_text = result_text.lower()  # convert everything to lower case
        index_of_am = result_text.rfind("am")  # contains the last index of the term "am"
        index_of_pm = result_text.rfind("pm")  # contains the last index of the term "pm"

        # retain the text content uptil am or pm in the corpus documents

        if index_of_am > index_of_pm:
            greater_index = index_of_am
        else:
            greater_index = index_of_pm
        result_text = result_text[:(greater_index + 2)]

        f = open(newpath + file[:-5] + '.txt', 'w', encoding='utf-8')
        result_text = result_text.lower()                                           # convert everything to lower case
        f.write(result_text.strip())
        f.close()
