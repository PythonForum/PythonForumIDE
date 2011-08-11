import wx
import string
from itertools import izip_longest
from ide_simple_frame import SimpleFrame

class ReplaceFrame(wx.Dialog):
    """Class with the GUI and the GUI functions"""

    def __init__(self, active_editor, *args, **kwargs):
        """"Displays the frame, creates the GUI"""
        super(ReplaceFrame, self).__init__(*args, **kwargs)
        self.sizer= wx.BoxSizer(wx.VERTICAL)
        
        self.panel= ReplaceFramePanel(self)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)
        
#        self.create_gui()
#        self.txt_to_replace.SetFocus()
#        self.active_editor = active_editor

        self.Show()

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
        self.replace_button = wx.Button(_panel, self.replace_id, "Replace", pos=(5, 110), size=(90, -1))
        self.case_check = wx.CheckBox(_panel, -1, "Case Sensitive", pos=(5, 80), size=(-1, -1))
        self.Bind(wx.EVT_BUTTON, self.on_replace, id=self.replace_id)
        self.sizer.Add(_panel, 1, wx.EXPAND)

    def incase_replace(self, st, x, y):
        """Replaces x with y in an non case sensitive way"""
        mod = st.lower().replace(x.lower(), y)
        out = ''
        for x, y in izip_longest(st, mod, fillvalue=' '):
            if x == y:
                out += y
            elif (x in string.ascii_uppercase) and (x == y.upper()):
                out += x
            else:
                out += y
        return out

    def on_replace(self, event):
        """Replaces text on the current editor (self.active_editor)"""
        self.str_to_replace = self.txt_to_replace.GetValue()
        self.str_replace_with = self.txt_replace_with.GetValue()
        if self.case_check.GetValue(): #If case sensitive on
            self.active_editor.SetText(self.active_editor.GetText().replace(
                self.str_to_replace, self.str_replace_with))
        else: #If case sensitive disabled
            self.active_editor.SetText(self.incase_replace(
                self.active_editor.GetText(), self.str_to_replace,
                self.str_replace_with))
        self.Destroy()
               
class ReplaceFramePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ReplaceFramePanel, self).__init__(*args, **kwargs)
        self.sizer= wx.BoxSizer(wx.HORIZONTAL)
        self._create_vsizer(self.sizer)
        self._create_buttons(self.sizer)
        self.SetSizer(self.sizer)
        self.Layout()
        
    def _create_vsizer(self, sizer):
        vsizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vsizer)
        vsizer.AddSpacer((-1, 10))
        self._create_inputs(vsizer)
        vsizer.AddSpacer((-1, 10))
        self._create_options(vsizer)
        vsizer.AddSpacer((-1, 10))
     
    def _create_inputs(self, sizer):
        grid_sizer= wx.FlexGridSizer(cols= 2, vgap= 10, hgap=10)
        sizer.Add(grid_sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        ctrl= wx.StaticText(self, label= "Search for:")
        grid_sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        ctrl= wx.TextCtrl(self, size= (150, -1))
        grid_sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.ctrl_txt_exisiting= ctrl
        ctrl= wx.StaticText(self, label= "Replace with:")
        grid_sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        ctrl= wx.TextCtrl(self, size= (150, -1))
        grid_sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.ctrl_txt_new= ctrl
       
    def _create_buttons(self, sizer):
        box_sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box_sizer)
        box_sizer.AddSpacer((-1, 10))
        ctrl= wx.Button(self, label= "Find next")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.btn_next= ctrl
        box_sizer.AddSpacer((-1, 5))
        ctrl= wx.Button(self, label= "Replace")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.btn_replace= ctrl
        box_sizer.AddSpacer((-1, 5))
        ctrl= wx.Button(self, label= "Replace all")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.btn_replace_all= ctrl
        box_sizer.AddSpacer((-1, 5))
        ctrl= wx.Button(self, label= "Cancel")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.btn_cancel= ctrl
        box_sizer.AddSpacer((-1, 10))
    
    def _create_options(self, sizer):
        box_sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box_sizer)
        ctrl= wx.CheckBox(self, label= " Match whole word only")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.check_whole_word= ctrl
        box_sizer.AddSpacer((-1, 10))
        ctrl= wx.CheckBox(self, label= " Match case")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.check_match_case= ctrl


        
        
        
        


if __name__ == '__main__':
    wx_app= wx.App(None)
    ReplaceFrame(active_editor= None, parent= None,
                 title="Find and Replace", size=(410, 150))
    wx_app.MainLoop()