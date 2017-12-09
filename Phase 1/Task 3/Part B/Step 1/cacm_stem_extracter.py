import re
import os

current_file = r'cacm_stem.txt'
content = open(current_file, 'r').read()

docs = re.split("# [\d]+",content)
docs = [w for w in docs if w != ""]

newpath = r'Stemmed_Corpus/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

for i,doc in enumerate(docs,1):
    print("Creating Stemmed Corpus file for CACM-" + str(i))
    f = open(newpath + 'CACM-' + str(i) + '.txt', 'w', encoding='utf-8')
    f.write(doc.strip())
    f.close()
