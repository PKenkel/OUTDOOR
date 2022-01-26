#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""

    



def change_concentration_demand(Instance, Parameter, Value, Index = None, *args):
    Instance.conc[Index] = Value
        
    return Instance

        
    




    