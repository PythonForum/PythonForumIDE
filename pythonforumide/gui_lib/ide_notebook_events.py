"""
Created on 31 Jul 2011

@author: D.W., David
"""

import wx
import wx.lib.agw.flatnotebook as fnb
from wx.lib.agw.flatnotebook import EVT_FLATNOTEBOOK_PAGE_CLOSED, \
                                    EVT_FLATNOTEBOOK_PAGE_CHANGED, \
                                    EVT_FLATNOTEBOOK_PAGE_CLOSING

class NotebookEvents(object):
    """ Creates the events for the notebook"""

    def __init__(self, view, model=None):
        """Calls the functions to bind events"""
        self.view = view
        self.model = model
        self.notebook= self.view.notebook
        self._create_binds()

    def _create_binds(self):
        """Create binds"""
        self.notebook.Bind(EVT_FLATNOTEBOOK_PAGE_CLOSED,
                           self._on_page_closed)

        self.notebook.Bind(EVT_FLATNOTEBOOK_PAGE_CHANGED,
                           self._on_page_changed)

        self.notebook.Bind(EVT_FLATNOTEBOOK_PAGE_CLOSING,
                           self._on_page_closing)

    def _on_page_changed(self, event):
        """sets the currently active page index and editor page"""
        nb_obj = event.GetEventObject()
        self.notebook._active_tab_index = nb_obj.GetSelection()
        active_editor_panel = nb_obj.GetCurrentPage()
        self.notebook._active_editor = active_editor_panel.editor
        event.Skip()

    def _on_page_closed(self, event):
        """Sets currently active page to none and renames the untitled pages"""
        event.Skip()
        wx.CallAfter(self.notebook.editor_tab_name_untitled_tabs)

    def _on_page_closing(self, event):
        """Called when tab is closed"""
        new_index= event.GetSelection()
        if not new_index:
            self.notebook._active_editor = None
        event.Skip()
