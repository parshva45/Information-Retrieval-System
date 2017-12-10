import pickle

# This script uses the cacm.rel.txt file and converts the given relevance information
# in this file to a dictionary to be used by BM25 with relevance model

current_file = r'cacm.rel.txt'
content = open(current_file, 'r').read()
content = content.split("\n")
content = [w for w in content if w != ""]
rel_dict = {}
for line in content:
    each = line.split(" ")
    q_id = each[0]
    if q_id in rel_dict:
        rel_dict[q_id].append(each[2])
    else:
        rel_dict[q_id] = []
        rel_dict[q_id].append(each[2])

print(rel_dict)

output = open('../../Encoded Data Structures/Encoded-QueryID_RelevantDocs.txt', 'wb')
pickle.dump(rel_dict, output)
output.close()
