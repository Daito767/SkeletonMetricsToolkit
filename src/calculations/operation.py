# -*- coding: utf-8 -*-
"""
Created on May 2024

@author: Ghimciuc Ioan
"""

import inspect
import logging
import importlib
from types import FunctionType


class Operation:
    def __init__(self, function: FunctionType, result_name: str, inputs_name: list[str]):
        self.function: FunctionType = function
        self.result_name: str = result_name
        self.inputs_name: list[str] = inputs_name

        self.name: str = function.__name__
        self.description: str = function.__doc__
        self.function_params: list[str] = inspect.getfullargspec(function).args

        self.errors: list[str] = list()

    def execute(self, storage: dict[str, any]) -> bool:
        try:
            kwargs = {param: storage[input_name] for param, input_name in zip(self.function_params, self.inputs_name)}
            storage[self.result_name] = self.function(**kwargs)
            return True
        except KeyError as e:
            self.errors.append(f"Missing parameter in storage: {e}")
        except Exception as e:
            self.errors.append(str(e))
        return False

    def __str__(self):
        return f"{self.name}({', '.join(self.function_params)})"


class OperationManager:
    def __init__(self, logger: logging.Logger):
        self.logger: logging.Logger = logger
        self.logger.info("Initializing OperationManager")

        self.functions_module = importlib.import_module('calculations.vector_operations')
        self.available_functions: dict[str, FunctionType] = self.get_available_operations()
        self._operations: list[Operation] = []
        self.storage: dict[str, any] = {}

    def get_available_operations(self) -> dict[str, FunctionType]:
        functions: dict[str, FunctionType] = {}
        for name, func in inspect.getmembers(self.functions_module, inspect.isfunction):
            functions[name] = func

        self.logger.info("Available operations loaded.")
        return functions

    def add_operation(self, operation: Operation) -> None:
        self._operations.append(operation)
        self.logger.info(f"Operation added: {operation}")

    def add_and_run_operation(self, operation: Operation) -> None:
        self._operations.append(operation)
        self.logger.info(f"Operation added: {operation}")

        self.logger.info(f"Executing operation: {operation}")
        operation.errors.clear()
        success = operation.execute(self.storage)
        if success:
            self.logger.info(f"Operation successful: {operation}")
        else:
            self.logger.error(f"Operation failed: {operation}. Errors: {operation.errors}")

    def remove_operation(self, operation: Operation) -> None:
        if operation in self._operations:
            self._operations.remove(operation)
            self.logger.info(f"Operation removed: {operation}")
        else:
            self.logger.warning(f"Attempted to remove operation that does not exist: {operation}")

    def run_operations(self) -> None:
        for operation in self._operations:
            self.logger.info(f"Executing operation: {operation}")
            operation.errors.clear()
            success = operation.execute(self.storage)
            if success:
                self.logger.info(f"Operation successful: {operation}")
            else:
                self.logger.error(f"Operation failed: {operation}. Errors: {operation.errors}")


if __name__ == "__main__":  # Example usage of the OperationManager with logging
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize the OperationManager with the logger
    manager = OperationManager(logger)

    # Example operations (assuming 'vector_add' and 'vector_subtract' exist in 'calculations.vector_operations')
    add_operation = Operation(manager.available_functions['vector_add'], 'result_add', ['vector1', 'vector2'])
    subtract_operation = Operation(manager.available_functions['vector_subtract'], 'result_subtract', ['vector1', 'vector2'])

    # Add operations to the manager
    manager.add_operation(add_operation)
    manager.add_operation(subtract_operation)

    manager._operations.clear()

    # Example storage data
    manager.storage['vector1'] = [1, 2, 3]
    manager.storage['vector2'] = [4, 5, 6]

    # Run operations
    manager.run_operations()

    # Print results from storage
    print(manager.storage)
