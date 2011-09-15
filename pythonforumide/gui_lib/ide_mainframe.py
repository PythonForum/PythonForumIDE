# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob, David, confab
"""
import wx
import os

from ide_menu import MenuBar
from ide_constant import ID_SHOW_TOOLBAR
from ide_toolbar import ToolBarPanel
from ide_mainframe_panel import MainFramePanel
from ide_replace_frame import ReplaceFrame
from utils.interpreter import PythonProcessProtocol
from utils.version import get_python_exe

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class MainFrame(wx.Frame):
    """Class with the GUI and GUI functions"""

    def __init__(self, *args, **kwargs):
        """Creates the frame, calls some construction methods."""
        super(MainFrame, self).__init__(*args, **kwargs)
        self._config = wx.GetApp().config
        self._create_menu()
        self.SetInitialSize((600,600))
        self.CreateStatusBar()
        self._frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frame_panel = wx.Panel(self)
        self._frame_sizer.Add(self._frame_panel, 1, wx.EXPAND)
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._frame_panel.SetSizer(self._sizer)
        self._create_main_panel()
        self.SetSizer(self._frame_sizer)
        self._apply_config_settings()
        self.Layout()
        self.Show()

    def _create_menu(self):
        """Creates a menu"""
        self.SetMenuBar(MenuBar(self))

    def _create_main_panel(self):
        self._sizer.AddSpacer((-1, 2))
        ctrl = MainFramePanel(self._frame_panel)
        self._sizer.Add(ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.mainframe_panel = ctrl
        self._sizer.AddSpacer((-1, 2))
        self.notebook = ctrl.notebook
        self.console = ctrl.console_rich_text

    def _apply_config_settings(self):
        """ Applys the stored config values"""
        self.SetSize((self._config["MainFrame.Width"],
                      self._config["MainFrame.Height"]))
        self.MoveXY(self._config["MainFrame.XPos"],
                    self._config["MainFrame.YPos"])
        self.menu_view_toolbar_show(self._config["MainMenu.View.Toolbar.Show"])

    def _store_config_settings(self):
        """ Stores the current config values"""
        width, height = self.GetSizeTuple()
        self._config["MainFrame.Width"] = width
        self._config["MainFrame.Height"] = height
        xpos, ypos = self.GetPositionTuple()
        self._config["MainFrame.XPos"] = xpos
        self._config["MainFrame.YPos"] = ypos
        self._config["MainMenu.View.Toolbar.Show"] = \
                self.MenuBar.IsChecked(ID_SHOW_TOOLBAR)

    def editor_tab_get_editor(self):
        """Returns the currently active editor instance from notebook"""
        return self.notebook.editor_tab_get_editor()

    def editor_open_file(self):
        """ Opens a dialof to chose the file to open"""
        dirname, filename = self.file_dialog("Open a file", wx.OPEN)
        self.notebook.editor_tab_open_file(dirname, filename)

    def editor_save(self):
        """Saves the currently active editor file"""
        active_editor = self.editor_tab_get_editor()
        if active_editor.filepath:
            active_editor.save_file()
        else:
            self.save_as_active_editor()

    def editor_save_as(self):
        """Save as for the currently active editor file"""
        dirname, filename = self.file_dialog("Save file as", wx.SAVE)
        if dirname and filename:
            path = os.path.join(dirname, filename)
            if path:
                active_editor= self.editor_tab_get_editor()
                if active_editor.save_file_as(path):
                    self.notebook.editor_tab_set_active_tab_text(filename)
                    active_editor.filepath = path

    def editor_undo(self):
        """Undo changes in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.Undo()

    def editor_redo(self):
        """Redo changes in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.Redo()

    def editor_cut(self):
        """Cut changes in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.Cut()

    def editor_copy(self):
        """Copy changes in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.Copy()

    def editor_paste(self):
        """Paste changes in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.Paste()

    def editor_delete_selection(self):
        """Deletes the selection in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.Clear()

    def editor_selectall(self):
        """Selectall in active editor"""
        active_editor = self.editor_tab_get_editor()
        if active_editor:
            active_editor.SelectAll()

    def editor_search_and_replace(self):
        """ Search and replace in active editor"""
        # Create a search frame and hook into the caller.
        # Allows this frame to be destroyed by the main window on close.
        active_editor = self.editor_tab_get_editor()
        replace_frame = ReplaceFrame(active_editor, self,
                                     title = "Find and Replace",
                                     size = (410, 150))
        replace_frame.Layout()

    def on_run(self):
        """Runs selected code in a new window."""
        # Create a test frame and hook into the caller.
        # Allows this frame to be destroyed by the main window on close.
        reactor = wx.GetApp().this_reactor

#       run_editor = SimpleFrame(wx.GetApp().TopWindow, title="")
#       run_panel = wx.richtext.RichTextCtrl(run_editor, style=wx.TE_READONLY)
#       run_editor.sizer.Add(run_panel, 1, wx.EXPAND)
#       run_editor.Layout()

        run_panel = self.console
        active_editor = self.editor_tab_get_editor()

        if active_editor.filepath:
            if active_editor.GetModify():
                active_editor.SaveFile(active_editor.filepath)
            filename = os.path.split(active_editor.filepath)[1]
            run_panel.WriteText("Running %s" % filename)
            run_panel.Newline()
            reactor.spawnProcess(PythonProcessProtocol(run_panel),
                                 get_python_exe(),
                                 ["python", str(active_editor.filepath)])

        else:
            run_panel.WriteText("Running unsaved script.")
            run_panel.Newline()
            script = StringIO()
            script.write(active_editor.GetText())
            script.seek(0)
            scr = script.read().replace("\r", '')

            reactor.spawnProcess(PythonProcessProtocol(run_panel),
                                 get_python_exe(),
                                 ["python", "-c", scr])

        return run_panel
#===============================================================================
# Mainframe actions
#===============================================================================
    def ask_exit(self):
        """Asks the user if he really wants to quit"""
        dial = wx.MessageDialog(None, "Do you really want to exit?",
                                "Exit Hex Baker", wx.YES_NO | wx.ICON_QUESTION)

        if dial.ShowModal() == wx.ID_YES:
            self._store_config_settings()
            self.Destroy()

    def on_exit(self):
        """Handles the event triggered by the user to exit"""
        try:
            current_text = self.editor_tab_get_editor().GetText()

            #Right now, this check if the current open file (the viewable tab)
            #has been saved or not. If not, prompt the user about quitting
            #If it has, just quit

            #TODO Check all tabs, not just the current one

            if self.editor_tab_get_editor().GetModify() == 1:
                return self.ask_exit()

            self._store_config_settings()
            return self.Destroy()
        except AttributeError:
            self._store_config_settings()
            return self.Destroy()

    def file_dialog(self, prompt, style):
        """Abstracted method to prompt the user for a file path.
        Returns a 2-tuple consisting of directory path and file name."""

        # TODO: we also need to work in a way of detecting if a file
        # has changed since last save/load, and if so prompt the user
        # to save before exit. (Yoriz - building on the above id like it
        # only to ask if there are unsaved changes otherwise just close
        # it can get anoying having to click ok every time you want to close)

        #The dialog is able to open any kind of files, even without extension
        dlg = wx.FileDialog(self, prompt, '.', '', '*', style)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
            dlg.Destroy()
            return dirname, filename
        else:
            return "", "" #Cancels the action
#===============================================================================
# state setters
#===============================================================================
    def menu_view_toolbar_show(self, enable = True):
        """Hides or shows the toolbar"""
        self.MenuBar.Check(ID_SHOW_TOOLBAR, enable)
        self.mainframe_panel.toolbar_show(enable)
