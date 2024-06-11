import importlib
import inspect
from types import FunctionType

import numpy as np


class Operation:
    def __init__(self, function: FunctionType, result_name, inputs_name: list):
        self.function: FunctionType = function
        self.result_name: str = result_name
        self.inputs_name: list[str] = inputs_name

        self.name: str = function.__name__
        self.description: str = function.__doc__
        self.function_params: list[str] = inspect.getfullargspec(function).args

        self.errors: list[str] = list()

    def execute(self, storage: dict[str, any]) -> None:
        try:
            # Creează un dicționar de argumente pe baza inputs_name și function_params
            kwargs = {param: storage[input_name] for param, input_name in zip(self.function_params, self.inputs_name)}

            # Apelează funcția cu argumentele extrase și stochează rezultatul
            storage[self.result_name] = self.function(**kwargs)
        except KeyError as e:
            self.errors.append(f"Missing parameter in storage: {e}")
        except Exception as e:
            self.errors.append(str(e))

    def __str__(self):
        return f"{self.name}({', '.join(self.function_params)})"


class OperationManager:
    def __init__(self):
        self.functions_module = importlib.import_module('calculations.vector_operations')
        self.available_functions: dict[str, FunctionType] = self.get_available_operations()
        self.operations: list[Operation] = []
        self.storage: dict[str, any] = {}

    def get_available_operations(self) -> dict[str, FunctionType]:
        functions: dict[str, FunctionType] = {}
        for name, func in inspect.getmembers(self.functions_module, inspect.isfunction):
            functions[name] = func

        return functions

    def run_operations(self):
        for operation in self.operations:
            operation.execute(self.storage)

