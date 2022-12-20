from glob import glob
import os
from collections import Counter

from document_data import DocumentData
from tokenizer import Tokenizer
from trie import Trie
import ir_datasets



class CorpusLoader:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer

    # TODO - implement cache
    def load_from_path(self, path, trie: Trie, current_documents: dict[int, DocumentData]) -> tuple[Trie, dict[int, DocumentData]]:
        doc_id = len(current_documents) + 1
        for filepath in glob(path):
            # opens and reads all files
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    readed_file = file.read()
            except(IsADirectoryError):
                print("IsADirectoryError")
            
            words = self.tokenizer.tokenize(readed_file)
            if len(words) > 0:
                trie.insert_document(words, doc_id)
                words_frequency = Counter(words)
                doc_data = DocumentData(os.path.basename(filepath), os.path.basename(filepath), doc_id, len(words), max(words_frequency.values()))
                current_documents[doc_id] = doc_data
                doc_id += 1
        trie.documents = current_documents
        return trie, current_documents


    def load_from_ir_datasets(self, dataset_name: str, trie: Trie, current_documents: dict[int, DocumentData]) -> tuple[Trie, dict[int, DocumentData]]:
        dataset = ir_datasets.load(dataset_name)
        # doc_id = len(current_documents) + 1
        for doc in dataset.docs_iter():
            if doc.text == '':
                print('empty doc', doc.doc_id)
                continue
            
            words = self.tokenizer.tokenize(doc.text+doc.title)
            assert len(words) > 0
            trie.insert_document(words, doc.doc_id)
            words_frequency = Counter(words)
            doc_data = DocumentData(doc.doc_id, doc.title, doc.doc_id, len(words), max(words_frequency.values()))
            current_documents[doc.doc_id] = doc_data
            # doc_id += 1
        trie.documents = current_documents
        return trie, current_documents

    def new_load_from_ir_datasets(self, dataset_name: str, current_vocabulary: dict[str, dict[int,int]], current_documents: dict[int, DocumentData]):
        dataset = ir_datasets.load(dataset_name)
        for doc in dataset.docs_iter():
            if doc.text == '':
                print('empty doc', doc.doc_id)
                continue
            words = self.tokenizer.tokenize(doc.text+doc.title)
            max_word_frequency = 0
            assert len(words) > 0
            doc_id = int(doc.doc_id)
            
            for word in words:
                if word not in current_vocabulary:
                    current_vocabulary[word] = {}
                if doc_id not in current_vocabulary[word]:
                    current_vocabulary[word][doc_id] = 0
                current_vocabulary[word][doc_id] += 1
                max_word_frequency = max(max_word_frequency, current_vocabulary[word][doc_id])

            doc_data = DocumentData('', doc.title, doc_id, len(words), max_word_frequency)
            current_documents[doc_id] = doc_data

        return current_vocabulary, current_documents
