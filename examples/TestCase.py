import sys
import os

a = os.path.dirname(__file__)
a = os.path.dirname(a)


b= a + '/src'
sys.path.append(b)


'testneu'

import outdoor

Excel_Path = "Test_Excel.xlsm"

Results_Path = os.path.dirname(a) + '/outdoor_examples/results/'

Data_Path =os.path.dirname(a) + '/outdoor_examples/data/'

ts = outdoor.get_DataFromExcel(Excel_Path)

(Opt,Info) = outdoor.solve_OptimizationProblem(ts, 'gurobi', 'local')


outdoor.Save_CaseStudy(Opt, Info, Results_Path)

outdoor.displayHeatBalanceResults(Opt,Info)
outdoor.displayBasicResults(Opt)

outdoor.save_dict_to_file(Data_Path, Info)