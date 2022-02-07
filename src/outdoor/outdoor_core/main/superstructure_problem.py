from ..model.optimization_model import SuperstructureModel


from ..optimizers.main_optimizer import SingleOptimizer

from ..optimizers.customs.custom_optimizer import (
    MCDAOptimizer,
    SensitivityOptimizer,
    TwoWaySensitivityOptimizer,
)


from ..utils.timer import time_printer
from ..optimizers.customs.change_params import prepare_mutable_parameters


class SuperstructureProblem:
    def __init__(self, parser_type="Superstructure"):

        PARSER_SET = {"Superstructure", "External"}
        if parser_type in PARSER_SET:
            self.parser = parser_type
        else:
            print(
                f"Parser type not recognized, \
                please use one of the following key words:{PARSER_SET}"
            )

    def solve_optimization_problem(
        self,
        input_data=None,
        optimization_mode="single",
        solver="gurobi",
        interface="local",
        options=None,
    ):

        solving_time = time_printer(
            programm_step="Superstructure optimization procedure"
        )
        if self.parser == "Superstructure":

            model_instance = self.setup_model_instance(input_data, optimization_mode)
            mode_options = self.set_mode_options(optimization_mode, input_data)

            optimizer = self.setup_optimizer(
                solver, interface, options, optimization_mode, mode_options, input_data
            )
            model_output = optimizer.run_optimization(model_instance)
            solving_time = time_printer(
                solving_time, "Superstructure optimization procedure"
            )
            return model_output
        else:
            print("Currently there is no routine for external data parsing implemented")
            pass

    def setup_model_instance(self, input_data, optimization_mode):
        timer = time_printer(programm_step="DataFile, Model- and ModelInstance setup")
        data_file = input_data.create_DataFile()
        model = SuperstructureModel(input_data)
        model.create_ModelEquations()

        if optimization_mode == "sensitivity" or optimization_mode == "cross-parameter sensitivity":
            mode_options = input_data.sensitive_parameters
            prepare_mutable_parameters(model, mode_options)

        model_instance = model.populateModel(data_file)
        timer = time_printer(timer, "DataFile, Model- and ModelInstance setup")

        return model_instance

    def setup_optimizer(
        self,
        solver,
        interface,
        options,
        optimization_mode,
        mode_options,
        superstructure,
    ):
        MODE_LIBRARY = {"single", "multi-objective", "sensitivity", "cross-parameter sensitivity"}

        if optimization_mode not in MODE_LIBRARY:
            print(
                f"Optimization mode is not supported, \
                please select from: {MODE_LIBRARY}"
            )

        timer = time_printer(programm_step="Optimizer setup")

        if optimization_mode == "single":
            optimizer = SingleOptimizer(solver, interface, options)
        elif optimization_mode == "multi-objective":
            optimizer = MCDAOptimizer(solver, interface, options, mode_options)
        elif optimization_mode == "sensitivity":
            optimizer = SensitivityOptimizer(
                solver, interface, options, mode_options, superstructure
            )
        elif optimization_mode == "cross-parameter sensitivity":
            optimizer = TwoWaySensitivityOptimizer(
                solver, interface, options, mode_options, superstructure
            )            
        else:
            pass

        timer = time_printer(passed_time=timer, programm_step="Optimizer setup")

        return optimizer

    def set_mode_options(self, optimization_mode, superstructure):
        if optimization_mode == "multi-objective":
            mode_options = superstructure.multi_objectives
        elif (
            optimization_mode == "sensitivity" or optimization_mode == "cross-parameter sensitivity"
        ):
            mode_options = superstructure.sensitive_parameters
        else:
            mode_options = None

        return mode_options
