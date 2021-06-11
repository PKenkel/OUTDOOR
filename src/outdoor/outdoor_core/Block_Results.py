from pyomo.environ import *

from .Block_Processing import searchTechnologies
from .Block_Processing import searchEnergyExchange
from .Block_Processing import printFormatting




def displayBasicResults(Instance):
    print('')
    print('')
    print('---------------')
    print('---------------')
    print('KEY FIGURE RESULTS')
    print('---------------')
    print('---------------')
    
    printFormatting('The chosen Technologies are:')
    CT = searchTechnologies(Instance)
    for i,j in CT.items():
        print(i, j)
        
    printFormatting('Total Costs are (in M€)')  
    print(value(Instance.TAC)/1000000)

    printFormatting('Total CAPEX are (in M€)')
    print(value(Instance.CAPEX)/1000000)
    
    printFormatting('Total OPEX are (in M€)')
    print(value(Instance.OPEX)/1000000)
    
    printFormatting('Total PROFITS are (in M€)')
    print(value(Instance.PROFITS_TOT)/1000000)
    
    printFormatting('Net Production Costs are')
    NPC  = value(Instance.TAC)/ value(Instance.MainProductFlow)
    print(NPC)
    
    printFormatting('Net Production Emissions are')
    NPE  = value(Instance.GWP_TOT)/ value(Instance.MainProductFlow)
    print(NPE)
    
    print('')
    print('')
    print('KEY FIGURE SECTION END')
    

    

    
def displayHeatBalanceResults(Instance,Info):
    Superstructure = Info['Superstructure']
    
    print('')
    print('')
    print('---------------')
    print('---------------')
    print('ENERGY BALANCE RESULTS')
    print('---------------')
    print('---------------')
    
    printFormatting('Exchanged Heat:')
    EX = searchEnergyExchange(Instance,Superstructure)
    for i,j in EX.items():
        print(i,j)
        
    printFormatting('Additional supplied heat and cooling energy is')
    Instance.ENERGY_DEMAND_HEAT_DEFI.pprint()
    
    printFormatting('Energy provided by high temperature heat pumpt is:')
    Instance.ENERGY_DEMAND_HP_USE.pprint()
    
    # printFormatting('Used Electricity:')
    # Instance.ENERGY_DEMAND_EL.pprint()
    
    print('')
    print('')
    print('ENERGY BALANCE SECTION END')
    