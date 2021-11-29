# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:25:35 2020


@author: Celina geändert am 01.09.2020: 
    Templates werden nicht eingelesen genauso wie "Tabelle1" sondern nur die neu hinzugefügten Tabellen
"""

import pandas as pd

from .wrapp_processes import wrapp_processUnits
from .wrapp_processes import wrapp_productPoolUnits
from .wrapp_processes import wrapp_sourceUnits
from .wrapp_processes import wrapp_distributors


from .wrapp_system import wrapp_SystemData

# function for Pandafunction to read an excelfile:

def get_DataFromExcel(PathName=None):
    
    """
    Description 
    -----------    
    - Function to read all spreadsheets of an exceldata  
    - put data from excel in Super Structure
    - One spreadsheet = one process 
    - Hidden spreadsheets with the name: 
      Tabelle1, Template_CC, Template_Stö, etc. will be skipped 
    
    Context 
    ----------
    -wrapp.ProcessUnits: to fill the Super Structure for all processes
    -wrapp.SystemData: to fill the Super Structure with the system datas
    -add_Units: add Process(Object) to Objectlist 
    
    Parameters
    ----------
    PathName : String, Path to Exceldata
        
    Returns
    -------
    Superstructure_Object  
    
    """

    datframe = pd.read_excel(PathName, sheet_name = None)

    PU_ObjectList  =[]

    ## Hidden tables with specific names will be skipped:
    Hidden_Tables = []
    Hidden_Tables.append('Template_PhysicalProcess')
    Hidden_Tables.append('Template_StoichReactor')
    Hidden_Tables.append('Template_YieldReactor')
    Hidden_Tables.append('Template_SteamGenerator')
    Hidden_Tables.append('Template_ElGenerator')
    Hidden_Tables.append('Template_ProductPool')
    Hidden_Tables.append('DataBank')
        
        
    for i in datframe.keys():
        if i == 'Systemblatt':
            Superstructure_Object = wrapp_SystemData(datframe[i])
        elif i in Hidden_Tables:
            continue
        elif i == "Pools":
            pools = wrapp_productPoolUnits(datframe[i])
            for k in pools:
                PU_ObjectList.append(k)
        elif i == "Sources":
            sources = wrapp_sourceUnits(datframe[i])
            for k in sources:
                PU_ObjectList.append(k)
        elif i == 'Distributor':
            distributors = wrapp_distributors(datframe[i])
            for k in distributors:
                PU_ObjectList.append(k)
        else:
            PU_ObjectList.append(wrapp_processUnits(datframe[i]))

              

         
    Superstructure_Object.add_UnitOperations(PU_ObjectList)

    return Superstructure_Object


