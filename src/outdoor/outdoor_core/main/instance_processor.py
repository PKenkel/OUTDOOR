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
    print('-- Create initial Model instance from DataFile')
    ModelInstance = S_Model.populateModel(Model_Data)    
    end_time = time.time()
    run_time = end_time-start_time
    print('-- Population finished, calculation time: ', run_time, ' --')

    return ModelInstance





def error_func(*args):
    raise ValueError('Parameter not in Variation Parameter set')
    
    

def change_Instance(Instance,parameter,value,index=None, superstructure=None):
    function_dictionary = {'electricity_price': change_utility_costs,
                           'chilling_price': change_utility_costs,
                           'capital_costs': change_capital_costs,
                           'component_concentration': change_concentration_demand,
                           'heating_demand': change_heat_demand}
    
    
    
    function_dictionary.get(parameter, error_func)(Instance,
                                                   parameter,
                                                   value,
                                                   index,
                                                   superstructure)
    
    
    return Instance

    
    
        








    