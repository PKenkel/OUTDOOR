from pyomo.environ import *

from .model.optimization_model import SuperstructureModel

import time



def solve_OptimizationProblem(Superstructure, 
                              OptimizationMode = 'single',
                              SolverName  = 'gurobi',
                              SolverInterface = 'local'):
    
    
    # optimization_mode_dict = {
    #     'single': 's'}
    
    
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
    start_time = time.time()
    
    ModelInformation = dict()
    
    
    print('-Creating DataFile from Superstructure--')
    Model_Data = Superstructure.create_DataFile()   
    print('--Creating Model and Model instance--')
    S_Model = SuperstructureModel(Superstructure)  
    S_Model.create_ModelEquations()
    
    
    
    ModelInstance = S_Model.populateModel(Model_Data)    
    end_time = time.time()
    print('Population time was')
    print(end_time-start_time)
    
    
    if OptimizationMode == 'single':
    
        (instance,info) = solve_singleRun(ModelInstance, 
                                          ModelInformation,
                                          Model_Data,
                                          SolverName,
                                          SolverInterface,
                                          Superstructure)
    
        return (instance,info)
    
    else:
        pass

    


def solve_singleRun(ModelInstance, 
                    ModelInformation, 
                    Model_Data, 
                    SolverName, 
                    SolverInterface,
                    Superstructure):
    
    start_time = time.time()
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
            print('Solver Name is not correct or solver not installed')
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



def solve_MultiRun(Superstructure, 
                   SensitivityParamaters,
                   SolverName = 'gurobi', 
                   SolverInterface  = 'local'):

    """
    Sensitivity Parameters =
    - Electricity Price
    - 
    """

    st = time.time()
    
    
    Sensi_Param = FUNCTION_PARAM(SensitivityParamaters)
    
    ModelInformation = dict()
    
    print('Creating Initial DataFile from Superstructure')
    Model_Data = Superstructure.create_DataFile()
    print('Creating Model and initial model instance')
    S_Model = SuperstructureModel(Superstructure)
    S_Model.create_ModelEquations()
    ModelInstance = S_Model.populateModel(Model_Data)
    
    # for

# def solve_OptimizationProblem(Superstructure, SolverName, SolverInterface = 'local'):
#     """

#     Parameters
#     ----------
#     Superstructre : Superstructure Object
#         Holds the Superstructure Object that is to be solved
        
#     SolverName : String
#         Holds the Name of the solver 

#     Returns
#     -------
#     results : Pyomo ModelInstance
#         Gives back the Model Instance after Optimization

#     """
#     st = time.time()
    
#     ModelInformation = dict()
    
    
#     print('-Creating DataFile from Superstructure--')
#     Model_Data = Superstructure.create_DataFile()   
#     print('--Creating Model and Model instance--')
#     S_Model = SuperstructureModel(Superstructure)  
#     S_Model.create_ModelEquations()
    
    
    
#     ModelInstance = S_Model.populateModel(Model_Data)
#     print('-----Starting optimization----')
#     et = time.time()
#     tt = et -st 
#     print('Population time was ')
#     print(tt)
#     print('-----')
    
#     start_time = time.time()
#     if SolverInterface == 'local':
#         try:
#             if SolverName == 'gurobi':
#                 solver = SolverFactory(SolverName, solver_io = 'python')
#                 results = solver.solve(ModelInstance, tee =True)
#             else:
#                 solver = SolverFactory(SolverName)
#                 results = solver.solve(ModelInstance, tee =True)
#         except:
#             print('Solver Name is not correct or solver not installaed')
#     else:
#         try:
#             results =  SolverManagerFactory('neos').solve(ModelInstance,opt=SolverName,tee=True)
#         except:
#             print('Solver not on neos server, or input wrong')
    
        
#     end_time = time.time()
#     run_time = end_time - start_time
    
    
#     ModelInformation['Solver'] = SolverName
#     ModelInformation['Run Time'] = run_time
#     ModelInformation['Data File'] = Model_Data
#     ModelInformation['Superstructure']  = Superstructure
    
#     print('-----------')
#     print('Optimization run time is')
#     print(run_time)
#     print('-----------')

#     return (ModelInstance, ModelInformation)



