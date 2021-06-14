
"""
Created on Mon Mar 23 15:26:49 2020

@author: Celina
"""
import sys 

# Definition des Systempfades der PySuOpt Bibliothek


import pandas as pd

from ..outdoor_core.superstructure_sytem.superstructure import Superstructure
from . import wrapping_functions as WF



def wrapp_SystemData(dfi):
    
    """
    Description 
    -----------    

    - dfi = dataframe of the first spreadsheet "Systemblatt"
    - Ranges will be set for different "areas" in the spreadsheet
    - all other functions to set the parameters will be called

    Context 
    ----------
    function is called in get_DataFromExcel()
    set-functions are called in this function to fill the Super Structure 
    for all Systems-Information
    
    Parameters
    ----------
    dfi : Dataframe
    
    Return
    --------- 
    Superstructure Object with lists of the system parameters 
    
    """

    # Setting the Ranges

    GeneralDataRange = WF.convert_total('B', 4, 'C', 20)
    UtilitylistRange = WF.convert_total('S', 5, 'U', 8)
    ComponentlistRange = WF.convert_total('E', 5, 'K', 30)
    TemperatureIntervals = WF.convert_total('B', 34, 'B', 39)
    ReactionsListRange = WF.convert_total('N', 5, 'N', 15)
    ReactantsListRange = WF.convert_total ('P', 5,'P', 15) 
    TemperaturePriceRange = WF.convert_total('T', 14, 'U',18 )

    #####



    df1 = dfi.iloc[GeneralDataRange]


    df2 = dfi.iloc[UtilitylistRange] 

    df3 = dfi.iloc[ComponentlistRange]

    df5 = dfi.iloc[TemperatureIntervals]
    df6 = dfi.iloc[ReactionsListRange]


    df7 = dfi.iloc[ReactantsListRange] 


    df8= dfi.iloc [TemperaturePriceRange]



    # SET GENERAL DATA
    # -----------------

    obj = Superstructure(ModelName= df1.iloc[1,1], 
                         Objective= df1.iloc[2,1], 
                         MainProduct= df1.iloc[3,1], 
                         ProductLoad= df1.iloc[4,1])
    
    
    obj.set_numberProcessSteps(df1.iloc[5,1])
    obj.set_operatingHours(df1.iloc[6,1])
    obj.set_cecpi(df1.iloc[7,1])
    
    
    obj.set_interestRate(df1.iloc[8,1])
    
    obj.set_linearizationDetail(df1.iloc[9,1])
    obj.add_linearisationIntervals 
    
    obj.set_omFactor(df1.iloc[10,1])
    
    
    
    # Heat Pumo values
    
    if df1.iloc[11,1] == 'Yes':
        COP = df1.iloc[12,1]
        Costs = df1.iloc[13,1]
        Lifetime = df1.iloc[14,1]
        T_IN = df1.iloc[15,1]
        T_OUT = df1.iloc[16,1]
        
        obj.set_heatPump(Costs,
                         Lifetime,
                         COP,
                         T_IN,
                         T_OUT
                         )
    
    
    

    # ADD LISTS OF COMPONENTS, ETC.
    # ----------------------------
    liste = WF.read_list(df2,0)
    obj.add_utilities(liste)

    liste = WF.read_list(df3,0)
    obj.add_components(liste) 
    

    liste = WF.read_list(df6,0)
    obj.add_reactions(liste)

    liste = WF.read_list(df7,0)
    obj.add_reactants(liste) 
    
    dict1 = WF.read_type1(df3,0,1)
    obj.set_lhv(dict1)

    dict2  = WF.read_type1(df3,0,3)
    obj.set_mw(dict2) 




    # ADD OTHER PARAMETERS
    # ---------------------
    
    obj.set_deltaEL(df2.iloc[0,1])

    dict1 = WF.read_type1(df2,0,2)
    obj.set_utilityEmissionsFactor(dict1)
    
    dict1 = WF.read_type1(df3,0,4)
    obj.set_deltaRM(dict1)
    
    liste = WF.read_type1(df3,0,5)
    obj.set_componentEmissionsFactor(liste) 
    
    obj.set_deltaCool(df8.iloc[4,1])


    liste1 = WF.read_list(df8,0)
    liste2 = WF.read_list(df8,1)

  
    obj.set_heatUtilities(liste1, liste2)
    
    dict3 = WF.read_type1(df2,0,1)
    obj.set_deltaUt(dict3)

    
    
    return obj





