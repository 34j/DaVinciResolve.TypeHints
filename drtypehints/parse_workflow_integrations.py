from drtypehints.parse_scripting import join_alias


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
    "TabBar": "TabText[],TabToolTip[],TabWhatsThis[],TabTextColor[],CurrentIndex,TabsClosable,Expanding,AutoHide,Movable,"+
    "DrawBase,UsesScrollButtons,DocumentMode,ChangeCurrentOnDrag",
    "Tree": "ColumnWidth[],ColumnCount,SortingEnabled,ItemsExpandable,ExpandsOnDoubleClick,AutoExpandDelay,HeaderHidden,"+
    "IconSize,RootIsDecorated,Animated,AllColumnsShowFocus,WordWrap,TreePosition,SelectionBehavior,SelectionMode,UniformRowHeights,"+
    "Indentation,VerticalScrollMode,HorizontalScrollMode,AutoScroll,AutoScrollMargin,TabKeyNavigation,AlternatingRowColors,FrameStyle,"+
    "LineWidth,MidLineWidth,FrameRect,FrameShape,FrameShadow",
    "TreeItem": "Selected,Hidden,Expanded,Disabled,FirstColumnSpanned,Flags,ChildIndicatorPolicy,Text[],StatusTip[],ToolTip[],"+
    "WhatsThis[],SizeHint[],TextAlignment[],CheckState[],BackgroundColor[],TextColor[],Icon[],Font[]",
}

general_functions = [
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
    "GetItems()Returnsdictionaryofallchildelements",
]

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

event_handlers = {
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

alias = {
    "Reason": join_alias(
        [
            "MouseFocusReason",
            "TabFocusReason",
            "ActiveWindowFocusReason",
            "OtherFocusreason",
        ]
    ),
    "Size": "number[]",
}

