from cmath import isclose
import math
from platform import node
from boolean_model import BooleanModel
from sympy import to_dnf, sympify
from trie import Trie , TrieNode
from query_tools import get_type_of_token, infix_to_postfix
from nltk.tokenize import word_tokenize
from vectorization_utils import get_idf , get_tf
from document_data import DocumentData

class FuzzyModel(BooleanModel):
    def __init__(self, documents:dict[int, DocumentData], vocabulary_dict: dict[str,dict[int,int]]):
        super().__init__(documents, vocabulary_dict)
        self.documents = documents
        self.fuzzy = True
        self.vocabulary_dict = vocabulary_dict
        self.all_words_nodes: list[TrieNode] = []
    
    def query(self, tokenized_query: list) -> list[tuple[int, float]]:
        processed_query = self.proccess_query(tokenized_query)   
        relevant_documents = self.eval_query(tokenized_query, processed_query)

        # result = []
        # for doc in relevant_documents:
        #     if relevant_documents[doc] >= 0.1:
        #         result.append((doc, relevant_documents[doc]))
        # print(result)
        # sort result by relevance
        return sorted(relevant_documents.items(), key=lambda x: x[1], reverse=True)

    def eval_query(self,tokenized_query, processed_query):
        is_in_CDNF = True
        for t in processed_query:
            if t == '|' or t == '~':
                is_in_CDNF = False
                break
        if not is_in_CDNF:
            cdnf_query = self.convert_to_CDNF(processed_query)
        else:
            cdnf_query = [x for x in processed_query if not x==')' and not x=='(' and not x=='&' and not x=='|']
        
        print(cdnf_query)
        # self.search_all_words_nodes(self.trie.root)
        dic_queryterm_with_doc = self.calculate_rank(tokenized_query, cdnf_query)
        dic_recall = self.recall(dic_queryterm_with_doc)
        # print(dic_recall , 'rank')
        # sorted_documents = sorted(dic_recall.items(), key=lambda x: x[1], reverse=True)
        return dic_recall

    def calculate_rank(self, tokenized_query, cdnf_query):
        fuzzy_set_of_term = {}
        rank_of_document = {}
        for token in tokenized_query:
            # node = self.trie.search(token)
            fuzzy_set_of_term[token] = self.calculate_fuzzy_set(token)
            
        
        for term in cdnf_query:
            is_negated = False
            if term[0] == '~':
                term = term[1:]
                is_negated = True
            
            for doc in fuzzy_set_of_term[term]:
                if not doc in rank_of_document:
                    if is_negated:
                        rank_of_document[doc] = -fuzzy_set_of_term[term][doc]
                    else :
                        rank_of_document[doc] = 1 - fuzzy_set_of_term[term][doc]
                else:
                    if is_negated:
                        rank_of_document[doc] *= -fuzzy_set_of_term[term][doc]
                    else :
                        rank_of_document[doc] *= 1 - fuzzy_set_of_term[term][doc]
            # for word in words:
            #     try:
            #         correlation_of_terms = correlation_terms_with_words[term][word]
            #     except KeyError:
            #         continue
            #     if correlation_of_terms == None:
            #         continue
                # if is_negated:
                #     correlation_of_terms = 1 - correlation_of_terms
                #     if math.isclose(correlation_of_terms, 0.0):
                #         continue

                # for doc_id in word.frequency_by_document.keys():

                #     if doc_id not in correlation_term_of_query_with_doc:
                #         correlation_term_of_query_with_doc[doc_id] = correlation_of_terms
                #     else:
                #         correlation_term_of_query_with_doc[doc_id] *= (1 - correlation_of_terms)
                        
        return rank_of_document

    def calculate_fuzzy_set(self, term):
        dict_corr_between_term_doc = {}
        if term in self.vocabulary_dict:
            document_of_term = self.vocabulary_dict[term]
            for doc in document_of_term:
                dict_corr_between_term_doc[doc] = get_tf(document_of_term[doc],self.documents[doc].length)*get_idf(len(self.documents),len(document_of_term)) 
        return dict_corr_between_term_doc
            
    # def search_all_words_nodes(self, root: TrieNode):
    #     if root.is_word():
    #         self.all_words_nodes.append(root)
    #     for next_node in root.transitions.values():
    #         self.search_all_words_nodes(next_node)
        
    def recall(self,dic_correlation):
        new_dic_correlation = {}
        for doc_id in dic_correlation:
            new_dic_correlation[doc_id] = 1 - dic_correlation[doc_id]
        
        return new_dic_correlation
        
    def convert_to_CDNF(self, processed_query):

        raw_query = self.convert_query_to_raw_string(processed_query)
        dnf = to_dnf(raw_query)
        # print(dnf,'dnf')
        # print(dnf.free_symbols is None)
        for var in dnf.free_symbols:
            new_dnf = ''
            for cc in dnf.args:
                # print(var not in cc.free_symbols , 'if')
                if var not in cc.free_symbols:
                    # print('entra al if')
                    exp = sympify(f'{var} | ~{var}')
                    new_cc = f'({str(cc)}) & ({str(exp)})'
                    new_dnf += f'({new_cc}) | '
                else:
                    # print('else')
                    new_dnf += f'({str(cc)}) | '
                    # print(new_dnf,'new dmf1')
            # print(new_dnf, 'new dnf')
            new_dnf = new_dnf[:-3]
            dnf = to_dnf(new_dnf)
            # print(type(dnf),'llllllllll')
        
        dnf = word_tokenize(str(dnf))
        print('ready', dnf)
        return [x for x in dnf if not x==')' and not x=='(' and not x=='&' and not x=='|']

    def convert_query_to_raw_string(self, query):
        raw_string = ''
        for term in query:
            raw_string += term
        return raw_string