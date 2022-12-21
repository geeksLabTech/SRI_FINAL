
import math
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
        self.vocabulary_dict: dict[str, dict[int, int]] = {}
        self.fuzzy_model = None
        self.boolean_model = None
        self.vectorial_model = None
        self.sli_model = None
        
    def load_and_process_corpus_from_path(self, path):
        # if os.path.exists(f'.cache/corpus.pickle'):
        #     with open(f'.cache/corpus.pickle', "rb") as file:
        #         self.trie = pickle.load(file)
        #     self.documents = self.trie.documents
        # else:
        self.vocabulary_dict, self.documents = self.corpus_loader.load_from_path(path, self.vocabulary_dict, self.documents)
            # with open(f'.cache/corpus.pickle', "wb") as file:
            #     pickle.dump(self.trie,file )
        # print(self.documents[1].path)

    def new_loader_from_ir_datasets(self, dataset_name: str):
        self.vocabulary_dict, self.documents = self.corpus_loader.new_load_from_ir_datasets(dataset_name, self.vocabulary_dict, self.documents)

    def test_ir_dataset(self, dataset: str, models: list[ImplementedModels], number_of_queries: int):
        # if number_of_queries < 0: process all queries 
        print("Testing Models")
                
        self.new_loader_from_ir_datasets(dataset)
        data = ir_datasets.load(dataset)
        expected_results: dict[int, list[int]] = {}
        for q in data.qrels_iter(): 
            # print('qid', q.query_id)
            if int(q.relevance) < 1:
                continue
            query_id = int(q.query_id)
            if not query_id in expected_results:
                expected_results[query_id] = []
            expected_results[query_id].append(int(q.doc_id))
        
        evaluations = {
            'vectorial': {},
            'boolean': {},
            'fuzzy': {},
            'sli': {}
        }
        print('len expected', len(expected_results))
        if number_of_queries < 0:
            number_of_queries = len(expected_results)
        for i, q in enumerate(data.queries_iter(), 1):
            # print('number of queries', number_of_queries)
            if number_of_queries == 0:
                break
            if number_of_queries > 0:
                number_of_queries -= 1
            # print('es este qid', q.query_id)
            query_id = i
            for model in models:
                if model == ImplementedModels.VECTORIAL:
                    r = self.process_query_with_vectorial_model(q.text)
                    # print('max', r[0][1])
                    max_r = r[0][1]
                    # Find best value to cut the results
                    documents_id = [doc[0] for doc in r if doc[1] >= max_r * 0.5]
                    evaluation_result = InformationRetrievalEvaluator.evaluate(expected_results[query_id], documents_id)
                    try:
                        evaluations['vectorial'][query_id] = evaluation_result
                    except KeyError:
                        print('KeyError with Vectorial', query_id, evaluation_result)
                elif model == ImplementedModels.SLI:
                    r = self.process_query_with_sli_model(q.text)
                    max_r = r[0][1]
                    # Find best value to cut the results
                    documents_id = [doc[0] for doc in r if doc[1] >= max_r * 0.5]
                    try:
                        evaluations['sli'][query_id] = InformationRetrievalEvaluator.evaluate(expected_results[query_id], documents_id)
                    except KeyError:
                        print('KeyError with Vectorial', query_id)
                    
                elif model == ImplementedModels.BOOLEAN:
                    r = self.process_query_with_boolean_model(q.text)
                    try:
                        evaluations['boolean'][query_id] = InformationRetrievalEvaluator.evaluate(expected_results[query_id], r)
                    except KeyError:
                        print('KeyError with Boolean', query_id)
                    
                elif model == ImplementedModels.FUZZY:
                    r = self.process_query_with_fuzzy_model(q.text)
                    max_r = r[0][1]
                    # Find best value to cut the results
                    documents_id = [doc[0] for doc in r if doc[1] >= max_r * 0.5]
                    try:
                        evaluations['fuzzy'][query_id] = InformationRetrievalEvaluator.evaluate(expected_results[query_id], documents_id)
                    except KeyError:
                        print('KeyError with Fuzzy', query_id)
                else:
                    print('model not implemented')
        print('current evaluations', evaluations)
        return evaluations

    # def load_and_process_corpus_from_ir_datasets(self, dataset: str):
    #     if os.path.exists(f'.cache/{dataset}.pickle'):
    #         with open(f'.cache/{dataset}.pickle', "rb") as file:
    #             self.trie = pickle.load(file)
    #         self.documents = self.trie.documents
    #     else:
    #         self.trie, self.documents = self.corpus_loader.new_load_from_ir_datasets(dataset, self.vocabulary_dict, self.documents)
    #         with open(f'.cache/{dataset}.pickle', "wb") as file:
    #             pickle.dump(self.trie,file )
                
    def process_query_with_vectorial_model(self, query: str) -> list[tuple[int, float]]:
        tokenized_query = self.tokenizer.tokenize(query)
        # TODO - change to create VectorialModel only once
        if not self.vectorial_model:
            self.vectorial_model = VectorialModel(self.documents, self.vocabulary_dict)
        return self.vectorial_model.process_query(tokenized_query)
    
    def process_query_with_sli_model(self, query: str) -> list[tuple[int, float]]:
        tokenized_query = self.tokenizer.tokenize(query)
        if not self.sli_model:
            self.sli_model = SLIModel(self.documents, self.vocabulary_dict)

        return self.sli_model.process_query(tokenized_query)

    def process_query_with_boolean_model(self, query: str) -> list[int]:
        boolean_model = BooleanModel(self.documents, self.vocabulary_dict)
        tokenized_query = self.tokenizer.tokenize(query)
        return boolean_model.query(tokenized_query)

    def process_query_with_fuzzy_model(self,query: str) -> list[tuple[int, float]]:
        print(query)
        if not self.fuzzy_model:
            self.fuzzy_model = FuzzyModel(self.documents, self.vocabulary_dict)
        
        tokenized_query = self.tokenizer.tokenize(query)
        return self.fuzzy_model.query(tokenized_query)
  



