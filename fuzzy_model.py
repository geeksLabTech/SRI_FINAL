from cmath import isclose
import math
from platform import node
from this import d
from boolean_model import BooleanModel
from sympy import to_dnf, sympify
from trie import Trie , TrieNode
from query_tools import get_type_of_token, infix_to_postfix
from nltk.tokenize import word_tokenize

class FuzzyModel(BooleanModel):
    def __init__(self,trie: Trie , documents):
        super().__init__(trie,documents)
        self.fuzzy = True
        self.trie = trie
        self.all_words_nodes: list[TrieNode] = []
    
    def query(self, tokenized_query, target_relevance):
        processed_query = self.proccess_query(tokenized_query)
        
        query_done = ''
        for term in processed_query:
            query_done +=term
        
        relevant_documents = self.eval_query(tokenized_query, query_done)
        result = []
        for doc in relevant_documents:
            if relevant_documents[doc] >= target_relevance:
                result.append((doc, relevant_documents[doc]))
        
        # sort result by relevance
        return sorted(result, key=lambda x: x[1], reverse=True)

    def eval_query(self,tokenized_query, str_query):
        cdnf_query = self.convert_to_CDNF(str_query)
        self.search_all_words_nodes(self.trie.root)
        dic_queryterm_with_doc = self.build_correlation_matrix(tokenized_query, cdnf_query,self.all_words_nodes)
        dic_recall = self.recall(dic_queryterm_with_doc)
        return dic_recall

    def build_correlation_matrix(self, tokenized_query, cdnf_query, words: list[TrieNode]):
        correlation_term_of_query_with_doc = {}
        correlation_terms_with_words = {}
        for token in tokenized_query:
            node = self.trie.search(token)
            if not node == None:
                correlation_terms_with_words[token] = self.calculate_correlation_between_term_and_words(node, words)
        
        for term in cdnf_query:
            is_negated = False
            if term[0] == '~':
                term = term[1:]
                is_negated = True
            
            for word in words:
                try:
                    correlation_of_terms = correlation_terms_with_words[term][word]
                except KeyError:
                    continue
                if correlation_of_terms == None:
                    continue
                if is_negated:
                    correlation_of_terms = 1 - correlation_of_terms
                    if math.isclose(correlation_of_terms, 0.0):
                        continue

                for doc_id in word.frequency_by_document.keys():
                    if doc_id not in correlation_term_of_query_with_doc:
                        correlation_term_of_query_with_doc[doc_id] = correlation_of_terms
                    else:
                        correlation_term_of_query_with_doc[doc_id] *= correlation_of_terms
                        
        return correlation_term_of_query_with_doc

    def calculate_correlation_between_term_and_words(self, node_term: TrieNode, words: list[TrieNode]):
        correlation_term_with_words = {}
        for word in words:
            number_document_included_this_term = len(word.frequency_by_document)
            document_included_term_of_query = len(node_term.frequency_by_document)
            number_of_common_document = len(set(word.frequency_by_document.keys()).intersection(set(node_term.frequency_by_document.keys())))
            corr =  number_of_common_document/(document_included_term_of_query + number_document_included_this_term - number_of_common_document)
            if math.isclose(corr, 0.0):
                correlation_term_with_words[word] = None
            else:
                correlation_term_with_words[word] = corr

        return correlation_term_with_words

    def search_all_words_nodes(self, root: TrieNode):
        if root.is_word():
            self.all_words_nodes.append(root)
        for next_node in root.transitions.values():
            self.search_all_words_nodes(next_node)
        
    def recall(self,dic_correlation):
        new_dic_correlation = {}
        for doc_id in dic_correlation:
            new_dic_correlation[doc_id] = 1 - dic_correlation[doc_id]
        
        return new_dic_correlation
        
    def convert_to_CDNF(self, dnf):

        dnf = to_dnf(dnf)
        # print(dnf,'dnf')
        # print(dnf.free_symbols is None)
        print('sera')
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
            # print(dnf,'ll')
        return [x for x in dnf if not x==')' and not x=='(' and not x=='&' and not x=='|']