from pyomo.environ import *
import datetime

import os


from .post_processor import searchTechnologies
from .post_processor  import searchEnergyExchange
from .post_processor import writeFormatting
import cloudpickle as pic


def Save_CaseStudy(Instance, ModelInformation, Resultspath):
    case_time = datetime.datetime.now()   
    case_time = str(case_time)
    
    if not  os.path.exists(Resultspath):
        os.makedirs(Resultspath)
        
    Resultspath = Resultspath + case_time + '.txt'
    Inputpath = Resultspath + case_time + 'inputdata.txt'
    
    
    write_Case(ModelInformation, Resultspath, Inputpath, case_time)
    write_BasicResults(Instance, Resultspath)
    write_EnergyBalanceResults(Instance, Resultspath, ModelInformation)


def write_Case(ModelInformation, Resultspath, Inputpath, case_time):    
    
    run_time = ModelInformation['Run Time']
    solver_name = ModelInformation['Solver']
    data_file = ModelInformation['Data File'][None]
    case_identifier = ModelInformation['Superstructure'].ModelName
    

    
    try: 
        
        nf = open(Resultspath, encoding='utf-8', mode='w')  
        nf.write('------------- \n')
        nf.write('------------- \n')
        nf.write('CASE STUDY \n')
        nf.write('------------- \n')
        nf.write(f'Identifier: {case_identifier} \n')
        nf.write('------------- \n')
        nf.write(f'Number: {case_time} \n')
        nf.write('------------- \n \n')
        nf.write(f'Runtime: {run_time} sec. \n')
        nf.write('------------- \n \n')
        nf.write(f'Solver Name: {solver_name} \n')
        nf.write('------------- \n \n')
        nf.write('END OF CASE STUDY \n')
        nf.write('------------- \n')
        nf.write('------------- \n \n')
    except IOError:
        print('Es gab einen Fehler beim Schreiben der Model Informations')
        
    
    try:
        nf2 = open(Inputpath, encoding='utf-8', mode='w')
        nf.write('------------- \n')
        nf2.write('CASE STUDY \n')
        nf2.write('------------- \n')
        nf2.write('------------- \n')
        nf2.write(f'Number: {case_time} \n')
        nf2.write('------------- \n \n')
        nf2.write(f'Input Data File: \n')
        for k in data_file.keys():
            nf2.write(f'{k}: {data_file[k]} \n \n')
        nf2.write('------------- \n \n')
        nf2.write('END OF CASE STUDY \n')
        nf2.write('------------- \n')
        nf2.write('------------- \n \n ')
    except IOError:
        print('Es gab einen Fehler beim Schreiben der InputDaten')






def write_BasicResults(Instance, Resultspath):
    
    technology_names = Instance.Names.extract_values()
    chosen_technologies = searchTechnologies(Instance)
    tac = value(Instance.TAC)/1000000
    capex = value(Instance.CAPEX)/1000000
    opex = value(Instance.OPEX)/1000000
    profits = value(Instance.PROFITS_TOT)/1000000
    npc = value(Instance.TAC)/ value(Instance.MainProductFlow)
    npe = value(Instance.GWP_TOT) / value(Instance.MainProductFlow)
    
    
    try:
        nf = open(Resultspath, encoding='utf-8', mode='a')
        nf.write('------------- \n')
        nf.write('------------- \n')
        nf.write('KEY FIGURE RESULTS \n')
        nf.write('------------- \n')
        nf.write('------------- \n \n')
        nf.write(f' The net present production costs are {npc} €/ton \n')
        nf.write('------------- \n \n')
        nf.write(f' The net present production emissions are {npe} ton/ton \n')
        nf.write('------------- \n \n')
        nf.write(f' The total annualized costs (TAC) are {tac} mio.€ \n')
        nf.write('------------- \n \n')
        nf.write(f' The capital costs (CAPEX) are {capex} mio. € \n')
        nf.write('------------- \n \n')
        nf.write(f' The operational costs (OPEX) are {opex} mio. € \n')
        nf.write('------------- \n \n')
        nf.write(f' The profits are {profits} mio. € \n')
        nf.write('------------- \n \n')
        nf.write(f'Considered Technologies are: \n')
        nf.write('------------- \n')
        for k in technology_names.keys():
            nf.write(f' {k}: {technology_names[k]} \n')  
        nf.write('------------- \n \n')    
        nf.write(f'Chosen Technologies are: \n')
        nf.write('------------- \n')
        for k in chosen_technologies.keys():
            nf.write(f' {k}: {chosen_technologies[k]} \n')
        nf.write('------------- \n \n')
        nf.write('END OF BASIC RESULTS \n')
        nf.write('------------- \n')
        nf.write('------------- \n \n')
        

        
        
    except IOError:
        print('Es gab einen Fehler beim schreiben der Basic Results')
    


def write_EnergyBalanceResults(Instance, Resultspath, ModelInformation):
    
    Superstructure = ModelInformation['Superstructure']
    
    cooling_demand_interval  = Instance.ENERGY_DEMAND_HEAT.extract_values()
    heat_demand_interval = Instance.ENERGY_DEMAND_COOL.extract_values()
    
    cooling_demand = Instance.ENERGY_DEMAND_COOL_UNIT.extract_values()
    heat_demand = Instance.ENERGY_DEMAND_HEAT_UNIT.extract_values()
    
    coolingwater_demand = value(Instance.ENERGY_DEMAND_COOLING)
    heat_prod_sell = value(Instance.ENERGY_DEMAND_HEAT_PROD_SELL)
    heat_prod_use = value(Instance.ENERGY_DEMAND_HEAT_PROD_USE)
    
    heat_demand_tot = Instance.ENERGY_DEMAND_HEAT_DEFI.extract_values()
    hp_use =  value(Instance.ENERGY_DEMAND_HP_USE)
    # el_demand = Instance.ENERGY_DEMAND['Electricity'].extract_values()
    heat_exchange = searchEnergyExchange(Instance, Superstructure)
    
    try:
        nf = open(Resultspath, encoding='utf-8', mode='a')
        
        nf.write('------------- \n')
        nf.write('------------- \n')          
        nf.write('ENERGY BALANCE RESULTS \n')
        nf.write('------------- \n')
        nf.write('------------- \n')  
    
        writeFormatting('The cooling demand of different units are', nf)
        for k in cooling_demand.keys():
            nf.write(f'{k} : {cooling_demand[k]} \n')

        writeFormatting('The heating demand of different units are', nf)        
        for k in heat_demand.keys():
            nf.write(f'{k} : {heat_demand[k]} \n')

        writeFormatting('The cooling demand of different units on intervals are' , nf)
        for k in cooling_demand_interval.keys():
            nf.write(f'{k} : {cooling_demand_interval[k]} \n')

        writeFormatting('The or heat demand of different units on intervals are',nf)        
        for k in cooling_demand_interval.keys():
            nf.write(f'{k} : {heat_demand_interval[k]} \n')

        writeFormatting('The exchanged heat on different temperature intervals is',nf)
        for k in heat_exchange.keys():
            nf.write(f' {k}: {heat_exchange[k]} \n')

        writeFormatting('The steam demand and in total are',nf)
        for k in heat_demand_tot.keys():
            nf.write(f'{k} : {heat_demand_tot[k]} \n')

        writeFormatting('The cooling water demand is',nf)
        nf.write(f' {coolingwater_demand} \n')
        
        writeFormatting('The produced heat is',nf)
        nf.write(f' {heat_prod_sell} \n')

        writeFormatting('The produced heat used is',nf)
        nf.write(f' {heat_prod_use} \n')

        # writeFormatting('The electricity demand for different untis is ',nf)
        # for k in el_demand.keys():
        #     nf.write(f'{k} : {el_demand[k]} \n')
            
            
        nf.write('------------- \n')     
        nf.write('------------- \n \n')  
        

        
        
        
        
        
        nf.write('------------- \n \n')
        nf.write(f' The used electricity for the heat pump is {hp_use} \n')
        nf.write('------------- \n \n')
        nf.write('END OF ENERGY BALANCE RESULTS \n')
        nf.write('------------- \n')
        nf.write('------------- \n \n')
        


    except IOError: 
        print('Es gab einen Fehler beim schreiben der Energy Balance Results')
    


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
        
    

