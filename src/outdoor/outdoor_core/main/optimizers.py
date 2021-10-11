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
    results = {}

    for k, v in multi_objectives.items():

        print("Changing Objective")
        change_Objective(ModelInstance, k)
        print("Objective changed")

        single_solved = solve_singleRun(ModelInstance, SolverName, SolverInterface)

        results[k] = single_solved

    print("MCDA Reformulation")
    change_Objective(ModelInstance, "MCDA", results, multi_objectives)

    print("Perform MCDA optimization")
    single_solved = solve_singleRun(ModelInstance, SolverName, SolverInterface)

    results["MCDA"] = single_solved

    end_time = time.time()
    run_time = end_time - start_time
    print("------")
    print("Multi-objective run solved, total solver time:")
    print(run_time)
    print("------")

    return results

def solve_sensitivityRun(
    ModelInstance, SolverName, SolverInterface, variations_parameter, Superstructure
):

    start_time = time.time()
    print("Preparing copy of initial model")
    InitialModel = copy.deepcopy(ModelInstance)
    print("Initial copy prepared")
    results = {}

    for i, k in variations_parameter.items():
        if type(k) is dict:
            dic = k
            for j, k2 in dic.items():
                value_list = k2
                for l in value_list:

                    ModelInstance = change_Instance(
                        ModelInstance, i, l, j, Superstructure
                    )

                    results[i, l, j] = solve_singleRun(
                        ModelInstance, SolverName, SolverInterface
                    )

                ModelInstance = InitialModel

        else:
            value_list = k
            for l in value_list:

                ModelInstance = change_Instance(ModelInstance, i, l)

                results[i, l] = solve_singleRun(
                    ModelInstance, SolverName, SolverInterface
                )

            ModelInstance = InitialModel

        end_time = time.time()
        run_time = end_time - start_time

        print("-----")
        print("Sensitivity Run solved, solver time:")
        print(run_time)
        print("-----")

    return results
