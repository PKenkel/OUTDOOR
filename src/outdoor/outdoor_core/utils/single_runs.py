#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:19:19 2021

@author: philippkenkel
"""
import time
from pyomo.environ import *


def solve_singleRun(ModelInstance, 
                    ModelInformation, 
                    Model_Data, 
                    SolverName, 
                    SolverInterface,
                    Superstructure):
    
    start_time = time.time()
    print('-----Starting optimization----')
    
    if SolverInterface == 'local':
        try:
            if SolverName == 'gurobi':
                solver = SolverFactory(SolverName, solver_io = 'python')
                results = solver.solve(ModelInstance, tee =True)
            else:
                solver = SolverFactory(SolverName)
                results = solver.solve(ModelInstance, tee =True)
        except:
            print('Solver Name is not correct or solver not installed')
    else:
        try:
            results =  SolverManagerFactory('neos').solve(ModelInstance,opt=SolverName,tee=True)
        except:
            print('Solver not on neos server, or input wrong')
    
        
    end_time = time.time()
    run_time = end_time - start_time
    
    ModelInformation['Solver'] = SolverName
    ModelInformation['Run Time'] = run_time
    ModelInformation['Data File'] = Model_Data
    ModelInformation['Superstructure']  = Superstructure
    
    print('-----------')
    print('Optimization run time is')
    print(run_time)
    print('-----------')

    return (ModelInstance, ModelInformation)