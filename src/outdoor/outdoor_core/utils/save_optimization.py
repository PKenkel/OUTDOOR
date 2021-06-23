# from pyomo.environ import *
import datetime

import os


from .save_singleCase import write_singleCase
from .save_multiCase import write_multiCase


import cloudpickle as pic


def save_caseStudy(ResultsFile, 
                   ModelInformation, 
                   Resultspath):
    
    
    case_time = datetime.datetime.now()   
    case_time = str(case_time)
    
    if not  os.path.exists(Resultspath):
        os.makedirs(Resultspath)
        
    Resultspath = Resultspath + case_time + '.txt'
    Inputpath = Resultspath + case_time + 'inputdata.txt'
    
    if type(ResultsFile) == dict:
        write_multiCase(ResultsFile, 
                        ModelInformation, 
                        Resultspath, 
                        Inputpath, 
                        case_time)        
    else:
        write_singleCase(ResultsFile, 
                         ModelInformation, 
                         Resultspath, 
                         Inputpath,
                         case_time)







def save_dict_to_file(path_name, ModelInformation):
    case_time = datetime.datetime.now()   
    case_time = str(case_time)
    
    if not  os.path.exists(path_name):
        os.makedirs(path_name)
        
    path_name = path_name + case_time + '.txt'
        
    data = ModelInformation['Data File']
    f = open(path_name,'w')
    f.write(str(data))
    f.close()





def load_dict_from_file(path_name):
    f = open(path_name,'r')
    data=f.read()
    f.close()
    return eval(data)




def save_instanceAsFile(Instance, path_name):
    case_time = datetime.datetime.now()   
    case_time = str(case_time)
    path_name = path_name + case_time + '.pkl'
    
    with open(path_name, 'wb') as output:
        pic.dump(Instance, output)


