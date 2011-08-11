# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob, David, confab
@reviewer: ghoulmaster
"""

import os
import wx
import wx.lib.agw.flatnotebook as fnb
from ide_editor import EditorPanel

class NoteBookPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Create a panel with a containing NoteBook control"""
        super(NoteBookPanel, self).__init__(*args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self._create_notebook(sizer)
            
    def _create_notebook(self, sizer):
        """ Creates the NoteBook control"""
        ctrl = NoteBook(self, agwStyle=fnb.FNB_X_ON_TAB | 
                fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_TAB_FOCUS | fnb.FNB_VC8,
                pos=(-100, -100))
        sizer.Add(ctrl, 1 , wx.EXPAND | wx.ALL, 0)
        self.notebook = ctrl

class NoteBook(fnb.FlatNotebook):
    def __init__(self, *args, **kwargs):
        super(NoteBook, self).__init__(*args, **kwargs)
        self._active_editor = None
        self._active_tab_index = None

    def editor_tab_new(self, page_name=""):
        """Opens a new editor tab"""
        editor_panel = EditorPanel(self)
        self.AddPage(editor_panel, page_name)
        self._active_editor = editor_panel.editor
        self.editor_tab_name_untitled_tabs()
        wx.CallAfter(self.SetSelection, self.GetPageCount() - 1)
        return editor_panel.editor
        
    def editor_tab_open_file(self, dirname, filename):
        """Loads a slected file into a new editor tab"""
        
        if dirname and filename:
            editor = self.editor_tab_new(filename)
            path = os.path.join(dirname, filename)
            editor.load_file(path)
            
    def editor_tab_close_active(self):
        """Closes the currently active editor tab"""
        self.DeletePage(self._active_tab_index)
        wx.CallAfter(self.editor_tab_name_untitled_tabs)
        
    def editor_tab_get_editor(self):
        """ Returns the currently active editor instance or None"""           
        return self._active_editor
                
    def editor_tab_set_active_tab_text(self, text):
        """Rename the currently active tab text"""
        if self._active_tab_index > -1:
            self.SetPageText(self._active_tab_index, text)
        
    def editor_tab_name_untitled_tabs(self):
        """Renumbers the untitled pages"""
        self.Freeze()
        empty_page_no = 1
        for page_no in xrange(self.GetPageCount()):
            page_text = self.GetPageText(page_no)
            if "Untitled" in page_text or not page_text:
                page = self.GetPage(page_no)
                self.SetPageText(page_no, "Untitled%s.py" % (empty_page_no))
                empty_page_no += 1
        self.Thaw()

    def active_editor_can_cut(self):
        """Returns True if the active editor can cut"""
        try:
            if self._active_editor:
                return self._active_editor.CanCut()
            else:
                return False
        except AttributeError:
            return True
    
    def active_editor_can_copy(self):
        """Returns True if the active editor can copy"""
        try:
            if self._active_editor:
                return self._active_editor.CanCopy()
            else:
                return False
        except AttributeError:
            return True
    
    def active_editor_can_paste(self):
        """Returns True if the active editor can paste"""
        if self._active_editor:
            return self._active_editor.CanPaste()
        else:
            return False
        
    def active_editor_can_delete(self):
        """Returns True if the active editor can delete"""
        try:
            if self._active_editor:
                return self._active_editor.HasSelection()
            else:
                return False
        except AttributeError:
            return True
    

if __name__ == '__main__':
    import ide_test_app as wx_app
    import ide_simple_frame 
    app = wx_app.Wx_App(False)
    frame = ide_simple_frame.SimpleFrame(None,
                                       title="Testing notebook without events")
    panel = NoteBookPanel(frame)
    frame.sizer.Add(panel, 1, wx.EXPAND)
    panel.notebook.editor_tab_new()
    frame.Layout()
    app.MainLoop()
