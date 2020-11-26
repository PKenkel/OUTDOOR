import sys
import os

a = os.path.dirname(__file__)
a = os.path.dirname(a)
a = a + '/src'
sys.path.append(a)

import outdoor

Excel_Path = "Test_Excel.xlsm"

Results_Path = "/Users/philippkenkel/Desktop/RESULTS_NEW/"

ts = outdoor.get_DataFromExcel(Excel_Path)

(Opt,Info) = outdoor.solve_OptimizationProblem(ts, 'gurobi')


outdoor.Save_CaseStudy(Opt, Info, Results_Path)

outdoor.displayHeatBalanceResults(Opt,Info)
outdoor.displayBasicResults(Opt)

