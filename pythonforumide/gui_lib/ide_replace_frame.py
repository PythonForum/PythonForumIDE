import wx

from ide_simple_frame import SimpleFrame

class ReplaceFrame(SimpleFrame):
    """Class with the GUI and the GUI functions"""

    def __init__(self, active_editor, *args, **kwargs):
        """"Displays the frame, creates the GUI"""
    
        super(ReplaceFrame, self).__init__(*args, **kwargs)
        self.create_gui()
        self.txt_to_replace.SetFocus()
        self.active_editor = active_editor

    def create_gui(self):
        """Creates and displays the GUI"""

        # TODO: This needs to be cleaned up with a sizer instead of absolute values.
        # As it is, the text box is cut off.
        # Also needs to have id's from gui_lib/ide_constants.py instead of literal constants.
        # I'm intentionally leaving it with long lines until that is done.

        _panel = wx.Panel(self)
        self.lbl_to_replace = wx.StaticText(_panel, -1, "Search for: ", (5, 8), (100, -1))
        self.txt_to_replace = wx.TextCtrl(_panel, id=-1, pos=(100, 5), size=(300, -1))
        self.lbl_replace_with = wx.StaticText(_panel, -1, "Replace with: ", (5, 53), (100, -1))
        self.txt_replace_with = wx.TextCtrl(_panel, id=-1, pos=(100, 50), size=(300, -1))
        self.replace_id = wx.NewId()
        self.replace_button = wx.Button(_panel, self.replace_id, "Replace", pos=(5, 80), size=(90, -1))
        self.Bind(wx.EVT_BUTTON, self.on_replace, id=self.replace_id)
        self.sizer.Add(_panel, 1, wx.EXPAND)

    def on_replace(self, event):
        """Replaces text on the current editor (self.active_editor)"""
        self.str_to_replace = self.txt_to_replace.GetValue()
        self.str_replace_with = self.txt_replace_with.GetValue()
        self.active_editor.SetText(self.active_editor.GetText().replace(
                self.str_to_replace, self.str_replace_with))
        self.Destroy()
