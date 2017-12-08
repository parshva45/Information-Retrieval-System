import pickle

with open("QueryID_RelevantDocs_encoded.txt", 'rb') as f:
    queryID_relevantDocs = pickle.loads(f.read())

with open("QueryID_Top100Docs_by_tf-idf_encoded.txt", 'rb') as f:
    queryID_top100Docs = pickle.loads(f.read())

with open("Cleaned_queries_encoded.txt", 'rb') as f:
    queryID_query = pickle.loads(f.read())

def calculate_total_no_of_relevant_docs(i):    #function to calculate the total no. of relevant docs for a particular query
    R = 0
    relevant_docs = queryID_relevantDocs[str(i)]
    top_100_docs = queryID_top100Docs[int(i)]
    for doc in relevant_docs:
        if doc in top_100_docs:
            R += 1
    return R

def calc_R_N_list(q):
    docName_R_N = {}                            #dictinary that has query ID as it's key and it's corresponding
                                                #mapping to "R" or "N" as it's value
    if str(q) in queryID_relevantDocs:
        relevant_docs = queryID_relevantDocs[str(q)]
        top_100_docs = queryID_top100Docs[q]
        for doc in top_100_docs:
            if doc in relevant_docs:
                docName_R_N[doc] = "R"             #"R" denotes the document is relevant
            else:
                docName_R_N[doc] = "N"             #"N" denotes the document is non-relevant
    return docName_R_N

def Reciprocal_rank(i):
    docName_R_N = calc_R_N_list(i)
    N_R_list = list(docName_R_N.values())
    try:
        rank = N_R_list.index("R")                 #gets the first occurence of "R"
    except ValueError:
        rank = 0
    if rank == 0:
        reciprocal_rank = 0
    else:
        reciprocal_rank = 1/rank
    return reciprocal_rank

#print(calculate_total_no_of_relevant_docs(1))
#print(Reciprocal_rank(1))

queryID_noOfRelevantDocs = {}

for id in queryID_relevantDocs:
    queryID_noOfRelevantDocs[id] = len(queryID_relevantDocs[id])

#print(queryID_noOfRelevantDocs)

queryID_finalRecall = {}
queryID_finalPrecision = {}
queryID_RR = {}
precision_at_5 = {}
precision_at_20 = {}

for qID in queryID_query:
    rank = 1
    R_count = 0
    PrecisionValueList = []
    RecallValueList = []
    no_of_rel_docs = queryID_noOfRelevantDocs[str(rank)]
    docName_R_N = calc_R_N_list(qID)
    RR = Reciprocal_rank(qID)
    if docName_R_N == {}:
        continue
    f = open("Precision_Recall_Tables/TF-IDF/Precision_Recall_Table_for_" +qID+'.txt', 'w')
    f.write("For Query: %s\n\n" %queryID_query[qID])
    f.write("RANK \t R/N \tPrecision \t  Recall\n\n")
    R_N_list = docName_R_N.values()
    for rel in docName_R_N:
        if docName_R_N[rel] == "R":
            R_count += 1
        precision = R_count/rank
        if rank == 5:
            precision_at_5[int(qID)] = precision
        if rank == 20:
            precision_at_20[int(qID)] = precision
        PrecisionValueList.append(precision)
        recall = R_count/no_of_rel_docs
        RecallValueList.append(recall)
        if rank <= 9:
            rank_str = "0"+str(rank)
        else:
            rank_str = str(rank)
        f.write(rank_str+"  \t  "+docName_R_N[rel]+"  \t  %.3f" %precision+"  \t  %.3f" %recall+"\n")
        rank += 1
    queryID_finalPrecision[qID] = precision
    queryID_finalRecall[qID] = recall
    queryID_RR[qID] = RR
    f.close()

f1 = open("Precision_Recall_Tables/TF-IDF/Final Evaluation.txt", 'w')
MAP = sum(queryID_finalPrecision.values()) / len(queryID_finalPrecision.keys())
f1.write("Mean Average Precision = %f\n\n" %MAP)

MRR = sum(queryID_RR.values()) / len(queryID_RR.keys())
f1.write("Mean Reciprocal Rank = %f\n\n" %MRR)
f1.close()

f2 = open("Precision_Recall_Tables/TF-IDF/P@KValuesForAllQueries.txt",'w')
for qID in queryID_query:
    if int(qID) in precision_at_5.keys():
        f2.write("For query: %s\n\n" %queryID_query[qID])
        f2.write("Precision at rank 5: %f\n" %precision_at_5[int(qID)])
        f2.write("Precision at rank 20: %f\n\n" %precision_at_20[int(qID)])
f2.close()
