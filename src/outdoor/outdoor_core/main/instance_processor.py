#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""

import time
from pyomo.environ import *

from .variation_analysis_tools.utility_cost_changer import change_utility_costs
from .variation_analysis_tools.capital_cost_changer import change_capital_costs
from .variation_analysis_tools.concentration_demand_changer import change_concentration_demand
from .variation_analysis_tools.heat_demand_changer import change_heat_demand
from .variation_analysis_tools.source_cost_changer import change_source_costs, change_product_price
from .variation_analysis_tools.opex_changer import change_opex_factor
from .variation_analysis_tools.simple_capex_changer import change_simple_capex


    
def create_initialInstance(S_Model, Model_Data):
    """
    Parameters
    ----------
    S_Model : SuperstructureModel Object, which is a Pyomo AbstractModel
    Model_Data : Model Data as Python Dictionary, created from Superstructure object

    Description
    -----------
    
    Takes the Abstract model as well as the intial data file and creates an inital
    Instance (Concrete model).

    Returns
    -------
    ModelInstance : Pyomo Concrete Model / Filled SuperstructureModel Object

    """

    start_time = time.time()
    print("-- Create initial Model instance from DataFile")
    ModelInstance = S_Model.populateModel(Model_Data)
    end_time = time.time()
    run_time = end_time - start_time
    print("-- Initial model created, calculation time: ", run_time, " --")

    return ModelInstance


def error_func(*args):
    raise ValueError("Parameter not in Variation Parameter set")
    
    

def change_Instance(Instance, parameter, value, index=None, superstructure=None):
    function_dictionary = {
        "electricity_price": change_utility_costs,
        "chilling_price": change_utility_costs,
        "capital_costs": change_capital_costs,
        "component_concentration": change_concentration_demand,
        "heating_demand": change_heat_demand,
        "source_costs": change_source_costs,
        "opex": change_opex_factor,
        "simple_capex": change_simple_capex,
        "product_price": change_product_price
    }

    function_dictionary.get(parameter, error_func)(
        Instance, parameter, value, index, superstructure
    )

    return Instance

    
    
        
def change_Objective(Instance, Obj, results=None, MultiObjectives=None):

    Instance.del_component(Instance.Objective)

    if Obj == "NPC":

        def Objective_rule(Instance):
            return Instance.NPC

        Instance.Objective = Objective(rule=Objective_rule, sense=minimize)

    elif Obj == "NPE":

        def Objective_rule(Instance):
            return Instance.NPE

        Instance.Objective = Objective(rule=Objective_rule, sense=minimize)

    elif Obj == "FWD":

        def Objective_rule(Instance):
            return Instance.NPFWD

        Instance.Objective = Objective(rule=Objective_rule, sense=minimize)

    elif Obj == "MCDA":

        print("change objective to MCDA")

        # Create list with all values, start with reference values
        npc = [MultiObjectives["NPC"][1]]
        npe = [MultiObjectives["NPE"][1]]
        npfwd = [MultiObjectives["FWD"][1]]


        # Add values from all preceding single-criterion runs    
        for k, v in results._results_data.items():
            npc_temp = v._data["NPC"]
            npe_temp = v._data["NPE"]
            npfwd_temp = v._data["NPFWD"]
            
            npc.append(npc_temp)
            npe.append(npe_temp)
            npfwd.append(npfwd_temp)

        # Check for best and worst values
        
        best_npc = min(npc)
        worst_npc = max(npc)

        best_npe = min(npe)
        worst_npe = max(npe)

        best_npfwd = min(npfwd)
        worst_npfwd = max(npfwd)


        # Create new set with objectives 
        # Create new parameter which is the score depending on criterion
        
        Instance.ObjSet = Set(initialize=["NPC", "NPE", "FWD"])
        
        Instance.V_pos = Param(
            Instance.ObjSet,
            initialize={
                "NPC": MultiObjectives["NPC"][0],
                "NPE": MultiObjectives["NPE"][0],
                "FWD": MultiObjectives["FWD"][0],
            },
        )

        Instance.V_neg = Param(
            Instance.ObjSet, initialize={"NPC": 0, "NPE": 0, "FWD": 0}
        )

        Instance.V = Var(Instance.ObjSet)


        def mTAC_rule(Instance):
            return (
                Instance.V["NPC"]
                == ((worst_npc - Instance.NPC) / (worst_npc - best_npc))
                * MultiObjectives["NPC"][0]
            )

        def mGWP_rule(Instance):
            return (
                Instance.V["NPE"]
                == ((worst_npe - Instance.NPE) / (worst_npe - best_npe))
                * MultiObjectives["NPE"][0]
            )

        def mFWD_rule(Instance):
            return (
                Instance.V["FWD"]
                == ((worst_npfwd - Instance.NPFWD) / (worst_npfwd - best_npfwd))
                * MultiObjectives["FWD"][0]
            )

        Instance.mTAC_Con = Constraint(rule=mTAC_rule)
        Instance.mGWP_Con = Constraint(rule=mGWP_rule)
        Instance.mFWD_Con = Constraint(rule=mFWD_rule)

        Instance.s_pos1 = Var(Instance.ObjSet, within=NonNegativeReals)
        Instance.s_pos2 = Var(Instance.ObjSet, within=NonNegativeReals)
        Instance.s_pos = Var(Instance.ObjSet)

        Instance.y_pos1 = Var(Instance.ObjSet, within=Binary)
        Instance.y_pos2 = Var(Instance.ObjSet, within=Binary)

        Instance.D_Pos = Var(bounds=(0, 1))

        def s1_pos_rule1(Instance, obj):
            return Instance.s_pos1[obj] <= Instance.V_pos[obj] - Instance.V[
                obj
            ] + 100000 * (1 - Instance.y_pos1[obj])

        def s1_pos_rule2(Instance, obj):
            return Instance.s_pos1[obj] >= Instance.V_pos[obj] - Instance.V[
                obj
            ] - 100000 * (1 - Instance.y_pos1[obj])

        def s1_pos_rule3(Instance, obj):
            return Instance.s_pos1[obj] <= 100000 * Instance.y_pos1[obj]

        def s2_pos_rule1(Instance, obj):
            return Instance.s_pos2[obj] <= Instance.V[obj] - Instance.V_pos[
                obj
            ] + 100000 * (1 - Instance.y_pos2[obj])

        def s2_pos_rule2(Instance, obj):
            return Instance.s_pos2[obj] >= Instance.V[obj] - Instance.V_pos[
                obj
            ] - 100000 * (1 - Instance.y_pos2[obj])

        def s2_pos_rule3(Instance, obj):
            return Instance.s_pos2[obj] <= 100000 * Instance.y_pos2[obj]

        def s_pos_tot_rule(Instance, obj):
            return Instance.s_pos[obj] == Instance.s_pos1[obj] + Instance.s_pos2[obj]

        def D_pos_rule(Instance):
            return Instance.D_Pos == sum(Instance.s_pos[obj] for obj in Instance.ObjSet)

        Instance.s_neg1 = Var(Instance.ObjSet, within=NonNegativeReals)
        Instance.s_neg2 = Var(Instance.ObjSet, within=NonNegativeReals)
        Instance.s_neg = Var(Instance.ObjSet)

        Instance.y_neg1 = Var(Instance.ObjSet, within=Binary)
        Instance.y_neg2 = Var(Instance.ObjSet, within=Binary)

        Instance.D_Neg = Var(bounds=(0, 1))

        def s1_neg_rule1(Instance, obj):
            return Instance.s_neg1[obj] <= Instance.V_neg[obj] - Instance.V[
                obj
            ] + 100000 * (1 - Instance.y_neg1[obj])

        def s1_neg_rule2(Instance, obj):
            return Instance.s_neg1[obj] >= Instance.V_neg[obj] - Instance.V[
                obj
            ] - 100000 * (1 - Instance.y_neg1[obj])

        def s1_neg_rule3(Instance, obj):
            return Instance.s_neg1[obj] <= 100000 * Instance.y_neg1[obj]

        def s2_neg_rule1(Instance, obj):
            return Instance.s_neg2[obj] <= Instance.V[obj] - Instance.V_neg[
                obj
            ] + 100000 * (1 - Instance.y_neg2[obj])

        def s2_neg_rule2(Instance, obj):
            return Instance.s_neg2[obj] >= Instance.V[obj] - Instance.V_neg[
                obj
            ] - 100000 * (1 - Instance.y_neg2[obj])

        def s2_neg_rule3(Instance, obj):
            return Instance.s_neg2[obj] <= 100000 * Instance.y_neg2[obj]

        def s_neg_tot_rule(Instance, obj):
            return Instance.s_neg[obj] == Instance.s_neg1[obj] + Instance.s_neg2[obj]

        def D_neg_rule(Instance):
            return Instance.D_Neg == sum(Instance.s_neg[obj] for obj in Instance.ObjSet)

        def y_pos_rule(Instance, obj):
            return Instance.y_pos1[obj] + Instance.y_pos2[obj] == 1

        def y_neg_rule(Instance, obj):
            return Instance.y_neg1[obj] + Instance.y_neg2[obj] == 1

        def s_rule(Instance, obj):
            return Instance.s_neg[obj] + Instance.s_pos[obj] == Instance.V_pos[obj]

        Instance.s_Con = Constraint(Instance.ObjSet, rule=s_rule)

        Instance.y_pos_Con = Constraint(Instance.ObjSet, rule=y_pos_rule)
        Instance.y_neg_Con = Constraint(Instance.ObjSet, rule=y_neg_rule)

        Instance.MCDA_Ob = Var()

        def MCDA_rule(Instance):
            return Instance.MCDA_Ob == Instance.D_Neg

        Instance.s1_pos_Con1 = Constraint(Instance.ObjSet, rule=s1_pos_rule1)
        Instance.s1_pos_Con2 = Constraint(Instance.ObjSet, rule=s1_pos_rule2)
        Instance.s1_pos_Con3 = Constraint(Instance.ObjSet, rule=s1_pos_rule3)
        Instance.s2_pos_Con1 = Constraint(Instance.ObjSet, rule=s2_pos_rule1)
        Instance.s2_pos_Con2 = Constraint(Instance.ObjSet, rule=s2_pos_rule2)
        Instance.s2_pos_Con3 = Constraint(Instance.ObjSet, rule=s2_pos_rule3)
        Instance.s_tot_pos_Con = Constraint(Instance.ObjSet, rule=s_pos_tot_rule)
        Instance.D_Pos_Con = Constraint(rule=D_pos_rule)

        Instance.s1_neg_Con1 = Constraint(Instance.ObjSet, rule=s1_neg_rule1)
        Instance.s1_neg_Con2 = Constraint(Instance.ObjSet, rule=s1_neg_rule2)
        Instance.s1_neg_Con3 = Constraint(Instance.ObjSet, rule=s1_neg_rule3)
        Instance.s2_neg_Con1 = Constraint(Instance.ObjSet, rule=s2_neg_rule1)
        Instance.s2_neg_Con2 = Constraint(Instance.ObjSet, rule=s2_neg_rule2)
        Instance.s2_neg_Con3 = Constraint(Instance.ObjSet, rule=s2_neg_rule3)
        Instance.s_tot_neg_Con = Constraint(Instance.ObjSet, rule=s_neg_tot_rule)
        Instance.D_Neg_Con = Constraint(rule=D_neg_rule)

        Instance.MCDA_Con = Constraint(rule=MCDA_rule)

        def Objective_rule(Instance):
            return Instance.MCDA_Ob

        Instance.Objective = Objective(rule=Objective_rule, sense=maximize)

    else:
        print("Error in change_Objetive function, no fitting input")
                








    