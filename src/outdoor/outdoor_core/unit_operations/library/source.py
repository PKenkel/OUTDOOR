import math 

from ..superclasses.virtual_process import VirtualProcess

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
   
        
   
