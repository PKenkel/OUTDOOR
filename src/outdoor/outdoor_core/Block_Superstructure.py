
import copy
from .Block_Capex import capex_calculator


class Superstructure():  
    
    
    def __init__(self, ModelName, Objective, MainProduct=None, ProductLoad=None, *args, **kwargs):
        
        super().__init__()
        
        
        # Lists
        # -----
        
        self.Objective_dic = {'NPE' : 'NPE', 'NPC': 'NPC'}
        self.Data_File = {None: {}}
        self.ModelName = ModelName
        
        
        # Unit Operations
        self.UnitsList = []
        self.UnitsNumberList = {'U': []}    
        self.UnitsNumberList2 = {'UU': []}   
        self.StoichRNumberList = {'U_STOICH_REACTOR': []}
        self.YieldRNumberList = {'U_YIELD_REACTOR': []}
        self.SplitterNumberList = {'U_SPLITTER': []}
        self.HeatGeneratorList = {'U_FUR' : []}
        self.ElectricityGeneratorList = {'U_TUR': []}
        self.ProductPoolList = {'U_PP': []}
        self.CostUnitsList = {'U_C':[]}
        self.SourceList = {'U_S': []}
        self.SourceSet = {'U_SU': []}
        
        
        
        # Heat Balance
        self.HeatIntervalList =  {'HI': []}
        self.HeatUtilitiesList = {'H_UT': []}

        # Others
        self.ComponentsList = {'I': []}
        self.ReactionsList = {'R': []}
        self.ReactantsList ={'M': []}
        self.UtilitiesList = {'UT' :[]}
        self.LinPointsList = {'J': []}
        self.LinIntervalsList = {'JI': []} 
        self.UnitNames = {'Names': {}}
        self.Heat_Temperatures = []
        self.HeatIntervals = {}
        
        # ParameterList
        self.NI_ParameterList =[]
        self.I_ParameterList =[]
        self.Database = None
        

        
        # Non-indexed Attributes
        # ----------------------
        
        try: 
            self.Objective = self.Objective_dic[Objective]
        except:
            self.Objective = 'NPC'
            
             
        self.MainProduct = MainProduct
        self.ProductLoad = ProductLoad
        self.NPC  = 0
        self.NPE = 0
        self.CAC = 0 
        
        
        self.IR = {'IR': 0}
        self.H = {'H': 0}
        self.K_O = {'K_OM' : 2.06875}
        self.CECPI = {'CECPI': 0}
        
        self.hourly_wage = {'hourly_wage': 41}
        self.working_hours = {'working_hours': 8322}
        self.capacity_flow = {'capacity_flow': None}
        self.process_steps = {'process_steps': 4}
        
        self.HP_Costs = {'HP_Costs': 0}
        self.HP_ACC_Factor = {'HP_ACC_Factor': 0}
        self.COP_HP = {'COP_HP': 3}
        self.HP_LT = None
        self.HP_T_IN = {}
        self.HP_T_OUT = {}
        self.HP_active = False
        
        self.linearizationDetail = 'average'

        
        
        
        # Indexed Attributes
        # ------------------
        
        self.CECPI_dic = {1994: 368.1, 1995: 381.1, 1996: 381.7, 1997: 386.5,
                          1998: 389.5, 1999: 390.6, 2000: 394.1, 2001: 394.3,
                          2002: 395.6, 2003: 402.0, 2004: 444.2, 2005: 468.2,
                          2006: 499.6, 2007: 525.4, 2008: 575.4, 2009: 521.9,
                          2010: 550.8, 2011: 585.7, 2012: 584.6, 2013: 567.1,
                          2014: 576.1, 2015: 556.8, 2016: 541.7, 2017: 566.1,
                          2018: 603.1}
        
        
        self.delta_rm = {'delta_rm': {}}
        self.delta_el = {'delta_el': 50}
        self.delta_q = {'delta_q': {}}
        self.delta_cool = {'delta_cool': 14}

        
        self.lhv = {'LHV':{}}
        self.em_fac_ut = {'em_fac_ut': {}}
        self.em_fac_comp = {'em_fac_comp': {}}
        self.alpha = dict()
        
        self.heat_utilities = {}
        
        
        
   



     
        

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------SET PARAMETERS METHODS------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

        
    def set_operatingHours(self, hours):
        self.H['H'] = hours
        
    def set_interestRate(self, IR):
        self.IR['IR'] = IR
        
    def set_omFactor(self, OM):
        self.K_O['K_OM'] = OM
        
    def set_cecpi(self, year):
        """
        Parameters
        ----------
        year : Integer
            Years from 1994 up to 2018 can be entered here
            
        """
        self.CECPI['CECPI'] = self.CECPI_dic[year]
        
            

    def set_heatPump(self, 
                     SpecificCosts,
                     LifeTime,
                     COP,
                     T_IN,
                     T_OUT
                     ):
        """

        Parameters
        ----------
        SpecificCosts : Float
            Specific Costs of Heat Pump in €/kW_installed Heat supply.
        LifeTime : Integer
            Lifetime of Heatpump in full years.
        COP : Float
            Coefficient of performance of heat pump, should be higher than 1.
        T_IN : Integer
            Inlettemperature of heat pump (low-ex temperature).
        T_OUT :Integer
            Goal Temperature of Heat Pumpt (e.g. low pressure steam).

        Description
        -------
        If "HP_active" == true, this method sets the values of the heat pump. 
        These values are used while initiating the superstructure to find the 
        Temperatureintervals in the Heatbalance as well as supplied heat and costs.
        If "HP_active" == false, this method will be skipped, and the model will
        not regard a heat pump in the heat balances.

        """
        try:
            self.HP_active = True
            self.HP_Costs['HP_Costs'] = SpecificCosts
            self.COP_HP['COP_HP']  = COP
            self.HP_LT = LifeTime
            self.HP_T_IN['Temperature'] = T_IN
            self.HP_T_OUT['Temperature'] = T_OUT
            self.__set_heatTemperatures(T_IN, T_OUT)
 
        except:
            print('Please chose for State either On or Off, a non-negative \
                  lifetime and for COP a value > 1')        

    def set_linearizationDetail(self, Detail):
        """
        Parameters
        ----------
        Detail : String
            Use: "fine" , "average" or "rough"
            
        Context
        -------
        Based on the Input different amounts of Intervals are calculated for the
        CAPEX of the process equipment:
            
            fine     :  300 
            average  :  20 
            rough    :  10  
            
        """
        self.linearizationDetail = Detail
 

    def set_numberProcessSteps(self, Number):
        self.process_steps['process_steps']  = Number

        

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------ADD COMPONENTS TO LIST METHODS ---------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------



        
    def add_UnitOperations(self, *args):
        """
        Parameters
        ----------
        *args : Either List of Process Objects or Single Objects
            Takes a number of Process Objects and sorts them into the UnitLists

        """

        for i in args:
            if type(i) == list:
                for j in i:
                    if j not in self.UnitsList:
                        self.UnitsList.append(j)
                        self.UnitsNumberList['U'].append(j.Number)
                        self.UnitsNumberList2['UU'].append(j.Number)
                        if j.Type == 'Stoich-Reactor':
                            self.StoichRNumberList['U_STOICH_REACTOR'].append(j.Number)
                            self.CostUnitsList['U_C'].append(j.Number)
                        elif j.Type == 'Yield-Reactor':
                            self.YieldRNumberList['U_YIELD_REACTOR'].append(j.Number)
                            self.CostUnitsList['U_C'].append(j.Number)
                        elif j.Type == 'HeatGenerator':
                            self.HeatGeneratorList['U_FUR'].append(j.Number)
                            self.CostUnitsList['U_C'].append(j.Number)
                            self.StoichRNumberList['U_STOICH_REACTOR'].append(j.Number)
                        elif j.Type == 'ElectricityGenerator':
                            self.ElectricityGeneratorList['U_TUR'].append(j.Number)
                            self.CostUnitsList['U_C'].append(j.Number)
                            self.StoichRNumberList['U_STOICH_REACTOR'].append(j.Number)
                        elif j.Type == 'ProductPool':
                            self.ProductPoolList['U_PP'].append(j.Number)
                        elif j.Type == 'Source':
                            self.SourceList['U_S'].append(j.Number)
                        else:
                            self.SplitterNumberList['U_SPLITTER'].append(j.Number)
                            self.CostUnitsList['U_C'].append(j.Number)

                        for k in j.Possible_Sources:
                            if k != j.Number:
                                self.SourceSet['U_SU'].append((k,j.Number))
            else:
                if i not in self.UnitsList:
                    self.UnitsList.append(i)
                    self.UnitsNumberList['U'].append(i.Number)
                    self.UnitsNumberList2['UU'].append(i.Number)
                    if i.Type == 'Stoich-Reactor':
                        self.StoichRNumberList['U_STOICH_REACTOR'].append(i.Number)
                        self.CostUnitsList['U_C'].append(i.Number)
                    elif i.Type == 'Yield-Reactor':
                        self.YieldRNumberList['U_YIELD_REACTOR'].append(i.Number)
                        self.CostUnitsList['U_C'].append(i.Number)
                    elif i.Type == 'HeatGenerator':
                        self.HeatGeneratorList['U_FUR'].append(i.Number)
                        self.CostUnitsList['U_C'].append(i.Number)
                        self.StoichRNumberList['U_STOICH_REACTOR'].append(i.Number)
                    elif i.Type == 'ElectricityGenerator':
                        self.ElectricityGeneratorList['U_TUR'].append(i.Number)
                        self.CostUnitsList['U_C'].append(i.Number)
                        self.StoichRNumberList['U_STOICH_REACTOR'].append(i.Number)
                    elif i.Type == 'ProductPool':
                        self.ProductPoolList['U_PP'].append(i.Number)
                    elif i.Type == 'Source':
                        self.SourceList['U_S'].append(i.Number)
                    else:
                        self.SplitterNumberList['U_SPLITTER'].append(i.Number)
                        self.CostUnitsList['U_C'].append(i.Number)

                    for k in i.Possible_Sources:
                        if k !=i.Number:
                            self.SourceSet['U_SU'].append((k,i.Number))
          

    def __set_unitNames(self):
        for i in self.UnitsList:
            self.UnitNames['Names'][i.Number] = i.Name
            

    def add_components(self, *args):
        """
        Parameters
        ----------
        *args : Either List of Strings of Single String Arguments
            Takes String Components and sorts them into ComponentsList 

        """
        for i in args:
            if type(i) == list:
                for j in i:
                    if j not in self.ComponentsList['I']:
                        self.ComponentsList['I'].append(j)
            else:
                if i not in self.ComponentsList['I']:
                    self.ComponentsList['I'].append(i)
            
        
                
    def add_reactions(self,*args):
        """
        Parameters
        ----------
        *args : Either List of Strings of Single String Arguments
            Takes String Reactions and sorts them into RaactionsList 
        """
        for i in args:
            if type(i) == list:
                for j in i:
                    if j not in self.ReactionsList['R']:
                        self.ReactionsList['R'].append(j)
            else:
                if i not in self.ReactionsList['R']:
                    self.ReactionsList['R'].append(i)
                    
                    
        
    def add_reactants(self,*args):
        """
        Parameters
        ----------
        *args : Either List of Strings of Single String Arguments
            Takes String Reactants and sorts them into ReactantsList 
        """
        for i in args:
            if type(i) == list:
                for j in i:
                    if j not in self.ReactantsList['M']:
                        self.ReactantsList['M'].append(j)
            else:
                if i not in self.ReactantsList['M']:
                    self.ReactantsList['M'].append(i)
                    
                    
                
    def add_utilities(self,*args):
        """
        Parameters
        ----------
        *args : Either List of Strings of Single String Arguments
            Takes String Utilities and sorts them into UtilitiesList 

        """
        for i in args:
            if type(i) == list:
                for j in i:
                    if j not in self.UtilitiesList['UT']:
                        self.UtilitiesList['UT'].append(j)
                        if j == 'Heat' or j =='Heat2':
                            self.HeatUtilitiesList['H_UT'].append(j)
            else:
                if i not in self.UtilitiesList['UT']:
                    self.UtilitiesList['UT'].append(i)
                    if i == 'Heat' or i =='Heat2':
                        self.HeatUtilitiesList['H_UT'].append(i)
    
    
    
    def set_lhv(self, lhv_dic):
        """
        Parameters
        ----------
        lhv_dic : Dictionary
            Takes Dictionaries of Type {'Component1': LHV_i, 'Component1': LHV_i....}

        """
        for i,j in lhv_dic.items():
            self.lhv['LHV'][i] = j      

    

    def add_linearisationIntervals(self):
        if self.linearizationDetail == "rough":
            n = 10
        elif self.linearizationDetail == "fine":
            n = 301
        else:        
            n = 20
            
        for i in range(1,n):
            self.LinPointsList['J'].append(i)
            self.LinIntervalsList['JI'].append(i)
            
        self.LinPointsList['J'].append(n)
        
        
    def __add_temperatureIntervals(self):     
        """
        Description
        -----------
        
        Takes the Superstructure Python List 
            
            - Heat_Temperatures 
        
        and creates the 
            
            - HeatIntervalsList 
        
        which is a SET Input for the Superstructure Model.
        
        
        
        Context
        -------
        
        Is called in the Superstructure Method
            
            - create_DataFile
        
        after all Temperatures are added to the Grid 
        

        """
        k= len(self.Heat_Temperatures)-1
        for i in self.Heat_Temperatures:
            self.HeatIntervals[k] = i
            if k != 0:
                self.HeatIntervalList['HI'].append(k)
            k -= 1
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------ADD PARAMETERS TO INDEXED DICTIONARYS --------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

            
            
    def __set_deltaQ(self):
        for i,j in self.heat_utilities.items():
            for k,t in self.HeatIntervals.items():
                if t <= i and k<len(self.HeatIntervals)-1:
                    self.delta_q['delta_q'][k+1] = j
        
                    
    def set_deltaEL(self, delta_el_value):
        self.delta_el['delta_el'] = delta_el_value      
        
        
        
    def set_deltaCool(self, delta_cool_value):
        self.delta_cool['delta_cool'] = delta_cool_value
            
            
            
    def set_deltaRM(self, delta_rm_dic):
        for i in delta_rm_dic:
            self.delta_rm['delta_rm'][i] = delta_rm_dic[i]
           
            
           
    def set_utilityEmissionsFactor(self, em_fac_ut_dic):
        for i in em_fac_ut_dic:
            self.em_fac_ut['em_fac_ut'][i]  =em_fac_ut_dic[i]
            
            
            
    def set_componentEmissionsFactor(self, em_fac_comp_dic):
        for i in em_fac_comp_dic:
            self.em_fac_comp['em_fac_comp'][i] = em_fac_comp_dic[i]
            
            
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------CROSS REFERENCES METHODS ---------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------        
            
         
    def __set_processTemperatures(self, *args): 
        
        """
        Description
        -----------
        Takes all Processes assigned to the Superstructur Object and checks 
        their Process Temperatures (T) T_IN and T_OUT values. 
        From these values it calls
        
            - add.HeatTemperatures(T)
        
        in order to set the Temperatures to the Heatintervals, List etc.
        
        
        
        Context
        -------
        Is called from the Superstructure Method 
            
            - create_DataFile()
        
        after Superstructure Construction in order to create Temperature Grid

        """
        
        for i in self.UnitsList:
            if i.Number in self.CostUnitsList['U_C']:
                for j in i.T_IN.values():
                        if j != {}:
                            self.__set_heatTemperatures(j)
                for j in i.T_OUT.values():
                    if j!= {}:
                            self.__set_heatTemperatures(j)
 
    def __set_heatTemperatures(self, *args):   
        """
        Parameters
        ----------
        Takes Single or list arguments of Floats which represents Temperatures
        
        
        
        Description
        -----------
        Takes Temperatures and addes them to the Pythonlist (if not already there)
            
            - Heat_Temperatures
            
        afterwards sorts the List in Numeric Order



        Context
        -------
        Is called from Methods:
                
                - add_ProcessTemperatures()
                - add_heatUtilities()
        
        to fill all Temperatures to a Grid
        
        """

        for i in args:
            if type(i)  == list:
                for j in i:
                    if j not in self.Heat_Temperatures and j is not None:
                        self.Heat_Temperatures.append(j)      
            else:
                if i not in self.Heat_Temperatures and i is not None:
                    self.Heat_Temperatures.append(i)
        self.Heat_Temperatures = sorted(self.Heat_Temperatures)
        
    def set_heatUtilities(self, TemperatureList, CostList):
        """
        Parameters
        ----------
        TemperatureList : Python List Containing Temperatures of Utilities
        CostList        : Python List Containing Costs of Utlities (same Order)
        
        Description
        -----------
        Takes T and C Values of Utlities an adds them to the Dictionary
            
            - heat_utilities 
        
        Also calls:
            
            - __set_heatTemperatures(TemperatureList)
        
        in order to add Temperatures to the T-Grid
        
        
        
        Context
        -------
        Is called as adding Method to add Utilities. Also Provides Cost Dictionary
        which is used later to calculate Costs of Heat Intervals
        
        PUBLIC


        """
        for i in range(len(TemperatureList)):
            self.heat_utilities[TemperatureList[i]] = CostList[i] 
            self.__set_heatTemperatures(TemperatureList[i])
            
    def __calc_heatPump(self):
        """
        

        Description
        -------
        This method is called via preparation of the heat balances.
        If "HP_active" == True, than yearly costs for the heat pump are calculated
        using Lifetime and Interest Rate. 
        Afterwards, TIN and TOUT are compared to the HeatIntervals and and the
        corresponding intervals are marked up for the heat balances inside the model.
        If "HP_active" == False Costs, Yearly Factor and COP are set to dummy values 
        (This is probably unnessacery).
        

        """
        if self.HP_active == True:
            ir = self.IR['IR']
            lt = self.HP_LT
            self.HP_ACC_Factor['HP_ACC_Factor'] = ((ir *(1 + ir)**lt)/((1 + ir)**lt -1)) 
            
            for i,j in self.HeatIntervals.items():
                if j == self.HP_T_IN['Temperature']:
                    self.HP_T_IN['Interval'] = i + 1
                elif j == self.HP_T_OUT['Temperature']:
                    self.HP_T_OUT['Interval'] = i + 1
                      
        else:
            self.HP_ACC_Factor['HP_ACC_Factor'] = 0
            self.HP_Costs['HP_Costs'] = 0     
            self.COP_HP['COP_HP']  = 3            
            
    def __fill_betaParameters(self):
        """
        Parameters
        ----------
        
        Used Attributes are:
            
            - self.UnitsList
            - Process Objects of UnitsList
            - self.HeatIntervals       (holding Data on T-Grid)
            - Process.HeatData        (holding Data on tau, TIN and TOUT)
        
        Sets Attributes:
            
            - Process.beta       (holding Data on partitioned Temperature Flow)
            - Process.tau_h      (holds Data on specific Heating Demand)
            - Process.tau_c      (holds Data on specific Cooling Demand)


        Description
        -----------
        
        Takes specific Energy Demand (H/C) as well as Tempertures for every Process
        and checks:
                1. If 0 < tau < 0  -- > If tau > 0 : tau_h , else tau_c
                2. Cross references TIN and TOUT as well as DeltaT with T-Grid
                    and calculates the Split (Portion) of TGrid(k) - TGrid(k-1) 
                    based on DeltaT
                3. Sets Splits as beta Attributes
                4. If TIN = TOUT and tau != 0  --> Process is isothermal, beta is
                    1 for on specific Heat Interval
                5. Appends beta to Process ParameterList
                
        """
        
        r = len(self.Heat_Temperatures)
        
        for i in self.UnitsList:
            if i.Number in self.CostUnitsList['U_C'] and i.Number not in self.HeatGeneratorList["U_FUR"] and i.Number not in self.ElectricityGeneratorList['U_TUR']:
                for k,j in i.HeatData.items():
                    tau = j['tau']
                    if tau is not None:
                        t_in = j['TIN']
                        t_out = j['TOUT']
                        if tau > 0:
                            DeltaT = t_out - t_in
                            i.tau_h['tau_h'][k,i.Number] = tau
                            i.tau_c['tau_c'][k,i.Number] = 0
                            for t,s in self.HeatIntervals.items():  
                                if t_in > s:
                                    i.beta['beta'][i.Number,k,t] = 0 
                                else:
                                    if t_out == s and t_out == t_in:
                                        i.beta['beta'][i.Number,k,t] = 1
                                    else:
                                        if t != 0:
                                            if t_out >= self.HeatIntervals[t-1]:
                                                i.beta['beta'][i.Number,k,t] = (self.HeatIntervals[t-1]-s) / DeltaT
                                            else:
                                                i.beta['beta'][i.Number,k,t] = 0
                        else:
                            DeltaT = t_in - t_out
                            i.tau_h['tau_h'][k,i.Number] = 0
                            i.tau_c['tau_c'][k,i.Number] = -tau
                            for t,s in self.HeatIntervals.items():
                                if t_out > s:
                                    i.beta['beta'][i.Number,k,t] = 0 
                                else:
                                    if t_out == s and t_out == t_in:
                                        i.beta['beta'][i.Number,k,t+1] = 1
                                    else:
                                        if t != 0:
                                            if t_in >= self.HeatIntervals[t-1]:
                                                i.beta['beta'][i.Number,k,t] = (self.HeatIntervals[t-1]-s) / DeltaT
                                            else:
                                                i.beta['beta'][i.Number,k,t] = 0
                i.ParameterList.append(i.beta)    

    def __calc_capexLinearizationParameters(self):
        """
        Description
        -----------
        Takes all Process Units as well as the Intervals Values and 
        calculates the piece-wise linearization of the CAPEX 
        
        Uses the Side Module
        
            - capex_calculator()


        """
        for i in self.UnitsList:
            if i.Number in self.CostUnitsList['U_C']:
                (i.lin_CAPEX_x, i.lin_CAPEX_y) = capex_calculator(i, self.CECPI, Detail = self.linearizationDetail)

                

    def __calc_accFactorParameter(self):
        """
        Description
        -----------
        Takes all Process Units and calculates the annual capex factor which is 
        used in the Superstructure Model

        """
        for i in self.UnitsList:
             if i.Number in self.CostUnitsList['U_C']:
                i.ACC_Factor['ACC_Factor'][i.Number] = i.calc_ACCFactor(self.IR)



    def __set_turnoverParameter(self):
        
        for i in self.UnitsList:
            if i.Number in self.CostUnitsList['U_C']:
                i.turn_over_acc['to_acc'][i.Number] = i.calc_TurnOver_ACC(self.IR)
                
                

                
    def __set_optionalFLH(self):
        for x in self.UnitsList:
            if x.FLH['flh'][x.Number] is None:
                x.FLH['flh'][x.Number] = self.H['H']        
        

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------CREATE DATA-FILE METHODS ---------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------ 
      
        
     
    # Fill Parameter List of Superstructure

    def __fill_nonIndexedParameterList(self):
        """
        Fills List with non-indexed Model-important parameters

        """
        self.NI_ParameterList.append(self.UnitsNumberList)
        self.NI_ParameterList.append(self.UnitsNumberList2)
        self.NI_ParameterList.append(self.StoichRNumberList)
        self.NI_ParameterList.append(self.YieldRNumberList)
        self.NI_ParameterList.append(self.SplitterNumberList)
        self.NI_ParameterList.append(self.HeatGeneratorList)
        self.NI_ParameterList.append(self.ElectricityGeneratorList)
        self.NI_ParameterList.append(self.ProductPoolList)
        self.NI_ParameterList.append(self.CostUnitsList)
        
        self.NI_ParameterList.append(self.SourceList)
        self.NI_ParameterList.append(self.SourceSet)
        
        self.NI_ParameterList.append(self.ComponentsList)
        self.NI_ParameterList.append(self.ReactantsList)
        self.NI_ParameterList.append(self.ReactionsList)
        self.NI_ParameterList.append(self.UtilitiesList)
        self.NI_ParameterList.append(self.HeatUtilitiesList)        
        self.NI_ParameterList.append(self.HeatIntervalList)
        self.NI_ParameterList.append(self.LinPointsList)
        self.NI_ParameterList.append(self.LinIntervalsList)
        self.NI_ParameterList.append(self.H)
        self.NI_ParameterList.append(self.K_O)
        self.NI_ParameterList.append(self.IR)
        self.NI_ParameterList.append(self.CECPI)
        self.NI_ParameterList.append(self.delta_el)
        self.NI_ParameterList.append(self.delta_cool)  
        self.NI_ParameterList.append(self.COP_HP)
        self.NI_ParameterList.append(self.HP_ACC_Factor)
        self.NI_ParameterList.append(self.HP_Costs)
        self.NI_ParameterList.append(self.capacity_flow)
        self.NI_ParameterList.append(self.hourly_wage)
        self.NI_ParameterList.append(self.working_hours)
        self.NI_ParameterList.append(self.process_steps)

        
    def __fill_indexedParameterList(self):
        """
        
        Fills List with indexed Model-important parameters

        """
        
        self.I_ParameterList.append(self.delta_q)
        self.I_ParameterList.append(self.delta_rm)
        self.I_ParameterList.append(self.em_fac_ut)
        self.I_ParameterList.append(self.em_fac_comp)
        self.I_ParameterList.append(self.lhv)
        self.I_ParameterList.append(self.UnitNames)

        
    

    # Add the Parameters from the Lists to the Model-Ready Data File
    # ---------------
    
        
    def __fill_nonIndexedParameters(self):
        """
        Description
        -----------
        First calls Function to Fill non-indexed Parameter List
        Afterwards returns Parameters into die Data_File that is to be used 
        for initialization of the AbstractModel

        """
        self.__fill_nonIndexedParameterList() 
        for i in self.NI_ParameterList:
            for j in i:
                self.Data_File[None][j] = {None: i[j]}
                
                
                
    # Indexed Parameters / Dictionaries 
                
    def __fill_indexedParameters(self):
        """
        Description
        -----------
        
        First calls __fill_indexedParameterList to fill indexed parameters from Superstructure
        Parameters, then fills Data_File with these Parameters.

        """
        
        self.__set_unitNames()
        
        self.__fill_indexedParameterList()
        x = self.I_ParameterList
        for i in x:
            for j,k in i.items():
                try: 
                    self.Data_File[None][j].update(k)
                except:
                    self.Data_File[None][j] = k
         
                        
        

    # Parameters origin from Process Units
 
    def __fill_processParameterList(self):
        """
        Description
        -----------
        
        Goes through all Processes and add the Parameters in their ParameterList
        to the Model-Ready DataFile

        """
        
        for z in self.UnitsList:
            z.fill_ParameterList()
            x = z.ParameterList
            for i in x:
                for j,k in i.items():
                    try: 
                        self.Data_File[None][j].update(k)
                    except:
                        self.Data_File[None][j] = copy.copy(k)        
   


    def __calc_capacityFlow(self):
        cap = self.ProductLoad / self.H['H'] * 1000
        cap =cap**0.242
        self.capacity_flow['capacity_flow'] = cap
        


        

    def __prepare_capexEquations(self):
        """
        Description
        ----------
        
        First adds Linearization Intervals, based on input (fine,average, rough).
        Afterwards, Caluculates piece-wise linear CAPEX for every Process Unit.
        At last calculates annual Cost Factor which is needed in the Model
            


        """
        
        self.add_linearisationIntervals()
        
        self.__calc_capexLinearizationParameters() 
      
        self.__calc_accFactorParameter()
        
        self.__set_optionalFLH()
        
        self.__set_turnoverParameter()
        
        self.__calc_capacityFlow()

        

    
    def __prepare_heatEquations(self):
        """
        Description
        -----------
        Fills Temperature Grid and calculates Heat Utility costs of different
        Heat intervals by calling:
            
            - add_ProcessTemperatures()
            - __add_temperatureIntervals()
            - __set_deltaQ()
            


        """
        
        self.__set_processTemperatures()
        
        self.__add_temperatureIntervals()
        
        self.__calc_heatPump()
        
        self.__set_deltaQ()
            
        self.__fill_betaParameters()
    

    # UNDER CONSTRUCTION --> Later input via predefined databases
         
    def load_data_from_txt(self,txt_name=None):
        try:
            f = open(txt_name,'r')
            data=f.read()
            f.close()
            self.Data_File = eval(data)
        except:
            pass
        
    def add_DataBase(self, txt_file):
        self.Database = txt_file

    # ------


    # Create Data File
    # -----------------
            

    def create_DataFile(self):
        """
        Description
        -----------
        First prepares Data for Heatbalances (T-Grid, Costs...)
            
            - preprace_HeatBalances()
        
            
        Afterwards prepares Data for Cost equation (Lin Intervals, Piece-wise
        linear costs...) by callingcalling:
            
            - __prepare_capexEquations()
            
        At last creates the Data File for the Superstructure Model by calling:
            
            - __fill_nonIndexedParameters()
            - __fill_indexedParameters()
            - __fill_processParameterList()
            # 
        

        Returns
        -------
        Data_File:   File with Superstructure Model ready Data

        """

        self.load_data_from_txt(self.Database)
        
        try:
            self.__prepare_heatEquations()
        except:
            print('No heat balance prepared')
        finally:
            try:
                self.__prepare_capexEquations()
            except:
                print('no Capex prepared')
            finally:
                try:
                    self.__fill_nonIndexedParameters()
                    self.__fill_indexedParameters()
                    self.__fill_processParameterList()
                except:
                    print('Something wrong in parameter init')
                finally:
                    return self.Data_File
        
    
        