# DaVinciResolve.TypeHints

Python project that generates lua type hints based on the most popular Lua Language Server [lua-language-server](https://marketplace.visualstudio.com/items?itemName=sumneko.lua).

## Sample

Sample is here. [typeHints.lua](https://github.com/34j/DaVinciResolve.TypeHints/blob/master/typeHints.lua)

## Coverage

- [x] `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt`
- [x] `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Workflow Integrations\README.txt`
- [ ] `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Fusion Fuse\Fusion Fuse Manual.pdf`
- [ ] Unorganized part of above references
- [ ] Discoverable properties / methods / registry attributes using `app:GetHelpRaw('ClassName')`
- [ ] Other not documented / undiscoverble properties / methods / registry attributes

## Requirements

Installation of DaVinci Resolve is required. The project is by default for Windows only due to an issue with the file path of the references, but if you edit the script, it should work well on other operating systems.

## Usage

Just copy `typeHints.lua` to your DaVinci Resolve Scripting folder. **`typeHints.lua` must be created by yourself due to copyright reasons.** Actually, it can be generated simply by copying and pasting the command below into a command prompt.

```shell
mkdir DaVinciResolve.TypeHints
cd DaVinciResolve.TypeHints
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install git+https://github.com/34j/DaVinciResolve.TypeHints.git
drtypehints
```

OR

```shell
git clone https://github.com/34j/DaVinciResolve.TypeHints.git
cd ./drtypehints
py -m venv venv
"./venv/Scripts/Activate.bat"
pip install -r requirements.txt
python -m drtypehints
```

## Alternatives

- [pedrolabonia/pydavinci: A python package that helps you script DaVinci Resolve](https://github.com/pedrolabonia/pydavinci)
    Python Wrapper for DaVinci Resolve Python apis (Properties and Methods are in snake_case)

As for Lua, no alternatives was found.

## Development

- [regex101: build, test, and debug regex](https://regex101.com/)
- [Annotations · sumneko/lua\-language\-server Wiki](https://github.com/sumneko/lua-language-server/wiki/Annotations)

## Contribution

Pull requests are welcome.
