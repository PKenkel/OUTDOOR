import math 

from ..superclasses.virtual_process import VirtualProcess



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
        self.decimal_numbers = {'Decimal_numbers': {}}
        self.decimal_set = []
        self.decimal_place = self.set_decimalPlace(Decimal_place)
        self.targets = []
        
        
        
    def set_targets(self, targets_list): 
        self.targets = targets_list

    def set_decimalPlace (self, decimal_place):
        self.decimal_place = decimal_place
        self.calc_decimalNumbers()
        
            
        
        
    def calc_decimalNumbers(self):
        X = [1, 2 ,3 ,4 ,8]
        XO = 0        
        self.decimal_numbers['Decimal_numbers'][self.Number,0] = XO
        self.decimal_set.append((self.Number,0))
        
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
        superstructure.decimal_set['DC_SET'].extend(self.decimal_set)
        
            
        for i in self.targets:
            combi = (self.Number,i) 
            
            if i not in superstructure.distributor_subset['U_DIST_SUB']:
                superstructure.distributor_subset['U_DIST_SUB'].append(combi)


    def fill_parameterList(self):
        

        super().fill_parameterList()
        
        self.ParameterList.append(self.decimal_numbers)
        
            



