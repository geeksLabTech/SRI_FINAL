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

    def __insert_word(self, word: str, doc_id: str) -> None:
        current_node = self.root
        for char in word:
            if char not in current_node.transitions:
                current_node.transitions[char] = TrieNode(char)
            current_node = current_node.transitions[char]
        if doc_id not in current_node.frequency_by_document:
            current_node.frequency_by_document[doc_id] = 0
        current_node.frequency_by_document[doc_id] += 1

    def insert_document(self, tokens: list[str], doc_id: str) -> None:
        for token in tokens:
            self.__insert_word(token, doc_id)

    def search(self, word: str) -> TrieNode:
        current_node = self.root
        for char in word:
            if char not in current_node.transitions:
                return None
            current_node = current_node.transitions[char]
        return current_node

    
            
            
        
        
    

