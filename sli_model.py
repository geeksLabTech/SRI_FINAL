import math
import numpy as np
from trie import Trie, TrieNode
from document_data import DocumentData


class SLIModel:
    def __init__(self, trie: Trie, documents: dict[int, DocumentData]) -> None:
        self.trie = trie
        self.documents = documents
        self.all_words_nodes = []
        self.search_all_words_nodes(trie.root)

    def get_similarity(self,doc_i, query):
        ''' Returns sililarity between a query and a document'''
        result = 0
        doc_norm = np.linalg.norm(doc_i)
        q_norm = np.linalg.norm(query)
        for i in range(0,min(len(doc_i),len(query))):
            result +=  doc_i[i]*query[i]
        return result / (doc_norm * q_norm)

    def search_all_words_nodes(self, root: TrieNode):
        if root.is_word():
            # TODO I Need here the word, not the node
            self.all_words_nodes.append(root)
        for next_node in root.transitions.values():
            self.search_all_words_nodes(next_node)


    def get_idf(self, node: TrieNode) -> float:
        return math.log10(len(self.documents) / len(node.frequency_by_document))

    def get_tf(self, frequency, max_frequency) -> int:
        return frequency / max_frequency

    def build_matrix(self):
        matrix = []

        for idx,word in enumerate(self.all_words_nodes):
            matrix.append([])
            for doc in self.trie.documents:
                node = self.trie.search(word)
                matrix[idx].append(1 if doc in node.frequency_by_document else 0)
        return matrix

    def build_vector(self, query):
        vector = []
        for word in self.all_words_nodes:
            if word in query:
                vector.append(1)
                continue

            vector.append(0)
        return vector

    # def get_similarity(self,t,matrix):
    #     similarity = []
    #     idx = self.trie.search(t).frequency_by_document
        
    #     d1 = matrix[idx-1,:]
    #     n1 = np.linalg.norm(d1)
        
    #     for i,r in enumerate(matrix):
    #         val = np.dot(d1,r)/(np.linalg.norm(r) * n1)
    #         similarity.append((val, i+1))
        
    #     similarity.sort(key=lambda x: -x[0])
    #     return similarity
    
    def process_query(self, query: list[str], a = 0.5) -> list[tuple[int, float]]:
        """
        Returns a dict with the document id as key and the similarity with the query as value.
        The dict is sorted in descending order by the similarity.
        """
        matrix = self.build_matrix()
        vector = self.build_vector(query)
        
        frequencies = []
        for token in query:
            frequencies.append(query.count(token))
        
        max_frequency = max(frequencies)
        weights_in_query = []
        weights_by_documents: dict[int, list[float]] = {}
        for x in self.documents:
            weights_by_documents[x] = []

        for i,token in enumerate(query):
            node = self.trie.search(token)
            if node is None:
                for key in weights_by_documents.items():
                    weights_by_documents[key].append(0)
            else:
                token_idf = self.get_idf(node)
                token_weight_in_query = (a + (1-a) *
                                         self.get_tf(frequencies[i], max_frequency)) * token_idf
                weights_in_query.append(token_weight_in_query)
                for doc_id in node.frequency_by_document:
                    token_weight_in_document = self.get_tf(node.frequency_by_document[doc_id],
                                           self.documents[doc_id].max_frequency_term) * token_idf
                    weights_by_documents[doc_id].append(token_weight_in_document)
        
        matrix = self.build_matrix()
        
        U,S,ST = np.linalg.svd(matrix)
        
        V = np.transpose(ST)
        
        sinv = []
        
        for t in S:
            if math.isclose(t,0):
                sinv.append(0.0)
            else:
                sinv.append(1.0/t)

        sinv = np.array(sinv)
        sinv_diag = np.diag(sinv)

        S1 = np.diag(S)
        # US = np.dot(U,S1)
        VS = np.dot(V,S1)

        tmp = np.dot(U,sinv_diag)
        tf_vector = [0]*len(self.all_words_nodes)

        for t in query:
            node = self.trie.search(t)

            if node.frequency_by_document > 0:
                tf_vector[node.frequency_by_document-1] += 1

        d1 = np.dot(tf_vector,tmp)
        n1 = np.linalg.norm(d1)
        similarity = []

        for i,v in enumerate(VS):
            val = np.dot(v,d1) / (np.linalg.norm(v) * n1)
            similarity.append((i+1,val))

        similarity.sort(key=lambda x: -x[0])

        print(similarity)
        return similarity

        
