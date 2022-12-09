import ir_datasets
def get_dicc():
    dataset = ir_datasets.load("cranfield")
    dic = {}
    for query in dataset.qrels_iter():
        if query.query_id not in dic:
            dic[query.query_id] = [(query.doc_id , query.relevance)]
        else :
            dic[query.query_id].append(query.doc_id , query.relevance)
    return dic