'''
Created on 4 Aug 2011

@author: D.W.
'''

import wx
from wx.richtext import RichTextCtrl

class ConsolePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(ConsolePanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_rich_text_ctrl()

        self.SetSizer(self.sizer)
        self.Layout()

    def _create_rich_text_ctrl(self):
        self._rt_ctrl = RichTextCtrl(self, style = wx.TE_READONLY)
        monospace_font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,
                                 False, u"Monospace")
        self._rt_ctrl.SetFont(monospace_font)
        self.sizer.Add(self._rt_ctrl, 1, wx.EXPAND | wx.ALL, 1)

if __name__ == '__main__':
    import ide_test_app as wx_app
    import ide_simple_frame
    app = wx_app.Wx_App(False)
    frame = ide_simple_frame.SimpleFrame(None,
                                       title="Testing console without events")
    panel = ConsolePanel(frame)
    frame.sizer.Add(panel, 1, wx.EXPAND)
    frame.Layout()
    app.MainLoop()
