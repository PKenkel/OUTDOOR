#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 11:54:16 2021

@author: philippkenkel
"""

from ...utils.timer import time_printer
from pyomo.environ import *

from .change_functions.utility_cost_changer import change_utility_costs
from .change_functions.capital_cost_changer import change_capital_costs
from .change_functions.concentration_demand_changer import (
    change_concentration_demand,
)
from .change_functions.heat_demand_changer import change_heat_demand
from .change_functions.source_cost_changer import (
    change_source_costs,
    change_product_price,
)
from .change_functions.opex_changer import change_opex_factor
from .change_functions.simple_capex_changer import change_simple_capex


from numpy import linspace


def calculate_sensitive_parameters(data_input):

    value_dic = dict()

    for i in data_input:
        start = i[1]
        stop = i[2]
        dx = i[3]

        if len(i) == 4:
            value_dic[i[0]] = list(linspace(start, stop, dx))
        elif len(i) == 5:
            try:
                value_dic[i[0]][i[4]] = list(linspace(start, stop, dx))
            except:
                value_dic[i[0]] = {}
                value_dic[i[0]][i[4]] = list(linspace(start, stop, dx))

    return value_dic


def error_func(*args):
    raise ValueError("Parameter not in Variation Parameter set")


def change_parameter(Instance, parameter, value, index=None, superstructure=None):
    timer = time_printer(programm_step = 'Change parameter')
    function_dictionary = {
        "electricity_price": change_utility_costs,
        "chilling_price": change_utility_costs,
        "capital_costs": change_capital_costs,
        "component_concentration": change_concentration_demand,
        "heating_demand": change_heat_demand,
        "source_costs": change_source_costs,
        "opex": change_opex_factor,
        "simple_capex": change_simple_capex,
        "product_price": change_product_price,
    }

    function_dictionary.get(parameter, error_func)(
        Instance, parameter, value, index, superstructure
    )
    timer = time_printer(timer, 'Change parameter')
    return Instance


def prepare_mutable_parameters(ModelInstance, input_data):
    def set_mutable(instance, parameter):
        if parameter == "electricity_price" or parameter == "chilling_price":
            instance.delta_ut._mutable = True
        elif parameter == "working_hours":
            instance.flh._mutable = True
        elif parameter == "capital_costs" or parameter == "simple_capex":
            instance.lin_CAPEX_x._mutable = True
            instance.lin_CAPEX_y._mutable = True
        elif parameter == "component_concentration":
            instance.conc._mutable = True
        elif parameter == "heating_demand":
            instance.tau_h._mutable = True
            instance.tau_c._mutable = True
        elif parameter == "source_costs":
            instance.materialcosts._mutable = True
        elif parameter == "opex":
            instance.K_OM._mutable = True
        elif parameter == "product_price":
            instance.ProductPrice._mutable = True
        else:
            raise ValueError("Parameter to set mutable not existing")

    for i in input_data:
        name = i[0]
        set_mutable(ModelInstance, name)
        
    return ModelInstance

