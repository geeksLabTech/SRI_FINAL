from cmath import log
import math
import numpy as np
from trie import Trie, TrieNode
from document_data import DocumentData
from collections import Counter
from vectorization_utils import get_tf, get_idf

class VectorialModel:
    def __init__(self, documents: dict[int, DocumentData], vocabulary_dict: dict[str, dict[int,int]]) -> None:
        self.documents = documents
        self.vocabulary_dict = vocabulary_dict
        
    def get_weight_of_a_word_in_document(self, word_frequency_in_doc: int, doc_id: int, docs_with_word: int) -> float:
        max_freq = self.documents[doc_id].max_frequency_term
        tf = get_tf(word_frequency_in_doc, max_freq)
        idf = get_idf(len(self.documents), docs_with_word)
        return tf * idf

    def create_documents_vectors(self) -> np.ndarray:
        matrix_with_weight = np.zeros((len(self.documents)+3, len(self.vocabulary_dict)))
        for i, word in enumerate(self.vocabulary_dict):
            dic = self.vocabulary_dict[word]
            docs_with_word = len(dic)
            for doc_id in dic:
                freq = dic[doc_id]
                matrix_with_weight[doc_id][i] = self.get_weight_of_a_word_in_document(freq, doc_id, docs_with_word)

        return matrix_with_weight

    def create_query_vector(self, query: list[str], a = 0.5) -> np.ndarray:
        query_vector = np.zeros(len(self.vocabulary_dict))
        frequency_dict = Counter(query)
        for i, word in enumerate(self.vocabulary_dict):
            if word in query:
                freq = frequency_dict[word]
                docs_with_word = len(self.vocabulary_dict[word])
                tf = get_tf(freq, max(frequency_dict.values()))
                idf = get_idf(len(self.documents), docs_with_word)
                query_vector[i] = (a + (1-a) * tf) * idf

        return query_vector

    def process_query(self, query: list[str], a = 0.5) -> list[tuple[int, float]]:
        """
        Returns a dict with the document id as key and the similarity with the query as value.
        The dict is sorted in descending order by the similarity.
        """
        documents_vectors = self.create_documents_vectors()
        query_vector = self.create_query_vector(query, a)
        # print('query vector: ', np.count_nonzero(query_vector))
        documents_by_similarity: dict[int, float] = {}

        for i in range(len(documents_vectors)):
            similarity = np.dot(query_vector, documents_vectors[i]) / (np.linalg.norm(query_vector) * np.linalg.norm(documents_vectors[i]))
            documents_by_similarity[i] = similarity

        sorted_documents = sorted(documents_by_similarity.items(), key=lambda x: x[1], reverse=True)
        # TODO - Find a best way to sort the documents
        # print('sorted documents: ', sorted_documents)
        # The first is always NaN
        return sorted_documents[1:]