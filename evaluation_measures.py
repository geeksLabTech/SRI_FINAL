
from download_data import get_dicc

def analyze_query(query_result : dict):
    dic = {}
    for i in query_result:
        dic[i] = (accuracy(i,query_result[i]),recall(i,query_result[i]),f1(i,query_result[i]))
        # break
    return dic

def accuracy (id_query:int , query_result : list):
    expected_result = get_dicc()
    # print(expected_result)
    true_positive = 0
    false_positive = 0
    for i in query_result:
        if id_query in expected_result:
            if detect_true_positive(i,expected_result[id_query]):
                true_positive+=1
                # print(true_positive)
            else:
                false_positive+=1
                # print(false_positive)
    if true_positive == 0 and false_positive == 0:
        return 0
    return true_positive/(true_positive + false_positive)

def detect_true_positive(document , list_document : list):
    for i in list_document:
        if str(i) == str(document):
            return True
    return False

def recall(id_query:int , query_result : list):
    true_positive_rec = 0
    not_recovery = 0
    expected_result = get_dicc()
    for i in query_result:
        if id_query in expected_result:
            if detect_true_positive(i,expected_result[id_query]):
                true_positive_rec+=1
            not_recovery = len(expected_result[id_query]) - true_positive_rec
    if true_positive_rec == 0 and not_recovery == 0:
        return 0
    return true_positive_rec/(true_positive_rec + not_recovery)

def f1(id_query:int , query_result : list):
    result_accuracy = accuracy(id_query, query_result)
    result_recall = recall(id_query, query_result)
    if result_accuracy == 0 and result_recall == 0:
        return 0
    return 2 * result_accuracy * result_recall/ (result_accuracy + result_recall)
        

    