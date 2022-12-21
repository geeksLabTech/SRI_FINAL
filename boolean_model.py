import os
import re
from collections import defaultdict
from glob import glob

import numpy as np

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from query_tools import get_type_of_token, infix_to_postfix
from sympy import to_dnf, Symbol


class BooleanModel():
    '''Boolean Model class for information retrieval'''
    def __init__(self, trie, documents) -> None:
        self.trie = trie
        self.documents = documents
        
    def query(self, tokenized_query):
        ''' query the corpus documents using a boolean model
        :param query: valid boolean expression to search for in the documents
        :returns: a list of all marching documents
        '''
        # preprocess query
        processed_query = self.proccess_query(tokenized_query)
        # eval query and return relevant documents
        return self.__eval_query(processed_query)

    def proccess_query(self, tokenized_query):
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
        if query.find("|") != -1: 
            try:
                dnf_q = str(to_dnf(query))
                query = dnf_q
            except:
                print("error converting to dnf")
        query = query.split()
        return query
            
    def __eval_query(self, tokenized_query):
        ''' Evaluates the query with the preprovcessed corpus
        :param tokenized_query: list of tokens in the query (postfix form)
        :returns: list of relevant document names
        '''
       
        tokenized_query = infix_to_postfix(tokenized_query)
        operands = []

        for token in tokenized_query:
            if get_type_of_token(token) == 3:
                right_op = operands.pop()
                left_op = operands.pop()

                result = self.__eval_operation(left_op, right_op, token)
                operands.append(result)
            else:
                operands.append(self.__relevants(token))

        if len(operands) != 1:
            print("Malformed query or postfix expression")
            return list()
        
        # Find out documents corresponding to set bits in the vector
        return operands.pop()

    def __eval_operation(self, left, right, op):
        """Performs specified operation on the vectors 
        :param left: left operand
        :param right: right operand
        :param op: operation to perform
        :returns: result of the operation
        """
        
        if op == "&":
            res = []
            for i in left:
                if i in right:
                    res.append(i)
            return res
            # return list(set(left).intersection(set(right)))
        elif op == "|":
            return left+right
            # return list(set(left).union(set(right)))
        else:
            return []
        
    def __relevants(self,word):
        ''' make a bitvector from the word'''

        negate = False

        # If word is "~good"
        if word[0] == "~":
            negate = True
            word = word[1:]
            
        node = self.trie.search(word)
        # if node:
        
        if node:
            relevant_docs = []
            if negate:
                relevant_docs = [ i for i in self.documents if not i in node.frequency_by_document and node.frequency_by_document[i] == 0]
            else:
                for i in self.documents:
                    if i in node.frequency_by_document.keys() and node.frequency_by_document[i] > 0:
                        relevant_docs.append(i)
                        
            return relevant_docs
        
        return []

    def remove_duplicates(self, text):
        ''' removes duplicates from text'''
        return list(set(text))

