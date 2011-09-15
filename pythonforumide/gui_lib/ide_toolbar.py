"""
Created on 31 Jul 2011

@author: D.W., David
"""

import wx
import ide_constant as ide
from ide_images import menu_icons

class ToolBarPanel(wx.Panel):
    """ Creates a panel to hold the toolbar"""

    def __init__(self, *args, **kwargs):
        """Creates the GUI"""
        super(ToolBarPanel, self).__init__(*args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        ctrl = ToolBar(self, style=wx.TB_HORIZONTAL | wx.TB_FLAT)
        sizer.Add(ctrl, 0, wx.EXPAND | wx.LEFT)
        self.toolbar = ctrl
        self.Layout()

class ToolBar(wx.ToolBar):
    """Toolbar class, creates the toolbar and binds events"""

    def __init__(self, *args, **kwargs):
        """Create the toolbar"""
        super(ToolBar, self).__init__(*args, **kwargs)
        self.SetToolBitmapSize((16, 16))
        self._add_toolbar_btn(ide.ID_NEW, ide.id_text_new,
                              menu_icons.get_icon_new())

        self._add_toolbar_btn(ide.ID_OPEN, ide.id_text_open,
                              menu_icons.get_icon_open())

        self._add_toolbar_btn(ide.ID_SAVE, ide.id_text_save,
                              menu_icons.get_icon_save())

        self._add_toolbar_btn(ide.ID_SAVEAS, ide.id_text_saveas,
                              menu_icons.get_icon_saveas())

        self.AddSeparator()

        self._add_toolbar_btn(ide.ID_CUT, ide.id_text_cut,
                              menu_icons.get_icon_cut())

        self._add_toolbar_btn(ide.ID_COPY, ide.id_text_copy,
                              menu_icons.get_icon_copy())

        self._add_toolbar_btn(ide.ID_PASTE, ide.id_text_paste,
                              menu_icons.get_icon_paste())

        self.AddSeparator()

        self._add_toolbar_btn(ide.ID_UNDO, ide.id_text_undo,
                              menu_icons.get_icon_undo())

        self._add_toolbar_btn(ide.ID_REDO, ide.id_text_redo,
                              menu_icons.get_icon_redo())

        self.Realize()

    def _add_toolbar_btn(self, id, id_text, icon_bmp=None):
        """ Creates tool bar buttons"""
        self.AddLabelTool(id=id, label=id_text.toolbar, bitmap=icon_bmp,
                          shortHelp=id_text.toolbar, longHelp=id_text.status)
