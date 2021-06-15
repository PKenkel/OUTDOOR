
from .model.optimization_model import SuperstructureModel
from .utils.instance_initializer import prepare_initialInstance
from .utils.single_runs import solve_singleRun
from .utils.multi_runs import solve_MultiRun


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

    
    (ModelInformation, ModelInstance, Model_Data) = prepare_initialInstance(Superstructure,
                                                                            SuperstructureModel)
    
    if OptimizationMode == 'single':
        (instance, info) = solve_singleRun(ModelInstance, 
                                           ModelInformation, 
                                           Model_Data, 
                                           SolverName, 
                                           SolverInterface,
                                           Superstructure)
        return (instance,info)
    
    elif OptimizationMode == 'sensitivity':
        pass
    else:
        pass
    
    



