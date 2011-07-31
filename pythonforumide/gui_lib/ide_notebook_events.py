'''
Created on 31 Jul 2011

@author: D.W.
'''

import wx
import wx.aui as aui

class NotebookEvents(object):
    def __init__(self, view, model= None):
        self.view = view
        self.model = model
        self._create_binds()
        
    def _create_binds(self):
        '''
        Create binds
        '''
        self.view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE,
                       self._on_page_closed)
        self.view.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED,
                       self._on_page_changed)
        
    def _on_page_changed(self, event):
        """sets the currently active page index and editor page"""
        self.view._active_tab_index= event.Selection
        self.view._active_editor_page= self.view.GetPage(self.view._active_tab_index)
        
    def _on_page_closed(self, event):
        """Sets currently active page to none and renames the untitled pages"""
        event.Skip()
        self.view._active_editor_page= None
        wx.CallAfter(self.view.name_untitled_pages)