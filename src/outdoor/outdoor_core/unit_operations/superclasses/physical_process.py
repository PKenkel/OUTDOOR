import math 
from .process import Process


        
        
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

        self.K_OM = {'K_OM': {self.Number: 0}}
        
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
                         maintenancefactor = None,
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
        
    def __set_maintenanceFactor(self, factor=None):
        self.K_OM['K_OM'][self.Number] = factor

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
                        Heat2ReferenceComponentList = [],
                        ChillingDemand = None,
                        ChillingReferenceFlow = None,
                        ChillingReferenceComponentsList = []
                        ):

        
        dic1 = {'Electricity': ElectricityDemand, 
                'Heat':  HeatDemand,
                'Heat2': Heat2Demand,
                'Chilling': ChillingDemand}

        dic2= {'Electricity': ElectricityReferenceComponentList,
                'Heat': HeatReferenceComponentList,
                'Heat2': Heat2ReferenceComponentList,
                'Chilling': ChillingReferenceComponentsList}

        dic3 = {'Electricity': ElectricityReferenceFlow,
                'Heat': HeatReferenceFlow,
                'Heat2': Heat2ReferenceFlow,
                'Chilling': ChillingReferenceFlow}
        
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
            elif kappa_2_ut_dic[i]  == 'FIN_CP':   
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 5 
            elif kappa_2_ut_dic[i]  == 'FOUT_CP':   
                self.kappa_2_ut['kappa_2_ut'][self.Number,i]  = 6               
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
        self.ParameterList.append(self.K_OM)
        self.ParameterList.append(self.turn_over_acc)

