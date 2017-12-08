import re

current_file = r'cacm_stem.txt'
content = open(current_file, 'r').read()
# print(content)
docs = re.split("# [\d]+",content)
docs = [w for w in docs if w != ""]
# print(docs)
for i,doc in enumerate(docs,1):
	print(i)
	f = open('Stemmed_Corpus/CACM-' + str(i) + '.txt' ,'w', encoding = 'utf-8')
	f.write(doc.strip())
	f.close()
