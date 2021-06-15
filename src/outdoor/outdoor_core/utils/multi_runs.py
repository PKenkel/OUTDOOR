#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:19:36 2021

@author: philippkenkel
"""

def solve_MultiRun(Superstructure, 
                   SensitivityParamaters,
                   SolverName = 'gurobi', 
                   SolverInterface  = 'local'):

    """
    Sensitivity Parameters =
    - Electricity Price
    - 
    """

    st = time.time()
    
    
    Sensi_Param = FUNCTION_PARAM(SensitivityParamaters)
    
    ModelInformation = dict()
    
    print('Creating Initial DataFile from Superstructure')
    Model_Data = Superstructure.create_DataFile()
    print('Creating Model and initial model instance')
    S_Model = SuperstructureModel(Superstructure)
    S_Model.create_ModelEquations()
    ModelInstance = S_Model.populateModel(Model_Data)