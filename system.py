
from sli_model import SLIModel
from trie import Trie
from document_data import DocumentData
from tokenizer import Tokenizer
from corpus_loader import CorpusLoader
from vectorial_model import VectorialModel
from boolean_model import BooleanModel
from fuzzy_model import FuzzyModel
from evaluation_measures import InformationRetrievalEvaluator
import pickle
import os
import ir_datasets
from enum import Enum

class ImplementedModels(Enum):
    BOOLEAN = 1
    VECTORIAL = 2
    FUZZY = 3
    SLI = 4

class InformationRetrievalSystem:
    def __init__(self, tokenizer: Tokenizer) -> None:
        
        if not os.path.exists(f'.cache/'):
            os.mkdir('.cache')
        
        self.trie = Trie()
        self.documents: dict[int, DocumentData] = {}
        self.tokenizer = tokenizer
        self.corpus_loader = CorpusLoader(tokenizer)
        
    def load_and_process_corpus_from_path(self, path):
        if os.path.exists(f'.cache/corpus.pickle'):
            with open(f'.cache/corpus.pickle', "rb") as file:
                self.trie = pickle.load(file)
            self.documents = self.trie.documents
        else:
            self.trie, self.documents = self.corpus_loader.load_from_path(path, self.trie, self.documents)
            with open(f'.cache/corpus.pickle', "wb") as file:
                pickle.dump(self.trie,file )
        # print(self.documents[1].path)

    def test_ir_dataset(self, dataset: str, models: list[ImplementedModels], number_of_queries: int):
        # if number_of_queries < 0: process all queries 
        print("Testing Models")
                
        self.load_and_process_corpus_from_ir_datasets(dataset)
        data = ir_datasets.load(dataset)
        expected_results: dict[str, list[int]] = {}
        for q in data.qrels_iter(): 
            if q.relevance < 1:
                continue
            if not q.query_id in expected_results:
                expected_results[q.query_id] = []
            expected_results[q.query_id].append(q.doc_id)
        
        evaluations = {
            'vectorial': {},
            'boolean': {},
            'fuzzy': {},
            'sli': {}
        }

        for q in data.queries_iter():
            if number_of_queries == 0:
                break
            if number_of_queries > 0:
                number_of_queries -= 1
            print(q.query_id)
            for model in models:
                if model == ImplementedModels.VECTORIAL:
                    r = self.process_query_with_vectorial_model(q.text)
                    documents_id = [doc[0] for doc in r if doc[1] >= 0.493]
                    try:
                        evaluations['vectorial'][q.query_id] = InformationRetrievalEvaluator.evaluate(expected_results[q.query_id], documents_id)
                    except KeyError:
                        print('KeyError with Vectorial', q.query_id)
                    # print('current evaluations', evaluations)
                elif model == ImplementedModels.SLI:
                    r = self.process_query_with_sli_model(q.text)
                    documents_id = [doc[0] for doc in r if doc[1] >= 0.493]
                    try:
                        evaluations['vectorial'][q.query_id] = InformationRetrievalEvaluator.evaluate(expected_results[q.query_id], documents_id)
                    except KeyError:
                        print('KeyError with Vectorial', q.query_id)
                    print('current evaluations', evaluations)
                elif model == ImplementedModels.BOOLEAN:
                    r = self.process_query_with_boolean_model(q.text)
                    try:
                        evaluations['boolean'][q.query_id] = InformationRetrievalEvaluator.evaluate(expected_results[q.query_id], r)
                    except KeyError:
                        print('KeyError with Boolean', q.query_id)
                    
                elif model == ImplementedModels.FUZZY:
                    r = self.process_query_with_fuzzy_model(q.text)
                    print('relevants fuzzy')
                    print()
                    print(r)
                    try:
                        evaluations['fuzzy'][q.query_id] = InformationRetrievalEvaluator.evaluate(expected_results[q.query_id], r)
                    except KeyError:
                        print('KeyError with Fuzzy', q.query_id)
                else:
                    print('model not implemented')
            print('current evaluations', evaluations)
        return evaluations

    def load_and_process_corpus_from_ir_datasets(self, dataset: str):
        if os.path.exists(f'.cache/{dataset}.pickle'):
            with open(f'.cache/{dataset}.pickle', "rb") as file:
                self.trie = pickle.load(file)
            self.documents = self.trie.documents
        else:
            self.trie, self.documents = self.corpus_loader.load_from_ir_datasets(dataset, self.trie, self.documents)
            with open(f'.cache/{dataset}.pickle', "wb") as file:
                pickle.dump(self.trie,file )
    def process_query_with_vectorial_model(self, query: str) -> list[tuple[int, float]]:
        tokenized_query = self.tokenizer.tokenize(query)
        # TODO - change to create VectorialModel only once
        vectorial_model = VectorialModel(self.trie, self.documents)
        return vectorial_model.process_query(tokenized_query)
    
    def process_query_with_sli_model(self, query: str) -> list[tuple[int, float]]:
        tokenized_query = self.tokenizer.tokenize(query)
        sli_model = SLIModel(self.trie, self.documents)
        return sli_model.process_query(tokenized_query)

    def process_query_with_boolean_model(self, query: str) -> list[int]:
        boolean_model = BooleanModel(self.trie, self.documents)
        tokenized_query = self.tokenizer.tokenize(query)
        return boolean_model.query(tokenized_query)

    def process_query_with_fuzzy_model(self,query: str) -> list[int]:
        print(query)
        fuzzy_model = FuzzyModel(self.trie, self.documents)
        print(type(fuzzy_model))
        tokenized_query = self.tokenizer.tokenize(query)
        return fuzzy_model.query(tokenized_query, 0.4)
  



