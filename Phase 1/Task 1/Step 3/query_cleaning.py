import re
import pickle
import os
from xml.etree import cElementTree as ET

query_file = r'cacm.query.txt'
content = open(query_file, 'r').read()
content = "<ROOT>\n" + content + "\n</ROOT>"
content = content.replace("</DOCNO>", "</DOCNO>\n<QUERY>")
xmlStr = content.replace("</DOC>", "</QUERY>\n</DOC>")
query_dict = {}
root = ET.fromstring(xmlStr)
encoded_dir = r'../Encoded Data Structures/'
if not os.path.exists(encoded_dir):
    os.makedirs(encoded_dir)

for query in root:
    q_id = query.find('DOCNO').text.strip()
    q = query.find('QUERY').text
    q = q.lower().replace("\n", " ")
    q = re.sub(' +', ' ', q).strip()
    q = re.sub(r"[^0-9A-Za-z,-\.:\\$]", " ", q)          # retain alpha-numeric text along with ',',':' and '.'
    q = re.sub(r"(?!\d)[$,%,:.,-](?!\d)", " ", q, 0)     # retain '.', '-' or ',' between digits
    q = q.split()
    for rt in q:
        if rt.startswith('-'):
            rt.replace(rt, rt.split('-')[1])
        if rt.endswith('-'):
            rt.replace(rt, rt.split('-')[0])
        else:
            continue
    q = ' '.join(q)
    query_dict[q_id] = q
for key, value in query_dict.items():
    print("Cleaned Query " + key + " : " + value)

f = open("Cleaned_Queries.txt", 'w', encoding='utf-8')
for quid in query_dict:
    f.write(quid + "\t" + query_dict[quid] + "\n")
f.close()

output = open(encoded_dir + 'Encoded-Cleaned_Queries.txt', 'wb')
pickle.dump(query_dict, output)
output.close()
