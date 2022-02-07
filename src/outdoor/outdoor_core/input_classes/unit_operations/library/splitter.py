import math 

from ..superclasses.physical_process import PhysicalProcess




class Splitter(PhysicalProcess):
    
    def __init__(self, Name, UnitNumber, Parent = None, *args, **kwargs):
        
        super().__init__(Name, UnitNumber,Parent)
        
        self.Type = "Splitter"
        
    def fill_unitOperationsList(self, superstructure):
        
        super().fill_unitOperationsList(superstructure)
        superstructure.SplitterNumberList['U_SPLITTER'].append(self.Number)
        
        
    