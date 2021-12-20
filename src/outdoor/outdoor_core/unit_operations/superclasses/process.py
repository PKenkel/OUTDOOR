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
        self.Connections = dict()
        
        
        
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
        
        
        if self.Group is not None:
            try:
                superstructure.groups[self.Group].append(self.Number)
            except:
                superstructure.groups[self.Group] = [self.Number]
                
        if self.Connections:
            superstructure.connections[self.Number] = dict()
            for i,j in self.Connections.items():
                superstructure.connections[self.Number][i] = j


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


    def set_connections(self, units_dict):
        self.Connections = units_dict
        



    
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

    



