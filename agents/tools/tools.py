from typing import Callable, List
from utils import Logger

TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null"
}

class ToolExecutionError(Exception):
    pass

class Parameter:
    def __init__(self, name: str, description: str, type: type, item_type: type=None, required: bool=False):
        self.name = name
        self.description = description
        self.type = type
        self.item_type = item_type
        self.required = required

class Tool:
    def __init__(self, name: str, func: Callable, description: str, arguments: List[Parameter]):
        self.name = name
        self.func = func
        self.description = description
        self.arguments = arguments
        self.log = Logger()

    def validate_arguments(self, *args, **kwargs):
        for i, arg in enumerate(args):
            if not isinstance(arg, self.arguments[i].type):
                self.log.info(f"Argument {self.arguments[i].name} ({i}): Expected {self.arguments[i].type}, got {type(arg)}")
                raise ToolExecutionError(f"Argument {self.arguments[i].name} ({i}): Expected {self.arguments[i].type}, got {type(arg)}")
        for key, value in kwargs.items():
            matching_args = [arg for arg in self.arguments if arg.name == key]
            if not matching_args:
                self.log.info(f"Unexpected argument: {key}")
                raise ToolExecutionError(f"Unexpected argument: {key}")
            arg = matching_args[0]
            if not isinstance(value, arg.type):
                self.log.info(f"Argument {arg.name}: Expected {arg.type}, got {type(value)}")
                raise ToolExecutionError(f"Argument {arg.name}: Expected {arg.type}, got {type(value)}")

    def execute(self, *args, **kwargs):
        self.log.info(f"Executing {self.name} with args: {args} and kwargs: {kwargs}")
        self.validate_arguments(*args, **kwargs)
        try:
            result = self.func(*args, **kwargs)
            self.log.info(f"Result: {result}")
        except Exception as e:
            self.log.info(f"Error executing {self.name}: {e}")
            raise ToolExecutionError(f"Error executing {self.name}: {e}")
        return result
    
    def get_schema(self) -> dict:
        schema = {
            "name": self.func.__name__,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [arg.name for arg in self.arguments if arg.required]
            }
        }
        for arg in self.arguments:
            arg_schema = {
                "type": TYPE_MAP.get(arg.type, "string"),
                "description": arg.description
            }
            if arg.type == list and arg.item_type:
                arg_schema["items"] = {"type": TYPE_MAP.get(arg.item_type, "string")}
            schema["parameters"]["properties"][arg.name] = arg_schema
        return schema