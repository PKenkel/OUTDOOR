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
        self._optimization_mode_set = {'Sensitivity analysis', 
                                       'Multi-criteria optimization', 
                                       'Cross-parameter sensitivity'}
        
        if optimization_mode in self._optimization_mode_set:
            self._optimization_mode = optimization_mode
        else: 
            print('Optimization mode not supported')



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



    def create_sensitivity_graph(self):
        
        if self._optimization_mode == 'Sensitivity analysis':
        
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
        else:
            print('Sensitivity graph presentation only available for  \
                  Sensitivity analysis mode')
            


# Private methods
                
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
                y = round(j._data['NPC'], 2)
                data[titel][0].append(x)
                data[titel][1].append(y)
            else:
                x = i[-1]
                y = round(j._data['NPC'], 2)
                data[titel][0].append(x)
                data[titel][1].append(y)   
        
        return data
            
  
    
    def create_mcda_table(self, table_type = 'values'):
        if self._optimization_mode == 'Multi-criteria optimization':
            
            data = self._collect_mcda_data(table_type)
            index = ['NPC', 'NPE', 'FWD']
            if table_type != 'relative closeness':
                table = tabulate(data,headers='keys', showindex = index) 
            else:
                table = tabulate(data, headers = 'keys')
            
            print('')
            print(table_type)
            print('--------')
            print(table)
            print('')
        else:
            print('MCDA table representation is only supported for optimization \
                  mode Multi-criteria optimization')
        
    
    
    def _collect_mcda_data(self, table_type = 'values'):
        data = dict()
        
        r_npc = round(self._multi_criteria_data['NPC'][1], 2)
        r_npe = round(self._multi_criteria_data['NPE'][1], 2)
        r_fwd = round(self._multi_criteria_data['FWD'][1], 2)
        
        if table_type == 'values':
            data['Ref'] = [r_npc, r_npe, r_fwd]
            
            for i,j in self._results_data.items():
                npc = round(j._data['NPC'], 2)
                npe = round(j._data['NPE'], 2)
                fwd = round(j._data['NPFWD'], 2)
                
                data[i] = [npc, npe, fwd]
                        
        else:
            
            npc_list = [r_npc]
            npe_list = [r_npe]
            fwd_list = [r_fwd]
            
            for i in self._results_data.values():
                npc_list.append(i._data['NPC'])
                npe_list.append(i._data['NPE'])
                fwd_list.append(i._data['NPFWD'])
            
            best_npc = min(npc_list)
            worst_npc = max(npc_list)
    
            best_npe = min(npe_list)
            worst_npe = max(npe_list)
    
            best_fwd = min(fwd_list)
            worst_fwd = max(fwd_list)  
            
            
            r_npc = round((worst_npc - r_npc) / (worst_npc-best_npc),3)
            r_npe = round((worst_npe - r_npe) / (worst_npe-best_npe),3)
            r_fwd = round((worst_fwd - r_fwd) / (worst_fwd-best_fwd),3)
            
            npc_weight = self._multi_criteria_data['NPC'][0]
            npe_weight = self._multi_criteria_data['NPE'][0]
            fwd_weight = self._multi_criteria_data['FWD'][0]
            
            
            # Prepare Reference values
            
            if table_type == 'scores':
                data['Ref'] = [r_npc, r_npe, r_fwd]
            else:
                data['Ref'] = [r_npc * npc_weight, 
                               r_npe * npe_weight, 
                               r_fwd * fwd_weight]
                
                
            
            
            # Prepare calculated values
            for i,j in self._results_data.items():
                npc = round((worst_npc - j._data['NPC']) / (worst_npc-best_npc),3)
                npe = round((worst_npe - j._data['NPE']) / (worst_npe-best_npe),3)
                fwd = round((worst_fwd - j._data['NPFWD']) / (worst_fwd-best_fwd),3)
                
                if table_type == 'scores':
                
                    data[i] =[npc, npe, fwd]
                
                else:
                    
                    data[i] = [npc * npc_weight, npe * npe_weight, fwd * fwd_weight]
                    

            if table_type == 'relative closeness':
                C = {}
                
                for i,j in data.items():
                    d_p = abs(npc_weight-j[0]) + abs(npe_weight-j[1]) + abs(fwd_weight-j[2])
                    d_n = abs(0-j[0]) + abs(0-j[1]) + abs(0-j[2])       
                    C[i]  = [round(d_n / (d_p+d_n),5)]   
                
                data = C
    
        
            
        return data
                    
                    
   
        
    
              

                
