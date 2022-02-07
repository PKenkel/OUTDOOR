#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""
from ....utils.linearizer import capex_calculator
    



def change_capital_costs(Instance, Parameter, Value, Index = None, Superstructure = None):
    
    for i in Superstructure.UnitsList:
        if i.Number == Index:
            unit_operation = i
            unit_operation.CAPEX_factors['C_Ref'][Index] = Value
            (x_vals,y_vals) = capex_calculator(unit_operation, Superstructure.CECPI,Superstructure.linearizationDetail)
            temp_x = x_vals['lin_CAPEX_x']
            temp_y = y_vals['lin_CAPEX_y']
            
            
            for i in range(len(temp_x)):
                Instance.lin_CAPEX_x[Index,i+1] = temp_x[Index,i+1]
                Instance.lin_CAPEX_y[Index,i+1] = temp_y[Index,i+1]

            break
    

    
            
        
    return Instance

        
    




    