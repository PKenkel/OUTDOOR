#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 15:26:08 2021

@author: philippkenkel
"""

from pyomo.environ import value
from tabulate import tabulate
import os
import datetime
import cloudpickle as pic


class MultipleResults:
    def __init__(self, optimization_mode=None):
        self._total_run_time = None
        self._case_time = None
        self._results_data = {}
        self._multi_criteria_data = None
        self._sensitivity_data = None
        self._optimization_mode_set = {
            "Sensitivity analysis",
            "Multi-criteria optimization",
            "Cross-parameter sensitivity",
        }

        if optimization_mode in self._optimization_mode_set:
            self._optimization_mode = optimization_mode
        else:
            print("Optimization mode not supported")

    def add_process(self, index, process_results):
        """
        Parameters
        ----------
        index : String or value
            Identifier for the single-run ModelOutput
        process_results : ModelOutput
            Single-run ModelOutput to be saved

        Description
        -------
        Adds a single-run ModelOutput to the MultiModelOutput data-file

        """
        self._results_data[index] = process_results

    def set_multi_criteria_data(self, data):
        """
        Parameters
        ----------
        data : DICT
            Data dictionary with MCDA data including:
                Objectives, Weighting and Reference values

        """
        self._multi_criteria_data = data

    def set_sensitivity_data(self, data):
        """
        Parameters
        ----------
        data : DICT
            Data dictionary for sensitivity run including:
                Sensitive parameter-names and values
        """
        self._sensitivity_data = data

    def fill_information(self, total_run_time):
        """
        Parameters
        ----------
        total_run_time : FLOAT
            The total run time of the overall Multi-run optimization.
            Is calculated and returned automatically by the Optimizer

        Description
        -----------
        Saves total run times of multi-run, also checks for current date time
        to save date-time as identifier for the run.

        """
        self._total_run_time = total_run_time
        self._case_time = datetime.datetime.now()
        self._case_time = str(self._case_time)

    def _collect_results(self):
        results = dict()

        for i, j in self._results_data.items():
            results[i] = j._collect_results()

        return results

    def print_results(self):

        for i, j in self._results_data.items():
            print("")
            print(f"Identifier of Single run:{i}")
            j.print_results()

    def get_results(self, pprint=True, save=None):
        results = dict()

        for i, j in self._results_data.items():
            results[i] = j._collect_results()

            if pprint is True:
                j._print_results(j._collect_results())

        if save is not None:
            if not os.path.exists(save):
                os.makedirs(save)

            save = save + "/" + "basic_results_file" + self._case_time + ".txt"

            self._save_results(results, save)

    def _save_results(self, data, path):
        with open(path, encoding="utf-8", mode="w") as f:

            f.write("\n")
            f.write(f"Run mode: {self._optimization_mode} \n")
            f.write(f"Total run time {self._total_run_time} \n \n \n")

            for i, j in data.items():

                f.write(f"Identifier of Single run: {i} \n")

                for k, t in j.items():
                    table = tabulate(t.items())
                    f.write("\n")
                    f.write(k)
                    f.write("-------- \n")
                    f.write(table)
                    f.write("\n")
                    f.write("\n \n")

                print("")

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

        path = path + "/" + "input_file" + self._case_time + "data.txt"

        with open(path, encoding="utf-8", mode="w") as f:

            for i, j in self._results_data.items():
                f.write(f"Identifier of single run: {i} \n")
                all_data = j._data

                for k, t in all_data.items():
                    f.write(f"{k}: {t} \n \n")

                f.write(" ----------------- \n \n")

    def save_file(self, path, option="raw"):
        """
        Parameters
        ----------
        path : String type of where to save the ProcessResults object as pickle
        class object.

        """
        if not os.path.exists(path):
            os.makedirs(path)

        if option == "tidy":

            for i in self._results_data.values():
                i._tidy_data()

        path = path + "/" + "data_file" + self._case_time + ".pkl"

        with open(path, "wb") as output:
            pic.dump(self, output, protocol=4)
