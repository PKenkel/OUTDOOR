__version__ = '0.0.0'

from .outdoor_core.OUTDOOR import solve_OptimizationProblem

from .outdoor_core.Block_Results import displayBasicResults
from .outdoor_core.Block_Results import displayHeatBalanceResults
from .outdoor_core.Block_DataSaving import Save_CaseStudy

from .excel_wrapper.ExcelWrapper import get_DataFromExcel
