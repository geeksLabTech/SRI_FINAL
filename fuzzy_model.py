from boolean_model import BooleanModel
from sympy import to_dnf, sympify
from trie import Trie
from query_tools import get_type_of_token, infix_to_postfix
from nltk.tokenize import word_tokenize

class FuzzyModel(BooleanModel):


    def __init__(self,trie: Trie , documents):
        super().__init__(trie,documents)
        self.fuzzy = True
        self.trie = trie
    
    def query(self, tokenized_query):
        processed_query = self.__proccess_query(tokenized_query)
        print(processed_query,'ll')
        return self.eval_query(processed_query)

    def __proccess_query(self, tokenized_query):
        # print("TOK:",tokenized_query)
        # tokenize query and convert to postfix
        # query = self.clean_text(query)
        # tokenized_query = word_tokenize(query)
        n_tokenized_query = [tokenized_query[0]]
        for i in range(1,len(tokenized_query)):
            if get_type_of_token(tokenized_query[i-1]) == 4:
                if get_type_of_token(tokenized_query[i]) == 4:
                    n_tokenized_query.append("&")
                    n_tokenized_query.append(tokenized_query[i])
                else:
                    n_tokenized_query.append(tokenized_query[i])
                continue
            n_tokenized_query.append(tokenized_query[i])      
                
        query = " ".join(n_tokenized_query)
        # print(query)
        query = str(to_dnf(query)) 
        t_query = word_tokenize(query)
        
        return t_query
    

    def eval_query(self,tokenized_query):
        tokenized_query = self.convert_to_CDNF(tokenized_query)
        print(tokenized_query, 'query')
        dic_queryterm_with_doc = self.build_correlation_matrix(tokenized_query,self.trie.root)
        dic_recall = self.recall(dic_queryterm_with_doc)
        return sorted(dic_recall.items(), key=lambda x: x[1])

    def build_correlation_matrix(self,tokenized_query, current_node):
        correlation_term_of_query_with_doc = {}
        for term in tokenized_query:
            node_term = self.trie.search(term)
            if current_node.is_word():
                number_document_included_this_term = len(current_node.frequency_by_document)
                document_included_term_of_query = len(node_term.frequency_by_document)
                number_of_common_document = len(set(current_node.frequency_by_document.keys()).intersection(set(node_term.frequency_by_document.keys())))
                correlation_of_terms = number_of_common_document/document_included_term_of_query + number_document_included_this_term - number_of_common_document
                for doc_id in current_node.frequency_by_document.keys():
                    if doc_id not in correlation_term_of_query_with_doc:
                        correlation_term_of_query_with_doc[doc_id,term] = correlation_of_terms
                    correlation_term_of_query_with_doc[doc_id,term] *= correlation_of_terms
            
            for next_node in current_node.transition:
                self.build_correlation_matrix(tokenized_query,next_node.value)

        return correlation_term_of_query_with_doc


    def recall(self,dic_corelation):
        for doc_id in dic_corelation.keys():
            dic_corelation[doc_id] = 1 - dic_corelation[doc_id]
        

    def convert_to_CDNF(self, dnf):
        dnf = to_dnf(dnf)
        for var in dnf.free_symbols:
            new_dnf = ''
            for cc in dnf.args:
                if var not in cc.free_symbols:
                    exp = sympify(f'{var} | ~{var}')
                    new_cc = f'({str(cc)}) & ({str(exp)})'
                    new_dnf += f'({new_cc}) | '
                else:
                    new_dnf += f'({str(cc)}) | '
            new_dnf = new_dnf[:-3]
            dnf = to_dnf(new_dnf)
        
        return dnf