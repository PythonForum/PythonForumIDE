"""
@author: Jakob, David, bunburya, confab, Somelauw
@reviewer: Somelauw, ghoulmaster, David
"""

#Do not remove
import sys
sys.path.append('..')
#

from utils.textutils import split_comments
#from utils.interpreter import PythonProcessProtocol
#from utils.version import get_python_exe, introduction
from utils.autocomplete import CodeCompletion
import wx.richtext
import wx.stc as stc
#import os.path
import wx

#try:
    #from cStringIO import StringIO
#except ImportError:
    #from StringIO import StringIO

#from ide_simple_frame import SimpleFrame
#from ide_replace_frame import ReplaceFrame

#TODO: make customisable font and sizes. Perhaps maked this named tuple?
faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

class EditorPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Create a panel with a containing Editor control"""
        super(EditorPanel, self).__init__(*args, **kwargs)
        self.SetBackgroundColour((255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self._create_editor(sizer)

    def _create_editor(self, sizer):
        """ Creates the Editor control"""
        ctrl = Editor(self, style=wx.BORDER_THEME, pos=(-100, -100))
        sizer.Add(ctrl, 1 , wx.EXPAND | wx.ALL, 1)
        self.editor = ctrl


class Editor(stc.StyledTextCtrl):
    """Inherits wxStyledTextCtrl and handles all editor functions"""
    def __init__(self, *args, **kwargs):
        """Starts the editor and calls some editor-related functions"""
        super(Editor, self).__init__(*args, **kwargs)

        self.conf = wx.GetApp().config

        self.filepath = ''
        self.indent_level = 0

        self.SetGenerics()
        self.SetMargins()
        self.SetStyles()
        self.SetBindings()
        self.SetAutoComplete()

    def SetAutoComplete(self):
        self.autocomp = CodeCompletion()

    def SetBindings(self):
        """Sets the key events bindings"""
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def SetGenerics(self):
        """Rather than do it in the __init__ and to help debugging the styles
        and settings are split into seperate SetOptions, this sets the generic
        options like Tabwidth, expandtab and indentation guides + others."""
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces) #set mono spacing here!
        # Presumably we should be reading this stuff from config?
        self.SetTabWidth(4)
        self.SetIndentationGuides(1)
        #Indentation will only use space characters if useTabs is false
        self.SetUseTabs(False)

    def SetMargins(self):
        """This is specifically for the margins. Like the other Set methods it
        is only really to be called in the __init__ its here more for
        readability purpsoses than anything else."""
        # margin 0 for breakpoints
        self.SetMarginSensitive(0, True)
        self.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(0, 0x3)
        self.SetMarginWidth(0, 12)
        # margin 1 for current line arrow
        self.SetMarginSensitive(1, False)
        self.SetMarginMask(1, 0x4)
        # margin 2 for line numbers
        self.SetMarginType(2, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(2, 28)

    def SetStyles(self, lang='python'):
        """This is different from the other Set methods that
        are called in the __init__ this one is for the highlighting and syntax of the langauge,
        this will eventually be callable with different langauge styles.
        For the moment, leave the lang kwarg in. """

        #INDICATOR STYLES FOR ERRORS (self.errorMark)
        self.IndicatorSetStyle(2, stc.STC_INDIC_SQUIGGLE)
        self.IndicatorSetForeground(2, wx.RED)
        self.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)

        # Python styles

        # White space
        self.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        # Comment
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "face:%(mono)s,fore:#007F00,back:#E8FFE8,italic,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "face:%(mono)s,fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "face:%(mono)s,fore:#7F007F,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "face:%(mono)s,fore:#7F007F,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "face:%(mono)s,fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "face:%(mono)s,fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "face:%(mono)s,fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "face:%(mono)s,fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "face:%(mono)s,fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "face:%(mono)s,bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "")
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "face:%(mono)s,fore:#990000,back:#C0C0C0,italic,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "face:%(mono)s,fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

    def SmartIndent(self):
        """Handles smart indentation for the editor"""
        # Read settings from the config file

        # Suggestion: instead of indent_amount and use_tab, maybe just
        # have one config value, specifying what is to be used as indent.
        # -bunburya

        # Determine how to indent
        usetab = self.conf["usetab"]
        if usetab:
            indent_amount = self.GetTabWidth()
            indent = "\t"
        else:
            indent_amount = int(self.conf["indent"])
            indent = indent_amount * " "

        # The column in which we can find the cursor
        cursorpos = self.GetColumn(self.GetCurrentPos())

        last_line_no = self.GetCurrentLine()
        last_line = split_comments(self.GetLine(last_line_no))[0]
        self.NewLine()
        indent_level = self.GetLineIndentation(last_line_no) // indent_amount

        # Should we increase or decrease the indent level
        colonpos = last_line.find(":")
        if colonpos >= 0 and cursorpos > colonpos:
            indent_level += 1
        elif any(last_line.lstrip().startswith(token)
                 for token in ["return", "break", "yield"]):
            indent_level = max([indent_level - 1, 0])

        self.AddText(indent * indent_level)

    def AutoComp(self, event, keycode):
        """TODO:
        - If you indent (via tab or SmartIndent) and then autocomplete,
          it seems that the program automatically indents again after
          printing the word.
        - Properly handle uppercase; the current implementation ignores
          caps lock.
        """
        if keycode == wx.WXK_BACK:
            self.autocomp.back()
        else:
            try:
                # this isn't perfect, doesn't handle caps lock
                if event.ShiftDown():
                    ch = chr(event.GetUniChar())
                else:
                    ch = chr(event.GetUniChar()).lower()
                self.autocomp.update_key(ch)
            except ValueError:
                self.autocomp.clear()
                return
        choices = list(self.autocomp.suggest())
        if choices:
            choices.sort()
            self.AutoCompShow(self.autocomp.len_entered-1, ' '.join(choices))

    def OnKeyDown(self, event):
        """Defines events for when the user presses a key"""
        key = event.GetKeyCode()
        control = event.ControlDown()
        alt = event.AltDown()

        number_keys = [49, 50, 51, 52, 53, 54, 56, 57, 58]

        if alt and key in number_keys:
                index = number_keys.index(key)
                self.GetParent().GetParent().SetSelection(index)

        if key == wx.WXK_RETURN and not control and not alt:
            self.SmartIndent()
        else:
            event.Skip()
        self.AutoComp(event, key)

    def CanCut(self):
        """ Returns true if there's a selection that can be cut"""
        if self.GetSelectedText():
            return True
        return False

    def CanCopy(self):
        """ Returns true if there's a selection that can be copied"""
        """ Uses CanCut could be altered for its own checking if required"""
        return self.CanCut()

    def CanPaste(self):
        """ Returns ture if the clipboard contains text"""
        """ Note: I dont know at present how to check clipboard for contents"""
        return True

    def CanDelete(self):
        """ Returns true if there's a selection that can be deleted"""
        """ Uses CanCut could be altered for its own checking if required"""
        return self.CanCut()

    def load_file(self, path):
        """Loads a new file"""
        self.LoadFile(path)
        self.filepath= path

    def save_file(self):
        """Saves the current file"""
        return self.SaveFile(self.filepath)

    def save_file_as(self, filepath):
        """Save the current file as a new filepath"""
        self.filepath= filepath
        return self.save_file()
