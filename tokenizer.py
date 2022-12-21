
from abc import ABC, abstractmethod
import re
# import spacy 
# import stanza 
# import spacy_stanza
# from negspacy.negation import Negex
# from negspacy.termsets import termset 

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class Tokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str) -> list:
        pass


class NltkTokenizer(Tokenizer):
    def __init__(self, language) -> None:
        self.stopwords = set(stopwords.words(language))
        self.stemmer = SnowballStemmer(language=language)
        self.lemmatizer = WordNetLemmatizer()

    def tokenize(self, text: str) -> list:
        # replace punctuation with spaces
        text = re.sub(r"[^\~\w\s]", " ", text)
        # remove all special characters
        # text = self.clean_text(text)
        text = self.remove_digits(text)
        # tokenize the document text
        words = word_tokenize(text)
        # remove stopwords from the text
        words = [word.lower() for word in words if word not in self.stopwords]
        # stem words in document
        words = [self.lemmatizer.lemmatize(word) for word in words]
        return words

    def remove_digits(self, text):
        ''' removes digits from text'''
        regex = re.compile(r"\d") 
        # Replace and return
        return re.sub(regex, "", text)

    def clean_text(self, text):
        ''' removes special characters from text'''
        print("text", text)
        text = text.replace(",.;:", " ")  
        # Regex pattern for a word
        regex = re.compile(r"[^\~\|\&a-zA-Z0-9\s]")
        # Replace and return
        return re.sub(regex, "", text)


# # Ignore this class for now
# class SpacyTokenizer(Tokenizer):
#     def __init__(self) -> None:
#         self.nlp_model = spacy_stanza.load_pipeline('en', download_method='REUSE_RESOURCES')
        

#     def tokenize(self, text: str) -> list:
#         tokenized_text = self.nlp_model(text)
#         return [token.lemma_.lower() for token in tokenized_text if not token.lemma_.lower()=='\n' and not token.is_punct and not token.is_stop]


