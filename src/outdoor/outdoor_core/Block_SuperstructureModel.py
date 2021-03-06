from pyomo.environ import *


class SuperstructureModel(AbstractModel):
        
    """
    Attributes
    ----------
    
    ** SETS **
    
    ** PARAMETERS **
    
    ** VARIABLES **
    
    
    


    Methods
    --------
    
    create_Sets:
    
    create_MassBalances:
        
    create_EnergyBalances:
        
    create_DecisionMaking:
        
    create_EconomicEvaluation:
              
    create_EnvironmentalEvaluation:
        
    create_Rest:
     
    create_ModelEquations:
        
        

    
    """

    def __init__(self, SuperStructure, *args, **kwargs):       
        super().__init__(*args, **kwargs)
        self.SS = SuperStructure

      
        
    def create_ModelEquations(self):
        self.create_Sets()

        self.create_MassBalances()
        self.create_EnergyBalances()
        self.create_EconomicEvaluation()
        self.create_EnvironmentalEvaluation()
        self.create_DecisionMaking()
        self.create_ObjectiveFunction()
        
    def populateModel(self, Data_file):
        self.ModelInstance = self.create_instance(Data_file)
        return self.ModelInstance


# Pyomo Model Methods
# --------------------


    # Set Method

    def create_Sets(self):
        
        # Process Units
        self.U = Set()
        self.UU = Set(within=self.U)
        self.U_STOICH_REACTOR = Set(within=self.U)
        self.U_YIELD_REACTOR = Set(within=self.U)
        self.U_SPLITTER = Set(within=self.U)     
        self.U_TUR = Set(within=self.U)
        self.U_FUR = Set(within=self.U)
        self.U_PP = Set(within=self.U)
        self.U_C = Set(within=self.U)
        
        # Components
        self.I = Set()
        self.M = Set(within=self.I)
        
        # Reactions, Utilities
        self.R = Set()
        self.UT = Set() 
        self.H_UT = Set(within=self.UT)
        self.HI = Set()
        
        # Linear CAPEX Set
        self.J =Set()
        self.JI = Set(within=self.J)
        


            
    
    # **** MASS BALANCES *****
    # -------------------------
        
    def create_MassBalances(self):
        """
        Description
        -------
        This method creates the PYOMO parameters and variables
        that are necessary for the generalMass Balances (eg. FLOWS, PHI, MYU etc.). 
        Afterwards Masse Balance Equations are written as PYOMO Constraints.

        """
        

         
        # Parameter
        self.myu = Param(self.U, self.UU, self.I, initialize=0)
        self.phi1 = Param(self.U, self.I, initialize=0)
        self.phi2 = Param(self.U, self.I, initialize=0)
        self.conc = Param(self.U, initialize=0)
        self.gamma = Param(self.U_STOICH_REACTOR, self.I, self.R,  initialize=0)
        self.theta = Param(self.U_STOICH_REACTOR, self.R, self.M, initialize=0)
        self.xi = Param(self.U_YIELD_REACTOR, self.I, initialize=0)
        self.alpha = Param(self.U, initialize=120000) 

        
        self.kappa_1_lhs_conc = Param(self.U, self.I, initialize=0)
        self.kappa_1_rhs_conc = Param(self.U, self.I, initialize=0)
        self.kappa_2_lhs_conc = Param(self.U, initialize=3)
        self.kappa_2_rhs_conc = Param(self.U, initialize=3)
        self.Names = Param(self.U)     
        self.ul_1 = Param(self.U, initialize = 10000000)
        self.ul_2 = Param(self.U, initialize = 10000000)
        


        # Variables
        self.FLOW = Var(self.U, self.UU, self.I,  within=NonNegativeReals)
        self.FLOW_IN = Var(self.U, self.I,  within=NonNegativeReals)
        self.FLOW_OUT = Var(self.U, self.I, within=NonNegativeReals)
        self.FLOW_WASTE  = Var(self.U, self.I, within=NonNegativeReals)
        self.FLOW_WASTE_TOTAL  =Var(self.I, within=NonNegativeReals)
        self.FLOW_ADD_1 = Var(self.U, within=NonNegativeReals)
        self.FLOW_ADD_2 = Var(self.U, within=NonNegativeReals) 
        self.FLOW_ADD_TOT = Var(self.U, self.I, within=NonNegativeReals)
        self.FLOW_SUM = Var(self.U, within=NonNegativeReals) 
        self.Y = Var(self.U, within=Binary)
        
        
        # Constraints
         
        def MassBalance_1_rule(self,u,i):
            return self.FLOW_IN[u,i] == self.FLOW_ADD_TOT[u,i] \
                + sum(self.FLOW[uu,u,i] for uu in self.UU) 

        def MassBalance_2_rule(self,u,i):
            return self.FLOW_ADD_TOT[u,i] <= self.alpha[u] * self.Y[u]
        
        def MassBalance_3_rule(self,u,i):
            return self.FLOW_ADD_TOT[u,i] <= self.FLOW_ADD_1[u] * self.phi1[u,i] \
                + self.FLOW_ADD_2[u] * self.phi2[u,i] + self.alpha[u] * (1-self.Y[u])

        def MassBalance_4_rule(self,u,i):
            return self.FLOW_ADD_TOT[u,i] >= self.FLOW_ADD_1[u] * self.phi1[u,i] \
                + self.FLOW_ADD_2[u] * self.phi2[u,i] - self.alpha[u] * (1-self.Y[u]) 
                
                
        def MassBalance_13_rule(self,u):
            return self.FLOW_ADD_1[u]  <= self.ul_1[u]
        
        def MassBalance_14_rule(self,u):
            return self.FLOW_ADD_2[u]  <= self.ul_2[u]

        def MassBalance_5_rule(self,u,i):
            if u in self.U_YIELD_REACTOR:
                return self.FLOW_OUT[u,i] == sum(self.FLOW_IN[u,i] for i in self.I) * self.xi[u,i]
            elif u in self.U_STOICH_REACTOR:
                return self.FLOW_OUT[u,i] == self.FLOW_IN[u,i] \
                    + sum(self.gamma[u,i,r] * self.theta[u,r,m] * self.FLOW_IN[u,m] \
                          for r in self.R for m in self.M)
            else:
                return self.FLOW_OUT[u,i] == self.FLOW_IN[u,i]

         
        def MassBalance_6_rule(self,u,uu,i):
            return self.FLOW[u,uu,i] <= self.myu[u,uu,i] * self.FLOW_OUT[u,i] \
                + self.alpha[u] * (1-self.Y[uu])
            
        def MassBalance_7_rule(self,u,uu,i):
            return self.FLOW[u,uu,i] <= self.alpha[u] * self.Y[uu]
        
        def MassBalance_8_rule(self,u,uu,i):
            return self.FLOW[u,uu,i] >= self.myu[u,uu,i] * self.FLOW_OUT[u,i] \
                - self.alpha[u] * (1-self.Y[uu])

        def MassBalance_9_rule(self,u,i):
            return self.FLOW_WASTE[u,i] == self.FLOW_OUT[u,i] \
                - sum(self.FLOW[u,uu,i] for uu in self.UU)

        def MassBalance_10_rule(self,i):
            return self.FLOW_WASTE_TOTAL[i]  == sum(self.FLOW_WASTE[u,i] for u in self.U)
         
        def MassBalance_11_rule(self,u):
            if self.kappa_2_lhs_conc[u] == 0 and self.kappa_2_rhs_conc[u]  == 0:
                return sum(self.FLOW_OUT[u,i] * self.kappa_1_lhs_conc[u,i] for i in self.I) \
                    == self.conc[u] * sum(self.FLOW_OUT[u,i] * self.kappa_1_rhs_conc[u,i] for i in self.I)
            elif self.kappa_2_lhs_conc[u]  == 0 and self.kappa_2_rhs_conc[u]  == 1:
                return sum(self.FLOW_OUT[u,i] * self.kappa_1_lhs_conc[u,i] for i in self.I) \
                    == self.conc[u] * sum(self.FLOW_IN[u,i] * self.kappa_1_rhs_conc[u,i] for i in self.I)
            elif self.kappa_2_lhs_conc[u]  == 1 and self.kappa_2_rhs_conc[u]  == 0:
                return sum(self.FLOW_IN[u,i] * self.kappa_1_lhs_conc[u,i] for i in self.I) \
                    == self.conc[u] * sum(self.FLOW_OUT[u,i] * self.kappa_1_rhs_conc[u,i] for i in self.I)
            elif self.kappa_2_lhs_conc[u]  == 1 and self.kappa_2_rhs_conc[u]  == 1:
                return sum(self.FLOW_IN[u,i] * self.kappa_1_lhs_conc[u,i] for i in self.I) \
                    == self.conc[u] * sum(self.FLOW_IN[u,i] * self.kappa_1_rhs_conc[u,i] for i in self.I)
            else:
                return Constraint.Skip
            
        def MassBalance_12_rule(self,u):
            return self.FLOW_SUM[u] == sum(self.FLOW_IN[u,i] for i in self.I)
        
    
         
        self.MassBalance_1 = Constraint(self.U, self.I, rule=MassBalance_1_rule)
        self.MassBalance_2 = Constraint(self.U, self.I, rule=MassBalance_2_rule)
        self.MassBalance_3 = Constraint(self.U, self.I, rule=MassBalance_3_rule)
        self.MassBalance_4 = Constraint(self.U, self.I, rule=MassBalance_4_rule)
        self.MassBalance_5 = Constraint(self.U, self.I, rule=MassBalance_5_rule)
        self.MassBalance_6 = Constraint(self.U, self.UU, self.I, rule=MassBalance_6_rule)
        self.MassBalance_7 = Constraint(self.U, self.UU, self.I, rule=MassBalance_7_rule)
        self.MassBalance_8 = Constraint(self.U, self.UU, self.I, rule=MassBalance_8_rule)
        self.MassBalance_9 = Constraint(self.U,  self.I, rule=MassBalance_9_rule)
        self.MassBalance_10 = Constraint(self.I, rule=MassBalance_10_rule)
        self.MassBalance_11 = Constraint(self.U, rule=MassBalance_11_rule)
        self.MassBalance_12 = Constraint(self.U, rule=MassBalance_12_rule)
        self.MassBalance_13 = Constraint(self.U, rule=MassBalance_13_rule)
        self.MassBalance_14 = Constraint(self.U, rule=MassBalance_14_rule)












    # **** ENERGY BALANCES *****
    # -------------------------

    def create_EnergyBalances(self):
        """
        Description
        -------
        This method creates the PYOMO parameters and variables
        that are necessary for the general Energy Balances (eg. TAU, REF_FLOW...). 
        Afterwards Energy Balance‚ Equations are written as PYOMO Constraints.

        """
        
        self.beta  = Param(self.U, self.H_UT, self.HI, initialize=0)
        self.tau_h = Param(self.H_UT, self.U, initialize=0)
        self.tau_c = Param(self.H_UT, self.U, initialize=0)
        
        self.alpha_hex  =  Param(initialize=10000000)
        self.Y_HEX = Var(self.HI, within=Binary)
        
        
        # Parameter
        self.tau = Param(self.U, self.UT, initialize=0)
        self.kappa_1_ut = Param(self.U, self.UT, self.I, initialize=0)
        self.kappa_2_ut = Param(self.U, self.UT, initialize=3)
        
        self.kappa_3_heat = Param(self.U, self.HI, initialize=0)
        
        self.kappa_3_heat2 = Param(self.U, self.HI, initialize=0)
        
        
        self.COP_HP = Param(initialize=0)
        self.Efficiency_TUR = Param(self.U_TUR, initialize=0)
        self.Efficiency_FUR = Param(self.U_FUR, initialize=0)
        self.LHV  = Param(self.I, initialize=0)
        self.H = Param()
        
        
        # Variables
        self.REF_FLOW_EL = Var(self.U, within = NonNegativeReals)
        self.REF_FLOW_HEAT = Var(self.U, within = NonNegativeReals)
        self.REF_FLOW_COOLING = Var(self.U, within = NonNegativeReals)
        
        self.ENERGY_DEMAND_EL = Var(self.U)
        self.EL_PROD_1 = Var(self.U_TUR, within = NonNegativeReals)
        self.ENERGY_DEMAND_EL_TOT = Var()
        
        
        self.ENERGY_DEMAND_HEAT = Var(self.U,self.HI, within= NonNegativeReals)
        self.ENERGY_DEMAND_COOL = Var(self.U,self.HI, within= NonNegativeReals)  
        self.ENERGY_DEMAND_HP = Var(within=NonNegativeReals)
        
        self.ENERGY_DEMAND_HEAT_UNIT = Var(self.U, within=NonNegativeReals)
        self.ENERGY_DEMAND_COOL_UNIT = Var(self.U, within=NonNegativeReals)
        
    
        self.ENERGY_DEMAND_HEAT_RESI = Var(self.HI, within=NonNegativeReals)
        self.ENERGY_DEMAND_HEAT_DEFI = Var(self.HI, within=NonNegativeReals)
        
        self.ENERGY_DEMAND_COOLING = Var(within=NonNegativeReals)
        self.ENERGY_DEMAND_HP_EL  = Var(within=NonNegativeReals)
        self.ENERGY_DEMAND_HP_USE = Var(within=NonNegativeReals)
        # self.ENERGY_DEMAND_HEAT_TOT = Var(self.HI)  
        self.EXCHANGE_TOT = Var()
        self.ENERGY_EXCHANGE = Var(self.HI, within=NonNegativeReals)
        self.ENERGY_DEMAND_HEAT_PROD_USE = Var(within=NonNegativeReals)
        self.ENERGY_DEMAND_HEAT_PROD_SELL = Var(within=NonNegativeReals)
        
        self.ENERGY_DEMAND_HEAT_PROD = Var(self.U_FUR, within=NonNegativeReals)
        
        # Constraints
        
        # Electrictiy Balance
        # --------------------
        
        def ElectricityBalance_1_rule(self,u):
            if self.kappa_2_ut[u,'Electricity'] == 1:
              return  self.REF_FLOW_EL[u] == sum(self.FLOW_IN[u,i] \
                                * self.kappa_1_ut[u,'Electricity',i] for i in self.I)
            elif self.kappa_2_ut[u,'Electricity'] == 0:
              return self.REF_FLOW_EL[u] == sum(self.FLOW_OUT[u,i] \
                                * self.kappa_1_ut[u,'Electricity',i] for i in self.I)
            else:
              return self.REF_FLOW_EL[u] == 0
            
        def ElectricityBalance_2_rule(self,u):
            return self.ENERGY_DEMAND_EL[u] == self.REF_FLOW_EL[u] * self.tau[u,'Electricity']
        
        def ElectricityBalance_3_rule(self,u):
            return self.EL_PROD_1[u] == self.Efficiency_TUR[u] \
                * sum(self.LHV[i] * self.FLOW_IN[u,i] for i in self.I)
            
        def ElectricityBalance_4_rule(self):
            return self.ENERGY_DEMAND_EL_TOT == sum(self.ENERGY_DEMAND_EL[u] for u in self.U) \
                - sum(self.EL_PROD_1[u] for u in self.U_TUR) + self.ENERGY_DEMAND_HP_EL
        
        
        self.ElectricityBalance_1 = Constraint(self.U, rule=ElectricityBalance_1_rule)
        self.ElectricityBalance_2 = Constraint(self.U, rule=ElectricityBalance_2_rule)
        self.ElectricityBalance_3 = Constraint(self.U_TUR, rule=ElectricityBalance_3_rule)  
        self.ElectricityBalance_4 = Constraint(rule=ElectricityBalance_4_rule)
        
        
        
        # Heat and Cooling Balance
        # -------------------------

        def HeatBalance_11_rule(self,u):
            if self.kappa_2_ut[u,'Heat'] == 1:
              return  self.REF_FLOW_HEAT[u] == sum(self.FLOW_IN[u,i] \
                                        * self.kappa_1_ut[u,'Heat',i] for i in self.I)
            elif self.kappa_2_ut[u,'Heat'] == 0:
              return self.REF_FLOW_HEAT[u] == sum(self.FLOW_OUT[u,i] \
                                        * self.kappa_1_ut[u,'Heat',i] for i in self.I)
            else:
              return self.REF_FLOW_HEAT[u] == 0

      
        def HeatBalance_1_rule(self,u,hi):
            return self.ENERGY_DEMAND_HEAT[u,hi] == \
                sum(self.beta[u,ut,hi] * self.tau_c[ut,u] \
                    * self.REF_FLOW_HEAT[u] for ut in self.H_UT)
        
        def HeatBalance_2_rule(self,u,hi):
            return self.ENERGY_DEMAND_COOL[u,hi] == \
                sum(self.beta[u,ut,hi] * self.tau_h[ut,u] \
                    * self.REF_FLOW_HEAT[u] for ut in self.H_UT)
        
        
        def HeatBalance_3_rule(self,u,hi):
            k = len(self.HI)
            if hi == 1:
                return sum(self.ENERGY_DEMAND_HEAT[u,hi] for u in self.U) \
                    + self.ENERGY_DEMAND_HEAT_PROD_USE - self.ENERGY_DEMAND_HEAT_RESI[hi] \
                        - self.ENERGY_EXCHANGE[hi] == 0
            elif hi == k:
                return sum(self.ENERGY_DEMAND_HEAT[u,hi] for u in self.U) \
                    + self.ENERGY_DEMAND_HEAT_RESI[hi-1] - self.ENERGY_DEMAND_COOLING \
                        - self.ENERGY_DEMAND_HP - self.ENERGY_EXCHANGE[hi] == 0
            else:
                return sum(self.ENERGY_DEMAND_HEAT[u,hi] for u in self.U) \
                    + self.ENERGY_DEMAND_HEAT_RESI[hi-1] - self.ENERGY_EXCHANGE[hi] \
                        - self.ENERGY_DEMAND_HEAT_RESI[hi]  == 0
             
        def HeatBalance_4_rule(self,u,hi):
            k = len(self.HI)
            if hi == 1:
                return sum(self.ENERGY_DEMAND_COOL[u,hi] for u in self.U) \
                    - self.ENERGY_EXCHANGE[hi] - self.ENERGY_DEMAND_HEAT_DEFI[hi] == 0
            elif hi == k-1:
                return sum(self.ENERGY_DEMAND_COOL[u,hi] for u in self.U) \
                    - self.ENERGY_DEMAND_HEAT_DEFI[hi] \
                        - self.ENERGY_EXCHANGE[hi]  \
                            - self.ENERGY_DEMAND_HP_USE == 0
            else:
                return sum(self.ENERGY_DEMAND_COOL[u,hi] for u in self.U) \
                    - self.ENERGY_EXCHANGE[hi] - self.ENERGY_DEMAND_HEAT_DEFI[hi] == 0  
                        
        def HeatBalance_5_rule(self,hi):
            if hi == 1 :
                return self.ENERGY_EXCHANGE[hi] <= sum(self.ENERGY_DEMAND_COOL[u,hi] for u in self.U)
            else:
                return self.ENERGY_EXCHANGE[hi] <= sum(self.ENERGY_DEMAND_COOL[u,hi] for u in self.U)
        
        def HeatBalance_6_rule(self,hi):
            if hi == 1 :
                return self.ENERGY_EXCHANGE[hi] <= sum(self.ENERGY_DEMAND_HEAT[u,hi] for u in self.U) \
                    + self.ENERGY_DEMAND_HEAT_PROD_USE
            else:
                return self.ENERGY_EXCHANGE[hi] <= sum(self.ENERGY_DEMAND_HEAT[u,hi] for u in self.U) \
                    + self.ENERGY_DEMAND_HEAT_RESI[hi-1]
        
        def HeatBalance_7_rule(self):
            return self.EXCHANGE_TOT == sum(self.ENERGY_EXCHANGE[hi] for hi in self.HI)
    
        def HeatBalance_8_rule(self):
            return self.ENERGY_DEMAND_HP_USE == self.ENERGY_DEMAND_HP / (1-(1/self.COP_HP))
        
        def HeatBalance_9_rule(self):
            return self.ENERGY_DEMAND_HP_EL == self.ENERGY_DEMAND_HP / (self.COP_HP - 1 )
        
        def HeatBalance_12_rule(self,hi):
            return self.ENERGY_EXCHANGE[hi] <= self.Y_HEX[hi] * self.alpha_hex
        
        def HeatBalance_13_rule(self,u):
            return self.ENERGY_DEMAND_HEAT_PROD[u] == self.Efficiency_FUR[u] \
                * sum(self.LHV[i] * self.FLOW_IN[u,i] for i in self.I) 
             
        def HeatBalance_14_rule(self,u):
            return self.ENERGY_DEMAND_HEAT_UNIT[u] == \
                sum(self.ENERGY_DEMAND_COOL[u,hi] for hi in self.HI)
        
        def HeatBalance_15_rule(self,u):
            return self.ENERGY_DEMAND_COOL_UNIT[u] ==\
                sum(self.ENERGY_DEMAND_HEAT[u,hi] for hi in self.HI)
                
        def HeatBalance_16_rule(self):
            return self.ENERGY_DEMAND_HEAT_PROD_USE == \
                sum(self.ENERGY_DEMAND_HEAT_PROD[u] for u in self.U_FUR) \
                    - self.ENERGY_DEMAND_HEAT_PROD_SELL
        
        
        
        
        self.HeatBalance_1 = Constraint(self.U, self.HI, rule = HeatBalance_1_rule)
        self.HeatBalance_2 = Constraint(self.U, self.HI, rule = HeatBalance_2_rule) 
        self.HeatBalance_3 = Constraint(self.U, self.HI, rule = HeatBalance_3_rule)    
        self.HeatBalance_4 = Constraint(self.U,self.HI, rule = HeatBalance_4_rule)
        self.HeatBalance_5 = Constraint(self.HI, rule = HeatBalance_5_rule)
        self.HeatBalance_6 = Constraint(self.HI, rule = HeatBalance_6_rule)
        self.HeatBalance_7 = Constraint(rule = HeatBalance_7_rule)
        self.HeatBalance_8 = Constraint(rule = HeatBalance_8_rule)
        self.HeatBalance_9 = Constraint(rule = HeatBalance_9_rule)
        self.HeatBalance_11 = Constraint(self.U, rule=HeatBalance_11_rule)
        self.HeatBalance_12 = Constraint(self.HI, rule= HeatBalance_12_rule)
        self.HeatBalance_13 = Constraint(self.U_FUR, rule=HeatBalance_13_rule)
        self.HeatBalance_14 = Constraint(self.U, rule= HeatBalance_14_rule)
        self.HeatBalance_15 = Constraint(self.U, rule= HeatBalance_15_rule)
        self.HeatBalance_16 = Constraint(rule=HeatBalance_16_rule)


        
        
        
    
        
    # **** COST BALANCES *****
    # -------------------------        
        
        
    def create_EconomicEvaluation(self):
        """
        Description
        -------
        This method creates the PYOMO parameters and variables
        that are necessary for the general Cost Calculation (eg. detla_ut, COST_UT etc.). 
        Afterwards Cost calculation equations are written as PYOMO Constraints.
        """
    



        self.HEN_C = Param(initialize=100)
        self.delta_cool = Param(initialize = 15)

        # Parameter
        self.delta_el = Param(initialize=0)
        self.delta_q = Param(self.HI, initialize=30)
        
        self.delta_rm = Param(self.I, initialize=0)
        
        self.ProductPrice =Param(self.U_PP, initialize=0)
        
        self.DC = Param(self.U, initialize=0)
        self.IDC = Param(self.U, initialize=0)
        self.ACC_Factor = Param(self.U, initialize=0)
        self.K_M = Param(self.U_C, initialize = 0.044875)
        
        self.HP_ACC_Factor = Param(initialize=1)
        self.HP_Costs = Param(initialize = 1)
        
        
    
        self.lin_CAPEX_x = Param(self.U_C, self.J, initialize=0)
        self.lin_CAPEX_y = Param(self.U_C, self.J, initialize=0)
        self.kappa_1_capex = Param(self.U_C, self.I, initialize= 0)
        self.kappa_2_capex = Param(self.U_C, initialize= 5)
        
        self.K_O = Param(initialize = 2.06875)
        self.working_hours = Param(initialize = 8322)
        self.process_steps = Param(initialize = 0)
        self.hourly_wage  = Param(initialize = 41)
        self.M_COST = Var(self.U_C)
        self.M_COST_TOT = Var(within=NonNegativeReals)
        self.capacity_flow = Param()
        
        
        self.O_H = Var()
        self.O_COST = Var()


        
        # Variables
        self.COST_UT = Var()
        self.COST_HEAT = Var(self.HI)
        self.COST_EL = Var()
        
        self.lin_CAPEX_s = Var(self.U_C, self.JI, within=NonNegativeReals)
        self.lin_CAPEX_z = Var(self.U_C, self.JI, within=Binary)
        self.lin_CAPEX_lambda = Var(self.U_C, self.J, bounds=(0,1))
        
        
        self.REF_FLOW_CAPEX = Var(self.U_C, within=NonNegativeReals)
        self.FCI = Var(self.U_C, within=NonNegativeReals)

        self.ACC = Var(self.U_C, within=NonNegativeReals)
        self.EC = Var(self.U_C, within=NonNegativeReals)
        
        self.ACC_HP = Var(within=NonNegativeReals)
        self.TAC = Var()
        self.OM_COST = Var(within=NonNegativeReals)
        self.OPEX =Var()
        self.CAPEX = Var() 
        self.RM_COST = Var(self.U_C, within=NonNegativeReals)
        self.RM_COST_TOT = Var(within=NonNegativeReals)
        self.PROFITS = Var(self.U_PP)
        self.PROFITS_TOT = Var()
        
        
        
        self.HEATCOST = Var(self.HI)
        self.ELCOST = Var()
        self.C_TOT = Var()
        self.HENCOST = Var(self.HI, within=NonNegativeReals)
        self.UtCosts = Var()
        
        self.to_acc = Param(self.U_C, initialize = 0)
        self.TO_CAPEX = Var(self.U_C, within=NonNegativeReals)
        self.TO_CAPEX_TOT = Var(within=NonNegativeReals)
        
        
        # Constraints
        
        # CAPEX Calculation
        # ------------------
        
        
        def CapexEquation_1_rule(self,u):
            if self.kappa_2_capex[u] == 1:
              return  self.REF_FLOW_CAPEX[u] == sum(self.FLOW_IN[u,i] \
                                            * self.kappa_1_capex[u,i] for i in self.I)
            elif self.kappa_2_capex[u] == 0:
              return self.REF_FLOW_CAPEX[u] == sum(self.FLOW_OUT[u,i] \
                                            * self.kappa_1_capex[u,i] for i in self.I)
            elif self.kappa_2_capex[u] == 2:
                return self.REF_FLOW_CAPEX[u] == self.ENERGY_DEMAND_EL[u]
            elif self.kappa_2_capex[u] == 3:
                return self.REF_FLOW_CAPEX[u] == self.ENERGY_DEMAND_HEAT_PROD[u]
            elif self.kappa_2_capex[u] == 4:
                return self.REF_FLOW_CAPEX[u] == self.EL_PROD_1[u]
            else:
              return self.REF_FLOW_CAPEX[u] == 0
            
        def CapexEquation_2_rule(self,u):
            return sum(self.lin_CAPEX_x[u,j] * self.lin_CAPEX_lambda[u,j] for j in self.J) \
                == self.REF_FLOW_CAPEX[u]
        
        def CapexEquation_3_rule(self,u):
            return self.EC[u] == sum(self.lin_CAPEX_y[u,j] * self.lin_CAPEX_lambda[u,j] for j in self.J)
        
        def CapexEquation_4_rule(self,u):
            return sum(self.lin_CAPEX_z[u,j] for j in self.JI) == 1
        
        def CapexEquation_5_rule(self,u,j):
            return self.lin_CAPEX_s[u,j] <= self.lin_CAPEX_z[u,j]
        
        
        def CapexEquation_6_rule(self,u,j):
            if j == 1:
                return self.lin_CAPEX_lambda[u,j] == self.lin_CAPEX_z[u,j] \
                    - self.lin_CAPEX_s[u,j]
            elif j == len(self.J):
                return self.lin_CAPEX_lambda[u,j] == self.lin_CAPEX_s[u,j-1]
            else:
                return self.lin_CAPEX_lambda[u,j] == self.lin_CAPEX_z[u,j] \
                    - self.lin_CAPEX_s[u,j] + self.lin_CAPEX_s[u,j-1]
        
        
        def CapexEquation_7_rule(self,u):
            return self.FCI[u] == self.EC[u] * (1+self.DC[u] + self.IDC[u])
        
        
        def CapexEquation_8_rule(self,u):
            return self.ACC[u] == self.FCI[u] * self.ACC_Factor[u]
        
        def CapexEquation_9_rule(self):
            return self.ACC_HP  == self.HP_ACC_Factor * self.HP_Costs * self.ENERGY_DEMAND_HP_USE

        def CapexEquation_10_rule(self):
            return self.CAPEX == sum(self.ACC[u] for u in self.U_C) *1000000 + \
                self.ACC_HP * 1000000 + self.TO_CAPEX_TOT * 1000000
        
        
        def CapexEquation_11_rule(self,u):
            return self.TO_CAPEX[u] == self.to_acc[u] * self.EC[u] 
        
        def CapexEquation_12_rule(self):
            return self.TO_CAPEX_TOT  == sum(self.TO_CAPEX[u] for u in self.U_C)
        
        self.CapexEquation_1 = Constraint(self.U_C,rule=CapexEquation_1_rule)
        self.CapexEquation_2 = Constraint(self.U_C,rule=CapexEquation_2_rule)
        self.CapexEquation_3 = Constraint(self.U_C,rule=CapexEquation_3_rule)
        self.CapexEquation_4 = Constraint(self.U_C,rule=CapexEquation_4_rule)
        self.CapexEquation_5 = Constraint(self.U_C,self.JI, rule=CapexEquation_5_rule)
        self.CapexEquation_6 = Constraint(self.U_C,self.J, rule=CapexEquation_6_rule)
        self.CapexEquation_7 = Constraint(self.U_C,rule=CapexEquation_7_rule)
        self.CapexEquation_8 = Constraint(self.U_C,rule=CapexEquation_8_rule)
        self.CapexEquation_9 = Constraint(rule=CapexEquation_9_rule)
        self.CapexEquation_10 = Constraint(rule=CapexEquation_10_rule)
         
        self.CapexEquation_11 = Constraint(self.U_C, rule=CapexEquation_11_rule)
        self.CapexEquation_12 = Constraint(rule=CapexEquation_12_rule)   
        
        # OPEX Calculation
        # ----------------   
        
        
        
        def HEN_CostBalance_1_rule(self,hi):
            return self.HEATCOST[hi] == self.ENERGY_DEMAND_HEAT_DEFI[hi] * self.delta_q[hi] 
        
        def HEN_CostBalance_2_rule(self):
            return self.UtCosts == (sum(self.HEATCOST[hi] for hi in self.HI) \
                                    - self.ENERGY_DEMAND_HEAT_PROD_SELL * self.delta_q[1] * 0.7 \
                                    + self.ENERGY_DEMAND_COOLING * self.delta_cool) *self.H
       
        def HEN_CostBalance_3_rule(self):
            return self.ELCOST == self.ENERGY_DEMAND_HP_EL * self.delta_el * self.H 
        
        def HEN_CostBalance_4_rule(self,hi):
            return self.HENCOST[hi]  <= 13.459 * 1000 *  self.ENERGY_EXCHANGE[hi] \
                + 3389.3 + self.alpha_hex * (1-self.Y_HEX[hi])
        def HEN_CostBalance_4b_rule(self,hi):
            return self.HENCOST[hi]  >= 13.459 * 1000 * self.ENERGY_EXCHANGE[hi] \
                + 3389.3 - self.alpha_hex * (1-self.Y_HEX[hi])
        
        def HEN_CostBalance_4c_rule(self,hi):
            return self.HENCOST[hi]  <= self.Y_HEX[hi] * self.alpha_hex
        
        def HEN_CostBalance_5_rule(self):
            return self.ACC_HP == self.HP_ACC_Factor * self.HP_Costs * self.ENERGY_DEMAND_HP_USE
        
        def HEN_CostBalance_6_rule(self):
            return self.C_TOT ==  self.UtCosts + sum(self.HENCOST[hi] for hi in self.HI)
        

        
        self.HEN_CostBalance_1 = Constraint(self.HI, rule = HEN_CostBalance_1_rule)
        self.HEN_CostBalance_2 = Constraint(rule = HEN_CostBalance_2_rule)
        self.HEN_CostBalance_3= Constraint(rule = HEN_CostBalance_3_rule)
        self.HEN_CostBalance_4 = Constraint(self.HI, rule=HEN_CostBalance_4_rule) 
        self.HEN_CostBalance_4b = Constraint(self.HI, rule=HEN_CostBalance_4b_rule)
        self.HEN_CostBalance_4c = Constraint(self.HI, rule=HEN_CostBalance_4c_rule)
        self.HEN_CostBalance_5 = Constraint(rule = HEN_CostBalance_5_rule)
        self.HEN_CostBalance_6 = Constraint(rule = HEN_CostBalance_6_rule)
        
                    
        # Utility Costs
        # -------------
         
        def Ut_CostBalance_2_rule(self):
            return self.COST_EL == self.ENERGY_DEMAND_EL_TOT * self.delta_el * self.H
        
        def Ut_CostBalance_3_rule(self):
            return self.COST_UT == self.COST_EL 
        
        

        self.Ut_CostBalance_2_ = Constraint(rule=Ut_CostBalance_2_rule)
        self.Ut_CostBalance_3 = Constraint(rule= Ut_CostBalance_3_rule)

        
        # Raw Materials and Operating and Maintenance
        # -------------------------------------------
            
        def RM_CostBalance_1_rule(self,u):
            return self.RM_COST[u] <= self.alpha[u] * self.Y[u]
        
        def RM_CostBalance_2_rule(self,u):
            return self.RM_COST[u] <= sum(self.FLOW_ADD_TOT[u,i] * self.delta_rm[i] for i in self.I) \
                + self.alpha[u] *  (1-self.Y[u]) 

        def RM_CostBalance_3_rule(self,u):
            return self.RM_COST[u] >= sum(self.FLOW_ADD_TOT[u,i] * self.delta_rm[i] for i in self.I) \
                - self.alpha[u] *  (1-self.Y[u]) 
            
        def RM_CostBalance_4_rule(self):
            return self.RM_COST_TOT == sum(self.RM_COST[u] for u in self.U_C) * self.H
        
        
        
        
        
        def OM_CostBalance_1_rule(self,u):
            return self.M_COST[u] == self.K_M[u] * self.FCI[u]
        
        def OM_CostBalance_2_rule(self):
            return self.M_COST_TOT == sum(self.M_COST[u] for u in self.U_C)
        
        def OM_CostBalance_3_rule(self): 
            return self.O_H == 2.13 * self.capacity_flow * self.process_steps * self.working_hours / 24 
   
        def OM_CostBalance_4_rule(self):
            return self.O_COST  == self.K_O * self.O_H * self.hourly_wage
        
        def OM_CostBalance_5_rule(self):
            return self.OM_COST == self.O_COST + self.M_COST_TOT *  1000000
        
        def Opex_1_rule(self):
            return self.OPEX == self.OM_COST + self.RM_COST_TOT + self.COST_UT + self.C_TOT
        
        
        
        self.OM_CostBalance_1 = Constraint(self.U_C, rule=OM_CostBalance_1_rule)
        self.OM_CostBalance_2 = Constraint(rule=OM_CostBalance_2_rule)
        self.OM_CostBalance_3 = Constraint(rule=OM_CostBalance_3_rule)
        self.OM_CostBalance_4 = Constraint(rule=OM_CostBalance_4_rule)
        self.OM_CostBalance_5 = Constraint(rule=OM_CostBalance_5_rule)
        
        
        
        self.RM_CostBalance_1 = Constraint(self.U_C, rule= RM_CostBalance_1_rule)
        self.RM_CostBalance_2 = Constraint(self.U_C, rule= RM_CostBalance_2_rule)
        self.RM_CostBalance_3 = Constraint(self.U_C, rule= RM_CostBalance_3_rule)
        self.RM_CostBalance_4 = Constraint(rule= RM_CostBalance_4_rule)
        
        
        
        self.OpexEquation = Constraint(rule=Opex_1_rule)
        
        
        
        

        # Profits
        # --------
        
        def Profit_1_rule(self,u):
            return self.PROFITS[u] == sum(self.FLOW_IN[u,i] for i in self.I) * self.ProductPrice[u]
        
        def Profit_2_rule(self):
            return self.PROFITS_TOT == sum(self.PROFITS[u] for u in self.U_PP) * self.H
        
        self.ProfitEquation_1 = Constraint(self.U_PP, rule= Profit_1_rule)
        self.ProfitEquation_2 = Constraint(rule= Profit_2_rule)
        
        
        
        # Complete costs
        # --------------
        
        def TAC_1_rule(self):
            return self.TAC == self.CAPEX + self.OPEX - self.PROFITS_TOT
        
        
        self.TAC_Equation = Constraint(rule=TAC_1_rule)
        
        



    
    # **** ENVIRONMENTAL BALANCES *****
    # -------------------------    
        
    def create_EnvironmentalEvaluation(self):
        
        # Parameter
        self.em_fac_ut = Param(self.UT, initialize=0)
        self.em_fac_comp = Param(self.I, initialize=0)
        self.LT = Param(self.U, initialize=1)
        
        # NEW
        self.em_fac_prod = Param(self.U_PP, initialize=0)
        self.em_fac_unit = Param(self.U_C, initialize=0)
        self.GWP_UNITS = Var(self.U_C)
        self.GWP_CREDITS = Var(self.U_PP)
        self.GWP_CAPTURE = Var(self.U)
        
        def GWP_6_rule(self,u):
            return self.GWP_UNITS[u] == self.em_fac_unit[u] / self.LT[u] * self.Y[u]
        
        def GWP_7_rule(self,u):
            return self.GWP_CREDITS[u] == self.em_fac_prod[u] \
                * sum(self.FLOW_IN[u,i] for i in self.I) * self.H
        
        def GWP_8_rule(self,u):
            return self.GWP_CAPTURE[u] == sum(self.FLOW_ADD_TOT[u,i] \
                                              * self.em_fac_comp[i] for i in self.I) * self.H
    
        self.EnvironmentalEquation6 = Constraint(self.U_C, rule=GWP_6_rule)
        self.EnvironmentalEquation7 = Constraint(self.U_PP, rule=GWP_7_rule)
        self.EnvironmentalEquation8 = Constraint(self.U, rule=GWP_8_rule)
        
    
        # Variables
        self.GWP_U = Var(self.U)
        self.GWP_UT = Var(self.UT)
        self.GWP_TOT =Var()
        
        
        # Constraints
        
        def GWP_1_rule(self,u):
            return self.GWP_U[u] == self.H \
                * sum(self.FLOW_WASTE[u,i] * self.em_fac_comp[i] for i in self.I)

        def GWP_2_rule(self):
            return self.GWP_UT['Electricity'] == self.H * self.ENERGY_DEMAND_EL_TOT \
                * self.em_fac_ut['Electricity'] \
                
        
        def GWP_3_rule(self):
            return self.GWP_UT['Heat'] == self.H * self.em_fac_ut['Heat'] \
                * sum(self.ENERGY_DEMAND_HEAT_DEFI[hi] for hi in self.HI)  \
                    - self.H * self.ENERGY_DEMAND_HEAT_PROD_SELL * self.em_fac_ut['Heat'] 
        
        def GWP_4_rule(self):
            return self.GWP_TOT == sum(self.GWP_U[u] for u in self.U_C)   \
                + sum(self.GWP_UT[ut] for ut in self.UT) - sum(self.GWP_CAPTURE[u] for u in self.U) \
                    - sum(self.GWP_CREDITS[u] for u in self.U_PP) + sum(self.GWP_UNITS[u] for u in self.U_C)
 
        
        def GWP_5_rule(self):
            return self.GWP_UT['Heat2'] == 0
        
        self.EnvironmentalEquation1 = Constraint(self.U, rule = GWP_1_rule)
        self.EnvironmentalEquation2 = Constraint(rule = GWP_2_rule)  
        self.EnvironmentalEquation3 = Constraint(rule = GWP_3_rule)
        self.EnvironmentalEquation4 = Constraint(rule = GWP_4_rule)
        self.EnvironmentalEquation5 = Constraint(rule = GWP_5_rule)
        
    # **** DECISION MAKING EQUATIONS *****
    # -------------------------

        
    def create_DecisionMaking(self):
        
        # Parameter
        
        
        # Variables

        
        # Constraints
        
        def TestRule(self):
            return self.Y[8000] == 1
        
        def TestRule2(self):
            return self.Y[4100] +self.Y[4200] == 1
        
        def TestRule3(self):
            return self.Y[1310] == self.Y[1320]
        
        def TestRule4(self):
            return self.FLOW_WASTE[2100,'H2'] + self.FLOW_WASTE[2200,'H2'] + self.FLOW_WASTE[2300,'H2'] \
                + self.FLOW_WASTE[2400,'H2'] + self.FLOW_WASTE[2500,'H2']== 0 
        
        def TestRule5(self):
            return self.ENERGY_DEMAND_HEAT_PROD_USE == 0
        
        
        def TestRule6(self):
            return self.TAC <= 176000000 

        def Test7(self):
            return self.Y[2300] == 0
        
        
        # self.TestCon1 = Constraint(rule=TestRule)
        # self.TestCon2 = Constraint(rule=TestRule2)
        # self.TestCon3 = Constraint(rule=TestRule3)
        self.TestCon4 = Constraint(rule=TestRule4)
        # self.TestCon5 = Constraint(rule=TestRule6)
        # self.TestCon6 = Constraint(self.HI, rule=TestRule6)
        # self.TestCon7 = Constraint(rule=Test7)  
     
        
        
    # **** OBJECTIVE FUNCTIONS *****
    # -------------------------      

    def create_ObjectiveFunction(self):
        
        # Parameter
        
        
        # Variables
        
        self.MainProductFlow = Var()
        
        
        # Constraints
        

        
        
        # Definition of Main Product and Product Load for NPC / NPE Calculation

        if self.SS.MainProduct != None:
            
            for x in self.SS.UnitsList:
                if x.Type == 'ProductPool':
                    if x.ProductType == 'MainProduct':
                        Number_Temp = x.Number 
                        
                        def MainProduct_1_rule(self):
                            return self.MainProductFlow == \
                                sum(self.FLOW_IN[Number_Temp,i] for i in self.I) * self.H
                        
                        def MainProduct_2_rule(self):
                            return self.MainProductFlow == self.SS.ProductLoad

            
        self.MainProduct_Equation_1 = Constraint(rule=MainProduct_1_rule)
        self.MainProduct_Equation_2 = Constraint(rule=MainProduct_2_rule)        
        




        # Definition of the used Objective Function
        # -----------------------------------------
        
        if self.SS.Objective == 'NPC':
            
            def Objective_rule(self):
                return self.TAC
            
        elif self.SS.Objective  == 'NPE':
            
            def Objective_rule(self):
                return self.GWP_TOT
            
        else:
            
            def Objective_rule(self):
                return self.TAC        
    
        self.Objective = Objective(rule=Objective_rule, sense=minimize)
        
      


