#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 10:33:07 2021

@author: philippkenkel
"""

from tabulate import tabulate



def MCDA_basic(design_dictionary):
    
    for i,j in design_dictionary.items():
        
        if i != 'MultiCriteria':
   
            npc = j._data['TAC'] * 1000000 / j._data['MainProductFlow']
            npe = j._data['GWP_TOT'] / j._data['MainProductFlow']
            fwd = j._data['FWD_TOT'] / j._data['MainProductFlow']
            
            print(f'{i} optimized design:')
            print('------------------------------')
            
            print(f'Net production costs are: {npc}')
            print('')
            print(f'Net CO2 emissions  are: {npe}')
            print('')
            print(f'Net fresh water demand is: {fwd}')
            print('')        
            
            print('Chosen Technologies are:')
            tec = j.return_chosen()
    
            for k,t in tec.items():
                print(k,t)
            
            print('')
            print('')
  
     

def MCDA_economics(design_dictionary):
    
    for i,j in design_dictionary.items():
        if i != 'MultiCriteria':
            capex = j._data['CAPEX']
            opex = j._data['OPEX']
            profits = j._data['PROFITS']
            
            el_costs = j._data['ENERGY_COST']['Electricity']/1000/opex*100
            hp_el = j._data['ELCOST']/opex/1000*100
            hex_cost = j._data['C_TOT']/opex/1000*100
            

            

            print(f'{i} optimized design:')
            print('------------------------------')            
            
            print('')
            print(f'CAPEX are: {capex}')
            print('')
            print(f'OPEX are: {opex}')
            print('')
            print(f'PROFITS are: {profits}')
            print('')
            print(f'Electricity share in OPEx is: {el_costs}')
            print('')
            print(f'Heat pump electrictiy share in OPEx is: {hp_el}')
            print('')           
            print(f'Heat exchanger share in OPEx is: {hex_cost}')
            print('') 
            print('') 


def create_table(design_dictionary, table_type = 'values'):
                              
    # Create empty lists for all calculated NPC, NPE and FWD values
    npc = []
    gwp = []
    fwd = []
    
    # Set values for conventional reference process
    
    ref_tac = design_dictionary['MultiCriteria']['NPC'][1]
    ref_gwp = design_dictionary['MultiCriteria']['NPE'][1]
    ref_fwd = design_dictionary['MultiCriteria']['FWD'][1]
    
    # Set values for weights
    
    npc_weight = design_dictionary['MultiCriteria']['NPC'][0]
    npe_weight = design_dictionary['MultiCriteria']['NPE'][0]
    fwd_weight = design_dictionary['MultiCriteria']['FWD'][0]   
    
    
    # Set MainProduct Flow
    
    mpf = design_dictionary['NPC']._data['MainProductFlow']
    
    # Calculate NPE, NPE and FWD from TAC, GWP and FWD
    ref_npc = ref_tac * 1e6 / mpf
    ref_gwp = ref_gwp / mpf
    ref_fwd = ref_fwd / mpf
    
    # Append to Lists
    
    npc.append(ref_npc)
    fwd.append(ref_fwd)
    gwp.append(ref_gwp)
    
        
    for i,j in design_dictionary.items():
        if i != 'MultiCriteria':
        # Calculate NPE, NPE and FWD from uns TAC, GWP and FWD
        
            npc1 = j._data['TAC'] * 1e6 / mpf
            npe1 = j._data['GWP_TOT'] / mpf
            fwd1 = j._data['FWD_TOT'] / mpf
            
            # Append to list
            npc.append(npc1)
            gwp.append(npe1)
            fwd.append(fwd1)
        
      
    # Search for best and worst values    
    npc_best = min(npc)
    npc_worst = max(npc)
    
    gwp_best = min(gwp)
    gwp_worst = max(gwp)
    
    fwd_best = min(fwd)
    fwd_worst = max(fwd)
    

    # Create empty dictionary for values
    
    table = {}
    
    
    if table_type == 'values':
        
        table['Ref'] = [ref_npc, ref_gwp, ref_fwd]
        
        for i,j in design_dictionary.items():
            if i != 'MultiCriteria':
                npc1 = j._data['TAC'] * 1e6 / mpf
                npe1 = j._data['GWP_TOT'] / mpf
                fwd1 = j._data['FWD_TOT'] / mpf
                
                table[i] = [npc1, npe1, fwd1]
            
        index  = ['NPC', 'NPE', 'FWD']
        table = tabulate(table, headers='keys', showindex=index)
            
    elif table_type == 'scores':
        npc1 = round((npc_worst - ref_npc) / (npc_worst-npc_best),3)
        npe1 = round((gwp_worst - ref_gwp) / (gwp_worst-gwp_best),3)
        fwd1 = round((fwd_worst - ref_fwd) / (fwd_worst-fwd_best),3)
            
        table['Ref'] = [npc1, npe1, fwd1]
            
        for i,j in design_dictionary.items():
            if i != 'MultiCriteria':
                npc1 = j._data['TAC'] * 1e6 / mpf
                npe1 = j._data['GWP_TOT'] / mpf
                fwd1 = j._data['FWD_TOT'] / mpf
                    
                npc1 = round((npc_worst - npc1) / (npc_worst-npc_best),3)
                gwp1 = round((gwp_worst - npe1) / (gwp_worst-gwp_best),3)
                fwd1 = round((fwd_worst - fwd1) / (fwd_worst-fwd_best),3) 
    
                table[i] = [npc1, gwp1, fwd1]
                
        index  = ['NPC', 'NPE', 'FWD']
        table = tabulate(table, headers='keys', showindex=index)

    elif table_type ==  'weighted scores':
        
        npc1 = round((npc_worst - ref_npc) / (npc_worst-npc_best),3)
        npe1 = round((gwp_worst - ref_gwp) / (gwp_worst-gwp_best),3)
        fwd1 = round((fwd_worst - ref_fwd) / (fwd_worst-fwd_best),3)
            
        table['Ref'] = [npc1 * npc_weight, npe1 * npe_weight , fwd1* fwd_weight]

        
        for i,j in design_dictionary.items():
            if i != 'MultiCriteria':
                npc1 = j._data['TAC'] * 1e6 / mpf
                npe1 = j._data['GWP_TOT'] / mpf
                fwd1 = j._data['FWD_TOT'] / mpf
                    
                npc1 = round((npc_worst - npc1) / (npc_worst-npc_best),3)
                gwp1 = round((gwp_worst - npe1) / (gwp_worst-gwp_best),3)
                fwd1 = round((fwd_worst - fwd1) / (fwd_worst-fwd_best),3) 
    
                table[i] = [npc1 * npc_weight, gwp1 * npe_weight , fwd1* fwd_weight]  
                
        index  = ['NPC', 'NPE', 'FWD']
        table = tabulate(table, headers='keys', showindex=index)     
           
    elif table_type == 'relative closenes':
        
        C = {}
            
        
        npc1 = round((npc_worst - ref_npc) / (npc_worst-npc_best),3)
        npe1 = round((gwp_worst - ref_gwp) / (gwp_worst-gwp_best),3)
        fwd1 = round((fwd_worst - ref_fwd) / (fwd_worst-fwd_best),3)
            
        table['Ref'] = [npc1 * npc_weight, npe1 * npe_weight , fwd1* fwd_weight]
            
        for i,j in design_dictionary.items():
            if i != 'MultiCriteria':
                npc1 = j._data['TAC'] * 1e6 / mpf
                npe1 = j._data['GWP_TOT'] / mpf
                fwd1 = j._data['FWD_TOT'] / mpf
                    
                npc1 = round((npc_worst - npc1) / (npc_worst-npc_best),3)
                gwp1 = round((gwp_worst - npe1) / (gwp_worst-gwp_best),3)
                fwd1 = round((fwd_worst - fwd1) / (fwd_worst-fwd_best),3) 
    
                table[i] = [npc1 * npc_weight, gwp1 * npe_weight , fwd1* fwd_weight]  

        for i,j in table.items():
            d_p = abs(npc_weight-j[0]) + abs(npe_weight-j[1]) + abs(fwd_weight-j[2])
            d_n = abs(0-j[0]) + abs(0-j[1]) + abs(0-j[2])       
            C[i]  = [round(d_n / (d_p+d_n),5)]   
                
        table = C
     
        table = tabulate(table, headers='keys')
        
        
        
    print('')
    print(table_type)
    print('--------')
    print(table)
    print('')
        
            
    


        
       
    
                