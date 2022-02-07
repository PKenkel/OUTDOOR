#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""
from ....utils.linearizer import capex_calculator
    



def change_opex_factor(Instance, Parameter, Value, Index = None, Superstructure = None):
    
    Instance.K_OM[Index] = Value

    
    return Instance

        
    




    