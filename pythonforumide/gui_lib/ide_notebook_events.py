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

    def ask_close(self, index):
        dial = wx.MessageDialog(None, "Do you really want to close this page?",
                                "Close page", wx.YES_NO | wx.ICON_QUESTION)

        if dial.ShowModal() == wx.ID_YES:
            self.close_accepted = True
            return self.notebook.DeletePage(index)

    def _on_page_closing(self, event):
        """Called when tab is closed"""

        #close_accepted == True means no asking to close page

        try:
            if self.close_accepted:
                self.close_accepted = False
                return
        except AttributeError:
            index = event.GetSelection()

            if self.notebook._active_editor.GetModify() == 1:
                event.Veto()
                return self.ask_close(index)

            if not index:
                self.notebook._active_editor = None

            event.Skip()
