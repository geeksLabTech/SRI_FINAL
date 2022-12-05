from io import TextIOWrapper
import math
import os
import re
from collections import defaultdict
from glob import glob

import numpy as np

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from query_tools import get_type_of_token, infix_to_postfix
from trie import Trie, TrieNode
from document_data import DocumentData

class InformationRetrievalSystem:
    def __init__(self) -> None:
        self.trie = Trie()
        self.documents: dict[int, DocumentData] = {}

    def load_and_process_corpus(self, path, language):
        '''Load and process the corpus'''
        doc_id = len(self.documents) + 1
        stopwords = set(stopwords.words(language))
        stemmer = SnowballStemmer(language=language)
        # gets all filepaths in the corpus
        for filepath in glob(path):
            # opens and reads all files
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    words = self.tokenize_document(file, stopwords, stemmer)
            except(IsADirectoryError):
                continue

            self.trie.insert_document(words, doc_id)
            words_frequency = [word.count() for word in words]
            doc_data = DocumentData(os.path.basename(filepath), len(words), max(words_frequency))
            self.documents[doc_id] = doc_data
            doc_id += 1

    def tokenize_document(self, file: TextIOWrapper, stopwords: set, stemmer: SnowballStemmer) -> list[str]:
        text = file.read()
         # replace punctuation with spaces
        text = re.sub(r"[^\w\s]", " ", text)
        # remove all special characters
        text = self.clean_text(text)
        text = self.remove_digits(text)
        # tokenize the document text
        words = word_tokenize(text)
        # remove stopwords from the text
        words = [word.lower() for word in words if word not in self.stopwords]
        # stem words in document
        words = [stemmer.stem(word) for word in words]
        return words

    def get_idf(self, node: TrieNode) -> float:
        return math.log10(len(self.documents) / len(node.frequency_by_document))

    def get_tf(self, frequency, max_frequency) -> int:
        return frequency / max_frequency

    def get_weight_of_a_word_in_document(self, word: str, doc_id: str) -> float:
        node = self.trie.search(word)
        if node is None:
            return 0
        return self.get_tf(node, self.documents[doc_id].max_frequency_term) * self.get_idf(len(self.documents), node.frequency_by_document[doc_id])

    def process_query_with_vectorial_model(self, query: list[str], a = 0.5) -> dict[str, float]:
        frequencies = []
        for token in query:
            frequencies.append(query.count(token))
        
        max_frequency = max(frequencies)
        weights_in_query = []
        weights_by_documents: dict[str, list[float]] = {}
        for x in self.documents:
            weights_by_documents[x] = []

        for i in range(len(query)):
            token = query[i]
            node = self.trie.search(token)
            if node is None:
                weights_by_documents[x].append(0)
            else:
                token_idf = self.get_idf(node)
                token_weight_in_query = (a + (1-a) * self.get_tf(frequencies[i], max_frequency)) * token_idf
                weights_in_query.append(token_weight_in_query)
                for doc_id in node.frequency_by_document:
                    token_weight_in_document = self.get_tf(node.frequency_by_document[doc_id], self.documents[doc_id].max_frequency_term) * token_idf
                    weights_by_documents[doc_id].append(token_weight_in_document)
        
        documents_by_similarity: dict[str, float] = {}
        for doc_id in weights_by_documents:
            documents_by_similarity[doc_id] = 0
            for i in range(len(weights_in_query)):
                documents_by_similarity[doc_id] += weights_in_query[i] * weights_by_documents[doc_id][i]

        return sorted(documents_by_similarity.items(), key=lambda x: x[1], reverse=True)

    def process_query_with_boolean_model(self, query: list[str]) -> list[str]:
        docs_by_token_matches: dict[str, list[int]] = {}
        for doc_id in self.documents:
            docs_by_token_matches[doc_id] = []
        
        for i, token in enumerate(query):
            node = self.trie.search(token)
            if node is None:
                return []
            for doc_id in node.frequency_by_document:
                docs_by_token_matches[doc_id].append(i)
        
        complete_matches = [x for x in docs_by_token_matches if len(docs_by_token_matches[x]) == len(query)]
        return complete_matches

    def remove_digits(self, text):
        ''' removes digits from text'''
        regex = re.compile(r"\d") 
        # Replace and return
        return re.sub(regex, "", text)

    def clean_text(self, text):
        ''' removes special characters from text'''
        text = text.replace(",.;:", " ")  
        # Regex pattern for a word
        regex = re.compile(r"[^a-zA-Z0-9\s]")
        # Replace and return
        return re.sub(regex, "", text)