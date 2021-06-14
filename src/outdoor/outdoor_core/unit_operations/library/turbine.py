import math 

from .stoich_reactor import StoichReactor

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
        
        
        