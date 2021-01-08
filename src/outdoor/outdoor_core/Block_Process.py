import math 





#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------GENERAL PROCESS CLASS-------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


class Process():


    
    def __init__(self, Name, UnitNumber, Parent= None, *args, **kwargs):

        super().__init__()
        
        # Lists
        self.ParameterList =[]



        # GENERAL ATTRIBUTES
        # ------------------

        # Non-indexed Attributes
        self.Name = Name
        self.Number = UnitNumber
        self.Type = None
        self.Group = None
        
        self.Possible_Sources = []
        

        


        # FLOW ATTRIBUTES
        # ---------------

        # Indexed Attributes 
        self.myu ={'myu': {}}
        self.conc  ={'conc': {self.Number: 0}}
        self.ul1 = {'ul_1': {self.Number: 10000 }}
        self.ul2 = {'ul_2': {self.Number: 10000 }}
        
        self.add_flow = dict()
        self.kappa_1_lhs_conc = {'kappa_1_lhs_conc': {}}
        self.kappa_2_lhs_conc = {'kappa_2_lhs_conc': {}}
        self.kappa_1_rhs_conc = {'kappa_1_rhs_conc': {}}
        self.kappa_2_rhs_conc = {'kappa_2_rhs_conc': {}}

        self.FLH = {'flh': {self.Number: None}}
        
        if Parent is not None:
            Parent.add_Units(self)



    # GENERAL DATA SETTING
    # --------------------

    def set_data_general(self,
                         ProcessGroup,
                         lifetime  = None,
                         emissions = 0,
                         full_load_hours = None
                         ):
       
        self.set_Group(ProcessGroup)
        self.set_full_load_hours(full_load_hours)

    def set_Name(self, Name):
        self.Name = Name
        
    def set_Number(self, Number):
        self.Number = Number
        
    def set_Group(self, processgroup):
        self.Group = processgroup

    def set_full_load_hours(self, full_load_hours = None):
        self.FLH['flh'][self.Number] = full_load_hours






    
    # FLOW DATA SETTING
    # -----------------

    def set_data_flow(self,
                      RequiredConcentration = None,
                      AdditionalFlowComposition1 = {},
                      AdditionalFlowComposition2 = {},
                      RightHandSideReferenceFlow = None,
                      LeftHandSideReferenceFlow = None,
                      RightHandSideComponentList = [],
                      LeftHandSideComponentList = [],
                      SplitfactorDictionary = None,
                      UpperLimitAdditionalFlow1 = None,
                      UpperLimitAdditionalFlow2 = None
                      ):


        dic1 = {'phi1': AdditionalFlowComposition1, 
                'phi2': AdditionalFlowComposition2}
        

        self.set_conc(RequiredConcentration)
        self.add_myuFactors(SplitfactorDictionary)
        self.add_addflowFactors(dic1)
        
        self.set_upperlimits(UpperLimitAdditionalFlow1,
                             UpperLimitAdditionalFlow2)

        self.add_kappa_1_lhs_conc(LeftHandSideComponentList)
        self.add_kappa_1_rhs_conc(RightHandSideComponentList)
        self.add_kappa_2_lhs_conc(LeftHandSideReferenceFlow)
        self.add_kappa_2_rhs_conc(RightHandSideReferenceFlow)

    def set_conc(self, concentration):
        self.conc['conc'][self.Number] = concentration
        

        
    def set_upperlimits(self, 
                        upper_limit_1=None, 
                        upper_limit_2=None):
        
        self.ul1['ul_1'][self.Number] = upper_limit_1
        self.ul2['ul_2'][self.Number] = upper_limit_2
  
        
  
    def add_myuFactors(self, myu_dic):
        """

        Parameters
        ----------
        myu_dic : Dictionary
            Example: dict = {(u'1,i1):value1, (u'1,i2): value2}

        """
        for i in myu_dic:
            self.myu['myu'][self.Number,i] = myu_dic[i]



    def add_addflowFactors(self, addflow_dic):
        """

        Parameters
        ----------
        addflow_dic : Dictionary
            Example: dict = {'phi1' :{i1 : value1, i2: value2},
            'phi2' : {i1 : value3 , i3: value4}}

        """
        for i in addflow_dic:
            for j in addflow_dic[i]:
                try: 
                    self.add_flow[i].update({(self.Number,j) : addflow_dic[i][j]})
                except:
                    self.add_flow[i] = {(self.Number,j) : addflow_dic[i][j]}
  
                
  
    def add_kappa_1_lhs_conc(self, kappa_1_lhs_conc_list):
        """
        Parameters
        ----------
        kappa_1_lhs_conc_dic : Dictionary
            Example: dict = ['I1','I2',...]

        """
        for i in kappa_1_lhs_conc_list:
            if type(i) == list:
                for j in i:
                    self.kappa_1_lhs_conc['kappa_1_lhs_conc'][self.Number,j] = 1
            else:
                self.kappa_1_lhs_conc['kappa_1_lhs_conc'][self.Number,i] = 1



    def add_kappa_1_rhs_conc(self, kappa_1_rhs_conc_list):
        """
        Parameters
        ----------
        kappa_1_rhs_conc_dic : Dictionary
            Example: dict = ['I1','I2',...]

        """
        for i in kappa_1_rhs_conc_list:
            if type(i) == list:
                for j in i:
                    self.kappa_1_rhs_conc['kappa_1_rhs_conc'][self.Number,j] = 1
            else:
                self.kappa_1_rhs_conc['kappa_1_rhs_conc'][self.Number,i] = 1



    def add_kappa_2_lhs_conc(self, kappa_2_lhs_conc_string):
        """
        Parameters
        ----------
        kappa_2_lhs_conc_dic : String
            Example: 'FIN' or 'FOUT'

        """
        
        if kappa_2_lhs_conc_string  == 'FIN':
            self.kappa_2_lhs_conc['kappa_2_lhs_conc'][self.Number]  = 1
        elif kappa_2_lhs_conc_string  == 'FOUT':
            self.kappa_2_lhs_conc['kappa_2_lhs_conc'][self.Number]  = 0
        else:
            self.kappa_2_lhs_conc['kappa_2_lhs_conc'][self.Number]  = 3



    def add_kappa_2_rhs_conc(self, kappa_2_rhs_conc_string):
        """
        Parameters
        ----------
        kappa_2_rhs_conc_dic : String
            Example: 'FIN' or 'FOUT'

        """
        if kappa_2_rhs_conc_string  == 'FIN':
            self.kappa_2_rhs_conc['kappa_2_rhs_conc'][self.Number]  = 1
        elif kappa_2_rhs_conc_string  == 'FOUT':
            self.kappa_2_rhs_conc['kappa_2_rhs_conc'][self.Number]  = 0
        else:
            self.kappa_2_rhs_conc['kappa_2_rhs_conc'][self.Number]  = 3


    def add_PossibleSources(self, SourceList):
        
        if type(SourceList) == list:
            for i in SourceList:
                if i not in self.Possible_Sources:
                    self.Possible_Sources.append(i)
        else:
            if SourceList not in self.Possible_Sources:
                self.Possible_Sources.append(SourceList)
                





    # ADDITIONAL METHODS 
    # ------------------





    def fill_ParameterList(self):
        """
        Fills ParameterList of Process Unit u which is used to fill Data_File
        In Superstructure Class

        """

        
        self.ParameterList.append(self.conc)
        self.ParameterList.append(self.myu)        
        self.ParameterList.append(self.add_flow)       
        self.ParameterList.append(self.kappa_1_lhs_conc)
        self.ParameterList.append(self.kappa_2_lhs_conc)
        self.ParameterList.append(self.kappa_1_rhs_conc)
        self.ParameterList.append(self.kappa_2_rhs_conc)
        self.ParameterList.append(self.FLH)
        self.ParameterList.append(self.ul1)
        self.ParameterList.append(self.ul2)
        
    



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------VIRTUAL PROCESSES-----------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class VirtualProcess(Process):
    
    def __init__(self, Name, UnitNumber, Parent=None, *args, **kwargs):
        
        super().__init__(Name, UnitNumber, Parent)
        
        
        
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------PHYSICAL / REAL PROCESSES---------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

class PhysicalProcess(Process):

    def __init__(self, Name, UnitNumber, Parent = None, *args, **kwargs):
        
        super().__init__(Name, UnitNumber, Parent)

        # Indexed Attributes
        self.LT  = {'LT': {self.Number: None}}
        self.em_fac_unit = {'em_fac_unit': {self.Number: None}}

         # ECONOMIC ATTRIBUTES
        # --------------------

        # Indexed Attributes
        self.DC_factor = {'DC': {self.Number: None}}
        self.IDC_factor = {'IDC': {self.Number: None}}
        self.CAPEX_factors = dict()
        
        self.CAPEX_factors_new = {'C_Ref': None, 'm_Ref': None,
                                  'CECPI_ref': None}
        
        self.ACC_Factor  = {'ACC_Factor': {self.Number: None}}
        self.lin_CAPEX_x = dict()
        self.lin_CAPEX_y = dict()
        self.kappa_1_capex = {'kappa_1_capex': {}}
        self.kappa_2_capex = {'kappa_2_capex': {}}

        self.K_M = {'K_M': {}}
        
        self.turn_over_acc = {'to_acc': {self.Number: 0}}
        self.turnover_factors = {'CostPercentage': None, 'TimeSpan': None, 'TimeMode': 'No Mode'}
        


        

        # ENERGY ATTRIBUTES
        # -----------------
        
        # Indexed Attributes
        self.tau = {'tau': {}}
        
        self.tau_h = {'tau_h':{}}
        self.tau_c = {'tau_c': {}}
        
        self.kappa_1_ut = {'kappa_1_ut': {}}
        self.kappa_2_ut = {'kappa_2_ut': {}}
        self.beta = {'beta': {}}
        
        
        self.HeatData = {'Heat': {}, 'Heat2': {}}
        self.T_IN = {'Heat': {}, 'Heat2':{}}
        self.T_OUT = {'Heat': {}, 'Heat2':{}}
        

        self.CECPI_dic = {1994: 368.1, 1995: 381.1, 1996: 381.7, 1997: 386.5,
                          1998: 389.5, 1999: 390.6, 2000: 394.1, 2001: 394.3,
                          2002: 395.6, 2003: 402.0, 2004: 444.2, 2005: 468.2,
                          2006: 499.6, 2007: 525.4, 2008: 575.4, 2009: 521.9,
                          2010: 550.8, 2011: 585.7, 2012: 584.6, 2013: 567.1,
                          2014: 576.1, 2015: 556.8, 2016: 541.7, 2017: 566.1,
                          2018: 603.1}


    # ECONOMIC DATA SETTING
    # ---------------------
    
    def set_data_general(self,
                         ProcessGroup,
                         lifetime,
                         emissions = 0,
                         full_load_hours = None,
                         maintenancefactor = 0.044875,
                         CostPercentage = None,
                         TimeSpan = None,
                         TimeMode = None
                         ):
        
        super().set_data_general(ProcessGroup,lifetime,emissions,full_load_hours)
        self.set_lifeTime(lifetime)
        self.set_em_fac_unit(emissions)
        self.set_Maintenance_factor(maintenancefactor)
        
        self.set_turnover_factors(CostPercentage, 
                                  TimeSpan,
                                  TimeMode)



    def set_em_fac_unit(self, emissionfactor):
        self.em_fac_unit['em_fac_unit'][self.Number] = emissionfactor
    
    def set_lifeTime(self, lifetime):
        self.LT['LT'][self.Number] = lifetime
        
    def set_Maintenance_factor(self, factor=0.044875):
        self.K_M['K_M'][self.Number] = factor

    def set_data_economic(self,
                          DirectCostFactor,
                          IndirectCostFactor,
                          ReferenceCosts,
                          ReferenceFlow,
                          CostExponent,
                          ReferenceYear,
                          ReferenceFlowType,
                          ReferenceFlowComponentList
                          ):
        
        
        self.set_DCFactor(DirectCostFactor)
        self.set_IDCFactor(IndirectCostFactor)
        
        self.add_capexFactors(ReferenceCosts,
                              ReferenceFlow,
                              CostExponent,
                              ReferenceYear)
        
        self.add_kappa_2_capex(ReferenceFlowType)
        self.add_kappa_1_capex(ReferenceFlowComponentList)
    


    def set_DCFactor(self, DC):
        self.DC_factor['DC'][self.Number] = DC



    def set_IDCFactor(self, IDC):
        self.IDC_factor['IDC'][self.Number] = IDC



    def add_capexFactors(self, CREF, MREF, F, YEAR_REF):
        
        self.CAPEX_factors['C_Ref'] = {self.Number: CREF}
        self.CAPEX_factors['m_Ref'] = {self.Number: MREF}
        self.CAPEX_factors['f'] = {self.Number: F}
        self.CAPEX_factors['CECPI_ref'] = {self.Number: self.CECPI_dic[YEAR_REF]}
        
        
    def set_turnover_factors(self, CostPercentage, TimeSpan = None, TimeMode = 'No Mode'):
        
        self.turnover_factors['CostPercentage'] = CostPercentage
        
        
        if TimeMode == 'Yearly':
            self.turnover_factors['TimeSpan'] = TimeSpan
            self.turnover_factors['TimeMode'] = 'Yearly'
        elif TimeMode == 'Hourly':
            self.turnover_factors['TimeSpan'] = TimeSpan
            self.turnover_factors['TimeMode'] = 'Hourly'
        else:
            self.turnover_factors['TimeSpan'] = None
            self.turnover_factors['TimeMode'] = 'No Mode'
         

        
    def add_kappa_1_capex(self, kappa_1_list):
        """
        Parameters
        ----------
        kappa_1_list : List
            Example: dict = ['I1','I2']

        """
        for i in kappa_1_list:
            if type(i) == list:
                for j in i:
                    self.kappa_1_capex['kappa_1_capex'][self.Number,j] = 1
            else:
                self.kappa_1_capex['kappa_1_capex'][self.Number,i] = 1



    def add_kappa_2_capex(self, kappa_2_capex_string):  
        """
        Parameters
        ----------
        kappa_2_lhs_conc_dic : String
            Example: 'FIN' or 'FOUT'

        """
        if kappa_2_capex_string  == 'FIN':
            self.kappa_2_capex['kappa_2_capex'][self.Number]  = 1
        elif kappa_2_capex_string  == 'FOUT':
            self.kappa_2_capex['kappa_2_capex'][self.Number]  = 0
        elif kappa_2_capex_string  == 'PEL':
            self.kappa_2_capex['kappa_2_capex'][self.Number]  = 2
        elif kappa_2_capex_string  == 'PHEAT':
            self.kappa_2_capex['kappa_2_capex'][self.Number]  = 3
        elif kappa_2_capex_string == 'PEL_PROD':
            self.kappa_2_capex['kappa_2_capex'][self.Number]  = 4
        else:
            self.kappa_2_capex['kappa_2_capex'][self.Number]  = 5
 
    def calc_ACCFactor(self, IR):
         IR = IR['IR']
         lt = self.LT['LT'][self.Number]
         fac= ((IR *(1 + IR)**lt)/((1 + IR)**lt -1))

         return fac
     
        
    def calc_TurnOver_ACC(self, IR):
        h = self.FLH['flh'][self.Number]
        lt = self.LT['LT'][self.Number]
        

        
        to_lt = self.turnover_factors['TimeSpan']
        to_tm = self.turnover_factors['TimeMode']
        to_c = self.turnover_factors['CostPercentage']
        
        
        if to_tm == 'No Mode':
            return 0
        
        elif to_tm == 'Yearly':
            number_of_turnovers = lt / to_lt
            number_of_turnovers = math.ceil(number_of_turnovers)
            number_of_turnovers = number_of_turnovers - 1 
        else: 
            h_tot = h * lt
            number_of_turnovers = h_tot / to_lt
            number_of_turnovers = math.ceil(number_of_turnovers)
            number_of_turnovers = number_of_turnovers - 1 
            
        total_turnover_costs = number_of_turnovers * to_c
        annual_factor = self.calc_ACCFactor(IR)
        annual_turnover_costs = annual_factor * total_turnover_costs
        
        return annual_turnover_costs


            
    # ENERGY DATA SETTING
    # -------------------

    def set_data_energy(self,
                        Temperature1 = None,
                        Temperature2 = None,
                        ElectricityDemand = None,
                        HeatDemand = None,
                        Heat2Demand = None,
                        ElectricityReferenceFlow = None,
                        ElectricityReferenceComponentList = [],
                        HeatReferenceFlow = None,
                        HeatReferenceComponentList = [],
                        Heat2ReferenceFlow = None,
                        Heat2ReferenceComponentList = []
                        ):

        
        dic1 = {'Electricity': ElectricityDemand, 'Heat':  HeatDemand,
                'Heat2': Heat2Demand}

        dic2= {'Electricity': ElectricityReferenceComponentList,
               'Heat': HeatReferenceComponentList,
               'Heat2': Heat2ReferenceComponentList}

        dic3 = {'Electricity': ElectricityReferenceFlow,
                'Heat': HeatReferenceFlow,
                'Heat2': Heat2ReferenceFlow}
        
        self.add_tauFactors(dic1)
        self.add_kappa_1_ut(dic2)
        self.add_kappa_2_ut(dic3)
        
        

    def add_tauFactors(self, tau_dic):
        """

        Parameters
        ----------
        tau_dic : Dictionary
            Example: dict= {'Utility1' : value1 , 'Utility2' : value2}

        """

        for i in tau_dic:
            self.tau['tau'][self.Number,i] = tau_dic[i]



    def add_kappa_1_ut(self, kappa_1_ut_dic):
        """
        Parameters
        ----------
        kappa_1_ut_dic : Dictionary
            Example: dict = {'Utility1': ['I1','I2'], 'Utitility2': [...]}

        """
        for i in kappa_1_ut_dic:
            for j in kappa_1_ut_dic[i]:
                self.kappa_1_ut['kappa_1_ut'][self.Number,i,j] = 1



    def add_kappa_2_ut(self, kappa_2_ut_dic):
        """
        Parameters
        ----------
        kappa_2_ut_dic : Dictionary
            Example: dict = {'Utility1': 'FIN', 'Utiltity2': 'FOUT'}

        """
        for i in kappa_2_ut_dic:
            if kappa_2_ut_dic[i]  == 'FIN':
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 1
            elif kappa_2_ut_dic[i]  == 'FOUT':
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 0
            else:
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 3



    def set_Temperatures(self,
                         T_IN_1 = None,
                         T_OUT_1 = None,
                         tau1 = None,
                         T_IN_2 = None,
                         T_OUT_2 = None,
                         tau2  = None):

        self.HeatData['Heat']['TIN'] = T_IN_1
        self.HeatData['Heat']['TOUT'] = T_OUT_1
        self.HeatData['Heat2']['TIN'] = T_IN_2
        self.HeatData['Heat2']['TOUT'] = T_OUT_2 
        self.HeatData['Heat']['tau'] = tau1
        self.HeatData['Heat2']['tau'] = tau2
        self.T_IN['Heat'] = T_IN_1
        self.T_IN['Heat2'] = T_IN_2
        self.T_OUT['Heat'] = T_OUT_1
        self.T_OUT['Heat2'] = T_OUT_2
        
        


    

    def fill_ParameterList(self):
        
        super().fill_ParameterList()
        self.ParameterList.append(self.LT)
        self.ParameterList.append(self.DC_factor)
        self.ParameterList.append(self.IDC_factor)
        self.ParameterList.append(self.tau)
        self.ParameterList.append(self.kappa_1_ut)
        self.ParameterList.append(self.kappa_2_ut)
        self.ParameterList.append(self.lin_CAPEX_x)
        self.ParameterList.append(self.lin_CAPEX_y)
        self.ParameterList.append(self.tau_h)
        self.ParameterList.append(self.tau_c)
        self.ParameterList.append(self.kappa_1_capex)
        self.ParameterList.append(self.kappa_2_capex)
        self.ParameterList.append(self.ACC_Factor)
        self.ParameterList.append(self.em_fac_unit)
        self.ParameterList.append(self.K_M)
        self.ParameterList.append(self.turn_over_acc)




#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------STOICHIOMETRIC REACTOR------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


class StoichReactor(PhysicalProcess):

    def __init__(self, Name, UnitNumber, Parent =None, *args, **kwargs):

        super().__init__(Name, UnitNumber, Parent)

        # Non-Indexed Attributes
        self.Type = "Stoich-Reactor"

        # Indexed Attrubutes
        self.gamma = {'gamma': {}}
        self.theta = {'theta': {}}


    # REACTION SETTING METHODS
    # ------------------------


    def add_gammaFactors(self, gamma_dic):
       
        """

        Parameters
        ----------
        gamma_dic : Dictionary
            Example: dict= {(i1, r1) : value1, (i2, r1): value2,
                            (i3, r1): value3}

        """
        for i in gamma_dic:
            self.gamma['gamma'][self.Number, i]  = gamma_dic[i]



    def add_thetaFactors(self, theta_dic):
        """

        Parameters
        ----------
        theta_dic: Dictionary
            Example:  dict= {(r1,m1): value1}
        """
        for i in theta_dic:
            self.theta['theta'][self.Number, i] = theta_dic[i]


    def set_data_reaction(self,
                          StoichiometricFactors,
                          ConversionFactors
                          ):
        
        if self.Type == "Stoich-Reactor":
            print(self.Name)
            self.add_gammaFactors(StoichiometricFactors)
            self.add_thetaFactors(ConversionFactors)
 

    def fill_ParameterList(self):
        super().fill_ParameterList()
        # if self.Type == "Stoich-Reactor":
        self.ParameterList.append(self.gamma)
        self.ParameterList.append(self.theta)


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------YIELD REACTOR---------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

         
class YieldReactor(PhysicalProcess):

    def __init__(self, Name, UnitNumber, Parent= None, *args, **kwargs):

        super().__init__(Name, UnitNumber, Parent)

        

        # Non-indexed Attributes
        self.Type = "Yield-Reactor"

        # Indexed Attributes
        self.xi = {'xi': {}}


    # REACTION SETTING METHODS
    # ------------------------


    def add_xiFactors(self, xi_dic):
        """

        Parameters
        ----------
        xi_dic : Dictionary
            Example: dict = {i1: value1, i2: value2, i3: value3}

        """
        for i in xi_dic:
            self.xi['xi'][self.Number,i] = xi_dic[i]
    def fill_ParameterList(self):
        super().fill_ParameterList()
        self.ParameterList.append(self.xi)





#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------HEAT AND STEAM GENERATOR----------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------



class HeatGenerator(StoichReactor):


    def __init__(self, Name, UnitNumber, Efficiency = None, Parent = None,
                 *args, **kwargs):

        super().__init__(Name, UnitNumber, Parent)

        # Non-Indexed Parameters
        self.Type = "HeatGenerator"
        self.Efficiency_FUR = {'Efficiency_FUR': {self.Number: Efficiency}}



    def set_Efficiency(self, Efficiency):
        """
        Parameters
        ----------
        Efficiency : Float
            Sets efficiency of the furnace process between 0 and 1
        """
        self.Efficiency_FUR['Efficiency_FUR'][self.Number]  = Efficiency
        
    def fill_ParameterList(self):
        super().fill_ParameterList()
        self.ParameterList.append(self.Efficiency_FUR)



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------ELECTRICTIY GENERATOR / TURBINE---------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------




class ElectricityGenerator(StoichReactor):


    def __init__(self, Name, UnitNumber, Efficiency = None,  Parent = None,
                 *args, **kwargs):

        super().__init__(Name, UnitNumber, Parent)

        # Non-Indexed Parameters
        self.Type = "ElectricityGenerator"
        self.Efficiency_TUR = {'Efficiency_TUR': {self.Number: Efficiency}}



    def set_Efficiency(self, Efficiency):
        """
        Parameters
        ----------
        Efficiency : Float
            Sets efficiency of the Combined gas and stea turbine
            process between 0 and 1
        """
        self.Efficiency_TUR['Efficiency_TUR'][self.Number]  = Efficiency


    def fill_ParameterList(self):
        super().fill_ParameterList()
        self.ParameterList.append(self.Efficiency_TUR)
        
        
        
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------PRODUCT POOL ---------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------



class ProductPool(VirtualProcess):


    def __init__(self, Name, 
                 UnitNumber, 
                 ProductType= "ByProduct", 
                 ProductPrice = None, 
                 ProductName= None, 
                 Parent = None, 
                 *args, 
                 **kwargs):

        super().__init__(Name, UnitNumber, Parent)

        # Non-Indexed Parameters
        self.Type = "ProductPool"
        self.ProductName = ProductName
        self.ProductPrice = {'ProductPrice': {self.Number: ProductPrice}}
        self.em_credits = {'em_fac_prod': {self.Number: 0}}
        
        
        if ProductType == 'MainProduct':
            self.ProductType = ProductType
        elif ProductType == 'WasteWaterTreatment':
            self.ProductType = ProductType
        else:
            self.ProductType = 'ByProduct'
        
            
            
    def set_EmissionCredits(self, emissionfactor):
        self.em_credits['em_fac_prod'][self.Number] = emissionfactor
        
            
    def set_ProductPrice(self, Price):
        self.ProductPrice['ProductPrice'][self.Number] = Price


    def fill_ParameterList(self):
        super().fill_ParameterList()
        self.ParameterList.append(self.ProductPrice)
        self.ParameterList.append(self.em_credits)


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#--------------------------RAW MATERIAL SOURCE --------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


class Source(VirtualProcess):
    
    def __init__(self, Name, 
                 UnitNumber,
                 Parent = None,
                 *args, 
                 **kwargs):

        super().__init__(Name, UnitNumber, Parent)
        
        self.Type = 'Source'
        self.Composition = {'phi': {}}
        self.MaterialCosts  = {'materialcosts': {self.Number: 0}}
        self.UpperLimit = {'ul': {self.Number: None}}
    
    
    
    def set_data_source(self, 
                        Costs,
                        UpperLimit,
                        Composition_dictionary):

        self.set_MaterialCosts(Costs)
        self.set_upperlimit(UpperLimit)
        self.set_composition(Composition_dictionary)

    def set_MaterialCosts(self, Costs):
        self.MaterialCosts['materialcosts'][self.Number] = Costs
        
        
    def set_composition(self, composition_dic):
        for i in composition_dic:       
            self.Composition['phi'][(self.Number,i)] = composition_dic[i]
        
    def set_upperlimit(self, UpperLimit):
        self.UpperLimit['ul'][self.Number] = UpperLimit
        
    
    def fill_ParameterList(self):
        super().fill_ParameterList()
        self.ParameterList.append(self.Composition)
        self.ParameterList.append(self.MaterialCosts)
        self.ParameterList.append(self.UpperLimit)
        
        
        