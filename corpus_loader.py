from glob import glob
import os
from document_data import DocumentData
from tokenizer import Tokenizer
from trie import Trie



class CorpusLoader:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self.tokenizer = tokenizer

    # TODO - implement cache
    def load(self, path, trie: Trie, current_documents: dict[int, DocumentData]) -> tuple[Trie, dict[int, DocumentData]]:
        doc_id = len(current_documents) + 1
        for filepath in glob(path):
            # opens and reads all files
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    readed_file = file.read()
            except(IsADirectoryError):
                print("IsADirectoryError")
            
            words = self.tokenizer.tokenize(readed_file)
            trie.insert_document(words, doc_id)
            words_frequency = [word.count() for word in words]
            doc_data = DocumentData(os.path.basename(filepath), len(words), max(words_frequency))
            current_documents[doc_id] = doc_data
            doc_id += 1
        
        return trie, current_documents

