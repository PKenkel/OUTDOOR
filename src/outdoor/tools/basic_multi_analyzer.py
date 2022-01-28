#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 15:12:24 2022

@author: philippkenkel
"""

import os
import pickle5 as pic5
import time
import copy
from tabulate import tabulate
from .basic_analyzer import BasicModelAnalyzer


class BasicMultiModelAnalyzer:
    def __init__(self, model_output=None):

        self.model_output = copy.deepcopy(model_output)

# -----------------------------------------------------------------------------
# -------------------------Private methods ------------------------------------
# -----------------------------------------------------------------------------

    def _save_results(self, data, idf, path):

        with open(path, encoding="utf-8", mode="a") as f:

            f.write(f"Identifier of Single run: {idf} \n")

            for k, t in data.items():
                table = tabulate(t.items())
                f.write("\n")
                f.write(k)
                f.write("-------- \n")
                f.write(table)
                f.write("\n")
                f.write("\n \n")
            print("")
        
# -----------------------------------------------------------------------------
# -------------------------Public methods -------------------------------------
# -----------------------------------------------------------------------------

    def set_model_output(self, model_output):
        """
        Parameters
        ----------
        model_output : MultiModelOutput Class
            Store MultiModelOutput Object in ModelAnalyzer

        """
        self.model_output = copy.deepcopy(model_output)

    def load_model_output(self, path):
        """
        Parameters
        ----------
        path : String
            Path string from where to load pickle file

        """

        timer = time.time()

        with open(path, "rb") as file:
            self.model_output = pic5.load(file)

        timer = time.time() - timer
        print(f"File loading time was {timer} seconds")

    def techno_economic_analysis(self, pprint=True, save=None):
        results = dict()

        if save is not None:
            if not os.path.exists(save):
                os.makedirs(save)
            save = save + "/" + "techno_economic_file" + self.model_output._case_time + ".txt"

            with open(save, encoding="utf-8", mode="w") as f:

                f.write("\n")
                f.write(f"Run mode: {self.model_output._optimization_mode} \n")
                f.write(f"Total run time {self.model_output._total_run_time} \n \n \n")

        for i, j in self.model_output._results_data.items():
            results[i] = BasicModelAnalyzer(j)
            data = results[i]._collect_techno_economic_results()

            if pprint is True:
                print("")
                print(f" Identifier of single run: {i}")
                results[i]._print_results(data)

            if save is not None:
                self._save_results(data, i, save)

    def environmental_analysis(self, pprint=True, save=None):
        results = dict()

        if save is not None:
            if not os.path.exists(save):
                os.makedirs(save)
            save = save + "/" + "environmental_file" + self.model_output._case_time + ".txt"

            with open(save, encoding="utf-8", mode="w") as f:

                f.write("\n")
                f.write(f"Run mode: {self.model_output._optimization_mode} \n")
                f.write(f"Total run time {self.model_output._total_run_time} \n \n \n")

        for i, j in self.model_output._results_data.items():
            results[i] = BasicModelAnalyzer(j)
            data = results[i]._collect_environmental_data()

            if pprint is True:
                print("")
                print(f" Identifier of single run: {i}")
                results[i]._print_results(data)

            if save is not None:
                self._save_results(data, i, save)
