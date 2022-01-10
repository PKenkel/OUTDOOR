#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:19:19 2021

@author: philippkenkel
"""
import time
from pyomo.environ import *
import copy
import os


from .instance_processor import change_Instance
from .instance_processor import change_Objective
from ..superstructure_sytem.optimized_design import ProcessResults
from ..superstructure_sytem.optimized_multi_design import MultipleResults


def solve_singleRun(ModelInstance, SolverName, SolverInterface):

    start_time = time.time()
    print("-----Solving single run----")

    if SolverInterface == "local":
        try:
            if SolverName == "gurobi":
                solver = SolverFactory(SolverName, solver_io="python")
                results = solver.solve(ModelInstance, tee=True)
            elif SolverName == "scip":
                solver = SolverFactory(SolverName)
                results = solver.solve(ModelInstance, tee=True)
            else:
                solver = SolverFactory(SolverName)
                results = solver.solve(ModelInstance, tee=True)
        except:
            print("Solver Name is not correct or solver not installed")

    elif SolverInterface == "executable":
        exe_path = os.path.dirname(__file__)
        exe_path = os.path.dirname(exe_path)
        exe_path = os.path.dirname(exe_path)
        exe_path = exe_path + "/solver_executables"
        try:
            solver = SolverFactory(
                SolverName, executable=exe_path + "/" + str(SolverName)
            )
            results = solver.solve(ModelInstance, tee=True)
        except:
            print("Solver Name is not correct or solver not installed")
    else:
        try:
            results = SolverManagerFactory("neos").solve(
                ModelInstance, opt=SolverName, tee=True
            )
        except:
            print("Solver not on neos server, or input wrong")


    end_time = time.time()
    run_time = end_time - start_time

    solved = ProcessResults(ModelInstance, SolverName, run_time)

    print("-----------")
    print("Single run solved, solver time:")
    print(run_time)
    print("-----------")


    return solved





def solve_multiObjectiveRun(
    ModelInstance, SolverName, SolverInterface, multi_objectives
):

    start_time = time.time()
    
    results = MultipleResults(optimization_mode='Multi-criteria optimization')
    
    

    for k, v in multi_objectives.items():

        print("Changing Objective")
        change_Objective(ModelInstance, k)
        print("Objective changed")

        single_solved = solve_singleRun(ModelInstance, SolverName, SolverInterface)
        
        results.add_process(k, single_solved)

    print("MCDA Reformulation")
    change_Objective(ModelInstance, "MCDA", results, multi_objectives)

    print("Perform MCDA optimization")
    single_solved = solve_singleRun(ModelInstance, SolverName, SolverInterface)
    
    results.add_process('MCDA', single_solved)

    end_time = time.time()
    run_time = end_time - start_time
    print("------")
    print("Multi-objective run solved, total solver time:")
    print(run_time)
    print("------")
    
    results.set_multi_criteria_data(multi_objectives)

    return results


def solve_sensitivityRun(
    ModelInstance, SolverName, SolverInterface, variations_parameter, Superstructure
):

    start_time = time.time()
    print("Preparing copy of initial model")
    InitialModel = copy.deepcopy(ModelInstance)
    print("Initial copy prepared")
    results = MultipleResults(optimization_mode='Sensitivity analysis')

    for i, k in variations_parameter.items():
        if type(k) is dict:
            dic = k
            for j, k2 in dic.items():
                value_list = k2
                for l in value_list:

                    ModelInstance = change_Instance(
                        ModelInstance, i, l, j, Superstructure
                    )

                    single_solved = solve_singleRun(
                        ModelInstance, SolverName, SolverInterface
                    )
                    
                    results.add_process((i,j,l), single_solved)

                ModelInstance = InitialModel

        else:
            value_list = k
            for l in value_list:

                ModelInstance = change_Instance(ModelInstance, i, l)

                single_solved = solve_singleRun(
                    ModelInstance, SolverName, SolverInterface
                )
                
                results.add_process((i,l), single_solved)

            ModelInstance = InitialModel

        results.set_sensitivity_data(variations_parameter)
        
        end_time = time.time()
        run_time = end_time - start_time

        print("-----")
        print("Sensitivity Run solved, solver time:")
        print(run_time)
        print("-----")

    return results



def solve_crossParameterRun(ModelInstance,
                            SolverName,
                            SolverInterface,
                            cross_parameters,
                            Superstructure):
    

    start_time = time.time()
    print("Preparing copy of initial model")
    # InitialModel = copy.deepcopy(ModelInstance)
    print("Initial copy prepared")
    
    results = MultipleResults(optimization_mode='Cross-parameter sensitivity')

    
    index_names = []
    
    dic_1 = {}
    dic_2 = {}
    
    for i in cross_parameters.keys():
        index_names.append(i)
        
    for i,j in cross_parameters.items():
        if i == index_names[0]:
            dic_1[i] = j
        elif i == index_names[1]:
            dic_2[i] = j
            
    
    for i,j in dic_1.items():
        if type(j) == dict:
            
            for i2,j2 in j.items():
                value_list = j2
                string1 = (i,i2)
                
                for l in value_list:
                    value1 = l
                    
                    for k,m in dic_2.items():
    
                        if type(m) == dict:
                            for k2,m2 in m.items():
                                string2 = (k, k2)
                                value_list2 = m2
                                for n in value_list2:
                                    value2 = n
                                    
                                    ModelInstance = change_Instance(ModelInstance, i, l, i2, Superstructure)
                                    ModelInstance = change_Instance(ModelInstance, k, n, k2, Superstructure)

                                    single_solved = solve_singleRun(
                                            ModelInstance, SolverName, SolverInterface
                                    )
                
                                    results.add_process((string1, value1, string2, value2), single_solved)
                                    
                                        
                        else:
                            string2 = k
                            value_list2 = m
                            for n in value_list2:
                                value2 = n
                                
                                ModelInstance = change_Instance(ModelInstance, i, l, i2, Superstructure)
                                ModelInstance = change_Instance(ModelInstance, k, n)

                                single_solved = solve_singleRun(
                                        ModelInstance, SolverName, SolverInterface
                                )
                
                                results.add_process((string1, value1, string2, value2), single_solved)
                                
        else:
            string1 = i
            value_list = j
            for l in value_list:
                value1 = l
                for k,m in dic_2.items():
                    if type(m) == dict:
                        for k2,m2 in m.items():
                            string2 = (k, k2)
                            value_list2 = m2
                            for n in value_list2:
                                value2 = n
                                
                                ModelInstance = change_Instance(ModelInstance, i, l)
                                ModelInstance = change_Instance(ModelInstance, k, n, k2, Superstructure)
                                 
                                single_solved = solve_singleRun(
                                     ModelInstance, SolverName, SolverInterface
                                )
                
                                results.add_process((string1, value1, string2, value2), single_solved)
                                        
                    else:
                        string2 = k
                        value_list2 = m
                        for n in value_list2:
                            value2 = n
                            
                            ModelInstance = change_Instance(ModelInstance, i,l)
                            ModelInstance = change_Instance(ModelInstance, k,n)                      
                
                            single_solved = solve_singleRun(
                                    ModelInstance, SolverName, SolverInterface
                            )
                
                            results.add_process((string1, value1, string2, value2), single_solved)

        
            


    return results


