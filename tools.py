import os

def get_size(file):
    size = os.path.getsize('./static/corpus/'+file)
    return round(size/(1024**2),2)