import math 

from ..superclasses.physical_process import PhysicalProcess


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







