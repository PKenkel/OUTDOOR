#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:19:11 2021

@author: philippkenkel
"""

from pyomo.environ import value


class ProcessResults:
    
    # UNDER CONSTRUCTION
    
    def __init__(self, model_instance=None, solver_name = None, run_time = None):
        self._data = {}
        self._solver = None
        self._run_time = None


        if model_instance is not None:
            self._fill_data(model_instance)
        if solver_name is not None and run_time is not None:
            self._fill_information(solver_name, run_time)


# Private Methods ---- 
# --------------------
    def _fill_data(self, instance):

        for i in instance.component_objects():
            if "pyomo.core.base.var.SimpleVar" in str(type(i)):
                self._data[i.local_name] = i.value

            elif "pyomo.core.base.param.ScalarParam" in str(type(i)):
                self._data[i.local_name] = i.value

            elif "pyomo.core.base.param.IndexedParam" in str(type(i)):
                self._data[i.local_name] = i._data

            elif "pyomo.core.base.var.IndexedVar" in str(type(i)):
                self._data[i.local_name] = i.extract_values()

            elif "pyomo.core.base.set.SetProduct_OrderedSet" in str(type(i)):
                self._data[i.local_name] = i.value_list

            elif "pyomo.core.base.set.OrderedScalarSet" in str(type(i)):
                self._data[i.local_name] = i.value_list
                
            elif "pyomo.core.base.objective.SimpleObjective" in str(type(i)):
                self._data['Objective Function'] = i.expr.to_string()
            else:
                continue
            

    def _fill_information(self, solver_name, run_time):
        self._solver = solver_name
        self._run_time = run_time
        
        
        
# Public Methods ------
# ---------------------        
            
    def pprint(self, data_name=None):
        if data_name is None:
            for  i,j in self._data.items():
                if type(j) is dict:
                    print("\t \t"+ "Key "+' : ' +"Value "+ "\n")
                    for k,v in j.items():
                        print("\t \t"+ str(k)+ ' : ' +str(v))
                else:
                    print("\t \t"+ "Key "+' : ' +"Value "+ "\n")
                    print("\t \t"+ str(j)+ "\n")
            
        else:
            if type(self._data[data_name]) == dict:
                print("\t \t"+ "Key "+' : ' +"Value "+ "\n")
                for i,j in self._data[data_name].items():
                    print("\t \t"+ str(i)+ ' : ' +str(j)+ "\n")
            else:
                print(self._data[data_name])
                
                
    def return_chosen(self):
       flow = self._data['FLOW_IN']
       y = self._data['Y']
       names = self._data['Names']
       chosen  = {}
       
       for i,j in y.items():
           if j == 1:
               tot_flow = 0
               for k in flow.keys():
                   if i == k[0]:
                       tot_flow = tot_flow + flow[k]
               if tot_flow >= 0.00001 :
                   chosen[i] = names[i]
       return chosen
        