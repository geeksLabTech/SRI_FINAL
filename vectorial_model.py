import math

from trie import Trie, TrieNode
from document_data import DocumentData


class VectorialModel:
    def __init__(self, trie: Trie, documents: dict[int, DocumentData]) -> None:
        self.trie = trie
        self.documents = documents
        
    def get_idf(self, node: TrieNode) -> float:
        return math.log10(len(self.documents) / len(node.frequency_by_document))

    def get_tf(self, frequency, max_frequency) -> int:
        return frequency / max_frequency

    def get_weight_of_a_word_in_document(self, word: str, doc_id: int) -> float:
        node = self.trie.search(word)
        if node is None:
            return 0
        return self.get_tf(node, self.documents[doc_id].max_frequency_term) * self.get_idf(node)

    def process_query(self, query: list[str], a = 0.5) -> list[tuple[int, float]]:
        """
        Returns a dict with the document id as key and the similarity with the query as value.
        The dict is sorted in descending order by the similarity.
        """

        frequencies = []
        for token in query:
            frequencies.append(query.count(token))
        
        max_frequency = max(frequencies)
        weights_in_query = []
        weights_by_documents: dict[int, list[float]] = {}
        for x in self.documents:
            weights_by_documents[x] = []

        for i in range(len(query)):
            token = query[i]
            node = self.trie.search(token)
            if node is None:
                for key in weights_by_documents:
                    weights_by_documents[key].append(0)
            else:
                token_idf = self.get_idf(node)
                token_weight_in_query = (a + (1-a) * self.get_tf(frequencies[i], max_frequency)) * token_idf
                weights_in_query.append(token_weight_in_query)
                for doc_id in node.frequency_by_document:
                    token_weight_in_document = self.get_tf(node.frequency_by_document[doc_id], self.documents[doc_id].max_frequency_term) * token_idf
                    weights_by_documents[doc_id].append(token_weight_in_document)
        
        documents_by_similarity: dict[int, float] = {}
        query_total_square_weight = sum([x**2 for x in weights_in_query])
        sqrt_query_total_square_weight = math.sqrt(query_total_square_weight)
        documents_by_total_squared_weights: dict[int, float] = {}
        # print("Weights by documents: ", weights_by_documents)
        # print('Weights in query: ')
        # print(len(weights_in_query))
        for doc_id in weights_by_documents:
            documents_by_similarity[doc_id] = 0
            for i in range(len(weights_in_query)):
                try:
                    documents_by_similarity[doc_id] += weights_in_query[i] * weights_by_documents[doc_id][i]
                    if not doc_id in documents_by_total_squared_weights:
                        documents_by_total_squared_weights[doc_id] = 0
                    documents_by_total_squared_weights[doc_id] += (weights_by_documents[doc_id][i] ** 2)
                except IndexError:
                    continue
            if documents_by_similarity[doc_id] == 0:
                del documents_by_similarity[doc_id]
        
        # Normalize
        normalization_dict: dict[int, float] = {}
        for key in documents_by_total_squared_weights:
            normalization_dict[key] = math.sqrt(documents_by_total_squared_weights[key]) * sqrt_query_total_square_weight
        
        for key in documents_by_similarity:
            documents_by_similarity[key] = documents_by_similarity[key] / normalization_dict[key]

        sorted_documents = sorted(documents_by_similarity.items(), key=lambda x: x[1], reverse=True)
        # TODO - Find a best way to sort the documents
        return sorted_documents