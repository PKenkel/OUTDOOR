import sys
import os

a = os.path.dirname(__file__)
a = os.path.dirname(a)


b= a + '/src'
sys.path.append(b)


'testfeature'

import outdoor

Excel_Path = "Test_Excel.xlsm"

Results_Path = a + '/examples/results'

ts = outdoor.get_DataFromExcel(Excel_Path)

(Opt,Info) = outdoor.solve_OptimizationProblem(ts, 'cplex')


outdoor.Save_CaseStudy(Opt, Info, Results_Path)

outdoor.displayHeatBalanceResults(Opt,Info)
outdoor.displayBasicResults(Opt)

