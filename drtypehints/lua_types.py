from typing import Iterable, TypedDict

class LuaFunctionField(TypedDict):
    name: str
    type: str

class LuaFunction(TypedDict):
    name: str
    fields: Iterable[LuaFunctionField]
    return_type: str
    description: str


class LuaClass(TypedDict):
    name: str
    functions: Iterable[LuaFunction]
    description: str
