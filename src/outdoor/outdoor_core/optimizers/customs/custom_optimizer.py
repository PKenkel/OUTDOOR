#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:19:19 2021

@author: philippkenkel
"""


import copy
from .change_objective import change_objective_function
from ...output_classes.multi_model_output import MultiModelOutput

from ..main_optimizer import SingleOptimizer
from ...utils.timer import time_printer

from .change_params import (
    prepare_mutable_parameters,
    calculate_sensitive_parameters,
    change_parameter,
)


class MCDAOptimizer(SingleOptimizer):
    def __init__(
        self, solver_name, solver_interface, solver_options=None, mcda_data=None
    ):
        super().__init__(solver_name, solver_interface, solver_options)
        self.mcda_data = mcda_data
        self.single_optimizer = SingleOptimizer(
            solver_name, solver_interface, solver_options
        )

    def run_optimization(self, model_instance):
        timer = time_printer(programm_step="MCDA optimization")

        model_output = MultiModelOutput(optimization_mode="Multi-criteria optimization")

        for k, v in self.mcda_data.items():
            change_objective_function(model_instance, k)
            single_solved = self.single_optimizer.run_optimization(model_instance)
            single_solved._tidy_data()
            model_output.add_process(k, single_solved)

        print("MCDA reformulation")
        change_objective_function(model_instance, "MCDA", model_output, self.mcda_data)
        single_solved = self.single_optimizer.run_optimization(model_instance)
        single_solved._tidy_data()
        model_output.add_process("MCDA", single_solved)
        model_output.set_multi_criteria_data(self.mcda_data)

        timer = time_printer(timer, "MCDA optimization")
        model_output.fill_information(timer)
        return model_output


class SensitivityOptimizer(SingleOptimizer):
    def __init__(
        self,
        solver_name,
        solver_interface,
        solver_options=None,
        sensi_data=None,
        superstructure=None,
    ):
        super().__init__(solver_name, solver_interface, solver_options)

        self.sensi_data = sensi_data
        self.superstructure = superstructure

        self.single_optimizer = SingleOptimizer(
            solver_name, solver_interface, solver_options
        )

    def run_optimization(self, model_instance):
        timer1 = time_printer(programm_step="Sensitivity optimization")
        self.sensi_data = calculate_sensitive_parameters(self.sensi_data)
        initial_model_instance = copy.deepcopy(model_instance)
        timer = time_printer(
            passed_time=timer1, programm_step="Create initial ModelInstance copy",
        )
        model_output = MultiModelOutput(optimization_mode="Sensitivity analysis")

        for i, k in self.sensi_data.items():
            if type(k) is dict:
                dic = k
                for j, k2 in dic.items():
                    value_list = k2
                    for l in value_list:

                        model_instance = change_parameter(
                            model_instance, i, l, j, self.superstructure
                        )

                        single_solved = self.single_optimizer.run_optimization(
                            model_instance
                        )
                        single_solved._tidy_data()
                        model_output.add_process((i, j, l), single_solved)

                    model_instance = initial_model_instance

            else:
                value_list = k
                for l in value_list:

                    model_instance = change_parameter(model_instance, i, l)

                    single_solved = self.single_optimizer.run_optimization(
                        model_instance
                    )

                    single_solved._tidy_data()
                    model_output.add_process((i, l), single_solved)

                model_instance = initial_model_instance

        model_output.set_sensitivity_data(self.sensi_data)

        timer = time_printer(timer1, "Sensitivity optimization")
        model_output.fill_information(timer)
        return model_output


class TwoWaySensitivityOptimizer(SingleOptimizer):
    def __init__(
        self,
        solver_name,
        solver_interface,
        solver_options=None,
        two_way_data=None,
        superstructure=None,
    ):

        super().__init__(solver_name, solver_interface, solver_options)

        self.cross_parameters = two_way_data
        self.superstructure = superstructure

        self.single_optimizer = SingleOptimizer(
            solver_name, solver_interface, solver_options
        )

    def run_optimization(self, model_instance):
        timer1 = time_printer(programm_step="Two-way sensitivity optimimization")
        self.cross_parameters = calculate_sensitive_parameters(self.cross_parameters)

        model_output = MultiModelOutput(optimization_mode="Cross-parameter sensitivity")

        index_names = list()
        dic_1 = dict()
        dic_2 = dict()

        for i in self.cross_parameters.keys():
            index_names.append(i)

        for i, j in self.cross_parameters.items():
            if i == index_names[0]:
                dic_1[i] = j
            elif i == index_names[1]:
                dic_2[i] = j

        for i, j in dic_1.items():
            if type(j) == dict:

                for i2, j2 in j.items():
                    value_list = j2
                    string1 = (i, i2)

                    for l in value_list:
                        value1 = l

                        for k, m in dic_2.items():

                            if type(m) == dict:
                                for k2, m2 in m.items():
                                    string2 = (k, k2)
                                    value_list2 = m2
                                    for n in value_list2:
                                        value2 = n

                                        model_instance = change_parameter(
                                            model_instance,
                                            i,
                                            l,
                                            i2,
                                            self.superstructure,
                                        )
                                        model_instance = change_parameter(
                                            model_instance,
                                            k,
                                            n,
                                            k2,
                                            self.superstructure,
                                        )

                                        single_solved = self.single_optimizer.run_optimization(
                                            model_instance
                                        )

                                        single_solved._tidy_data()

                                        model_output.add_process(
                                            (string1, value1, string2, value2),
                                            single_solved,
                                        )

                            else:
                                string2 = k
                                value_list2 = m
                                for n in value_list2:
                                    value2 = n

                                    model_instance = change_parameter(
                                        model_instance, i, l, i2, self.superstructure
                                    )
                                    model_instance = change_parameter(
                                        model_instance, k, n
                                    )

                                    single_solved = self.single_optimizer.run_optimization(
                                        model_instance
                                    )

                                    single_solved._tidy_data()

                                    model_output.add_process(
                                        (string1, value1, string2, value2),
                                        single_solved,
                                    )

            else:
                string1 = i
                value_list = j
                for l in value_list:
                    value1 = l
                    for k, m in dic_2.items():
                        if type(m) == dict:
                            for k2, m2 in m.items():
                                string2 = (k, k2)
                                value_list2 = m2
                                for n in value_list2:
                                    value2 = n

                                    model_instance = change_parameter(
                                        model_instance, i, l
                                    )
                                    model_instance = change_parameter(
                                        model_instance, k, n, k2, self.superstructure
                                    )

                                    single_solved = self.single_optimizer.run_optimization(
                                        model_instance
                                    )

                                    single_solved._tidy_data()

                                    model_output.add_process(
                                        (string1, value1, string2, value2),
                                        single_solved,
                                    )

                        else:
                            string2 = k
                            value_list2 = m
                            for n in value_list2:
                                value2 = n

                                model_instance = change_parameter(model_instance, i, l)
                                model_instance = change_parameter(model_instance, k, n)

                                single_solved = self.single_optimizer.run_optimization(
                                    model_instance
                                )

                                single_solved._tidy_data()

                                model_output.add_process(
                                    (string1, value1, string2, value2), single_solved
                                )

        timer = time_printer(timer1, "Two-way sensitivity optimimization")
        model_output.fill_information(timer)
        return model_output