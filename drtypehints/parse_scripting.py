from pathlib import Path
from typing import Optional, Iterable
import re
from drtypehints.lua_types import LuaClass, LuaFunction, LuaFunctionField

from logging import getLogger
import humps

SCRIPTING_PATH = Path(
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt"
)


def get_predefined_typings() -> str:
    text = """resolve = resolve ---@type Resolve
app = app ---@type Resolve
fusion = fusion ---@type Fusion
fu = fu ---@type Fusion\n"""
    return text


def join_alias(items: Iterable[str]) -> str:
    return '"' + '"|"'.join(items) + '"'


def get_alias():
    ALIAS = {
        "Color": "string",
        "Duration": "number",
        "CustomData": "string",
        "Item": "TimelineItem",
        "TrackType": '"video"|"audio"|"subtitle"',
        "Format": '"dpx"|"cin"|"tif"|"jpg"|"png"|"ppm"|"bmp"|"xpm"',
        "MetaDataValue": "string",
        "Note": "string",
        "Keyframe": "integer",
        "Clip": "MediaPoolItem",
        "GradeMode": join_alias({
            "1", "2", "3"
        }),
        "Timecode": "string",
        "PropertyKey": join_alias(
            [
                "Pan",
                "Tilt",
                "ZoomX",
                "ZoomY",
                "ZoomGang",
                "RotationAngle",
                "AnchorPointX",
                "AnchorPointY",
                "Pitch",
                "Yaw",
                "FlipX",
                "FlipY",
                "CropLeft",
                "CropRight",
                "CropTop",
                "CropBottom",
                "CropSoftness",
                "CropRetain",
                "DynamicZoomEase",
                "CompositeMode",
                "Opacity",
                "Distortion",
                "RetimeProcess",
                "MotionEstimation",
                "Scaling",
                "ResizeFilter",
            ]
        ),
        "Setting": join_alias(
            [
                "SelectAllFrames",
                "MarkIn",
                "MarkOut",
                "TargetDir",
                "CustomName",
                "UniqueFilenameStyle",
                "ExportVideo",
                "ExportAudio",
                "FormatWidth",
                "FormatHeight",
                "FrameRate",
                "PixelAspectRatio",
                "VideoQuality",
                "AudioCodec",
                "AudioBitDepth",
                "AudioSampleRate",
                "ColorSpaceTag",
                "GammaTag",
                "ExportAlpha",
                "EncodingProfile",
                "MultiPassEncode",
                "AlphaMode",
                "NetworkOptimization",
            ]
        ),
    }
    return ALIAS


def parse_param(param_text: str) -> str:
    param_text = param_text.split("=")[0]
    return param_text.translate(str.maketrans("", "", "[]{}."))


def parse_type(type_text: str) -> str:
    # +? is lazy, \[, \{ for escape
    list_match = re.fullmatch(r"\[(.+?),? ?s?\.*\]", type_text)
    dict_match = re.fullmatch(r"\{(.+?),? ?s?\.*\}", type_text)
    assert not (list_match and dict_match)
    if list_match or dict_match:
        prefix = "" if list_match else "{ [string]: "
        suffix = "[]" if list_match else "}"
        inner = list_match.group(1) if list_match else dict_match.group(1)
        return prefix + parse_type(inner) + suffix

    type_text = humps.pascalize(type_text)
    type_text = type_text.split("=")[0]
    type_text = type_text.translate(str.maketrans("", "", "123"))

    type_regex = {
        "Name": "string",
        "Path": "string",
        "folder": "Folder",
        "Folder": "Folder",
        "File": "string",
        "Idx": "integer",
        "Id": "integer",
        "Index": "integer",
        "Frame": "integer",
        "Duration": "number",
        "Value": "any",
        "TimelineItem": "TimelineItem",
        "Label": "string",
        "Timecode": "Timecode",
    }
    for key, value in type_regex.items():
        if key in type_text:
            type_text = value
            break

    parse_dict = {
        "Bool": "boolean",
        "String": "string",
        "Int": "integer",
        "None": "nil",
    }
    return parse_dict.get(type_text, type_text)


def parse_function(function_text: str, self_type: str) -> Optional[LuaFunction]:
    try:
        function_expression = function_text.split("-->")[0].replace(" ", "")
        name = function_expression.split("(")[0]
        arguments_raw = filter(
            lambda x: x != "",
            function_expression.split("(")[1].split(")")[0].split(","),
        )
        return_type_raw = function_text.split("-->")[1].split("#")[0].replace(" ", "")
        description = function_text.split("# ")[1]
    except:
        return None

    # parse them
    fields = [
        LuaFunctionField(name=parse_param(arg), type=parse_type(arg))
        for arg in arguments_raw
    ]
    # delete ... fields
    fields = [LuaFunctionField(name="self", type=self_type)] + list(
        filter(lambda x: x["name"] != "..." and x["type"] != "...", fields)
    )

    return_type = parse_type(return_type_raw)
    return LuaFunction(
        name=name, fields=fields, return_type=return_type, description=description
    )


def parse_class(class_text: str) -> LuaClass:
    logger = getLogger(__name__)
    class_text_lines = class_text.splitlines()
    name = class_text_lines[0]
    functions = []
    for line in class_text_lines[1:]:
        function = parse_function(line, name)
        if function:
            functions.append(function)
        else:
            logger.warning(f"Could not parse function: {line}")

    return LuaClass(name=name, functions=functions, description=name)


def get_classes() -> Iterable[LuaClass]:
    text = SCRIPTING_PATH.read_text().replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace('\n  Export', '  Export') # inconsistency in the reference
    text = re.sub(" +", " ", text)
    api_text = text.split("Basic Resolve API")[1].split(
        "List and Dict Data Structures"
    )[0]
    classes = api_text.split("\n\n")[1:][:-1]
    classes = [parse_class(class_text) for class_text in classes]
    return classes
