from pyomo.environ import *

    
def searchTechnologies(Instance):
    CT = dict()
    
    for i in Instance.Y:
        if value(Instance.Y[i]) == 0:
            CT[i] = 'Not Chosen'
        else:
            if value(Instance.FLOW_SUM[i]) <= 0.000001 :
                CT[i] = 'Not Chosen'
            else:
                CT[i] = 'Chosen'
                
    return CT


def searchEnergyExchange(Instance, Superstructure):
    EX = dict()
    
    for i in Instance.ENERGY_EXCHANGE:
        t_up = Superstructure.HeatIntervals[i]
        t_low = Superstructure.HeatIntervals[i-1]
        EX[t_up,t_low]  = value(Instance.ENERGY_EXCHANGE[i])
        
    return EX
    
        
def printFormatting(title):
    print('')
    print('')
    print(title)
    print('---------------')
    

def writeFormatting(title,file):
    file.write(' \n')
    file.write(' \n')
    txt_str =   title  + ':' + '\n'
    file.write(txt_str)
    file.write('------------------- \n')