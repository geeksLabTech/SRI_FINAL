import os

def get_size(file):
    try:
        size = os.path.getsize('./static/corpus/'+str(file))
    except:
        size = 0
    return round(size/(1024**2),2)