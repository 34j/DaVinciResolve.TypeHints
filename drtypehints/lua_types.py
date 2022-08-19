from typing import Iterable, TypedDict

class LuaFunctionField(TypedDict):
    name: str
    type: str

class LuaProperty(TypedDict):
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
    properties: Iterable[LuaProperty]
    description: str

def join_alias(items: Iterable[str]) -> str:
    return '"' + '"|"'.join(items) + '"'