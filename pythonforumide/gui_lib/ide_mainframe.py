# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob, David
"""
import os
import wx
import gui_lib.ide_menu as ide_menu
import gui_lib.ide_toolbar as ide_toolbar
import gui_lib.ide_constant as ide
from ide_notebook import Notebook
from ide_notebook_events import NotebookEvents

class MainFrame(wx.Frame):
    """Class with the GUI and GUI functions"""

    def __init__(self, *args, **kwargs):
        """Creates the frame, calls some construction methods."""
        wx.Frame.__init__(self, *args, **kwargs)
        self.config= wx.GetApp().config
        self.SetInitialSize((600,600))
        self.SetSize((int(self.config["MainFrame.Width"]),
                           int(self.config["MainFrame.Height"])))
        self.Center(wx.BOTH)
        self.CreateStatusBar()
        self.frame_sizer= wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.frame_sizer)
        self.frame_panel= wx.Panel(self, style= wx.BORDER_THEME)
        self.frame_sizer.Add(self.frame_panel, 1, wx.EXPAND|wx.ALL, 1)
        
        self.panel_sizer= wx.BoxSizer(wx.VERTICAL)
        self.frame_panel.SetSizer(self.panel_sizer)
        
        self._create_notebook_panel()
        
        self._create_menu()
        self._create_toolbar()
        #self._create_notebook_panel()
        self._start_up()
        self.Layout()
        self.Show()
           
    def _create_menu(self):
        """Creates a menu"""
        self.SetMenuBar(ide_menu.MenuBar(self))
        
    def _create_toolbar(self):
        """Creates a toolbar"""
        tb= ide_toolbar.ToolBar(self, style= wx.TB_HORIZONTAL|wx.NO_BORDER|
                                wx.TB_FLAT)
        self.SetToolBar(tb)
         
    def _create_notebook_panel(self):
        '''Create the notebook panel'''
        self.notebook = Notebook(self.frame_panel)
        NotebookEvents(self.notebook)
        self.panel_sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 0)
              
    def _start_up(self):
        '''
        Adds a new blank editor tab
        perhaps open last edited in the future, for now just open new.
        '''
        self.notebook.new_editor_tab()
        
    def on_exit(self):
        '''Handles the event triggered by the user to exit'''
        dial = wx.MessageDialog(self,'Do you really want to exit?',
                        'Exit Python IDE',
                        wx.YES_NO | wx.ICON_QUESTION)
        # TODO: we also need to work in a way of detecting if a file
        # has changed since last save/load, and if so prompt the user
        # to save before exit.
        
        self.config["MainFrame.Width"]= self.GetSize()[0]
        self.config["MainFrame.Height"]= self.GetSize()[1]
        
        if dial.ShowModal() == wx.ID_YES:
             self.Destroy()

    def get_file(self, prompt, style):
        """Abstracted method to prompt the user for a file path.
        Returns a 2-tuple consisting of directory path and file name."""
        dlg = wx.FileDialog(self, prompt, '.', '', '*.*', style)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
        else:
            # so maybe add error handling here.
            raise RuntimeError("Something has gone wrong with the dialog")
        dlg.Destroy()
        return dirname, filename

    def on_run(self, event):
        """Supposedly handles the Run Event"""
        #Not working, this is being done somewhere else (confab made it)
        from ide_outputframe import OutputFrame
        output_app = wx.PySimpleApp()
        output_frame = OutputFrame(parent = None, title="")        
        output_frame.Show()
        output_app.MainLoop()

if __name__=='__main__':
    import ide_test_app as wx_app
    app = wx_app.Wx_App(False)
    MainFrame(None, title= "Testing main frame with no events")
    app.MainLoop()
