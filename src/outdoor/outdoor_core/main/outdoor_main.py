import time
from ..model.optimization_model import SuperstructureModel


from .optimizers import solve_singleRun
from .optimizers import solve_multiRun

from .instance_processor import create_initialInstance

from ..utils.var_parameters import calculate_sensitiveParameters
from ..utils.var_parameters import prepare_mutableParameters




def solve_OptimizationProblem(Superstructure, 
                              OptimizationMode = 'single',
                              SolverName  = 'gurobi',
                              SolverInterface = 'local'):
    
    
    """

    Parameters
    ----------
    Superstructre : Superstructure Object
        Holds the Superstructure Object that is to be solved
        
    OptimizationMode: 'single', 'sensitivity', 'monte-carol'
        Defines which optimization will be carried out, right now only single is valid.
        
    SolverName : String
        Holds the Name of the solver 

    Returns
    -------
    results : Pyomo ModelInstance and Info-File
        Gives back the Model Instance after Optimization

    """
    
    # -- START OPTIMIZATION ALGORITHM -- 
    # ----------------------------------
    start_time = time.time()
    ModelInformation = dict()
    
    # -- CREATING THE DATA FILE FROM THE SUPERSTRUCTURE OBJECT --
    # -----------------------------------------------------------
    print('-- Creating DataFile from Superstructure --')
    Model_Data = Superstructure.create_DataFile()   
    end_time = time.time()
    run_time = end_time - start_time
    total_time = run_time
    print('-- DataFile created, calculation time: ',run_time, ' seconds  --')
    
    # -- WRITING THE MODEL EQUATION AS PYOMO ABSTRACT MODEL --
    # --------------------------------------------------------
    start_time = time.time()
    print('-- Creating Model --')
    S_Model = SuperstructureModel(Superstructure)  
    S_Model.create_ModelEquations()
    end_time = time.time()
    run_time = end_time - start_time
    
    total_time = total_time+run_time
    print('-- Model equations written, calculation time: ', run_time, ' seconds --')
    print('')
    
    
    # -- PERFORMING OPTIMIZATION BASED ON SINGLE/SENSI CHOICE --
    # ----------------------------------------------------------
    print('-- Start global optimization -- ')
    start_time = time.time()
    
    
    if OptimizationMode == 'single':
        
        # -- SINGLE OPTIMIZATION, CREATE AN INSTANCE, SOLVE THE INSTANCE --
        # -----------------------------------------------------------------
        print('-- Single optimization Run -- ')
        ModelInstance = create_initialInstance(S_Model,Model_Data)
        
        results = solve_singleRun(ModelInstance, 
                                  SolverName,
                                  SolverInterface)
        
        end_time = time.time()
        run_time = end_time - start_time
        total_time = total_time + run_time
        print('-- Single run optimization finished, optimization time: ', run_time, ' seconds --')
        print('')
        print('-- Total case study run time: ', total_time, ' seconds --')
        
        
        # -- SAVE INFORMATION ABOUT THE SINGLE RUN IN DICTIONARY --
        # ---------------------------------------------------------
        ModelInformation['Solver'] = SolverName
        ModelInformation['Run Time'] = total_time
        ModelInformation['Data File'] = Model_Data
        ModelInformation['Superstructure']  = Superstructure
    
        return (results, ModelInformation)
    
    elif OptimizationMode == 'sensitivity':
        
        # -- VARIATION OPTIMIZATION, PREPARE PARAMETERS, SOLVE VARIATION --
        # -----------------------------------------------------------------

        prepare_mutableParameters(S_Model, Superstructure)
        variations_parameters = calculate_sensitiveParameters(Superstructure)
        ModelInstance = create_initialInstance(S_Model,Model_Data) 

        results = solve_multiRun(ModelInstance,
                                 SolverName,
                                 SolverInterface,
                                 variations_parameters,
                                 Superstructure)
        
        end_time = time.time()
        run_time = end_time - start_time
        total_time = total_time + run_time
        
        print(' -- Variation run optimizaton finished, optimization time: ', run_time, ' seconds --')
        print('')
        print('-- Total case study run time: ', total_time, ' seconds --')
        
        
        # -- SAVE INFORMATION ABOUT THE VARIATION RUN IN DICTIONARY --
        # ------------------------------------------------------------
        
        ModelInformation['Solver'] = SolverName
        ModelInformation['Run Time'] = total_time
        ModelInformation['Data File'] = Model_Data
        ModelInformation['Superstructure']  = Superstructure
        ModelInformation['VariationParameters'] = variations_parameters 
        
        
        return (results,ModelInformation)
    else:
        pass
    
    
    



