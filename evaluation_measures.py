
from download_data import get_dicc

class InformationRetrievalEvaluator:
    @staticmethod
    def evaluate(expected_result: list[int], query_result: list[int]) -> dict[str, float]:
        return InformationRetrievalEvaluator.f1(set(expected_result), set(query_result), True)

    @staticmethod
    def accuracy(expected_results: set[int], query_result: set[int]) -> float:
        true_positive = expected_results.intersection(query_result)
        false_positive = query_result.difference(expected_results)
        union = true_positive.union(false_positive)
        if len(union) == 0:
            return 0
        return len(true_positive) / len(union)
        
    @staticmethod
    def recall(expected_results: set[int], query_result: set[int]) -> float:
        true_positive = expected_results.intersection(query_result)
        not_recovered = expected_results.difference(query_result)
        union = true_positive.union(not_recovered)
        if len(union) == 0:
            return 0
        return len(true_positive) / len(union)
    
    @staticmethod
    def f1(expected_results: set[int], query_result: set[int], return_all_measures: bool):
        accuracy = InformationRetrievalEvaluator.accuracy(expected_results, query_result)
        recall = InformationRetrievalEvaluator.recall(expected_results, query_result)
        if accuracy + recall == 0:
            f1 = 0
        else:
            f1 = 2 * accuracy * recall / (accuracy + recall)
        if return_all_measures:
            return {
                'accuracy': accuracy,
                'recall': recall,
                'f1': f1
            }
        return f1



        

    