"""
Created on 31 Jul 2011

@author: D.W., confab
@reviewer: ghoulmaster
"""

import wx
import ide_constant as ide
from ide_mainframe import MainFrame

class MainFrameEvents(object):
    """Handles the MainFrame eventss"""
    def __init__(self, view, model= None):
        """Sets the binds and does other stuff"""
        self.view = view
        self.model = model
        self.mainframe= self.view
        self.mainframe_panel= self.mainframe.mainframe_panel
        self.notebook= self.view.mainframe_panel.notebook
        self._create_menu_file_binds()
        self._create_menu_edit_binds()
        self._create_menu_view_binds()
        self._create_menu_search_binds()
        self._create_menu_run_binds()
        self._create_remaining_binds()
#-------------------------------------------------------------------- Menu File
    def _create_menu_file_binds(self):
        """ Creates the binds for the file menu"""
        self.mainframe.Bind(wx.EVT_MENU, self._on_new, id=ide.ID_NEW)
        self.mainframe.Bind(wx.EVT_MENU, self._on_open, id=ide.ID_OPEN)  
        self.mainframe.Bind(wx.EVT_MENU, self._on_save, id=ide.ID_SAVE)
        self.mainframe.Bind(wx.EVT_MENU, self._on_save_as, id=ide.ID_SAVEAS)
        self.mainframe.Bind(wx.EVT_MENU, self._on_close_tab, id=ide.ID_CLOSETAB)
        self.mainframe.Bind(wx.EVT_MENU, self._on_exit_app, id=ide.ID_EXITAPP)
        
    def _on_new(self, event):
        """Opens a new tab with a new editor instance"""
        self.notebook.editor_tab_new()
    
    def _on_open(self, event):
        """Opens a new tab and ask for a file to load"""
        self.mainframe.editor_open_file()
    
    def _on_save(self, event):
        """Saves the currently active file"""
        self.mainframe.editor_save()
        
    def _on_save_as(self, event):
        """Save as required filename"""
        self.mainframe.editor_save_as()
        
    def _on_close_tab(self, event):
        """Closes the current editor tab"""
        self.notebook.editor_tab_close_active()
        
    def _on_exit_app(self, event):
        """ application wants to exit"""
        self.mainframe.on_exit()
#-------------------------------------------------------------------- Menu edit
    def _create_menu_edit_binds(self):
        """ Creates the binds for the edit menu"""
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_undo, id=ide.ID_UNDO)
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_redo, id=ide.ID_REDO)
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_cut, id=ide.ID_CUT)
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_copy, id=ide.ID_COPY)
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_paste, id=ide.ID_PASTE)
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_delete, id=ide.ID_DELETE)
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_selectall, 
                       id=ide.ID_SELECTALL)
        
    def _on_editor_undo(self, event):
        """Undo for the current editor tab"""
        active_editor= self.notebook.editor_tab_get_editor()
        if active_editor.CanUndo():
            self.mainframe.editor_undo()
   
    def _on_editor_redo(self, event):
        """Redo for the current editor tab"""
        active_editor= self.notebook.editor_tab_get_editor()
        if active_editor.CanRedo():
            self.mainframe.editor_redo()
        
    def _on_editor_cut(self, event):
        """Cut for the current editor tab"""
        active_editor= self.notebook.editor_tab_get_editor()
        if active_editor.CanCut():
            self.mainframe.editor_cut()
        
    def _on_editor_copy(self, event):
        """Copy for the current editor tab"""
        active_editor= self.notebook.editor_tab_get_editor()
        if active_editor.CanCopy():
            self.mainframe.editor_copy()
    
    def _on_editor_paste(self, event):
        """paste for the current editor tab"""
        active_editor= self.notebook.editor_tab_get_editor()
        if active_editor.CanPaste():
            self.mainframe.editor_paste()
        
    def _on_editor_delete(self, event):
        """Clear for the current editor tab"""
        active_editor= self.notebook.editor_tab_get_editor()
        if active_editor.CanDelete():
            self.mainframe.editor_delete_selection()
    
    def _on_editor_selectall(self, event):
        """Selectall for the current editor tab"""
        if active_editor:
            self.mainframe.editor_selectall()
#-------------------------------------------------------------------- Menu View
    def _create_menu_view_binds(self):
        """ Creates the binds for the view menu"""
        self.mainframe.Bind(wx.EVT_MENU, self._on_view_toolbar_state,
                       id= ide.ID_SHOW_TOOLBAR)
        
    def _on_view_toolbar_state(self, event):
        self.mainframe_panel.toolbar_show(event.Checked())
#------------------------------------------------------------------ Menu search
    def _create_menu_search_binds(self):
        """ Creates the binds for the search menu"""
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_search_and_replace, 
                       id=ide.ID_SEARCH)
    
    def _on_editor_search_and_replace(self, event):
        """Replace for the current editor tab"""
        self.mainframe.editor_search_and_replace()
#--------------------------------------------------------------------- Menu run
    def _create_menu_run_binds(self):
        """ Creates the binds for the run menu"""
        self.mainframe.Bind(wx.EVT_MENU, self._on_editor_run,
                            id=ide.ID_RUNFILE)
        
    def _on_editor_run(self, event):
        """Runs selected code in a new window."""
        self.mainframe.on_run()
#--------------------------------------------------------------- Non menu binds
    def _create_remaining_binds(self):
        """ Creates the non menu binds"""
        self.view.Bind(wx.EVT_UPDATE_UI, self._evt_update_ui)
        self.mainframe.Bind(wx.EVT_CLOSE, self._on_exit_app)
             
    def _evt_update_ui(self, event):
        """Events to update the view"""

        event_id = event.GetId()
        active_editor= self.notebook.editor_tab_get_editor()
        if event_id== ide.ID_CUT:
            if active_editor:
                event.Enable(active_editor.CanCut())
            else:
                event.Enable(False)
        elif event_id== ide.ID_COPY:
            if active_editor:
                event.Enable(active_editor.CanCopy())
            else:
                event.Enable(False)
        elif event_id== ide.ID_PASTE:
            if active_editor:
                event.Enable(active_editor.CanPaste())
            else:
                event.Enable(False)
        elif event_id== ide.ID_DELETE:
            if active_editor:
                event.Enable(active_editor.CanDelete())
            else:
                event.Enable(False)
        elif event_id== ide.ID_UNDO:
            if active_editor:
                event.Enable(active_editor.CanUndo())
            else:
                event.Enable(False)
        elif event_id== ide.ID_REDO:
            if active_editor:
                event.Enable(active_editor.CanRedo())
            else:
                event.Enable(False)
        elif event_id in (ide.ID_SAVE, ide.ID_SAVEAS, ide.ID_CLOSETAB,
                          ide.ID_SEARCH, ide.ID_RUNFILE):
            if active_editor:
                event.Enable(True)
            else:
                event.Enable(False)
        else:
            event.Skip()
        
                

