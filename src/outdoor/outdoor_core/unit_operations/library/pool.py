import math 

from ..superclasses.virtual_process import VirtualProcess

        
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
        self.fw_credits = {'fw_fac_prod': {self.Number: 0}}
        self.min_production = {'MinProduction': {self.Number: 0}}
        self.max_production = {'MaxProduction': {self.Number: 10000000}}
        
        
        
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
        
    def set_freshwaterCredits(self, freshwaterfactor):
        self.fw_credits['fw_fac_prod'][self.Number] = freshwaterfactor
        
        
            
    def set_productPrice(self, Price):
        self.ProductPrice['ProductPrice'][self.Number] = Price
        
    def set_productionLimits(self, MinProduction = 0, MaxProduction = 10000000):
        self.min_production['MinProduction'][self.Number] = MinProduction 
        self.max_production['MaxProduction'][self.Number] = MaxProduction 

    def fill_parameterList(self):
        super().fill_parameterList()
        self.ParameterList.append(self.ProductPrice)
        self.ParameterList.append(self.em_credits)
        self.ParameterList.append(self.min_production)
        self.ParameterList.append(self.max_production)
        self.ParameterList.append(self.fw_credits)
        


