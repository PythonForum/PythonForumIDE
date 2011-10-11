"""
Created on 4 Aug 2011

@author: D.W., David
@reviewer: David
"""

import wx
from wx.richtext import RichTextCtrl

class ConsolePanel(wx.Panel):
    """Creates the Panel GUI"""

    def __init__(self, *args, **kwargs):
        """Super the panel and create GUI"""
        super(ConsolePanel, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_rich_text_ctrl()

        self.SetSizer(self.sizer)
        self.Layout()

    def _create_rich_text_ctrl(self):
        """Creates the textbox for the console"""
        self._rt_ctrl = RichTextCtrl(self, style=wx.TE_READONLY)
        monospace_font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL,
                                 False, u"Monospace")
        self._rt_ctrl.SetFont(monospace_font)
        self.sizer.Add(self._rt_ctrl, 1, wx.EXPAND | wx.ALL, 1)
