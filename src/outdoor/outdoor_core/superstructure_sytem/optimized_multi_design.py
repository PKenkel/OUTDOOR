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
from matplotlib.colors import ListedColormap
from matplotlib import cm
import numpy as np
import matplotlib




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
                    
                    
   
    def _collect_cross_parameter_data(self):
        npc_index = ['Case', 'NPC']
        npc_data = dict()
        
        for i,j in self._results_data.items():
            npc_data[i] = j._data['NPC']
            
        npc_table = tabulate(npc_data.items(), headers=npc_index)
        
        return (npc_table,npc_data)


    
    def _collect_results(self):
        results = dict()
        
        for i,j in self._results_data.items():
            results[i] = j._collect_results()

            


        return results

        

    def print_results(self):
        
        for i,j in self._results_data.items():
            print('')
            print(f'Identifier of Single run:{i}')
            j.print_results()
            
            
    def save_results(self, path):
        
        if not  os.path.exists(path):
            os.makedirs(path)
            
        path = path + '/' + 'results_file'  + self._case_time + '.txt'
        
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
            
        path = path + '/' + 'input_file' + self._case_time + 'data.txt'
        
        with open(path, encoding = 'utf-8', mode = 'w') as f:
            
            for i,j in self._results_data.items():
                f.write(f'Identifier of single run: {i} \n')
                all_data = j._data
                
                for k,t in all_data.items():
                    f.write(f'{k}: {t} \n \n')
                    
                f.write(' ----------------- \n \n')


            

    def save_file(self, path, option='raw'):
        """

        Parameters
        ----------
        path : String type of where to save the ProcessResults object as pickle
        class object.

        """
        if not  os.path.exists(path):
            os.makedirs(path)  
            
        if option == 'tidy':
            
            for i in self._results_data.values():
                i._tidy_data()
                
        path = path + '/' + 'data_file' + self._case_time + '.pkl'
        
        with open(path, 'wb') as output:
            pic.dump(self, output, protocol=4)




    def create_sensitivity_graph(self):
        
        if self._optimization_mode == 'Sensitivity analysis':
        
            data  = self._collect_sensi_data()
            
            len_ = len(data)
            
            fig = plt.figure()
            
            count = 1
  
            for i,j in data.items():
                
                x_vals = j[0]
                y_vals = j[1]
                titel = i

                ax = fig.add_subplot(len_,1,count)
                
                ax.set_xlabel(titel)
                ax.set_ylabel('Net production costs in €/t')

                
                ax.plot(x_vals, y_vals, linestyle='--', 
                    marker='o')  
                
                count +=1
                
            
            return fig
        else:
            print('Sensitivity graph presentation only available for  \
                  Sensitivity analysis mode')
            


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



    def create_plot_bar(self, 
                        user_input, 
                        save='No',
                        Path=None):
        
        for i,j in self._results_data.items():
            
            
            j.create_plot_bar(user_input,
                              save,
                              Path)
            
    def create_flowsheet(self, path):
        
        for i,j in self._results_data.items():
            
            path_  = path + '/' + str(i)
            
            j.create_flowsheet(path_)
            



    def _get_contour_numbers(self, process_design, plist):
        """

        Parameters
        ----------
        process_design : ProcessResults File
            DESCRIPTION.
        plist : List
           List with number of processes to be checked if chosen

        Returns
        -------
        number : Int
            Number associated with the chosen technology combination
        string : String
            Name of the technology combination
            
        Description
        -----------
        Takes a ProcessResults object and checks for alle chosen technologies if
        the required technologies (in plist) are chosen in this design. 
        Afterwards hands back the identifier for the technology choices and the name.

        """
        
        # Set-up required variables:
        number = 0
        string_list = list()
        
        # Retreave chosen technologies for the current ProcessDesign
        
        dic = process_design.return_chosen()

        # Set up the numbers for the colorcontours , depending on number 
        # of checkable processes.

        if len(plist) == 2:
            numbers = {plist[0]:1,
                       plist[1]:2}
            
        if len(plist) == 3: 
            numbers = {plist[0]:1,
                       plist[1]:2,
                       plist[2]:4}
            
        if len(plist) == 4: 
            numbers = {plist[0]:1,
                       plist[1]:2,
                       plist[2]:4,
                       plist[3]:8}   
         
        # Check which processes are chosen in the current processdesign 
        pset = set(plist)
        dset = set(dic.keys())
        cset = pset.intersection(dset)
        
        
        # Iterate through the set of chosen and searched processes and safe the 
        # according number and process name string
        
        for i in cset:
            number += numbers[i]
            string_list.append(dic[i])
            
        string = str(string_list)

        
        return number, string        



    def _get_2d_array(self, input_, iterator):
        """
        

        Parameters
        ----------
        input_ : 1 Dimensional list 
        iterator : Int
            Lenth of the x / y axis

        Returns
        -------
        output_ : 2-dimensional numpy array

        Description
        -----------
        
        Takes a one dimensional list with two dimensional data and converts
        it into a two dimensional numpy array, which is readable for matplotlibs
        imshow graph. 
        """
        
        # Set-up required variables
        
        list1 = list()
        temp = list()
        count = 0
        
        # Iterate through the input and produce a 2-dimensional list from it
        
        for j in input_:
            count +=1 
            if count <=iterator:
                temp.append(j)
            else:          
                list1.append(temp)
                temp = []
                temp.append(j) 
                count = 1
                
        list1.append(temp)   
        
        # Convert list into numpy array
        output_ = np.array(list1)
        
        return output_        




            
    def _get_graph_data(self, process_list): 
        """
        
        Parameters
        ----------
        process_list : List
            Process numbers to be checked.

        Returns
        -------
        X : Numpy array
            x-axis values
        Y : Numpy array
            y-axis values
        Z : Two-dimensional Numpy array
            Net production costs of x and y
        C : Two-dimensional Numpy array
            Map of indentifiers for technology choice of x and y
        label_dict : Dictionary
            Dictionary with labels and identifier numbers 
            
        Description
        -----------
        
        Iterates through all ProcessDesigns in the MultipleDesign and calls:
            - self._get_contour_numbers
            - self._get_2d_array
            
        It gets all x and y-axis data from the ProcessResults as well as 
        net production costs(NPC), from there it creates the axis and 
        two-dimensional Z and C arrays which hold costs and technology choice 
        information.

        """
        
        # Set-up required variables
        
        label_dict = dict()
        n_list = list()
        x = list()
        y = list()
        z = list()
        
        # Iterate through all ProcessResults and get x,y,z and c values
        for i,j in self._results_data.items():
            
            npc = j._data['NPC']
            
            x.append(i[1])
            y.append(i[3])
            z.append(round(npc,0))
            
            n,s  = self._get_contour_numbers(j, process_list)
            
            if n not in label_dict.keys():
                label_dict[n] = s
                
            n_list.append(n)   
            
        iterator = len(set(x))
        
        # Turn x- and y-axis lists into numpy arrays
        
        y1 = np.array(list(dict.fromkeys(y)))
        x1 = np.array(list(dict.fromkeys(x)))
        
        # Produce meshgrid and Z and C for imshow / contour plots
    
        X,Y = np.meshgrid(x1,y1)  
        
        Z = self._get_2d_array(z, iterator)
        C = self._get_2d_array(n_list, iterator)
        
        Z = np.transpose(Z)
        C = np.transpose(C)    
        
        return X,Y,Z,C,label_dict    

        


    def create_crossparater_graph(self,process_list, xlabel, ylabel, clabel):
        
        # Define color-palette for usage
        
        color_palette = ['blue', 
                         'red', 
                         'orange', 
                         'green', 
                         'limegreen', 
                         'grey', 
                         'mediumpurple', 
                         'magenta',
                         'cyan',
                         'goldenrod',
                         'lightgrey',
                         'skyblue',
                         'moccasin',
                         'lightpink',
                         'olive']     
        
        
        # Define set_axes method for convenience
        
        def set_axes(x,y):
            x_max = float(np.max(x))
            x_min = float(np.min(x))
            y_max = float(np.max(y))
            y_min = float(np.min(y))
            
            x_ticks = x[0]
            y_ticks = np.transpose(y)[0]
            
            for i in range(len(x_ticks)):
                x_ticks[i] =round(x_ticks[i],0)
                
            for i in range(len(y_ticks)):
                y_ticks[i] =round(y_ticks[i],0)       
            
            return x_max, x_min, y_max, y_min, x_ticks, y_ticks
        
        
        
        # Get x,y,z,c, and labels from get_graph_data
        # Get axis data from set_axes method
        

        x,y,z,c,label_dict = self._get_graph_data(process_list)
        x_max, x_min, y_max, y_min, x_ticks, y_ticks = set_axes(x,y) 
        
        
        # Set-up figure 
        plt.rcParams['figure.dpi'] = 400
        plt.rcParams["font.family"] = "serif"   
        
        fig = plt.figure()


        # Prepare labels for the colorbar              

        labels = list()
        col_dict = dict()
        label_items = sorted(label_dict.keys())
                
        for i in label_items:
            col_dict[i] = color_palette[i+1]
            labels.append(label_dict[i])
            
    
        # Create custom colormap for imshow figure
        cm = ListedColormap([col_dict[t] for t in col_dict.keys()])
        
        
        labels= np.array(labels)
        len_lab = len(labels)
        norm_bins = np.sort([*col_dict.keys()]) + 0.5
        norm_bins = np.insert(norm_bins, 0, np.min(norm_bins) - 1.0)
    
        # Prepare format of the colorbar
        norm = matplotlib.colors.BoundaryNorm(norm_bins, len_lab, clip=True)       
        fmt = matplotlib.ticker.FuncFormatter(lambda k, pos: labels[norm(k)])   
        diff = norm_bins[1:] - norm_bins[:-1]
        tickz = norm_bins[:-1] + diff / 2

        
    
        # Create graph 1: Heatmap of technology choice (c)
    
        ax = fig.add_subplot(111)
        
        graph_1 = ax.imshow(c, 
                            cmap=cm,
                            norm=norm,
                            extent= [x_min,x_max,y_min,y_max], 
                            interpolation='none', 
                            origin = 'lower',
                            aspect='auto',
                            alpha=1)
    
    
        cbar = plt.colorbar(graph_1,
                            format=fmt,
                            ticks = tickz,
                            label=clabel, 
                            shrink=1)
        
    
        		

        # Create graph 2: Contour levels of NPC (z)
        
        contour_levels = list(np.linspace(np.min(z)+5, np.max(z)-5, 10))
    
        
        ax = fig.add_subplot(111)       
        graph_2 = ax.contour(x,y,z,
                             colors='black',
                             levels=contour_levels)
        
         
        ax.clabel(graph_2, 
                  fmt='%1.0f €/MWh', 
                  fontsize = 8)
        
        
          
        
        
        # Set lables of axes
        
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    
        plt.show()









     
    
              

                
