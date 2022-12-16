
from download_data import get_dicc

class InformationRetrievalEvaluator:
    @staticmethod
    def evaluate(expected_result: list[str], query_result: list[str]) -> dict[str, float]:
        return InformationRetrievalEvaluator.f1(set(expected_result), set(query_result), True)

    @staticmethod
    def accuracy(expected_results: set[str], query_result: set[str]) -> float:
        true_positive = expected_results.intersection(query_result)
        false_positive = query_result.difference(expected_results)
        return len(true_positive) / (len(true_positive) + len(false_positive))
        
    @staticmethod
    def recall(expected_results: set[str], query_result: set[str]) -> float:
        true_positive = expected_results.intersection(query_result)
        not_recovered = len(expected_results) - len(true_positive)
        return len(true_positive) / (len(true_positive) + not_recovered)
    
    @staticmethod
    def f1(expected_results: set[str], query_result: set[str], return_all_measures: bool):
        accuracy = InformationRetrievalEvaluator.accuracy(expected_results, query_result)
        recall = InformationRetrievalEvaluator.recall(expected_results, query_result)
        f1 = 2 * accuracy * recall / (accuracy + recall)
        if return_all_measures:
            return {
                'accuracy': accuracy,
                'recall': recall,
                'f1': f1
            }
        return f1



def analyze_query(query_result : dict):
    dic = {}
    for i in query_result:
        dic[i] = (accuracy(i,query_result[i]),recall(i,query_result[i]),f1(i,query_result[i]))
    return dic

def accuracy (id_query:int , query_result : list):
    expected_result = get_dicc()
    true_positive = 0
    false_positive = 0
    for i in query_result:
        if detect_true_positive(i,expected_result[id_query]):
            true_positive+=1
        else:
            false_positive+=1
    
    return true_positive/true_positive + false_positive

def detect_true_positive(document , list_document : list):
    for i in list_document:
        if i == document:
            return True
    return False

def recall(id_query:int , query_result : list):
    true_positive_rec = 0
    expected_result = get_dicc()
    for i in query_result:
        if detect_true_positive(i,expected_result[id_query]):
            true_positive_rec+=1
    not_recovery = len(expected_result[id_query]) - true_positive_rec
    return true_positive_rec/true_positive_rec + not_recovery

def f1(id_query:int , query_result : list):
    result_accuracy = accuracy(id_query, query_result)
    result_recall = recall(id_query, query_result)
    return 2 * result_accuracy * result_recall/ result_accuracy + result_recall
        

    