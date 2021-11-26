import time
from ..model.optimization_model import SuperstructureModel


from .optimizers import solve_singleRun
from .optimizers import solve_sensitivityRun
from .optimizers import solve_multiObjectiveRun
from .optimizers import solve_crossParameterRun

from .instance_processor import create_initialInstance

from ..utils.var_parameters import calculate_sensitiveParameters
from ..utils.var_parameters import prepare_mutableParameters



def solve_OptimizationProblem(
    Superstructure,
    OptimizationMode="single",
    SolverName="gurobi",
    SolverInterface="local",
):

    """

    Parameters
    ----------
    Superstructre : Superstructure Object
        Holds the Superstructure Object that is to be solved
        
    OptimizationMode: String: 'single', 'sensitivity', 'multi-criteria', 'cross-parameter'
        Defines which optimization will be carried out. Default is "single"
        
        SINGLE: Single criterion optimization for the set-up defined in 
                the superstructure object.
        SENSITIVITY: Single criterion optimization with the set-up defined 
                    in the superstructe object, 
                    parameters which are defined as sensitivity 
                    paramteres are varied.
        MULTI-CRITERIA: Multi-criteria optimization with given parameter 
                        set for defined criteria.
        CROSS-PARAMETER: A cross parameters sensitivity run, where two parameters
                        have to be declared as sensitive parameters.
                        An optimization for all combinations of these two parameters
                        is performend and returned.
                        
        
    SolverName : String
        Holds the Name of the solver. Solvers have to be installed or 
        executable has to be available.
        Solvers that are supported are: Cbc, Gurobi, Scip, Couenne, Bonmin.
        Default is "gurobi"
        
    SolverInterface: String: 'local', 'remote', 'executable'
        Defines the connection of solver and computer. 
        LOCA: Solver is installed on the machine
        REMOTE: SolverFactory of Neos solver is used. (Momentarily not working)
        EXECUTABLE: Executabl-file of solver (e.g. scip, couenne) is saved 
                    in /src/outdoor/solver_executables
        
        Default is "local"


    Returns
    -------
    results : Optimized Desing Object and Info-File
        Gives back the Optimized Desing object holding the data 
        of the Single/Multi run designs as python dictionaries.

    """

    # -- START OPTIMIZATION ALGORITHM --
    # ----------------------------------
    start_time = time.time()
    ModelInformation = dict()

    # -- CREATING THE DATA FILE FROM THE SUPERSTRUCTURE OBJECT --
    # -----------------------------------------------------------
    print("-- Creating DataFile from Superstructure --")
    Model_Data = Superstructure.create_DataFile()
    end_time = time.time()
    run_time = end_time - start_time
    total_time = run_time
    print("-- DataFile created, calculation time: ", run_time, " seconds  --")

    # -- WRITING THE MODEL EQUATION AS PYOMO ABSTRACT MODEL --
    # --------------------------------------------------------
    start_time = time.time()
    print("-- Creating Model --")
    S_Model = SuperstructureModel(Superstructure)
    S_Model.create_ModelEquations()
    end_time = time.time()
    run_time = end_time - start_time

    total_time = total_time + run_time
    print("-- Model equations written, calculation time: ", run_time, " seconds --")
    print("")

    # -- PERFORMING OPTIMIZATION BASED ON SINGLE/SENSI CHOICE --
    # ----------------------------------------------------------
    print("-- Start global optimization -- ")
    start_time_go = time.time()

    if OptimizationMode == "single":

        # -- SINGLE OPTIMIZATION, CREATE AN INSTANCE, SOLVE THE INSTANCE --
        # -----------------------------------------------------------------
        print("-- Single optimization Run -- ")
        ModelInstance = create_initialInstance(S_Model, Model_Data)

        results = solve_singleRun(ModelInstance, SolverName, SolverInterface)

        end_time_go = time.time()
        run_time_go = end_time_go - start_time_go
        total_time = total_time + run_time_go
        print(
            "-- Single run optimization finished, optimization time: ",
            run_time_go,
            " seconds --",
        )
        print("")
        print("-- Total case study run time: ", total_time, " seconds --")


    elif OptimizationMode == "sensitivity":

        # -- VARIATION OPTIMIZATION, PREPARE PARAMETERS, SOLVE VARIATION --
        # -----------------------------------------------------------------

        print("--- Sensitivity optimization Run ---")
        prepare_mutableParameters(S_Model, Superstructure)
        variations_parameters = calculate_sensitiveParameters(Superstructure)
        ModelInstance = create_initialInstance(S_Model, Model_Data)

        results = solve_sensitivityRun(
            ModelInstance,
            SolverName,
            SolverInterface,
            variations_parameters,
            Superstructure,
        )

        end_time_go = time.time()
        run_time_go = end_time_go - start_time_go
        total_time = total_time + run_time_go

        print(
            " -- Sensitivity analysis optimizaton finished, optimization time: ",
            run_time_go,
            " seconds --",
        )
        results.fill_information(total_time)
        print("")
        print("-- Total case study run time: ", total_time, " seconds --")


    elif OptimizationMode == "multi-objective":

        # -- MULTI-OBJECTIVE RUN, CREATE AN INSTANCE, SOLVE MULTIPLE CRITERIA -
        # -----------------------------------------------------------------
        print("-- Multi-objective optimization run -- ")
        ModelInstance = create_initialInstance(S_Model, Model_Data)
        MultiObjectives = Superstructure.Objectives

        results = solve_multiObjectiveRun(
            ModelInstance, SolverName, SolverInterface, MultiObjectives
        )

        end_time_go = time.time()
        run_time_go = end_time_go - start_time_go
        total_time = total_time + run_time_go
        print(
            "-- Multi-criteria run finished, optimization time: ",
            run_time_go,
            " seconds --",
        )
        
        results.fill_information(total_time)
        
        
        print("")
        print("-- Total case study run time: ", total_time, " seconds --")


    elif OptimizationMode == 'cross-parameter':
        
        # -- CROSS-PARAMETER SENSITIVITY RUN, PREPARE PARAMTERS, SOLVE VARIATIONS -
        # -----------------------------------------------------------------
        print("-- Cross-parameter sensitivity run-- ")
        prepare_mutableParameters(S_Model, Superstructure)
        cross_parameters = calculate_sensitiveParameters(Superstructure)
        ModelInstance = create_initialInstance(S_Model, Model_Data)
        
        results = solve_crossParameterRun(
            ModelInstance,
            SolverName,
            SolverInterface,
            cross_parameters,
            Superstructure)
        
        
        end_time_go = time.time()
        run_time_go = end_time_go - start_time_go
        total_time = total_time + run_time_go
        
        print(
            "-- Cross-parameter sensitivity run finished, optimization time: ",
            run_time_go,
            " seconds --",
        )
        
        results.fill_information(total_time)

        print("")
        print("-- Total case study run time: ", total_time, " seconds --")        
        
        
        

    else:
        print('Optimization mode not defined')
        pass
    
    
    return (results,total_time)
    
