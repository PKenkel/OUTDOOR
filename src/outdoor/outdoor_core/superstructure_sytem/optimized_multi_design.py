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
import matplotlib.pyplot as plt


class MultipleResults:
    
    def __init__(self, optimization_mode = None):
        self._total_run_time = None
        self._case_time = None
        self._results_data = {}
        self._multi_criteria_data = None
        self._sensitivity_data = None
        self._optimization_mode = optimization_mode


    def add_process(self, index, process_results):    
        self._results_data[index] = process_results
        
    def set_multi_criteria_data(self, data):
        self._multi_criteria_data = data
        
    def set_sensitivity_data(self, data):
        self._sensitivity_data = data
        
    def fill_information(self, total_run_time):
        self._total_run_time = total_run_time
        self._case_time = datetime.datetime.now()
        self._case_time = str(self._case_time)
        
        

    def print_results(self):
        
        for i,j in self._results_data.items():
            print('')
            print(f'Identifier of Single run:{i}')
            j.print_results()
            
            
    def save_results(self, path):
        
        if not  os.path.exists(path):
            os.makedirs(path)
            
        path = path + self._case_time + '.txt'
        
        with open(path, encoding='utf-8', mode = 'w') as f:
            
            f.write('\n')
            f.write(f'Run mode: {self._optimization_mode} \n')
            f.write(f'Total run time {self._total_run_time} \n \n \n')
        
            for i,j in self._results_data.items():
                
                f.write(f'Identifier of Single run: {i} \n')
                all_results = j._collect_results()
                
                for k,t in all_results.items():
                        
                    table = tabulate(t.items())
                    f.write('\n')
                    f.write(k)
                    f.write('-------- \n')
                    f.write(table)
                    f.write('\n')
                    f.write('\n \n')

                print('')

                
    def _collect_sensi_data(self):
        
        data = {}
               
        for i,j in self._results_data.items():
            
            if len(i) > 2: 
                titel = i[0:2] 
            else:
                titel = i[0]
                
            if titel not in data.keys():
                data[titel] = ([[], []])
                x = i[-1]
                y = round(j._data['TAC'] * 1e6 / j._data['MainProductFlow'], 2)
                data[titel][0].append(x)
                data[titel][1].append(y)
            else:
                x = i[-1]
                y = round(j._data['TAC'] * 1e6 / j._data['MainProductFlow'], 2)
                data[titel][0].append(x)
                data[titel][1].append(y)   
        
        return data
            
                

                
    def create_sensi_graph(self):
        
        data  = self._collect_sensi_data()
  
        for i,j in data.items():
            
            x_vals = j[0]
            y_vals = j[1]
            titel = i
            
            fig, ax  = plt.subplots()
            
            ax.set_xlabel(titel)
            ax.set_ylabel('Net production costs in €/t')
            fig.set_dpi(750)
            
            ax.plot(x_vals, y_vals, linestyle='--', 
                marker='o')       
            