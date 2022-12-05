import math


class TrieNode:
    def __init__(self) -> None:
        # This represents how many times a word that end at this node is repeated in a given document
        self.frequency_by_document: dict[str, int] = {}
        # Given the next character, this dictionary will return the next node
        self.transitions: dict[str, TrieNode] = {}

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode("")
        self.documents_by_length: dict[str, int] = {}
        self.documents_by_max_frequency_term: dict[str, int] = {}
        self.total_documents = 0

    def __insert_word(self, word: str, doc_id: str) -> None:
        current_node = self.root
        for char in word:
            if char not in current_node.transitions:
                current_node.transitions[char] = TrieNode(char)
            current_node = current_node.transitions[char]
        if doc_id not in current_node.frequency_by_document:
            current_node.frequency_by_document[doc_id] = 0
        current_node.frequency_by_document[doc_id] += 1
        if current_node.frequency_by_document[doc_id] > self.documents_by_max_frequency_term[doc_id]:
            self.documents_by_max_frequency_term[doc_id] = current_node.frequency_by_document[doc_id]

    def insert_document(self, tokens: list[str], doc_id: str) -> None:
        self.documents_by_max_frequency_term[doc_id] = 0
        for token in tokens:
            self.__insert_word(token, doc_id)
        self.documents_by_length[doc_id] = len(tokens)
        self.total_documents += 1

    def search(self, word: str) -> TrieNode:
        current_node = self.root
        for char in word:
            if char not in current_node.transitions:
                return None
            current_node = current_node.transitions[char]
        return current_node

    def get_idf(self, node: TrieNode) -> float:
        return math.log10(self.total_documents / len(node.frequency_by_document))

    def get_tf(self, frequency, max_frequency) -> int:
        return frequency / max_frequency

    def get_weight_of_a_word_in_document(self, word: str, doc_id: str) -> float:
        node = self.search(word)
        if node is None:
            return 0
        return self.get_tf(node, self.documents_by_max_frequency_term[doc_id]) * self.get_idf(self.total_documents, node.frequency_by_document[doc_id])

    def process_query_with_vectorial_model(self, query: list[str], a = 0.5) -> dict[str, float]:
        frequencies = []
        for token in query:
            frequencies.append(query.count(token))
        
        max_frequency = max(frequencies)
        weights_in_query = []
        weights_by_documents: dict[str, list[float]] = {}
        for x in self.documents_by_length:
            weights_by_documents[x] = []

        for i in range(len(query)):
            token = query[i]
            node = self.search(token)
            if node is None:
                weights_by_documents[x].append(0)
            else:
                token_idf = self.get_idf(node)
                token_weight_in_query = (a + (1-a) * self.get_tf(frequencies[i], max_frequency)) * token_idf
                weights_in_query.append(token_weight_in_query)
                for doc in node.frequency_by_document:
                    token_weight_in_document = self.get_tf(node.frequency_by_document[doc], self.documents_by_max_frequency_term[doc]) * token_idf
                    weights_by_documents[doc].append(token_weight_in_document)
        
        documents_by_similarity: dict[str, float] = {}
        for doc in weights_by_documents:
            documents_by_similarity[doc] = 0
            for i in range(len(weights_in_query)):
                documents_by_similarity[doc] += weights_in_query[i] * weights_by_documents[doc][i]

        return sorted(documents_by_similarity.items(), key=lambda x: x[1], reverse=True)

    def process_query_with_boolean_model(self, query: list[str]) -> list[str]:
        docs_by_token_matches: dict[str, list[int]] = {}
        for doc_id in (len(self.documents_by_length)):
            docs_by_token_matches[doc_id] = []
        
        for i, token in enumerate(query):
            node = self.search(token)
            if node is None:
                return []
            for doc_id in node.frequency_by_document:
                docs_by_token_matches[doc_id].append(i)
        
        complete_matches = [x for x in docs_by_token_matches if len(docs_by_token_matches[x]) == len(query)]
        return complete_matches
            
            
        
        
    

