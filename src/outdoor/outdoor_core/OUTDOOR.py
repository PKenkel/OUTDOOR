from pyomo.environ import *

from .Block_SuperstructureModel import SuperstructureModel

import time


def solve_OptimizationProblem(Superstructure, SolverName, SolverInterface = 'local'):
    """

    Parameters
    ----------
    Superstructre : Superstructure Object
        Holds the Superstructure Object that is to be solved
        
    SolverName : String
        Holds the Name of the solver 

    Returns
    -------
    results : Pyomo ModelInstance
        Gives back the Model Instance after Optimization

    """
    
    ModelInformation = dict()
    
    
    print('-Creating DataFile from Superstructure--')
    Model_Data = Superstructure.create_DataFile()   
    print('--Creating Model and Model instance--')
    S_Model = SuperstructureModel(Superstructure)  
    S_Model.create_ModelEquations()
    
    
    start_time = time.time()
    ModelInstance = S_Model.populateModel(Model_Data)
    print('-----Starting optimization----')
    
    if SolverInterface == 'local':
        try:
            if SolverName == 'gurobi':
                solver = SolverFactory(SolverName, solver_io = 'python')
                results = solver.solve(ModelInstance, tee =True)
            else:
                solver = SolverFactory(SolverName)
                results = solver.solve(ModelInstance, tee =True)
        except:
            print('Solver Name is not correct or solver not installaed')
    else:
        try:
            results =  SolverManagerFactory('neos').solve(ModelInstance,opt=SolverName,tee=True)
        except:
            print('Solver not on neos server, or input wrong')
    
        
    end_time = time.time()
    run_time = end_time - start_time
    
    
    ModelInformation['Solver'] = SolverName
    ModelInformation['Run Time'] = run_time
    ModelInformation['Data File'] = Model_Data
    ModelInformation['Superstructure']  = Superstructure
    
    print('-----------')
    print('Optimization run time is')
    print(run_time)
    print('-----------')

    return (ModelInstance, ModelInformation)


    

