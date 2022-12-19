
class DocumentData:
    def __init__(self, path: str, title:str, id:int, lenght: int, max_frequency_term: int) -> None:
        self.path = path
        self.title = title
        self.id = id
        self.length = lenght
        self.max_frequency_term = max_frequency_term
