#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 12:19:11 2021

@author: philippkenkel
"""

from pyomo.environ import value
from tabulate import tabulate
import os 
import datetime
import cloudpickle as pic
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pydot





class ProcessResults:
    
    
    def __init__(self,model_instance=None, solver_name = None, run_time = None):
        self._data = {}
        self._solver = None
        self._run_time = None
        self._case_time = None
        self._objective_function = None
        self._product_load = None
        
        

        if model_instance is not None:
            self._fill_data(model_instance)
        if solver_name is not None and run_time is not None:
            self._fill_information(solver_name, run_time)


# Private Methods ---- 
# --------------------


    # Filling methods, to create data file 

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
                    
                self._data['Objective Function'] = i.expr.to_string()
            
            elif "pyomo.core.base.objective.ScalarObjective" in str(type(i)):
                
                self._data['Objective Function'] = i.expr.to_string()
            else:
                continue

            

    def _fill_information(self, solver_name, run_time):
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
        self._objective_function = self._data['Objective Function']
        self._product_load = self._data['MainProductFlow']
        
        


    # Extracting methods to get important results
    

    
    def _collect_basic_results(self):
        """
        Decription
        -------       
        Collects basice results data from the ProcessResults._data dictionary 
        for further results output. Data that is collected is:
            Objective function name, Yearly product load, Solver name and run time
            Net production costs (in €/ton), Net production GHG emissione (t/t) and
            Net production fresh water demand (t/t)
        Data is collected and returned as dictionary.

        Returns
        -------
        basic_results : Dictionary

        """
        
        basic_results = {}
        
        basic_results['Basic results'] = {}
        
        basic_results['Basic results']['Objective Function'] = \
            self._objective_function
            
        basic_results['Basic results']['Yearly product load'] = \
            self._product_load
            
        basic_results['Basic results']['Solver run time'] = \
            self._run_time
            
        basic_results['Basic results']['Solver name'] = \
            self._solver        
            
        basic_results['Basic results']['Net production costs'] = \
            round(self._data['NPC'], 2)
            
        basic_results['Basic results']['Net production GHG emissions'] = \
            round(self._data['NPE'], 3)
            
        basic_results['Basic results']['Net present FWD'] = \
            round(self._data['NPFWD'], 3)
            
        return basic_results

     
    def _collect_capitalcost_shares(self):
        """
        Decription
        ----------
        Collects data from the ProcessResults._data dictionary. 
        Data that is collected are the shares (in %) of different unit-operations
        in the total annual capital investment. Data is returned as dictionary

        Returns
        -------
        capitalcost_shares : Dictionary

        """
        capitalcost_shares = {'Capital costs shares': {}}
        
        total_costs = self._data['CAPEX']
        
        capitalcost_shares['Capital costs shares']['Heat pump'] \
            = round(self._data['ACC_HP'] / total_costs *100,2)
        
        
        for i,j in self._data['ACC'].items():
            if j >= 1e-3:
                index_name = self._data['Names'][i]
                capitalcost_shares['Capital costs shares'][index_name] \
                    = round((j + self._data['TO_CAPEX'][i]) / total_costs * 100,2)
        
        
        return capitalcost_shares
    

    def _collect_economic_results(self):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary. 
        Data that is collected are base economic values, and depict the shares
        of the total costs of:
            CAPEX (all unit-operations)
            Raw material purchase
            Electricity costs
            Chilling costs
            Heat integration costs (Heating, Cooling utilities as well as HEN)
            Operating and Maintenance
            Waste water treatment
            Profits from Byproducts
 
        Returns
        -------
        economic_results : Dictionary

        """
        economic_results = {'Economic results': {}}
        
        total_costs = self._data['TAC'] / 1000

        profits  = 0
        wwt  = 0
        
        for i,j in self._data['PROFITS'].items():
            if j < 0:
                wwt -= j * self._data['H'] / 1000
            else:
                profits -= j * self._data['H'] / 1000
                
                
        
        economic_results['Economic results']['CAPEX share'] \
            = round(self._data['CAPEX'] / total_costs * 100,2)
        
        economic_results['Economic results']['Raw material consumption share'] \
            = round(self._data['RM_COST_TOT'] /1000 / total_costs * 100, 2)
            
        economic_results['Economic results']['Operating and Maintanence share'] \
            = round(self._data['M_COST_TOT'] / total_costs * 100, 2)
            
        economic_results['Economic results']['Electricity share'] \
            = round((self._data['ENERGY_COST']['Electricity'] + \
                   self._data['ELCOST']) /1000 / total_costs * 100, 2)
        
        economic_results['Economic results']['Chilling share'] \
            = round(self._data['ENERGY_COST']['Chilling'] /1000 / total_costs * 100, 2)  
            
        economic_results['Economic results']['Heat integration share'] \
            = round(self._data['C_TOT'] / 1000 / total_costs * 100, 2)
                  
        economic_results['Economic results']['Waste treatment share'] \
            = round(wwt / total_costs * 100, 2)
        
        economic_results['Economic results']['Profits share'] \
            = round(profits / total_costs * 100, 2)
            
            
        return economic_results
            
        
    def _collect_electricity_shares(self):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary. 
        Data that is collected are the shares (in %) of different unit-operations
        in the total electricity demand . 

        Returns
        -------
        electricity_shares : Dictionary


        """
        electricity_shares = {'Electricity demand shares': {}}
                
        total_el = self._data['ENERGY_DEMAND_HP_EL'] * self._data['H']
         
        for i,j in self._data['ENERGY_DEMAND'].items():
            if i[1] == 'Electricity' and j >= 1e-05:
                total_el += j * self._data['flh'][i[0]]
        

        
        electricity_shares['Electricity demand shares']['Heatpump electricity share'] \
            = round(self._data['ENERGY_DEMAND_HP_EL'] * self._data['H'] \
                    / total_el * 100, 2)
        
                
        for i,j in self._data['ENERGY_DEMAND'].items():
            if i[1] == 'Electricity' and j >= 1e-05:
                index_name = self._data['Names'][i[0]]
                electricity_shares['Electricity demand shares'] \
                    [index_name] \
                    = round(j * self._data['flh'][i[0]] / total_el * 100, 2)
    

        return electricity_shares
       
                
    def _collect_heatintegration_results(self):
        """
        Description
        -----------
        
        Collects data from the ProcessResults._data dictionary. 
        Data that is collected are basic heat integration data:
            Total heating / cooling demand (in MW)
            Total heat recovery (from unit-operations) (in MW)
            Total High pressure steam production, internal (in MW)
            Total internal usage of this HP steam (rest is sold to market)
            Total Heat supplied by High Temperature heat pump (in MW)
            Net heating and cooling demand (in MW)
            
        Returns
        -------
        heatintegration_results : Dictionary


        """
        heatintegration_results = {'Heating and cooling': {}}
        
        total_heating = 0
        total_cooling = 0
        net_heating = 0
        steam = 0
        
        for i in self._data['ENERGY_DEMAND_HEAT_UNIT'].values():
            if i >= 1e-05:
                total_heating += i 
                
        for i in self._data['ENERGY_DEMAND_COOL_UNIT'].values():
            if i >= 1e-05:
                total_cooling += i
            
        for i in self._data['ENERGY_DEMAND_HEAT_PROD'].values():
            if i >= 1e-05:
                steam += i
                
        for i in self._data['ENERGY_DEMAND_HEAT_DEFI'].values():
            if i >= 1e-05:
                net_heating += i
            
        heatintegration_results['Heating and cooling']['Total heating demand'] \
            = round(total_heating, 2)  
            
        heatintegration_results['Heating and cooling']['Total cooling demand'] \
            = round(total_cooling, 2)       

        heatintegration_results['Heating and cooling']['Total heat recovery'] \
            = round(self._data['EXCHANGE_TOT'], 2)
            
        heatintegration_results['Heating and cooling']['HP Steam produced'] \
            = round(steam, 2)                                        

        heatintegration_results['Heating and cooling']['Internally used HP Steam'] \
            = round(self._data['ENERGY_DEMAND_HEAT_PROD_USE'], 2)
        
        heatintegration_results['Heating and cooling']\
            ['High temperature heat pump heat supply'] \
            = round(self._data['ENERGY_DEMAND_HP_USE'],2)

        heatintegration_results['Heating and cooling']['Net heating demand'] \
            = round(net_heating, 2)    
        
        heatintegration_results['Heating and cooling']['Net cooling demand'] \
            = round(self._data['ENERGY_DEMAND_COOLING'], 2)          
        
        
        return heatintegration_results
            
        
    def _collect_GHG_results(self):
        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary. 
        Data that is collected are the annual GHG emissions from:
            Direct emissions in unit-operations (sum in t/y)
            Indirect emissions from Electricity and Chilling (sum in t/y)
            Indirect emissions from Heat (sum in t/y)
            Emissions from building the plant (t/y)
            Emissions from buying raw materials / Negative emissions 
                from carbon capture (t/y)
            Avoided burden credits from byproduct selling (t/y)

        Returns
        -------
        GHG_results : Dictionary

        """
        GHG_results = {'Green house gas emission shares': {}}
            
        ghg_d = 0   
        ghg_b = 0
        ghg_ab = 0
        
        for i in self._data['GWP_U'].values():
            if i is not None and i >= 1e-05:
                ghg_d += i
                
        for i in self._data['GWP_UNITS'].values():
            if i is not None and i >= 1e-05:
                ghg_b += i
                
        for i in self._data['GWP_CREDITS'].values():
            if i is not None and i >= 1e-05:
                ghg_ab += i

        GHG_results['Green house gas emission shares']['Direct emissions'] \
            = round(ghg_d, 0)
            
        GHG_results['Green house gas emission shares']['Electricity'] \
            = round(self._data['GWP_UT']['Electricity'], 0)
            
        GHG_results['Green house gas emission shares']['Heat'] \
            = round(self._data['GWP_UT']['Heat'], 0)
                       
        GHG_results['Green house gas emission shares']['Chilling'] \
            = round(self._data['GWP_UT']['Chilling'], 0)
                        
        GHG_results['Green house gas emission shares']['Plant building emissions'] \
            = round(ghg_b, 0)
            
        GHG_results['Green house gas emission shares']['Raw Materials / Carbon Capture'] \
            = round(-self._data['GWP_CAPTURE'], 0) 
                    
        GHG_results['Green house gas emission shares']['Avoided burden for byproducts'] \
            = round(-ghg_ab, 0)         
        

        
        return GHG_results
    

    def _collect_FWD_results(self):

        """
        Description
        -----------
        Collects data from the ProcessResults._data dictionary. 
        Data that is collected are the annual fresh water demand from:
            Indirect demand from Electricity and Chilling (sum in t/y)
            Indirect demand from Heat (sum in t/y)
            Demand from buying raw materials 
            Avoided burden credits from byproduct selling (t/y)

        Returns
        -------
        FWD_results: Dictionary
        """
        
        FWD_results = {'Fresh water demand shares': {}}
        
        FWD_results['Fresh water demand shares']['Indirect demand from raw materials'] \
            = round(-self._data['FWD_S'], 0)
        
        FWD_results['Fresh water demand shares']['Utilities (Electricity and chilling)'] \
            = round(self._data['FWD_UT1'], 0)

        FWD_results['Fresh water demand shares']['Utilities (Heating)'] \
            = round(self._data['FWD_UT2'], 0)
            
        FWD_results['Fresh water demand shares']['Avoided burden from byproducds'] \
            = round(-self._data['FWD_C'], 0)

        return FWD_results
    

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
        
        self.results = {}
        
        self.results.update(self._collect_basic_results())
        
        chosen_technologies = {'Chosen technologies': self.return_chosen()}
        self.results.update(chosen_technologies)
        
        self.results.update(self._collect_economic_results())
        self.results.update(self._collect_capitalcost_shares())
        self.results.update(self._collect_electricity_shares())
        self.results.update(self._collect_heatintegration_results())
        self.results.update(self._collect_GHG_results())
        self.results.update(self._collect_FWD_results())
        
        return self.results                
        
                        



        
        
        
# Public Methods ------
# --------------------- 


    def create_plot_bar(self, 
                        user_input, 
                        save = False,    
                        Path = None,
                        gui = False):
        
                
        
        fig = plt.figure()
        ax1 = fig.add_subplot()
        
  

        data = self._collect_results()[user_input]
        
        labels = list()
        values = list()
        
        for i,j in data.items():
            labels.append(i)
            values.append(j)
        
        value_sum = round(sum(values))
        
        series = pd.Series(data=data, index=data.keys(), name=' ')
        
        plot_labels = {'Breakdown': None,
                       'titel': user_input,
                       'total': ' ',
                       }
        
        
        if value_sum == 100:
            plot_labels['Breakdown'] = 'Breakdown (%)'
            
            if user_input == 'Economic results':
                NPC = round(self._data['NPC'])
                plot_labels['total'] = f'NPC are {NPC} €/ ton'         
          
        else:
            if user_input == 'Heating and cooling':
                plot_labels['Breakdown'] = 'Amounts in MW'

            else:
                plot_labels['Breakdown'] = 'Breakdown'

        

        
        if plot_labels['total']:   
          total = plot_labels['total']
        else:
          total = None
         
        titel = plot_labels['titel']
        
      
        plt.rcParams['figure.dpi'] = 160
        
        my_colors = plt.cm.Greys(np.linspace(0.0, 0.7, len(values)))
        
        axes = pd.DataFrame(series).T.plot(
                                           kind='bar', 
                                           stacked=True,
                                           rot='horizontal', 
                                           figsize=(3, 4),
                                           title= f' {titel}, {total}',
                                           edgecolor = 'k',
                                           color=my_colors,
                                           legend=None,
                                           ax = ax1
                                           )                
        
        ax1.tick_params(
                        axis='x',          
                        which='both',      
                        bottom=False,      
                        top=False,        
                        labelbottom=False
                        )
        
        axes.spines['top'].set_visible(False)
  
        colLabels = [plot_labels['Breakdown'] for i in range(len(values))]
        array=(np.array(values, dtype=float).reshape((len(values), 1)))
        
        ax1.table(cellText=array,
                          rowLabels=labels,
                          rowColours=my_colors,
                          colLabels=colLabels,
                          cellLoc='center',
                          loc='bottom'
                        )    


              
        # Save input file if save statement = True
        if save == True:
            date_time_now = datetime.datetime.now().strftime("%Y_%m_%d__%H-%M-%S")
            
            if Path == None:
                my_path = os.path.abspath(__file__)
                plt.savefig('/{}_Chart_{}.pdf'.format(date_time_now, user_input), dpi=160, bbox_inches='tight')
                print('Saved in {}'.format(my_path))
    
            if Path is not None:
                assert os.path.exists(
                    Path), "This file path does not seem to exist: "+str(Path)
                plt.savefig(Path.rstrip('.py')+'/{}_Chart_{}.pdf'.format(date_time_now, user_input), dpi=160, bbox_inches='tight')
                print('Saved in {}'.format(Path))
        
        
                
        # Create temp-file for presentation in GUI
        if gui == True:     
            plt.savefig('temp/new.png', dpi =160, bbox_inches='tight')
            
            


        return fig



    def save_results(self, path):
        """

        Parameters
        ----------
        path : String type of where to save the results as .txt file

        Decription
        -------
        Collects all important results from the ProcessResults Class object and 
        saves the data as tables in a text file.

        """
        all_results = self._collect_results()
        
        if not  os.path.exists(path):
            os.makedirs(path)
        
        
        path = path + '/results_file' + self._case_time + '.txt'
          
        with open(path, encoding='utf-8', mode = 'w') as f:
                        
            for i,j in all_results.items():
                table = tabulate(j.items())
                
                f.write('\n')
                f.write(i)
                f.write('-------- \n')
                f.write(table)
                f.write('\n')
                f.write('\n \n')

            print('')


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
        
        if not  os.path.exists(path):
            os.makedirs(path)        
            
        path = path + '/' + 'input_file' + self._case_time + '_data.txt'
        

        
        with open(path, encoding = 'utf-8', mode = 'w') as f:
            
            for i,j in self._data.items():
                f.write(f'{i}: {j} \n \n')


    def save_file(self, path):
        """

        Parameters
        ----------
        path : String type of where to save the ProcessResults object as pickle
        class object.

        """
        
        path = path + '/' + 'data_file' + self._case_time + '.pkl'
        
        with open(path, 'wb') as output:
            pic.dump(self, output)
            


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
               if tot_flow >= 0.0001 :
                   chosen[i] = names[i]
       return chosen
        




    def print_results(self):
        """
        Description
        -------
        Collects all important results data and prints them as tables to the 
        console. 

        """
        
        all_results = self._collect_results()
        
        for i,j in all_results.items():
            print('')
            print('')
            print(i)
            print('--------------')        
            print(tabulate(j.items()))         
            print('')
            
         
            
    def create_flowchart(self, path):
        
        def make_node(graph, name, shape):
            """
            Parameters
            ----------
            graph : Dot class
            name : String

            shape : String (Options check documentation of graphviz module)

         
            Returns
            -------
            node : Pydot Node object

            """
            
            node = pydot.Node(name, height=0.5, width=2, fixedsize=True)
            node.set_shape(shape)
            graph.add_node(node)
            
            return node
        
        def make_link(graph, a_node, b_node, label = None, width = 1,  
                      style = 'solid'):
            """

            Parameters
            ----------
            graph : Dot object
            a_node : pydot node object (starting point)
            b_node : pydot node object (ending point)
            label : Label (can be string but also float etc. )
            width : 
                DESCRIPTION. The default is 1.
            style : TYPE, optional
                DESCRIPTION. The default is 'solid'. For options check
                            documentation of graphviz module
 
            Returns
            -------
            edge : pydot Edge object

            """
            edge = pydot.Edge(a_node, b_node)
            edge.set_penwidth(width)
            edge.set_style(style)
            
            if label is not None:
                edge.set_label(label)
                
            graph.add_edge(edge)
            
            return edge
                
        data = {}
        
        for i,j in self._data['FLOW_FT'].items():
            if j > 1e-04:
                data[i] = round(j, 2)
                
        for i,j in self._data['FLOW_ADD'].items():
            if j > 1e-04:
                data[i] =round(j,2)
                     

        flowchart  = pydot.Dot('flowchart', rankdir = 'LR', ratio="compress", 
                               size="15!,1",  dpi="500")
        
        # size="width, height" -> definiert MAXIMUM Breite/Höhe. Wenn "!" 
        # hinter der zahlt steht, ist es die MINIMUM Breite/Höhe
     
        nodes = {}
        edges = {}    

        for i,j in data.items():
           
            for v in i:
                
                if v not in nodes.keys():
                    
                    if v in self._data['U_S']:
                        nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                                'ellipse')
                         
                    elif v in self._data['U_STOICH_REACTOR']:
                        
                        if v in self._data['U_TUR']:
                            nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                            'doubleoctagon') 
                            
                        elif v in self._data['U_FUR']:
                            nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                            'doubleoctagon')
                           
                        else:
                            nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                                 'octagon')
       
                    elif v in self._data['U_YIELD_REACTOR']:
                        nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                            'octagon')
         
                    elif v in self._data['U_PP']:
                        nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                            'house')
               
                    elif v in self._data['U_DIST']:
                        nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                            'circle')
                        
                    else:
                        nodes[v] = make_node(flowchart, self._data['Names'][v], 
                                            'box')

        
        for i,j in data.items():
            edges[i[0],i[1]] = make_link(
                flowchart, nodes[i[0]], nodes[i[1]], f'{j} t/h')
            
        if not  os.path.exists(path):
            os.makedirs(path)
            
        path  = path + '/flowchart.png'
            
        flowchart.write_png(path)    
    

        