#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""


def change_heat_demand(Instance, Parameter, Value, Index = None, Superstructure = None):
    '# currently not working in excel wrapper'
    if Value > 0:
        tau_h = Value
        Instance.tau_h[Index] = tau_h
        
    else:
        tau_c = Value
        Instance.tau_c[Index] = tau_c

            
        
    return Instance

        
    




    