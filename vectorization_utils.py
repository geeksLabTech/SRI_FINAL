import numpy as np

def get_idf(total_documents: int, docs_with_word: int) -> float:
        return np.log( (1 + total_documents) / (1 + docs_with_word) ) + 1

def get_tf(frequency, max_frequency) -> int:
    return frequency / max_frequency