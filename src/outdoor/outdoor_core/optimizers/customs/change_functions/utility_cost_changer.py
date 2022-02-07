#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""

    



def change_utility_costs(Instance, Parameter, Value, *args):
    if Parameter =='electricity_price':
        Instance.delta_ut['Electricity'] = Value
    elif Parameter =='chilling_price':
        Instance.delta_ut['Chilling'] = Value
    else:
        raise ValueError('Parameter Name not correct for utility costs change')
        
    return Instance

        
    




    