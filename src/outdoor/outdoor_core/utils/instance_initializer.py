#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""

import time
from pyomo.environ import *




def prepare_initialInstance(Superstructure, SuperstructureModel):
    """
    Parameters
    ----------
    Superstructure : Superstructure object with data

    SuperstructureModel : Superstructure Model with Equations

    Returns
    -------
    ModelInformation : Dictionary
    
    ModelInstance : Concrete Superstructure model
    
    Model_Data : Model Data file dictionary

    """
    
    start_time = time.time()
    ModelInformation = dict()
    print('-Creating DataFile from Superstructure--')
    Model_Data = Superstructure.create_DataFile()   
    print('--Creating Model and Model instance--')
    S_Model = SuperstructureModel(Superstructure)  
    S_Model.create_ModelEquations()
    
    
    
    ModelInstance = S_Model.populateModel(Model_Data)    
    end_time = time.time()
    print('Population time was')
    print(end_time-start_time)
    
    return (ModelInformation, ModelInstance, Model_Data)
    
    







    