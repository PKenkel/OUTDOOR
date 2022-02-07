#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""



def change_source_costs(Instance, Parameter, Value, Index = None, Superstructure = None):
    
    Instance.materialcosts[Index] = Value
    
    return Instance

        
    

def change_product_price(Instance, Parameter, Value, Index = None, Superstructure = None):
    
    for i in Superstructure.UnitsList:
        if i.Number == Index:
            
            Instance.ProductPrice[Index] = Value 
            
    return Instance


    