# https://github.com/sumneko/lua-language-server/wiki/Annotations
from typing import Generator
from drtypehints.lua_types import LuaFunction, LuaClass


def get_alias_text(alias_dict: dict) -> Generator[str, None, None]:
    for key, value in alias_dict.items():
        yield f'---@alias {key} {value}'
        
def get_class_text(lua_class: LuaClass) -> Generator[str, None, None]:
    yield f'---@class {lua_class["name"]}'
    
    for property in lua_class["properties"]:
        property_text = f'---@field {property["name"]} {property["type"]}'
        yield property_text
    
    for function in lua_class['functions']:
        fun_text = f"---@field {function['name']} "
        
        fun_text += "fun("
        SEP = ', '
        for field in function['fields']:
            fun_text += f'{field["name"]}: {field["type"]}'
            fun_text += SEP
        if fun_text.endswith(SEP):
            fun_text = fun_text[:-len(SEP)]
        fun_text += ')'
        
        fun_text += f': {function["return_type"]}'
        fun_text += ' '
        fun_text += f'{function["description"]}'
        yield fun_text