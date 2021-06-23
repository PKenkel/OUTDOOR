import sys
import os
from pyomo.environ import *

import tracemalloc
tracemalloc.start()


a = os.path.dirname(__file__)
a = os.path.dirname(a)


b = a + '/src'
sys.path.append(b)


import outdoor 

Excel_Path = "Test_Excel.xlsm"

Results_Path = os.path.dirname(a) + '/outdoor_examples/results/'

Data_Path =os.path.dirname(a) + '/outdoor_examples/data/'

ts = outdoor.get_DataFromExcel(Excel_Path)

# ts.add_sensi_parameters('electricity_price',10,100,2)
# ts.add_sensi_parameters('heating_demand',5,20,4,('Heat',2200))
# ts.add_sensi_parameters('component_concentration',3,9,2,3000)
# ts.add_sensi_parameters('capital_costs',1,4,2,2200)

# (Opt,Info) = outdoor.solve_OptimizationProblem(ts, 'sensitivity', 'gurobi', 'local')
(Opt2,Info) = outdoor.solve_OptimizationProblem(ts, 'single', 'gurobi', 'local')


outdoor.save_caseStudy(Opt2,
                       Info,
                       Results_Path)
                       

# Opt2  = Opt['capital_costs',30]


# outdoor.Save_CaseStudy(Opt2, Info, Results_Path)

# outdoor.displayHeatBalanceResults(Opt2,Info)
# outdoor.displayBasicResults(Opt2)

outdoor.save_dict_to_file(Data_Path, Info)


current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")

