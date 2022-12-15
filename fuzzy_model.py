from boolean_model import BooleanModel
from sympy import to_dnf, sympify
from trie import Trie
class FuzzyModel(BooleanModel):


    def __init__(self,path,language , trie: Trie):
        super().__init__(path,language)
        self.fuzzy = True
        self.trie = trie
    
    
        

    def eval_query(self,tokenized_query):
        correlation_matrix = self.build_correlation_matrix()

    def build_correlation_matrix(self):
        correlation_matrix ={}
        for node in self.trie:
            



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