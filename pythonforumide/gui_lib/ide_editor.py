"""
@author: Jakob, David, bunburya, confab
@reviewer: Somelauw, ghoulmaster, David
"""

#YES DIRT HACK GET OVER IT. Dont remove it might go before it goes into master
import sys
sys.path.append('..')

from utils.textutils import split_comments
from utils.interpreter import PythonProcessProtocol
from utils.version import get_python_exe
from utils.autocomplete import CodeCompletion
import wx.richtext
import wx.stc as stc
import os.path
import wx

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from ide_simple_frame import SimpleFrame
from ide_replace_frame import ReplaceFrame

#TODO: make customisable font and sizes. Perhaps maked this named tuple?
faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

class Editor(stc.StyledTextCtrl):
    """Inherits wxStyledTextCtrl and handles all editor functions"""
    def __init__(self, parent):
        """Starts the editor and calls some editor-related functions"""
        super(Editor, self).__init__(parent)

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
        self.autocomp.add_builtins()
        self.autocomp.add_keywords()

    def SetBindings(self):
        """Sets the key events bindings"""
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
    
    def SetGenerics(self):
        """Rather than do it in the __init__ and to help debugging the styles
        and settings are split into seperate SetOptions, this sets the generic
        options like Tabwidth, expandtab and indentation guides + others."""
        self.SetLexer(stc.STC_LEX_PYTHON) #is this giving us trouble? 
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces) #set mono spacing here!
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
        http://paste.pocoo.org/show/446107/ are called in the 
        __init__ this one is for the highlighting and syntax of the langauge,
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
        
        indent_amount = int(self.conf["indent"])
        usetab = self.conf["usetab"]

        last_line_no = self.GetCurrentLine()
        last_line = split_comments(self.GetLine(last_line_no))[0]
        self.NewLine()
        indent_level = self.GetLineIndentation(last_line_no) // indent_amount
        
        if last_line.rstrip().endswith(':'):
            indent_level += 1
        elif any(last_line.lstrip().startswith(token) 
                 for token in ["return", "break", "yield"]):
            indent_level = max([indent_level - 1, 0])

        if usetab:
            indent = "\t" * indent_level
        else:
            indent = indent_amount * " " * indent_level

        self.AddText(indent)
        print self.conf
    
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
                print ch
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
        if key == wx.WXK_RETURN and not control and not alt:
            self.SmartIndent()
        else:
            event.Skip()
        self.AutoComp(event, key)

    def on_undo(self):
        """Checks if can Undo and if yes undoes"""
        if self.CanUndo() == 1:
            self.Undo()
        
    def on_redo(self):
        """Checks if can Redo and if yes redoes"""
        if self.CanRedo() == 1:
            self.Redo()

    def on_cut(self):
        """Cuts selected text"""
        self.Cut()
        
    def on_copy(self):
        """Copies selected text"""
        self.Copy()
        
    def on_paste(self):
        """Pastes selected text"""
        self.Paste()
        
    def on_clear(self):
        """Deletes selected text"""
        self.Clear()

    def on_select_all(self):
        """Selects all the text"""
        self.SelectAll()
        
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
    
    def on_replace(self):
        """Displays a find/replace dialog"""
        
        # Create a search frame and hook into the caller.
        # Allows this frame to be destroyed by the main window on close.
        replace_frame = ReplaceFrame(active_editor=self,
                                     parent=wx.GetApp().TopWindow,
                                     title="Find and Replace", size=(410, 150))
        replace_frame.Layout()
        

    def on_run(self):
        """Runs selected code in a new window."""
        # Create a test frame and hook into the caller.
        # Allows this frame to be destroyed by the main window on close.
        reactor = wx.GetApp().this_reactor        
        
        run_editor = SimpleFrame(wx.GetApp().TopWindow, title="")
        run_panel = wx.richtext.RichTextCtrl(run_editor, style=wx.TE_READONLY)
        run_editor.sizer.Add(run_panel, 1, wx.EXPAND)
        run_editor.Layout()
        
        if self.filepath:
            if self.GetModify():      
                self.SaveFile(self.filepath)
            filename = os.path.split(self.filepath)[1]
            run_panel.WriteText("Running %s" % filename)
            run_panel.Newline()
            reactor.spawnProcess(PythonProcessProtocol(run_panel), 
                                          get_python_exe(), 
                                          ["python", str(self.filepath)])
        
        else:
            run_panel.WriteText("Running unsaved script.")
            run_panel.Newline()
            script = StringIO()
            script.write(self.GetText())
            script.seek(0)
            reactor.spawnProcess(PythonProcessProtocol(run_panel), 
                                          get_python_exe(), 
                                            ["python", "-c", script.read()])
        
        
        return run_panel

if __name__=='__main__':
    """Adds the editor to the frame"""
    import ide_test_app as wx_app
    import ide_simple_frame 
    app = wx_app.Wx_App(False)
    frame= ide_simple_frame.SimpleFrame(None, title= "Testing editor")
    panel= ide_simple_frame.TestPanel(frame)
    frame.sizer.Add(panel, 1, wx.EXPAND)
    editor= Editor(panel)
    panel.sizer.Add(editor, 1, wx.EXPAND)
    frame.Layout()
    app.MainLoop()
