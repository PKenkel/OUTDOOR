# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:52:43 2020

@author: Celina
"""


import pandas as pd
import outdoor.excel_wrapper.Wrapping_Functions  as WF


def wrapp_GeneralData(obj, df1):   
    """
    Description 
    -----------     
    Get general Process Data: Lifetime and Group

    Context 
    ----------
    Function is called in Wrapp_ProcessUnits 
    
    Parameters
    ----------
    df1 : Dataframe which holds information of LT and Group
    
    """
    
    Name = df1.iloc[0,0]

    LifeTime = df1.iloc[4,0]

    ProcessGroup = df1.iloc[3,0]
    
    if not pd.isnull(df1.iloc[12,0]):
        emissions = df1.iloc[12,0]
    else:
        emissions = 0
       
    if not pd.isnull(df1.iloc[13,0]):
        
        maintenance_factor = df1.iloc[13,0]
    else: 
        maintenance_factor  = 0.044875
        
    cost_percentage  = None
    time_span  = None
    time_mode = 'No Mode'
    

    if not pd.isnull(df1.iloc[14,0]):
        cost_percentage = df1.iloc[14,0]
        time_span = df1.iloc[15,0]
        
        if df1.iloc[16,0] == 'Yearly':
            time_mode = 'Yearly'
        else:
            time_mode = 'Hourly'
            
    if not pd.isnull(df1.iloc[17,0]):
        full_load_hours = df1.iloc[17,0]
    else:
        full_load_hours = None

    obj.set_data_general(ProcessGroup, 
                         LifeTime, 
                         emissions,
                         full_load_hours,
                         maintenance_factor, 
                         cost_percentage, 
                         time_span, 
                         time_mode)
    if not pd.isnull(df1.iloc[20,0]):
        obj.add_PossibleSources(df1.iloc[20,0])
    
def wrapp_ReacionData(obj, df1, df2 = None):
    
    """
    Description 
    -----------     
    Get Reaction Data (Stoichiometric or Yield Function) from Excel sheet

    Context 
    ----------
    Function is called in Wrapp_ProcessUnits
     
    Parameters
    ----------
    df1 : Dataframe which either holds Stoichiometric or Yield Coefficents
    df2:  Dataframe which is either empty or holds conversion factors
    
    """
    
    if obj.Type == "Yield-Reactor":

        dict1  = WF.read_type1(df1,0,1)
        obj.add_xiFactors(dict1)  
        
    else:

        dict1 = WF.read_type2(df1,0,1,2)
        obj.add_gammaFactors(dict1)
        
        dict2 = WF.read_type2(df2,0,1,2)
        obj.add_thetaFactors(dict2)
        

def wrapp_EnergyData(obj, df, df2, df3):
    
    """
    Description 
    -----------
    Define specific columns from the spreadsheet to set the energydatas.
    Sets Demands, ReferenceFlow Types and Components for El, Heat1 and Heat2.
    But only if there are values in the Excel, if not, than these values are left
    as None
    
    Also: Calls wrapp_Temperatures, which sets Temperature and Tau for Heat

    Context 
    ----------
    Function is called in Wrapp.ProcessUnits
    
    Parameters
    ----------
    df  : Dataframe which holds inforation of energy demand and reference flow type
    df2 : Dataframe which holds information of reference flow components
    df3 : Dataframe which holds information on heat temperatures
    
    """
    

    # Set Reference Flow Type:
    
    if not pd.isnull(df.iloc[0,1]):
        ProcessElectricityDemand = df.iloc[0,1] 
        ProcessElectricityReferenceFlow = df.iloc[1,1]
        
        ProcessElectricityReferenceComponentList = WF.read_list_new(df2, 1, 2)
    else:
        ProcessElectricityDemand = 0
        ProcessElectricityReferenceFlow = None
        ProcessElectricityReferenceComponentList = []

        
    if not pd.isnull(df.iloc[0,2]):
        ProcessHeatDemand = df.iloc[0,2]
        ProcessHeatReferenceFlow = df.iloc[1,2]
        ProcessHeatReferenceComponentList = WF.read_list_new(df2, 2, 2)
    else:
        ProcessHeatDemand = None
        ProcessHeatReferenceFlow = None
        ProcessHeatReferenceComponentList = []

        
    if not pd.isnull(df.iloc[0,3]):
        ProcessHeat2Demand = df.iloc[0,3]
        ProcessHeat2ReferenceFlow = df.iloc[1,3]
        ProcessHeat2ReferenceComponentList = WF.read_list_new(df2, 3, 2)
    else:
        ProcessHeat2Demand = None
        ProcessHeat2ReferenceFlow = None
        ProcessHeat2ReferenceComponentList = []
        

    wrapp_Temperatures(obj, df3, df)    
    
    obj.set_data_energy(None,
                        None,
                        ProcessElectricityDemand,
                        ProcessHeatDemand,
                        ProcessHeat2Demand,
                        ProcessElectricityReferenceFlow,
                        ProcessElectricityReferenceComponentList,
                        ProcessHeatReferenceFlow,
                        ProcessHeatReferenceComponentList,
                        ProcessHeat2ReferenceFlow,
                        ProcessHeat2ReferenceComponentList
                        )
    
def wrapp_Temperatures(obj, df1, df2): 
    """
    Description
    -----------
    Set Process Temperatures and specific energy demand (tau) from Excel file
    If no Temperatures and tau are defined everything is set to None
    
    Sets Tau1 and Tau2 only if the values are really available, otherwise
    Temperatures and Tau values are set to None
    

    Parameters
    ----------
    obj : Process unit object
    
    df1 : Dataframe holding the information about the Temperatures needed

    df2 : Dataframe holding the inforamation about specific energy damand
    
    """
    

    obj.set_Temperatures()
    
    if not pd.isnull(df2.iloc[0,2]):
        TIN1 = df1.iloc[7,0]
        TOUT1 = df1.iloc[8,0]
        tau1 = df2.iloc[0,2]
        obj.set_Temperatures(TIN1, TOUT1, tau1) 
    
    if not pd.isnull(df2.iloc[0,3]):
        tau2 = df2.iloc[0,3] 
        TIN2 = df1.iloc[9,0]
        TOUT2 = df1.iloc[10,0]       
        obj.set_Temperatures(TIN1, TOUT1, tau1, TIN2, TOUT2, tau2)
   
 
def wrapp_AdditivesData(obj,df1, df2, df3):
    
    """
    Description 
    -----------
    Define specific columns from the spreadsheet to set the added Input-flows  
    Define specific columns from the spreadsheet to set the concentration datas

    Context 
    ----------
    function is called in Wrapp.ProcessUnits
    
    Parameters
    ----------
    df1 : Dataframe
    df2 : Dataframe    
    
    """   
    
    additional_flow_composition_1 = {}
    additional_flow_composition_2 = {}

    req_concentration = None
    upper_limit_1 = 10000
    upper_limit_2 = 10000
    
    
    
    for x in range(len(df1)):
        if  df1.iloc[x,2] == 'phi1':
            additional_flow_composition_1[df1.iloc[x,0]] = df1.iloc[x,3]

        else:
            if not pd.isnull(df1.iloc[x,0]):
                additional_flow_composition_2[df1.iloc[x,0]] = df1.iloc[x,3]
    
    

    if not pd.isnull(df1.iloc[0,1]): 
        upper_limit_1 = df1.iloc[0,1]
               
    if not  pd.isnull(df1.iloc[1,1]): 
        upper_limit_2 = df1.iloc[1,1]
        

    lhs_comp_list = WF.read_list (df2,1)
    
    rhs_comp_list = WF.read_list (df2,3)

    lhs_ref_flow = df2.iloc[0,0]

    rhs_ref_flow = df2.iloc[0,2]


    if not pd.isnull(df2.iloc[0,4]):
        req_concentration = df2.iloc[0,4]
        
    myu_dict = WF.read_type2 (df3,0,1,2)
   
    
    obj.set_data_flow(req_concentration,
                      additional_flow_composition_1,
                      additional_flow_composition_2,
                      rhs_ref_flow,
                      lhs_ref_flow,
                      rhs_comp_list,
                      lhs_comp_list,
                      myu_dict,
                      upper_limit_1,
                      upper_limit_2                     
                      )


def wrapp_EconomicData(obj, df, df2):
    
    """
    Description 
    -----------
    Get Economic information from Excel Sheet Colomns defined in df and df2

    
    Context
    -----------
    Function is called in Wrapp.ProcessUnits 
    
    
    Parameters
    ----------
    df  : Dataframe with economic CAPEX Factors and Components List
    df2 : Dataframe with General Factors for Direct and Indirect Costs 
         
     """  
    
    ReferenceCosts = df.iloc[0,1]
    ReferenceFlow = df.iloc[1,1]
    CostExponent = df.iloc[2,1]
    ReferenceYear= df.iloc[3,1]
    
    DirectCostFactor = df2.iloc[5,0] 
    
    IndirectCostFactor = df2.iloc[6,0]
    
    ReferenceFlowType = df.iloc[4,1]
    
    ReferenceFlowComponentList = WF.read_list_new(df, 1, 5)

    
    
    # Set Economic Data in Process Unit Object
    
    obj.set_data_economic(DirectCostFactor,
                          IndirectCostFactor,
                          ReferenceCosts,
                          ReferenceFlow,
                          CostExponent,
                          ReferenceYear,
                          ReferenceFlowType,
                          ReferenceFlowComponentList
                          )
    
     
 
def wrapp_ProductpoolData(obj, series): 
    
    """ 
    Description 
    ----------- 
    Define specific columns from the 
    spreadsheet Productpool to set Productname, Productprice and Producttype

    Context 
    ----------
    function is called in Wrapp_ProcessUnits
    
    Parameters
    ----------
    df : Dataframe
    
    """
            
         
        
    obj.ProductName= series[4]
    obj.set_ProductPrice(series[8])
    obj.ProductType = series[9] 
    obj.set_Group(series[7])
    
    EmissionCredits = 0
    
    if not pd.isnull(series[10]):
        EmissionCredits = series[10]

    obj.set_EmissionCredits(EmissionCredits)    
 
    
def wrapp_SourceData(obj, series, df, counter):
    
    dic = {}
    
    dic = WF.read_type1(df, 0 , counter)
    
    UpperLimit = 100000
    Costs = 0
    
    if not pd.isnull(series[7]):
        UpperLimit = series[7]

        
    
    if not pd.isnull(series[6]):
        Costs = series[6]
        
        
    obj.set_data_source(Costs,
                        UpperLimit,
                        Composition_dictionary  = dic
                        )
    


