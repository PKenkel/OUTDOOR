# To Dos
# - Chance Input Reading of PHI1 and PHI2 , but also change this in the Excel
#   sheet



# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:56:00 2020

@author: Celina
"""

import pandas as pd
from ..outdoor_core.Block_Process import *
from .Wrapp_UnitData import *
import outdoor.excel_wrapper.Wrapping_Functions  as WF



def wrapp_processUnits(dfi):
    
    """  
    Description 
    -----------
    - dfi = completely dataframe of one spreadsheet for one process
    - Function defines all ranges for the different "areas" in one spreadsheet
    - processclass will be set  
    - Depending on the process class, function to set the other parameters will be called

    Context 
    ---------- 
    function is called in get_DataFromExcel()
    
    Parameters
    ----------
    dfi : Dataframe 
    
    """


    # Set the Excel Ranges
    GeneralDataRange = WF.convert_total ('E', 10, 'E', 30)
    EnergyDataRange = WF.convert_total('M', 10, 'P', 30)
    KappaUtRange = WF.convert_total('M', 10, 'P', 30)
    BalanceDataRange= WF.convert_total('S', 10, 'U', 30)
    EconomicDataRange= WF.convert_total('H', 11, 'I', 30)
    
    PossibleSourcesRange = WF.convert_total('W', 10, 'W', 27)
    
    ConcDataRange = WF.convert_total2('B', 10, 'F', 30)
    GammaDataRange = WF.convert_total2('H', 10,'J', 30)
    ThetaDataRange = WF.convert_total2('L', 10, 'N', 30)
    XiDataRange = WF.convert_total2('H', 10, 'J',30)



    process_class = dfi.iat[10,4]   

    if process_class == "Stoich.Reactor":
        
        obj = StoichReactor(dfi.iat[8,4],dfi.iat [9,4])  
        wrapp_EnergyData(obj, dfi.iloc[EnergyDataRange], dfi.iloc[KappaUtRange], dfi.iloc[GeneralDataRange])
        wrapp_ReacionData(obj, dfi.iloc[GammaDataRange], dfi.iloc[ThetaDataRange]) 


    elif process_class == "Yield.Reactor":
        
        obj = YieldReactor(dfi.iat[8,4],dfi.iat[9,4])
        wrapp_EnergyData(obj, dfi.iloc[EnergyDataRange], dfi.iloc[KappaUtRange], dfi.iloc[GeneralDataRange])
        wrapp_ReacionData(obj, dfi.iloc[XiDataRange])

        
    elif process_class == "Heat.Generator":
        
        obj = HeatGenerator(dfi.iat[8,4],dfi.iat[9,4], Efficiency = dfi.iat[19,4])
        wrapp_ReacionData(obj, dfi.iloc[GammaDataRange], dfi.iloc[ThetaDataRange])       
        
    elif process_class == "Elect.Generator":
        
        obj =  ElectricityGenerator(dfi.iat[8,4],dfi.iat[9,4], Efficiency = dfi.iat[19,4])
        wrapp_ReacionData(obj, dfi.iloc[GammaDataRange], dfi.iloc[ThetaDataRange])


    # everything else is a splitter for now
    else:
        
        obj = PhysicalProcess(dfi.iat[8,4],dfi.iat[9,4]) 
        wrapp_EnergyData(obj, dfi.iloc[EnergyDataRange], dfi.iloc[KappaUtRange], dfi.iloc[GeneralDataRange])
        
    wrapp_GeneralData(obj, dfi.iloc[GeneralDataRange])
    wrapp_EconomicData(obj, dfi.iloc[EconomicDataRange], dfi.iloc[GeneralDataRange])
    wrapp_AdditivesData(obj,  dfi.iloc[PossibleSourcesRange], dfi.iloc[ConcDataRange] ,dfi.iloc[BalanceDataRange])

    return obj


def wrapp_productPoolUnits(dfi):
    
    DataRange = WF.convert_total ('D', 6, 'K', 12)
    DataFrame = dfi.iloc[DataRange]
    PoolList = []
    
    
    for index, series in DataFrame.items():
        if not pd.isnull(series[4]):
            obj = ProductPool(series[4], series[5])
            wrapp_ProductpoolData(obj, series)
            PoolList.append(obj)

    return PoolList
    
  
    


def wrapp_sourceUnits(dfi):
    GeneralDataRange = WF.convert_total('E',6,'O',10)
    CompositionDataRange  = WF.convert_total('D', 12, 'O', 23)
    SourcesList = []
    
    
    df1 = dfi.iloc[GeneralDataRange]
    df2 = dfi.iloc[CompositionDataRange]
    counter = 1
    
    for index, series in df1.items():
        if not pd.isnull(series[4]):

            obj = Source(series[4], series[5])
            wrapp_SourceData(obj, series, df2, counter)
            SourcesList.append(obj)
            counter += 1 
            
    return SourcesList


def wrapp_distributors(dfi):
    DataRange = WF.convert_total('E',6,'O',23)
    distributor_list = []
    
    df1 = dfi.iloc[DataRange]
    
    counter = 3
    
    for index,series in df1.items():
        if not pd.isnull(series[4]):
            obj = Distributor(series[4], series[5])
            wrapp_DistributorData(obj, series, df1, counter)
            distributor_list.append(obj)
            
    return distributor_list
            
        
    



