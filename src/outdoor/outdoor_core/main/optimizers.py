#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:19:19 2021

@author: philippkenkel
"""
import time
from pyomo.environ import *
import copy

from .instance_processor import change_Instance

def solve_singleRun(ModelInstance, 
                    SolverName, 
                    SolverInterface):
    
    start_time = time.time()
    print('-----Solving single run----')
    
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
    
    print('-----------')
    print('Single run solved')
    print(run_time)
    print('-----------')

    return ModelInstance






# TODO:
    # durch die varations parameter gehen und alle bearbeiten
    

# def solve_multiRun(ModelInstance,
#                    SolverName,
#                    SolverInterface, 
#                    variations_parameter):
#     results = {}
    
#     for i in variations_parameter.keys():
        
#         if i == 'electricity_price':
#             for j in variations_parameter[i]:
#                 ModelInstance = copy.deepcopy(ModelInstance)
#                 ModelInstance.delta_ut['Electricity'] = j
#                 results[i,j] = solve_singleRun(ModelInstance,
#                                                SolverName,
#                                                SolverInterface)
                
#     return results


def solve_multiRun(ModelInstance,
                   SolverName,
                   SolverInterface,
                   variations_parameter):
    
    results ={}
    
    
    for i,k in variations_parameter.items():
        if type(k) is dict:
            dic = k 
            for j,k2 in dic.items():
                value_list = k2
                for l in value_list:
                    
                    ModelInstance = copy.deepcopy(ModelInstance)
                    
                    ModelInstance = change_Instance(ModelInstance,
                                                    i, 
                                                    l,
                                                    k)
                    results[i,l] = solve_singleRun(ModelInstance,
                                                   SolverName,
                                                   SolverInterface)
        else:
            value_list = k
            for l in value_list:
                
                ModelInstance = copy.deepcopy(ModelInstance)
                
                ModelInstance = change_Instance(ModelInstance, 
                                                i,
                                                l)
                
                results[i,l] = solve_singleRun(ModelInstance,
                                               SolverName,
                                               SolverInterface)
    
    return results

                
            


    