"""
Created on 4 Aug 2011

@author: Main, David
"""

import wx

from ide_notebook import NoteBookPanel
from ide_notebook_events import NotebookEvents
from ide_headered_panel import HeaderedPanel, HeaderedPanelEvents
from ide_console import ConsolePanel

from ide_constant import ID_SHOW_TOOLBAR
from ide_toolbar import ToolBarPanel

class MainFramePanel(wx.Panel):
    """ Creates the mainframe panel"""

    def __init__(self, *args, **kwargs):
        """Initializes the panel"""
        super(MainFramePanel, self).__init__(*args, **kwargs)
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._create_toolbar()
        self._create_notebook_panel()
        self._create_console()
        self._create_first_tab()
        self.SetSizer(self._sizer)
        self.Layout()

    def _create_toolbar(self):
        """Creates a toolbar"""
        ctrl= ToolBarPanel(self)
        self._sizer.Add(ctrl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 3)
        self.toolbar= ctrl

    def _create_notebook_panel(self):
        """Create the notebook panel"""
        self._sizer.AddSpacer((-1, 2))
        headered_panel = HeaderedPanel(self, style = wx.BORDER_THEME)
        HeaderedPanelEvents(headered_panel)
        self._sizer.Add(headered_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        ctrl = headered_panel.add_panel_ctrl(NoteBookPanel, "", 100)
        NotebookEvents(ctrl)
        self.notebook = ctrl.notebook

    def _create_console(self):
        """Create a console window"""
        self._sizer.AddSpacer((-1, 4))
        headered_panel = HeaderedPanel(self, style = wx.BORDER_THEME)
        HeaderedPanelEvents(headered_panel)
        self._sizer.Add(headered_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        ctrl = headered_panel.add_panel_ctrl(ConsolePanel, "Console", 30)
        self.console_rich_text = ctrl._rt_ctrl
        self._sizer.AddSpacer((-1, 2))

    def _create_first_tab(self):
        """Adds a new blank editor tab
        perhaps open last edited in the future, for now just open new."""
        self.notebook.editor_tab_new()

    def toolbar_show(self, enable= True):
        """Show/hide the toolbar"""
        self.toolbar.Show(enable)
        self.Layout()
