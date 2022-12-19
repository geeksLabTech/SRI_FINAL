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
            assert len(words) > 0
            trie.insert_document(words, doc_id)
            words_frequency = Counter(words)
            doc_data = DocumentData(os.path.basename(filepath), len(words), max(words_frequency.values()))
            current_documents[doc_id] = doc_data
            doc_id += 1
        
        return trie, current_documents


    def load_from_ir_datasets(self, dataset_name: str, trie: Trie, current_documents: dict[int, DocumentData]) -> tuple[Trie, dict[int, DocumentData]]:
        dataset = ir_datasets.load(dataset_name)
        doc_id = len(current_documents) + 1
        for doc in dataset.docs_iter():
            if doc.text == '':
                print('empty doc', doc.doc_id)
                continue
            
            words = self.tokenizer.tokenize(doc.text+doc.title)
            assert len(words) > 0
            trie.insert_document(words, doc_id)
            words_frequency = Counter(words)
            doc_data = DocumentData(doc.doc_id, len(words), max(words_frequency.values()))
            current_documents[doc_id] = doc_data
            doc_id += 1
        
        return trie, current_documents
