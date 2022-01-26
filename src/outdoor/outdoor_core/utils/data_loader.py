import cloudpickle as pic
import os 
import sys
import pickle5 as pic5
import time


a = os.path.dirname(__file__)
a = os.path.dirname(a)
a = os.path.dirname(a)
a = os.path.dirname(a)

sys.path.append(a)


import outdoor


def load_file(path):
    t1 = time.time()
    _path = path
    
    process_design = None

    
    with open(_path, "rb") as file:
        process_design = pic5.load(file)
        
    t2 = time.time()
    t = t2-t1
    print(f'total time was {t} seconds')
    return process_design

        
    

            
            
            