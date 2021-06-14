import math 

from .stoich_reactor import StoichReactor


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



