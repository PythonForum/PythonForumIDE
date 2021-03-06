"""
Created on 31 Jul 2011

@author: D.W., David
"""

import wx

class SimpleFrame(wx.Frame):
    """Frame to use for testing"""

    def __init__(self, *args, **kwargs):
        """Initiates the frame and the GUI"""
        super(SimpleFrame, self).__init__(*args, **kwargs)
        self.SetInitialSize(kwargs.get("size", (600, 600)))
        self.Center(wx.BOTH)
        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.Show()

class SimplePanel(wx.Panel):
    """Panel to use for testing"""

    def __init__(self, *args, **kwargs):
        """Creates the GUI for the test panel"""
        super(SimplePanel, self).__init__(*args, **kwargs)
        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)