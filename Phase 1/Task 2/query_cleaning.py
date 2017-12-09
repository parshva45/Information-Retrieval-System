import re
import pickle
from xml.etree import cElementTree as ET

current_file = r'cacm.query.txt'
content = open(current_file, 'r').read()
content = "<ROOT>\n" + content + "\n</ROOT>"
content = content.replace("</DOCNO>", "</DOCNO>\n<QUERY>")
xmlstr = content.replace("</DOC>", "</QUERY>\n</DOC>")
query_dict = {}
root = ET.fromstring(xmlstr)
for query in root:
    q_id = query.find('DOCNO').text.strip()
    q = query.find('QUERY').text
    q = q.lower().replace("\n", " ")
    q = re.sub(' +', ' ', q).strip()
    q = re.sub(r"[^0-9A-Za-z,-\.:\\$]"," ", q)   #retain alpha-numeric text along with ',',':' and '.'
    q = re.sub(r"(?!\d)[$,%,:.,-](?!\d)"," ", q, 0)    #retain '.', '-' or ',' between digits
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
    print(key + " : " + value)

f = open("Cleaned_queries.txt", 'w', encoding='utf-8')
for id in query_dict:
    f.write(id + "\t" + query_dict[id] + "\n")
f.close()

output = open('Cleaned_queries_encoded.txt', 'wb')
pickle.dump(query_dict, output)
output.close()
