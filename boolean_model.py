
import os
import re
from collections import defaultdict
from glob import glob

import numpy as np

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

from query_tools import get_type_of_token, infix_to_postfix
from sympy import to_dnf

class BooleanModel():
    '''Boolean Model class for information retrieval'''

    def __init__(self, path, language) -> None:

        # path: path to the documents corpus
        self.corpus = path

        # documents: dictionary that links documents with the filename of the document
        self.documents = dict()

        # postings: ditionary that links terms with the documents that contain them
        # If the term "Goalkeeper" appears in documents 1 and 3, the postings in 'goalkeeper'
        # should be [1,3]
        self.postings = defaultdict(list)

        # language: language of the documents corpus (english, spanish)
        # Stop words are common words like ‘the’, ‘and’, ‘I’, etc. that are very
        # frequent in text, and so don’t convey insights into the specific topic
        # of a document. We can remove these stop words from the text in a given
        # corpus to clean up the data, and identify words that are more rare and
        # potentially more relevant to what we’re interested in.
        self.stopwords = set(stopwords.words(language))

        # stemmer: stemmer of the words in order to get better results
        # Stemming is a technique used to extract the base form of the words by
        # removing affixes from them. It is just like cutting down the branches
        # of a tree to its stems. For example, the stem of the words eating, eats,
        # eaten is eat. Search engines use stemming for indexing the words.
        self.stemmer = SnowballStemmer(language=language)

        # set of all the terms in the corpus
        self.vocabulary = set()

        self.__load_and_process_corpus()
    
    def __load_and_process_corpus(self):
        '''Load and process the corpus'''
        # counter for the documents
        if os.path.isfile(self.corpus+"doc_c.cache"):
            with open(self.corpus+"doc_c.cache", "r") as f:
                c_doc_id = int(f.read()) 
        else:
            c_doc_id = 1
                
        # gets all filepaths in the corpus
        for filepath in glob(self.corpus):
            # verify if the file has already been processed
            if os.path.isfile(filepath+".cache"):
                # load from cache
                with open(filepath+".cache", "r") as f:
                    text = f.read()
                text = text.split()
                doc_id = int(text[0])
                terms = text[1:]
            # opens and reads all files
            else:
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        if filepath.endswith(".cache"):
                            continue
                        text = file.read() 
                except(IsADirectoryError):
                    continue
                
                doc_id = c_doc_id
                c_doc_id += 1
            
                # replace punctuation with spaces
                text = re.sub(r"[^\w\s]", " ", text)
                
                # remove all special characters
                text = self.clean_text(text)
                text = self.remove_digits(text)
                
                # print(text)

                # tokenize the document text
                words = word_tokenize(text)

                # remove stopwords from the text
                words = [word.lower()
                        for word in words if word not in self.stopwords]

                # stem words in document
                # words = [self.stemmer.stem(word) for word in words]

                # get a list of all the unique terms
                terms = self.remove_duplicates(words)
                
                # write to cache
                with open(filepath+".cache", "w") as f:
                    f.write(str(doc_id) + " ")
                    f.write(" ".join(terms))
                # add all terms to the postings list
            for term in terms:
                self.postings[term].append(doc_id)

            # add doc to documents list for later indexing
            self.documents[doc_id] = os.path.basename(filepath)
            # increment doc_id for the next doc
            doc_id += 1
        # vocabulary:list with all the postings keys
        self.vocabulary = self.postings.keys()
        # write to doc_c.cache
        with open(self.corpus+"doc_c.cache", "w") as f:
            f.write(str(c_doc_id-1))
        return

    def query(self, query):
        ''' query the corpus documents using a boolean model
        :param query: valid boolean expression to search for in the documents
        :returns: a list of all marching documents
        '''

        # tokenize query and convert to postfix
        print(query)
        tokenized_query = word_tokenize(query)
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
        print(t_query)
        tokenized_query = infix_to_postfix(t_query)
        print("eval query")
        # eval query and return relevant documents
        return self.__eval_query(tokenized_query)

    def __eval_query(self, tokenized_query):
        ''' Evaluates the query with the preprovcessed corpus
        :param tokenized_query: list of tokens in the query (postfix form)
        :returns: list of relevant document names
        '''

        operands = []

        for token in tokenized_query:
            print(token)
            print()
            if get_type_of_token(token) == 3:
                right_op = operands.pop()
                left_op = operands.pop()

                
                result = self.__eval_operation(left_op, right_op, token)
                operands.append(result)
            else:
                # token = self.stemmer.stem(token.lower())
                operands.append(self.__bitvector(token))

        if len(operands) != 1:
            print("Malformed query or postfix expression")
            return list()
        # Find out documents corresponding to set bits in the vector
        matching_docs = [self.documents[i+1]
                         for i in np.where(operands[0])[0]]

        return matching_docs

    def __eval_operation(self, left, right, op):
        """Performs specified operation on the vectors 
        :param left: left operand
        :param right: right operand
        :param op: operation to perform
        :returns: result of the operation
        """
        
        if op == "&":
            return left & right
        elif op == "|":
            return left | right
        else:
            return 0
        
    def __bitvector(self,word):
        ''' make a bitvector from the word'''
        # Size of bit vector
        doc_count = len(self.documents)

        negate = False

        # If word is "~good"
        if word[0] == "~":
            negate = True
            word = word[1:]

        if word in self.vocabulary:
            # Word is in corpus, so make a bit vector for it
            bit_vector = np.zeros(doc_count, dtype=bool)

            # Locate query token in the dictionary and retrieve its postings
            posting = self.postings[word]

            # Set bit for doc_id in which query token is present
            for doc_id in posting:
                bit_vector[doc_id - 1] = True

            if negate:
                # Instance of NOT token,
                # bit vector is supposed to be inverted
                bit_vector = np.invert(bit_vector)

            # Return bit vector of the word
            return bit_vector

        else:
            # Word is not in corpus
            print(
                "Warning:",
                word,
                "was not found in the corpus!",
            )
            return np.zeros(doc_count, dtype=bool)

    def remove_duplicates(self, text):
        ''' removes duplicates from text'''

        return list(set(text))

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

