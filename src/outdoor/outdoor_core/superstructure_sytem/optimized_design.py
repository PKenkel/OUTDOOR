#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:19:11 2021

@author: philippkenkel


Function list:
    - fill data
    - fill information
    - tidy data
    - save results /print results
    - save data
    - save file
    - return chosen
    - collect results
"""


from tabulate import tabulate
import os
import datetime
import cloudpickle as pic


class ProcessResults:
    def __init__(self, model_instance=None, solver_name=None, run_time=None, gap = None):
        self._data = {}
        self._solver = None
        self._run_time = None
        self._case_time = None
        self._objective_function = None
        self._product_load = None
        self._optimality_gap = None
        

        if model_instance is not None:
            self._fill_data(model_instance)
        if solver_name is not None and run_time is not None:
            self._fill_information(solver_name, run_time, gap)

# -----------------------------------------------------------------------------
# -------------------------Private methods ------------------------------------
# -----------------------------------------------------------------------------

    def _fill_data(self, instance):
        """

        Parameters
        ----------
        instance : SupstructureModel Class objective that is already solved


        Description
        -------
        Goes through all block of the Model object and extracts the data
        (Parameter, Variables, Sets, Objectives) to a Python dictionary
        that is called ProcessDesign._data

        """

        for i in instance.component_objects():

            if "pyomo.core.base.var.SimpleVar" in str(type(i)):

                self._data[i.local_name] = i.value

            elif "pyomo.core.base.var.ScalarVar" in str(type(i)):
                self._data[i.local_name] = i.value

            elif "pyomo.core.base.param.SimpleParam" in str(type(i)):
                self._data[i.local_name] = i.value

            elif "pyomo.core.base.param.ScalarParam" in str(type(i)):

                self._data[i.local_name] = i.value

            elif "pyomo.core.base.param.IndexedParam" in str(type(i)):

                self._data[i.local_name] = i.extract_values()

            elif "pyomo.core.base.var.IndexedVar" in str(type(i)):
                self._data[i.local_name] = i.extract_values()

            elif "pyomo.core.base.set.SetProduct_OrderedSet" in str(type(i)):
                self._data[i.local_name] = i.value_list

            elif "pyomo.core.base.sets.SimpleSet" in str(type(i)):

                self._data[i.local_name] = i.value_list

            elif "pyomo.core.base.sets.ScalarSet" in str(type(i)):

                self._data[i.local_name] = i.value_list

            elif "pyomo.core.base.objective.SimpleObjective" in str(type(i)):

                self._data["Objective Function"] = i.expr.to_string()

            elif "pyomo.core.base.objective.ScalarObjective" in str(type(i)):

                self._data["Objective Function"] = i.expr.to_string()
            else:
                continue

    def _fill_information(self, solver_name, run_time, gap):
        """
        Parameters
        ----------
        solver_name : String
        run_time : Float

        Description
        -------
        Fills important case data of the ProcessDesign Object:
            Solver name, Run time, Case time, Solved Objective function,
            Yearly Product load

        """
        self._solver = solver_name
        self._run_time = run_time
        self._case_time = datetime.datetime.now()
        self._case_time = str(self._case_time)
        self._objective_function = self._data["Objective Function"]
        self._product_load = self._data["MainProductFlow"]
        self._optimality_gap = gap

    def _tidy_data(self):

        temp = dict()
        exeptions = ["Y", "Y_DIST", "lin_CAPEX_z", "Y_HEX"]
        for i, j in self._data.items():
            if "index" not in i:
                if type(j) == dict:
                    temp[i] = dict()
                    for k, m in j.items():
                        if i not in exeptions:
                            if m != 0:
                                temp[i][k] = m
                        else:
                            temp[i][k] = m
                else:
                    temp[i] = j
        self._data = temp

    # Extracting methods to get important results

    def _collect_results(self):
        """
        Description
        ----------
        Calls all collector methods to fill ProcessResults.results dictionary
        with all important results

        Returns
        -------
        TYPE: results dictionary
        """

        model_results = dict()

        basic_results = dict()

        basic_results["Basic results"] = {}

        basic_results["Basic results"]["Objective Function"] = self._objective_function

        basic_results["Basic results"]["Yearly product load"] = self._product_load

        basic_results["Basic results"]["Solver run time"] = self._run_time

        basic_results["Basic results"]["Solver name"] = self._solver

        basic_results["Basic results"]["Net production costs"] = round(
            self._data["NPC"], 2
        )

        basic_results["Basic results"]["Net production GHG emissions"] = round(
            self._data["NPE"], 3
        )

        basic_results["Basic results"]["Net present FWD"] = round(
            self._data["NPFWD"], 3
        )

        model_results.update(basic_results)

        chosen_technologies = {"Chosen technologies": self.return_chosen()}
        model_results.update(chosen_technologies)

        return model_results

    def _save_results(self, model_results, path):
        """
        Parameters
        ----------
        path : String type of where to save the results as .txt file

        Decription
        -------
        Collects all important results from the ProcessResults Class object and
        saves the data as tables in a text file.

        """
        all_results = model_results

        if not os.path.exists(path):
            os.makedirs(path)

        path = path + "/results_file" + self._case_time + ".txt"

        with open(path, encoding="utf-8", mode="w") as f:

            for i, j in all_results.items():
                table = tabulate(j.items())

                f.write("\n")
                f.write(i)
                f.write("-------- \n")
                f.write(table)
                f.write("\n")
                f.write("\n \n")

            print("")

    def _print_results(self, model_data):
        """
        Description
        -------
        Collects all important results data and prints them as tables to the
        console.

        """

        all_results = model_data

        for i, j in all_results.items():
            print("")
            print("")
            print(i)
            print("--------------")
            print(tabulate(j.items()))
            print("")

# -----------------------------------------------------------------------------
# -------------------------Public methods -------------------------------------
# -----------------------------------------------------------------------------

    def get_results(self, pprint=True, save=None):
        model_results = self._collect_results()

        if pprint is True:
            self._print_results(model_results)

        if save is not None:
            self._save_results(model_results, save)

    def save_data(self, path):
        """

        Parameters
        ----------
        path : String type of where to save the complete data as .txt file


        Decription
        -------
        Collects all data from the ProcessResults Class object and saves the
        data as tables in a text file.

        """

        if not os.path.exists(path):
            os.makedirs(path)

        path = path + "/" + "input_file" + self._case_time + "_data.txt"

        with open(path, encoding="utf-8", mode="w") as f:

            for i, j in self._data.items():
                f.write(f"{i}: {j} \n \n")

    def save_file(self, path, option="raw"):
        """

        Parameters
        ----------
        path : String type of where to save the ProcessResults object as pickle
        class object.

        """
        if option == "tidy":
            self._tidy_data()

        path = path + "/" + "data_file" + self._case_time + ".pkl"

        with open(path, "wb") as output:
            pic.dump(self, output)

    def return_chosen(self):
        flow = self._data["FLOW_SUM"]
        flow_s = self._data["FLOW_SOURCE"]

        y = self._data["Y"]
        names = self._data["Names"]
        chosen = {}

        for i, j in y.items():
            if j == 1:
                try:
                    if flow[i] >= 0.001:
                        chosen[i] = names[i]
                except:
                    pass

            else:
                try:
                    if flow_s[i] >= 0.001:
                        chosen[i] = names[i]
                except:
                    pass

        return chosen


