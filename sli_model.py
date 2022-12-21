import math
import numpy as np
from trie import Trie, TrieNode
from document_data import DocumentData
from vectorial_model import VectorialModel


class SLIModel(VectorialModel):
    def __init__(self, documents: dict[int, DocumentData], vocabulary_dict: dict[str, dict[int, int]]) -> None:
        self.documents = documents
        self.vocabulary_dict = vocabulary_dict
        self.documents_vectors = self.create_documents_vectors()
        self.DTk_transpose, self.vector_to_multiply_by_query = self.precalculate_neccesary_values()

    def precalculate_neccesary_values(self):
        documents_vectors_transposed = self.documents_vectors.transpose()
        T, S, DT = np.linalg.svd(documents_vectors_transposed)
        k = 100
        Tk = T[:, :k]
        Sk = S[:k]
        DTk = DT[:k, :]

        Sk_diag = np.diag(Sk)
        DTk_transpose = DTk.transpose()
        
        vector_to_multiply_by_query = np.dot(np.linalg.inv(Sk_diag), Tk.transpose())
        return DTk_transpose, vector_to_multiply_by_query
    
        
    def process_query(self, query: list[str], a = 0.5) -> list[tuple[int, float]]:
        """
        Returns a dict with the document id as key and the similarity with the query as value.
        The dict is sorted in descending order by the similarity.
        """
        
        query_vector = self.create_query_vector(query, a)

        qk = np.dot(self.vector_to_multiply_by_query, query_vector)

        documents_by_similarity: dict[int, float] = {}

        for i in range(len(self.DTk_transpose)):
            similarity = np.dot(qk, self.DTk_transpose[i]) / (np.linalg.norm(qk) * np.linalg.norm(self.DTk_transpose[i]))
            documents_by_similarity[i] = similarity

        sorted_documents = sorted(documents_by_similarity.items(), key=lambda x: x[1], reverse=True)
        return sorted_documents[1:]

        
