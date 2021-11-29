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

Data_Path = os.path.dirname(a) + '/outdoor_examples/data/'

ts = outdoor.get_DataFromExcel(Excel_Path)

# (Opt,calc_time) = outdoor.solve_OptimizationProblem(ts, 'single','gurobi', 'local')

(Opt,calc_time) = outdoor.solve_OptimizationProblem(ts, 'multi-objective','gurobi', 'local')

# (Opt,Info) = outdoor.solve_OptimizationProblem(ts, 'sensitivity', 'gurobi', 'local')

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")




# ts.add_sensi_parameters('electricity_price',10,100,2)
# ts.add_sensi_parameters('heating_demand',5,20,4,('Heat',2200))
# ts.add_sensi_parameters('component_concentration',3,9,2,3000)
# ts.add_sensi_parameters('capital_costs',1,4,2,2200)


