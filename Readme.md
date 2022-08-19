# DaVinciResolve.TypeHints

Python project that generates lua type hints based on the most popular Lua Language Server [lua-language-server](https://marketplace.visualstudio.com/items?itemName=sumneko.lua).

## Sample

Sample is here. [typeHints.lua](https://github.com/34j/DaVinciResolve.TypeHints/blob/master/typeHints.lua)

## Coverage

- [x] `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt`
- [x] `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Workflow Integrations\README.txt`

## Usage

Just copy `typeHints.lua` to your DaVinci Resolve Scripting folder. **`typeHints.lua` must be created by yourself due to copyright reasons.**

```shell
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

## Development

- [regex101: build, test, and debug regex](https://regex101.com/)
- [Annotations · sumneko/lua\-language\-server Wiki](https://github.com/sumneko/lua-language-server/wiki/Annotations)

## Contribution

Pull requests are welcome.
