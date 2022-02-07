#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 12:19:19 2021

@author: philippkenkel
"""

import pyomo.environ as pyo

from ..output_classes.model_output import ModelOutput
from ..utils.timer import time_printer


class SingleOptimizer:
    def __init__(self, solver_name, solver_interface, solver_options=None):

        SOLVER_LIBRARY = {"gurobi", "cbc", "scip"}
        INTERFACE_LIBRARY = {"local", "executable"}

        # setup name
        if solver_name in SOLVER_LIBRARY:
            self.solver_name = solver_name
        else:
            self.solver_name = solver_name
            print("Solver not in library, correct optimization not garanteed")

        # setup interface
        if solver_interface in INTERFACE_LIBRARY:
            self.solver_interface = solver_interface
        else:
            print("Solver interface not in library, correct optimization not garanteed")

        # check for gurobi
        if self.solver_name == "gurobi":
            self.solver_io = "python"

        # create solver
        if solver_interface == "local":
            if solver_name == "gurobi":
                self.solver = pyo.SolverFactory(
                    self.solver_name, solver_io=self.solver_io
                    )
            else:
                self.solver = pyo.SolverFactory(self.solver_name)
        else:
            pass

        self.solver = self.set_solver_options(self.solver, solver_options)

    def run_optimization(self, model_instance):
        timer = time_printer(programm_step='Single optimization run')

        results = self.solver.solve(model_instance, tee=True)
        gap = (
            (
                results["Problem"][0]["Upper bound"]
                - results["Problem"][0]["Lower bound"]
            )
            / results["Problem"][0]["Upper bound"]
        ) * 100
        timer = time_printer(timer, 'Single optimization run')
        model_output = ModelOutput(model_instance, self.solver_name, timer, gap)
        return model_output

    def set_solver_options(self, solver, options):
        if options is not None:
            for i, j in options.items():
                solver.options[i] = j
        else:
            pass
        return solver
