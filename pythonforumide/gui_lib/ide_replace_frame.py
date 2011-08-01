import wx

class ReplaceFrame(wx.Frame):
    """Class with the GUI and the GUI functions"""
    def __init__(self, parent, id):
        """"Displays the frame, creates the GUI"""
        wx.Frame.__init__(self, parent, id, "Find and Replace", size=(410, 150))
        self.create_gui()
        self.to_replace.SetFocus()
        self.parent = parent

    def create_gui(self):
        """Creates and displays the GUI"""
        self.panel = wx.Panel(self)
        self.to_replace_label = wx.StaticText(self.panel, -1, "Search for: ",
                                              (5, 8), (100, -1) )
        self.to_replace = wx.TextCtrl(self.panel, id=-1, pos=(100, 5),
                                      size = (300, -1) )
        self.replace_for_label = wx.StaticText(self.panel, -1, "Replace with: ",
                                               (5, 53), (100, -1) )
        self.to_replace_with = wx.TextCtrl(self.panel, id=-1, pos=(100, 50),
                                           size = (300, -1) )
        self.replace_id = wx.NewId()
        self.replace_button = wx.Button(self.panel, self.replace_id, "Replace",
                                        pos=(5, 80), size=(90, -1))
        self.Bind(wx.EVT_BUTTON, self.on_replace, id=self.replace_id)

    def on_replace(self, event):
        """Replaces text on the current editor (self.parent)"""
        self.to_replace_text = self.to_replace.GetValue()
        self.to_replace_with_text = self.to_replace_with.GetValue()
        self.parent.SetText(self.parent.GetText().replace(
                            self.to_replace_text,
                            self.to_replace_with_text))
        self.Destroy()
