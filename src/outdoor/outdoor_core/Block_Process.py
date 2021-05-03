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
        
        
        self.kappa_1_lhs_conc = {'kappa_1_lhs_conc': {}}
        self.kappa_2_lhs_conc = {'kappa_2_lhs_conc': {}}
        self.kappa_1_rhs_conc = {'kappa_1_rhs_conc': {}}
        self.kappa_2_rhs_conc = {'kappa_2_rhs_conc': {}}

        self.FLH = {'flh': {self.Number: None}}
        
        if Parent is not None:
            Parent.add_UnitOperations(self)



        

    
    def fill_unitOperationsList(self, superstructure):
        superstructure.UnitsList.append(self)
        superstructure.UnitsNumberList['U'].append(self.Number)
        superstructure.UnitsNumberList2['UU'].append(self.Number)
        
        for i in self.Possible_Sources:
            if i is not self.Number:
                superstructure.SourceSet['U_SU'].append((i,self.Number))
        
        


    # GENERAL DATA SETTING
    # --------------------

    def set_generalData(self,
                         ProcessGroup,
                         lifetime  = None,
                         emissions = 0,
                         full_load_hours = None
                         ):
       
        self.set_group(ProcessGroup)
        self.set_full_load_hours(full_load_hours)

    def set_name(self, Name):
        self.Name = Name
        
    def set_number(self, Number):
        self.Number = Number
        
    def set_group(self, processgroup):
        self.Group = processgroup

    def set_full_load_hours(self, full_load_hours = None):
        self.FLH['flh'][self.Number] = full_load_hours






    
    # FLOW DATA SETTING
    # -----------------

    def set_flowData(self,
                      RequiredConcentration = None,
                      RightHandSideReferenceFlow = None,
                      LeftHandSideReferenceFlow = None,
                      RightHandSideComponentList = [],
                      LeftHandSideComponentList = [],
                      SplitfactorDictionary = None,
                      ):
        

        self.__set_conc(RequiredConcentration)
        self.__set_myuFactors(SplitfactorDictionary)


        self.__set_kappa_1_lhs_conc(LeftHandSideComponentList)
        self.__set_kappa_1_rhs_conc(RightHandSideComponentList)
        self.__set_kappa_2_lhs_conc(LeftHandSideReferenceFlow)
        self.__set_kappa_2_rhs_conc(RightHandSideReferenceFlow)
        

    def __set_conc(self, concentration):
        self.conc['conc'][self.Number] = concentration
        
  
    def __set_myuFactors(self, myu_dic):
        """

        Parameters
        ----------
        myu_dic : Dictionary
            Example: dict = {(u'1,i1):value1, (u'1,i2): value2}

        """
        for i in myu_dic:
            self.myu['myu'][self.Number,i] = myu_dic[i]
                
  
    def __set_kappa_1_lhs_conc(self, kappa_1_lhs_conc_list):
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



    def __set_kappa_1_rhs_conc(self, kappa_1_rhs_conc_list):
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



    def __set_kappa_2_lhs_conc(self, kappa_2_lhs_conc_string):
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



    def __set_kappa_2_rhs_conc(self, kappa_2_rhs_conc_string):
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


    def set_possibleSources(self, SourceList):
        
        if type(SourceList) == list:
            for i in SourceList:
                if i not in self.Possible_Sources:
                    self.Possible_Sources.append(i)
        else:
            if SourceList not in self.Possible_Sources:
                self.Possible_Sources.append(SourceList)
                





    # ADDITIONAL METHODS 
    # ------------------





    def fill_parameterList(self):
        """
        Fills ParameterList of Process Unit u which is used to fill Data_File
        In Superstructure Class

        """

    
        self.ParameterList.append(self.conc)
        self.ParameterList.append(self.myu)            
        self.ParameterList.append(self.kappa_1_lhs_conc)
        self.ParameterList.append(self.kappa_2_lhs_conc)
        self.ParameterList.append(self.kappa_1_rhs_conc)
        self.ParameterList.append(self.kappa_2_rhs_conc)
        self.ParameterList.append(self.FLH)

    



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




    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.CostUnitsList['U_C'].append(self.Number)
        


    # ECONOMIC DATA SETTING
    # ---------------------
    
    def set_generalData(self,
                         ProcessGroup,
                         lifetime,
                         emissions = 0,
                         full_load_hours = None,
                         maintenancefactor = 0.044875,
                         CostPercentage = None,
                         TimeSpan = None,
                         TimeMode = None
                         ):
        
        super().set_generalData(ProcessGroup,lifetime,emissions,full_load_hours)
        self.__set_lifeTime(lifetime)
        self.__set_unitoperationEmissionsFactor(emissions)
        self.__set_maintenanceFactor(maintenancefactor)
        
        self.__set_turnoverFactors(CostPercentage, 
                                  TimeSpan,
                                  TimeMode)



    def __set_unitoperationEmissionsFactor(self, emissionfactor):
        self.em_fac_unit['em_fac_unit'][self.Number] = emissionfactor
    
    def __set_lifeTime(self, lifetime):
        self.LT['LT'][self.Number] = lifetime
        
    def __set_maintenanceFactor(self, factor=0.044875):
        self.K_M['K_M'][self.Number] = factor

    def set_economicData(self,
                          DirectCostFactor,
                          IndirectCostFactor,
                          ReferenceCosts,
                          ReferenceFlow,
                          CostExponent,
                          ReferenceYear,
                          ReferenceFlowType,
                          ReferenceFlowComponentList
                          ):
        
        
        self.__set_dcFactor(DirectCostFactor)
        self.__set_idcFactor(IndirectCostFactor)
        
        self.__set_capexFactors(ReferenceCosts,
                                ReferenceFlow,
                                CostExponent,
                                ReferenceYear)
        
        self.__set_kappa_2_capex(ReferenceFlowType)
        self.__set_kappa_1_capex(ReferenceFlowComponentList)



    def __set_dcFactor(self, DC):
        self.DC_factor['DC'][self.Number] = DC



    def __set_idcFactor(self, IDC):
        self.IDC_factor['IDC'][self.Number] = IDC



    def __set_capexFactors(self, CREF, MREF, F, YEAR_REF):
        
        self.CAPEX_factors['C_Ref'] = {self.Number: CREF}
        self.CAPEX_factors['m_Ref'] = {self.Number: MREF}
        self.CAPEX_factors['f'] = {self.Number: F}
        self.CAPEX_factors['CECPI_ref'] = {self.Number: self.CECPI_dic[YEAR_REF]}
        
        
    def __set_turnoverFactors(self, CostPercentage, TimeSpan = None, TimeMode = 'No Mode'):
        
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
         

        
    def __set_kappa_1_capex(self, kappa_1_list):
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



    def __set_kappa_2_capex(self, kappa_2_capex_string):  
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
         
         "Public"
         return fac
     
        
    def calc_turnoverACC(self, IR):
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
        "Public"
        return annual_turnover_costs


            
    # ENERGY DATA SETTING
    # -------------------

    def set_energyData(self,
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
        
        self.__set_tauFactors(dic1)
        self.__set_kappa_1_ut(dic2)
        self.__set_kappa_2_ut(dic3)
        
        

    def __set_tauFactors(self, tau_dic):
        """

        Parameters
        ----------
        tau_dic : Dictionary
            Example: dict= {'Utility1' : value1 , 'Utility2' : value2}

        """

        for i in tau_dic:
            self.tau['tau'][self.Number,i] = tau_dic[i]



    def __set_kappa_1_ut(self, kappa_1_ut_dic):
        """
        Parameters
        ----------
        kappa_1_ut_dic : Dictionary
            Example: dict = {'Utility1': ['I1','I2'], 'Utitility2': [...]}

        """
        for i in kappa_1_ut_dic:
            for j in kappa_1_ut_dic[i]:
                self.kappa_1_ut['kappa_1_ut'][self.Number,i,j] = 1



    def __set_kappa_2_ut(self, kappa_2_ut_dic):
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
            elif kappa_2_ut_dic[i]  == 'FIN_M':
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 2
            elif kappa_2_ut_dic[i]  == 'FOUT_M':
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 4                
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
        
        "Public"
        


    

    def fill_parameterList(self):
        
        super().fill_parameterList()
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
#--------------------------SPLITTER PROCESS------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------




class Splitter(PhysicalProcess):
    
    def __init__(self, Name, UnitNumber, Parent = None, *args, **kwargs):
        
        super().__init__(Name, UnitNumber,Parent)
        
        self.Type = "Splitter"
        
    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.SplitterNumberList['U_SPLITTER'].append(self.Number)
        
        
        




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

    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.StoichRNumberList['U_STOICH_REACTOR'].append(self.Number)

    def set_gammaFactors(self, gamma_dic):
       
        """

        Parameters
        ----------
        gamma_dic : Dictionary
            Example: dict= {(i1, r1) : value1, (i2, r1): value2,
                            (i3, r1): value3}

        """
        for i in gamma_dic:
            self.gamma['gamma'][self.Number, i]  = gamma_dic[i]



    def set_thetaFactors(self, theta_dic):
        """

        Parameters
        ----------
        theta_dic: Dictionary
            Example:  dict= {(r1,m1): value1}
        """
        for i in theta_dic:
            self.theta['theta'][self.Number, i] = theta_dic[i]


    def set_reactionData(self,
                          StoichiometricFactors,
                          ConversionFactors
                          ):
        
        if self.Type == "Stoich-Reactor":
            print(self.Name)
            self.add_gammaFactors(StoichiometricFactors)
            self.add_thetaFactors(ConversionFactors)
 

    def fill_parameterList(self):
        super().fill_parameterList()
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
        self.inert_components = []
        self.ic_on_ = 0
        self.ic_on = {'ic_on': {}}
        

        # Indexed Attributes
        self.xi = {'xi': {}}


            
    # REACTION SETTING METHODS
    # ------------------------

    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.YieldRNumberList['U_YIELD_REACTOR'].append(self.Number)
        
        if self.ic_on_ == 1:
            self.ic_on['ic_on'][self.Number] = 1
            for i in self.inert_components:
                superstructure.YieldSubSet['YC'].append((self.Number,i))
                

        
    def set_inertComponents(self, inert_components_list):
        for i in inert_components_list:
            if i not in self.inert_components:
                self.inert_components.append(i)
            
        if self.inert_components:
            self.ic_on_ = 1
            


    def set_xiFactors(self, xi_dic):
        """

        Parameters
        ----------
        xi_dic : Dictionary
            Example: dict = {i1: value1, i2: value2, i3: value3}

        """
        for i in xi_dic:
            self.xi['xi'][self.Number,i] = xi_dic[i]
            
    def fill_parameterList(self):
        super().fill_parameterList()
        self.ParameterList.append(self.xi)
        self.ParameterList.append(self.ic_on)





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

    def fill_unitOperationsList(self, superstructure):
        super().fill_unitOperationsList(superstructure)
        superstructure.HeatGeneratorList['U_FUR'].append(self.Number)

    def set_efficiency(self, Efficiency):
        """
        Parameters
        ----------
        Efficiency : Float
            Sets efficiency of the furnace process between 0 and 1
        """
        self.Efficiency_FUR['Efficiency_FUR'][self.Number]  = Efficiency
        
    def fill_parameterList(self):
        super().fill_parameterList()
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


    def fill_unitOperationsList(self, superstructure):
        super().fill_unitOperationsList(superstructure)
        superstructure.ElectricityGeneratorList['U_TUR'].append(self.Number)

    def set_efficiency(self, Efficiency):
        """
        Parameters
        ----------
        Efficiency : Float
            Sets efficiency of the Combined gas and stea turbine
            process between 0 and 1
        """
        self.Efficiency_TUR['Efficiency_TUR'][self.Number]  = Efficiency


    def fill_parameterList(self):
        super().fill_parameterList()
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
        
            
    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.ProductPoolList['U_PP'].append(self.Number)
        
            
    def set_emissionCredits(self, emissionfactor):
        self.em_credits['em_fac_prod'][self.Number] = emissionfactor
        
            
    def set_productPrice(self, Price):
        self.ProductPrice['ProductPrice'][self.Number] = Price


    def fill_parameterList(self):
        super().fill_parameterList()
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
        self.EmissionFactor = {'em_fac_source': {self.Number: 0}}
        
    
    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.SourceList['U_S'].append(self.Number)
    
    def set_sourceData(self, 
                        Costs,
                        UpperLimit,
                        EmissionFactor,
                        Composition_dictionary):

        self.__set_materialCosts(Costs)
        self.__set_upperlimit(UpperLimit)
        self.__set_poolEmissionFactor(EmissionFactor)
        self.__set_composition(Composition_dictionary)

    def __set_materialCosts(self, Costs):
        self.MaterialCosts['materialcosts'][self.Number] = Costs
        
        
    def __set_composition(self, composition_dic):
        for i in composition_dic:       
            self.Composition['phi'][(self.Number,i)] = composition_dic[i]
        
    def __set_upperlimit(self, UpperLimit):
        self.UpperLimit['ul'][self.Number] = UpperLimit
        
    def __set_poolEmissionFactor(self, EmissionFactor):
        self.EmissionFactor['em_fac_source'][self.Number] = EmissionFactor
    
    def fill_parameterList(self):
        super().fill_parameterList()
        self.ParameterList.append(self.Composition)
        self.ParameterList.append(self.MaterialCosts)
        self.ParameterList.append(self.UpperLimit)
        self.ParameterList.append(self.EmissionFactor)
   
        
   
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#-------------------------DISTRIBUTOR CLASS------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


class Distributor (VirtualProcess): 
    """
    Description 
    -----------  
    - new Processtype 
    - Distributing the Inputflow to different targets 
    - dividing the flow in a bilinear way 
    -it can be chosen how small can be the smallest division 
    (e.g. 0.1, 0.01, 0.001, etc.)
    
 
    
    Context 
    ----------
    the class is called in the Super Structure Block
    
    Parameters
    ---------- 
    Type: Distributor 
    Decimal_numbers:  1,2,3 or 4 -> it shows the decimal place 
    for the smallest possible devision
    (maximal: 4)
        
    Returns
    -------


    """
    
    
    
    """"FINISHED:
        Distributor kann jetzt erstzeugt werden mit Ansage einer Dezimalstelle 
        und der Targets. Es gibt eine Funktion zum schreiben des Subsets und des
        Parameter-Vektors der angibt wie viele Möglichekeiten es zum aufsplitten gibt.
        
        Außerdem wird ein Kombi-Set aus Distr,Target gebildet und dem Superstructure 
        Objekt übergeben.
        
        ToDos: 
            - Schreiben der Variables / Sets in Superstructure
            - Übertragen der Parameter / Sets in die superstructure
            - SChreiben eines Wrappers
            - DAtenBlatt in Excel
            - Exetions in Excel_Wrapper für "Distributor-Blatt"
            - Tests und Debugging
        """
    
    
    def __init__(self, Name, UnitNumber, Decimal_place= 3, Targets= None,
                 Parent= None, *args, **kwargs):

        super().__init__(Name, UnitNumber,  Parent) 
        
        self.Type = "Distributor"  
        self.Decimal_numbers = {'Decimal_numbers': {}}
        self.decimal_numbers = {'Decimal_numbers': {}}
        self.decimal_set = []
        self.decimal_place = Decimal_place
        self.targets = []
        
        
        
    def set_targets(self, targets_list): 
        self.targets = targets_list

    def set_decimalPlace (self, decimal_place):
        self.decimal_place = decimal_place
        
            
        
        
    def calc_decimalNumbers(self):
        X = [1, 2 ,3 ,4 ,8]
        XO = 0        
        self.decimal_numbers['Decimal_numbers'][self.Number,0] = XO
        
        for i in range(1,self.decimal_place+1):
            for j in X:
                idx = X.index(j)+1
                idx = idx + (i-1) * 5
                entr = j / (10**i)
                
                self.decimal_numbers['Decimal_numbers'][self.Number,idx] = entr 
                self.decimal_set.append((self.Number,idx))
                
                
                


    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        
        if not hasattr(superstructure, 'distributor_list'):
            setattr(superstructure, 'distributor_subset', {'U_DIST_SUB': []})
            setattr(superstructure, 'distributor_list', {'U_DIST': []})
            setattr(superstructure, 'decimal_vector', {'D_VEC': []})
            setattr(superstructure, 'decimal_set', {'DC_SET': []})
        
 
        superstructure.distributor_list['U_DIST'].append(self.Number)
        superstructure.decimal_set['DC_SET'].append(self.decimal_set)
        
            
        for i in self.targets:
            combi = (self.Number,i) 
            
            if i not in superstructure.distributor_subset['U_DIST_SUB']:
                superstructure.distributor_subset['U_DIST_SUB'].append(combi)


    def fill_parameterList(self):

        super().fill_parameterList()
        
        self.ParameterList.append(self.decimal_numbers)
        
            



