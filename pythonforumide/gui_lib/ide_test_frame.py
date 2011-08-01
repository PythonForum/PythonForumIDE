"""
Created on 31 Jul 2011

@author: D.W., David
"""

import wx

class TestFrame(wx.Frame):
    """Frame to use for testing"""
    def __init__(self, *args, **kwargs):
        """Initiates the frame and the GUI"""
        super(TestFrame, self).__init__(*args, **kwargs)
        self.SetInitialSize((600,600))
        self.Center(wx.BOTH)
        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.Show()
        
class TestPanel(wx.Panel):
    """Panel to use for testing"""
    def __init__(self, *args, **kwargs):
        """Creates the GUI for the test panel"""
        super(TestPanel, self).__init__(*args, **kwargs)
        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

if __name__ == '__main__':
    """Adds the test panel to the test frame"""
    app = wx.PySimpleApp(False)
    frame= TestFrame(None, title= "Testing TestFrame")
    panel= TestPanel(frame)
    frame.sizer.Add(panel, 1, wx.EXPAND)
    frame.Layout()
    app.MainLoop()
