from typing import Generator, Iterable
from xmlrpc.client import boolean
from drtypehints.lua_types import (
    join_alias,
    LuaFunction,
    LuaClass,
    LuaFunctionField,
    LuaProperty,
)
import re
import humps


def get_alias():
    alias = {
        "Reason": join_alias(
            [
                "MouseFocusReason",
                "TabFocusReason",
                "ActiveWindowFocusReason",
                "OtherFocusreason",
            ]
        ),
        "Size": "integer[] # {width, height} {640, 480}",
        "Position": "integer[] {X, Y} {0, 0}",
        "Geometry": "integer[] # {X, Y, width, height} {0, 0, 640, 480}",
        "Key": "string",
        "ID": "string",
        "Font": "string",
        "Color": "string",
    }
    return alias


def parse_type(param_or_type_text: str) -> str:
    list_match = re.fullmatch(r"(.+?)\[\]", param_or_type_text)
    if list_match:
        return parse_type(list_match.group(1)) + "[]"

    type_in = {
        "Name": "string",
        "Text": "string",
        "Pos": "integer[]",
        "Count": "integer",
        "element": "element",
        "WhatsThis": "string",
        "Value": "integer",
        "auto": "boolean",
        "Shape": "Size",
        "Rect": "Size",
        "Is": "boolean",
        "Index": "integer",
        "Show": "boolean",
        "Indent": "integer",
        "Margin": "integer",
        "Auto": "boolean",
        "Hidden": "boolean",
        "Size": "Size",
    }
    type_regex = {
        "r": "integer",
        "g": "integer",
        "b": "integer",
        "int": "integer",
        "Do.+": "boolean",
        ".+?ed": "boolean",
        ".+?able": "boolean",
        ".+?ing": "boolean",
        "Uses.+": "boolean",
        "Prefix": "string",
        "Suffix": "string",
        ".+?tate": "boolean",
        "Single.+": "boolean",
        ".+?Only": "boolean",
        "Down": "boolean",
        "Min.+": "integer",
        "Max.+": "integer",
        ".+?Width": "integer",
        ".+?Height": "integer",
    }

    param_or_type_text = humps.pascalize(param_or_type_text)  # type: ignore

    for key, value in type_in.items():
        if key in param_or_type_text:
            return value

    for key, value in type_regex.items():
        if re.fullmatch(key, param_or_type_text):
            return value
        
    # to avoid Pos -> Po[] etc.
    list_match = re.fullmatch(r"(.+?)s", param_or_type_text)
    if list_match:
        return parse_type(list_match.group(1)) + "[]"
    
    return param_or_type_text


def parse_general_functions(type_) -> Generator[LuaFunction, None, None]:
    general_functions_raw = [
        "Show()",
        "Hide()",
        "Raise()",
        "Lower()",
        "Close()Returnsboolean",
        "Find(ID)Returnselement",
        "GetChildren()Returnslist",
        "AddChild(element)",
        "RemoveChild(element)",
        "SetParent(element)",
        "Move(point)",
        "Resize(size)",
        "Size()Returnssize",
        "Pos()Returnsposition",
        "HasFocus()Returnsboolean",
        "SetFocus(reason)",
        "FocusWidget()Returnselement",
        "IsActiveWindow()Returnsboolean",
        "SetTabOrder(element)",
        "Update()",
        "Repaint()",
        "SetPaletteColor(r,g,b)",
        "QueueEvent(name,info)",
        "GetItems()Returnselements",
    ]
    for text in general_functions_raw:
        if m := re.match(r"(.*)\(", text):
            name = m.group(1)
        else:
            raise AssertionError(f"{text}")
        fields_ = m.group(1).split(",") if (m := re.match(r"\((.*)\)", text)) else []
        fields = [LuaFunctionField(name="self", type=type_)] + [
            LuaFunctionField(name=f_, type=parse_type(f_)) for f_ in fields_
        ]
        if m := re.match(r"Returns(.*)", text):
            return_type = parse_type(m.group(1))
        else:
            return_type = "nil"
        yield LuaFunction(
            name=name, fields=fields, return_type=return_type, description=""
        )


def parse_specific_functions() -> dict[str, list[LuaFunction]]:
    specific_functions = {
        "Label": "SetSelection(int,int),boolHasSelection(),stringSelectedText(),intSelectionStart()",
        "Button": "Click(),Toggle(),AnimateClick()",
        "CheckBox": "Click(),Toggle(),AnimateClick()",
        "ComboBox": "AddItem(string),InsertItem(string),AddItems(list),InsertItems(int,list),"
        + "InsertSeparator(int),RemoveItem(int),Clear(),SetEditText(string),ClearEditText(),Count(),ShowPopup(),HidePopup()",
        "SpinBox": "SetRange(int,int),StepBy(int),StepUp(),StepDown(),SelectAll(),Clear()",
        "Slider": "SetRange(int,int),TriggerAction(string)",
        "LineEdit": "SetSelection(int,int),boolHasSelectedText(),stringSelectedText(),intSelectionStart(),"
        + "SelectAll(),Clear(),Cut(),Copy(),Paste(),Undo(),Redo(),Deselect(),Insert(string),Backspace(),Del(),"
        + "Home(bool),End(bool),intCursorPositionAt(point)",
        "TextEdit": "InsertPlainText(string),InsertHTML(string),Append(string),SelectAll(),Clear(),Cut(),Copy(),"
        + "Paste(),Undo(),Redo(),ScrollToAnchor(string),ZoomIn(int),ZoomOut(int),EnsureCursorVisible(),"
        + "MoveCursor(moveOperation,moveMode),boolCanPaste(),stringAnchorAt(point),boolFind(string,findFlags)",
        "TabBar": "intAddTab(strubg),intInsertTab(string),intCount(),RemoveTab(int),MoveTab(int,int)",
        "Tree": "AddTopLevelItem(item),InsertTopLevelItem(item),SetHeaderLabel(string),intCurrentColumn(),"
        + "intSortColumn(),intTopLevelItemCount(),itemCurrentItem(),itemTopLevelItem(int),itemTakeTopLevelItem(int),"
        + "itemInvisibleRootItem(),itemHeaderItem(),intIndexOfTopLevelItem(item),itemItemAbove(item),itemItemBelow(item),"
        + "itemItemAt(point),Clear(),rectVisualItemRect(item),SetHeaderLabels(list),SetHeaderItem(item),InsertTopLevelItems(list),"
        + "AddTopLevelItems(list),listSelectedItems(),listFindItems(string,flags),SortItems(int,order),ScrollToItem(item),"
        + "ResetIndentation(),SortByColumn(int,order),intFrameWidth()",
        "TreeItem": "AddChild(item),InsertChild(item),RemoveChild(iitem),SortChildren(int,order),InsertChildren(int,list),"
        + "AddChildren(list),intIndexOfChild(item),itemClone(),treeTreeWidget(),itemParent(),itemChild(int),itemTakeChild(int),"
        + "intChildCount(),intColumnCount()",
        "Window": "Show(),Hide(),RecalcLayout()",
        "Dialog": "Exec(),IsRunning(),Done(),RecalcLayout()",
    }
    d = {}
    for class_name, function_text_raw in specific_functions.items():
        function_texts = function_text_raw.split("),")
        d[class_name] = []
        for text in function_texts:
            if m := re.match(r"(.*)\(", text):
                name = m.group(1)
            else:
                raise AssertionError(f"{text}, Key: {class_name}")
            if m := re.match(r"\((.*)", text):
                fields_ = m.group(1).split(",")
            else:
                fields_ = []
            fields = [LuaFunctionField(name="self", type=class_name)] + [
                LuaFunctionField(name=f_, type=parse_type(f_)) for f_ in fields_
            ]
            return_type = "nil"
            d[class_name].append(
                LuaFunction(
                    name=name, fields=fields, return_type=return_type, description=""
                )
            )
    return d


def parse_specific_properties() -> dict[str, list[LuaProperty]]:
    properties = {
        "Label": "Text,Alignment,FrameStyle,WordWrap,Indent,Margin",
        "Button": "Text,Down,Checkable,Checked,Icon,IconSize,Flat",
        "CheckBox": "Text,Down,Checkable,Checked,Tristate,CheckState",
        "ComboBox": "ItemText[],Editable,CurrentIndex,CurrentText,Count",
        "SpinBox": "Value,Minimum,Maximum,SingleStep,Prefix,Suffix,Alignment,ReadOnly,Wrapping",
        "Slider": "Value,Minimum,Maximum,SingleStep,PageStep,Orientation,Tracking,SliderPosition",
        "LineEdit": "Text,PlaceholderText,Font,MaxLength,ReadOnly,Modified,ClearButtonEnabled",
        "TextEdit": "Text,PlaceholderText,HTML,Font,Alignment,ReadOnly,TextColor,TextBackgroundColor,TabStopWidth,Lexer,LexerColors",
        "ColorPicker": "Text,Color,Tracking,DoAlpha",
        "Font": "Family,StyleName,PointSize,PixelSize,Bold,Italic,Underline,Overline,StrikeOut,Kerning,Weight,Stretch,MonoSpaced",
        "Icon": "File",
        "TabBar": "TabText[],TabToolTip[],TabWhatsThis[],TabTextColor[],CurrentIndex,TabsClosable,Expanding,AutoHide,Movable,"
        + "DrawBase,UsesScrollButtons,DocumentMode,ChangeCurrentOnDrag",
        "Tree": "ColumnWidth[],ColumnCount,SortingEnabled,ItemsExpandable,ExpandsOnDoubleClick,AutoExpandDelay,HeaderHidden,"
        + "IconSize,RootIsDecorated,Animated,AllColumnsShowFocus,WordWrap,TreePosition,SelectionBehavior,SelectionMode,UniformRowHeights,"
        + "Indentation,VerticalScrollMode,HorizontalScrollMode,AutoScroll,AutoScrollMargin,TabKeyNavigation,AlternatingRowColors,FrameStyle,"
        + "LineWidth,MidLineWidth,FrameRect,FrameShape,FrameShadow",
        "TreeItem": "Selected,Hidden,Expanded,Disabled,FirstColumnSpanned,Flags,ChildIndicatorPolicy,Text[],StatusTip[],ToolTip[],"
        + "WhatsThis[],SizeHint[],TextAlignment[],CheckState[],BackgroundColor[],TextColor[],Icon[],Font[]",
    }
    d = {}
    for class_name, property_text_raw in properties.items():
        property_texts = property_text_raw.split(",")
        d[class_name] = []
        for text in property_texts:
            name = text.replace("[]", "")
            d[class_name].append(LuaProperty(name=name, type=parse_type(name)))
    return d


def get_ui_classes():
    specific_properties = parse_specific_properties()
    specific_functions = parse_specific_functions()

    for class_name in set(
        list(specific_properties.keys()) + list(specific_functions.keys())
    ):
        functions = list(parse_general_functions(class_name))
        properties = []
        if class_name in specific_functions:
            functions += specific_functions[class_name]
        if class_name in specific_properties:
            properties += specific_properties[class_name]
        yield LuaClass(
            name=class_name, functions=functions, properties=properties, description=""
        )


def get_event_handlers():
    events = {
        "Button": "Clicked,Toggled,Pressed,Released",
        "CheckBox": "Clicked,Toggled,Pressed,Released",
        "ComboBox": "CurrentIndexChanged,CurrentTextChanged,TextEdited,EditTextChanged,EditingFinished,ReturnPressed,Activated",
        "SpinBox": "ValueChanged,EditingFinished",
        "Slider": "ValueChanged,SliderMoved,ActionTriggered,SliderPressed,SliderReleased,RangeChanged",
        "LineEdit": "TextChanged,TextEdited,EditingFinished,ReturnPressed,SelectionChanged,CursorPositionChanged",
        "TextEdit": "TextChanged,SelectionChanged,CursorPositionChanged",
        "ColorPicker": "ColorChanged",
        "TabBar": "CurrentChanged,CloseRequested,TabMoved,TabBarClicked,TabBarDoubleClicked",
        "Tree": "CurrentItemChanged,ItemClicked,ItemPressed,ItemActivated,ItemDoubleClicked,ItemChanged,ItemEntered,"
        + "ItemExpanded,ItemCollapsed,CurrentItemChanged,ItemSelectionChanged",
        "Window": "Close,Show,Hide,Resize,MousePress,MouseRelease,MouseDoubleClick,MouseMove,Wheel,KeyPress,KeyRelease,"
        + "FocusIn,FocusOut,ContextMenu,Enter,Leave",
    }
    for name_, properties_ in events.items():
        name = name_ + "EventHandler"
        properties_ = properties_.split(",")
        properties = [LuaProperty(name=name, type="Event") for name in properties_]
        yield LuaClass(
            name=name,
            functions=[],
            properties=properties,
            description=name_ + " Event Handler",
        )


def get_event_args():
    event_args = {
        "MousePress": "Pos,GlobalPos,Button,Buttons",
        "MouseRelease": "Pos,GlobalPos,Button,Buttons",
        "MouseDoubleClick": "Pos,GlobalPos,Button,Buttons",
        "MouseMove": "Pos,GlobalPos,Button,Buttons",
        "Wheel": "Pos,GlobalPos,Buttons,Delta,PixelDelta,AngleDelta,Orientiation,Phase",
        "KeyPress": "Key,Text,IsAutoRepeat,Count",
        "KeyRelease": "Key,Text,IsAutoRepeat,Count",
        "ContextMenu": "Pos,GlobalPos",
        "Move": "Pos,OldPos",
        "FocusIn": "Reason",
        "FocusOut": "Reason",
    }
    for name_, properties_ in event_args.items():
        name = name_ + "EventArgs"
        properties = [
            LuaProperty(name=p, type=parse_type(p)) for p in properties_.split(",")
        ]
        yield LuaClass(
            name=name,
            properties=properties,
            functions=[],
            description=name_ + " Event Args",
        )


def ui_manager_class(ui_classes: Iterable[LuaClass]) -> LuaClass:
    functions = []
    for cl in ui_classes:
        function = LuaFunction(
            name=cl["name"],
            return_type=cl["name"],
            fields=[LuaFunctionField(name="self", type="UIManager"), LuaFunctionField(name="ui", type=cl["name"])],
            description="",
        )
        functions.append(function)
    return LuaClass(
        name="UIManager", functions=functions, properties=[], description=""
    )


def get_classes():
    ui_classes = list(get_ui_classes())
    yield from ui_classes
    yield from get_event_args()
    yield from get_event_handlers()
    yield ui_manager_class(get_ui_classes())
