
from trie import Trie
from document_data import DocumentData
from tokenizer import Tokenizer
from corpus_loader import CorpusLoader
from vectorial_model import VectorialModel
from boolean_model import BooleanModel
from fuzzy_model import FuzzyModel
class InformationRetrievalSystem:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.trie = Trie()
        self.documents: dict[int, DocumentData] = {}
        self.tokenizer = tokenizer
        self.corpus_loader = CorpusLoader(tokenizer)
        
    def load_and_process_corpus_from_path(self, path):
        self.trie, self.documents = self.corpus_loader.load_from_path(path, self.trie, self.documents)

    def load_and_process_corpus_from_ir_datasets(self, dataset: str):
        self.trie, self.documents = self.corpus_loader.load_from_ir_datasets(dataset, self.trie, self.documents)
        
    def process_query_with_vectorial_model(self, query: str) -> list[tuple[int, float]]:
        tokenized_query = self.tokenizer.tokenize(query)
        # TODO - change to create VectorialModel only once
        vectorial_model = VectorialModel(self.trie, self.documents)
        return vectorial_model.process_query(tokenized_query)

    def process_query_with_boolean_model(self, query: str) -> list[str]:
        # TODO - update boolean model to use Trie and dict with DocumentData
        boolean_model = BooleanModel(self.trie, self.documents)
        # print(self.documents)
        tokenized_query = self.tokenizer.tokenize(query)

        # TODO - update boolean model to use tokenized query
        return boolean_model.query(tokenized_query)

    def process_query_with_fuzzy_model(self,query: str) -> list[str]:
        fuzzy_model = FuzzyModel(self.trie, self.documents)
        tokenized_query = self.tokenizer.tokenize(query)
        print('lalal')
        return fuzzy_model.query(query)
    # def process_query_with_boolean_model(self, query: list[str]) -> list[str]:
    #     docs_by_token_matches: dict[str, list[int]] = {}
    #     for doc_id in self.documents:
    #         docs_by_token_matches[doc_id] = []
        
    #     for i, token in enumerate(query):
    #         node = self.trie.search(token)
    #         if node is None:
    #             return []
    #         for doc_id in node.frequency_by_document:
    #             docs_by_token_matches[doc_id].append(i)
        
    #     complete_matches = [x for x in docs_by_token_matches if len(docs_by_token_matches[x]) == len(query)]
    #     return complete_matches
