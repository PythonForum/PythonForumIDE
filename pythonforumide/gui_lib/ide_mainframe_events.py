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
        self._create_binds()
      
    def _create_binds(self):
        """Create binds"""
        self.view.Bind(wx.EVT_UPDATE_UI, self._evt_update_ui)
        self.view.Bind(wx.EVT_MENU, self._on_new, id=ide.ID_NEW)
        self.view.Bind(wx.EVT_MENU, self._on_open, id=ide.ID_OPEN)  
        self.view.Bind(wx.EVT_MENU, self._on_exit, id=ide.ID_EXITAPP)
        self.view.Bind(wx.EVT_MENU, self._on_save, id=ide.ID_SAVE)
        self.view.Bind(wx.EVT_MENU, self._on_save_as, id=ide.ID_SAVEAS)
        self.view.Bind(wx.EVT_CLOSE, self._on_exit)
        self.view.Bind(wx.EVT_MENU, self._on_editor_close, id=ide.ID_CLOSETAB)
        self.view.Bind(wx.EVT_MENU, self._on_editor_undo, id=ide.ID_UNDO)
        self.view.Bind(wx.EVT_MENU, self._on_editor_redo, id=ide.ID_REDO)
        self.view.Bind(wx.EVT_MENU, self._on_editor_cut, id=ide.ID_CUT)
        self.view.Bind(wx.EVT_MENU, self._on_editor_copy, id=ide.ID_COPY)
        self.view.Bind(wx.EVT_MENU, self._on_editor_paste, id=ide.ID_PASTE)
        self.view.Bind(wx.EVT_MENU, self._on_editor_delete, id=ide.ID_DELETE)
        self.view.Bind(wx.EVT_MENU, self._on_editor_selectall, 
                       id=ide.ID_SELECTALL)
        self.view.Bind(wx.EVT_MENU, self._on_editor_search_and_replace, 
                       id=ide.ID_SEARCH)
        self.view.Bind(wx.EVT_MENU, self._on_editor_run, id=ide.ID_RUNFILE)        
    
    def _on_new(self, event):
        """Opens a new tab with a new editor instance"""
        self.view.notebook.new_editor_tab()
    
    def _on_open(self, event):
        """Opens a new tab and ask for a file to load"""
        self.view.notebook.open_editor_tab()
    
    def _on_editor_close(self, event):
        """Closes the current editor tab"""
        self.view.notebook.close_active_editor()
        
    def _on_save(self, event):
        """Saves the currently active file"""
        self.view.notebook.save_active_editor_tab()
        
    def _on_save_as(self, event):
        """Save as required filename"""
        self.view.notebook.save_as_active_editor_tab()
    
    def _on_editor_undo(self, event):
        """Undo for the current editor tab"""
        self.view.notebook.undo_active_editor()
   
    def _on_editor_redo(self, event):
        """Redo for the current editor tab"""
        self.view.notebook.redo_active_editor()
        
    def _on_editor_cut(self, event):
        """Cut for the current editor tab"""
        self.view.notebook.cut_active_editor()
        
    def _on_editor_copy(self, event):
        """Copy for the current editor tab"""
        self.view.notebook.copy_active_editor()
    
    def _on_editor_paste(self, event):
        """paste for the current editor tab"""
        self.view.notebook.paste_active_editor()
        
    def _on_editor_delete(self, event):
        """Clear for the current editor tab"""
        self.view.notebook.clear_active_editor()
    
    def _on_editor_selectall(self, event):
        """Selectall for the current editor tab"""
        self.view.notebook.selectall_active_editor()
        
    def _on_editor_search_and_replace(self, event):
        """Replace for the current editor tab"""
        self.view.notebook.replace_active_editor()
    
    def _on_exit(self, event):
        """ application wants to exit"""
        self.view.on_exit()
    
    def _on_editor_run(self, event):
        """Runs selected code in a new window."""
        self.view.notebook.run_active_editor()
         
    def _evt_update_ui(self, event):
        """Events to update the view"""
        event_id = event.GetId()
        if event_id== ide.ID_CUT:
            event.Enable(self.view.notebook.active_editor_can_cut())
        elif event_id== ide.ID_COPY:
            event.Enable(self.view.notebook.active_editor_can_copy())
        elif event_id== ide.ID_PASTE:
            event.Enable(self.view.notebook.active_editor_can_paste())
        elif event_id== ide.ID_DELETE:
            event.Enable(self.view.notebook.active_editor_can_delete())
        elif event_id== ide.ID_UNDO:
            event.Enable(self.view.notebook.active_editor_can_undo())
        elif event_id== ide.ID_REDO:
            event.Enable(self.view.notebook.active_editor_can_redo())
        elif event_id== ide.ID_SAVE:
            event.Enable(self.view.notebook.active_editor_can_save())
        elif event_id== ide.ID_SAVEAS:
            event.Enable(self.view.notebook.active_editor_can_saveas())
        elif event_id== ide.ID_CLOSETAB:
            event.Enable(self.view.notebook.active_editor_can_close_tab())
        elif event_id== ide.ID_SEARCH:
            event.Enable(self.view.notebook.active_editor_can_search())
        elif event_id== ide.ID_RUNFILE:
            event.Enable(self.view.notebook.active_editor_can_run())
        else:
            event.Skip()
