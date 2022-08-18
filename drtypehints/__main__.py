from io import TextIOWrapper
from typing import Iterable
from drtypehints.parse_scripting import get_classes,get_alias, get_predefined_typings
from drtypehints.generate_lua_text import get_alias_text, get_class_text
import click
from pathlib import Path

def writelines(file: TextIOWrapper, lines: Iterable[str]) -> None:
    for line in lines:
        file.write(line + '\n')

@click.command
@click.option('--out', 'out_path', type=click.Path(exists=False), default='typeHints.lua')
def generate_file(out_path: str) -> None:
    alias = get_alias()
    classes = get_classes()
    with Path(out_path).open('w') as file:
        file.write('-- This file is auto-generated by davinci-resolve-type-hints\n')
        file.write('-- Just copy this file to your DaVinci Resolve Scripting folder\n\n\n')
        file.write(get_predefined_typings() + "\n\n")
        
        file.write('-- alias\n\n')
        writelines(file, get_alias_text(alias))
        
        file.write('\n\n')
        
        file.write('-- classes\n\n')
        for lua_class in classes:
            writelines(file, get_class_text(lua_class))            
            file.write('\n')

generate_file()