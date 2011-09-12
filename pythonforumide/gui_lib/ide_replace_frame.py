# -*- coding: utf-8 -*-
"""
Created Sun Sep 11 14:16:42 2011

@author: David
"""

import wx
import string
from itertools import izip_longest

from ide_simple_frame import SimpleFrame
from ide_constant import ID_FIND_CANCEL, ID_FIND_REPLACE_ALL, ID_FIND_REPLACE

class ReplaceFrame(wx.Dialog):
    """Class with the GUI and the GUI functions"""

    def __init__(self, active_editor, *args, **kwargs):
        """"Displays the frame, creates the GUI"""
        super(ReplaceFrame, self).__init__(*args, **kwargs)
        self.active_editor = active_editor
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel = ReplaceFramePanel(self)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

        self.Show()

    def on_cancel(self, event):
        """Destroys the frame when user hits Cancel button"""
        self.Destroy()

class ReplaceFramePanel(wx.Panel):
    """Replace Frame Panel, creates GUI, handles events"""

    def __init__(self, parent):
        """Displays the frame, creates the GUI, inherits variables"""
        super(ReplaceFramePanel, self).__init__(parent)
        self.Bind(wx.EVT_KEY_UP, self.on_key_down)
        self.sizer= wx.BoxSizer(wx.HORIZONTAL)
        self._create_vsizer(self.sizer)
        self._create_buttons(self.sizer)
        self.SetSizer(self.sizer)
        self.Layout()
        self.set_binds()
        self.active_editor = self.GetParent().active_editor

    def _create_vsizer(self, sizer):
        """Creates the vertical sizer for the GUI"""
        vsizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vsizer)
        vsizer.AddSpacer((-1, 10))
        self._create_inputs(vsizer)
        vsizer.AddSpacer((-1, 10))
        self._create_options(vsizer)
        vsizer.AddSpacer((-1, 10))

    def _create_inputs(self, sizer):
        """Draws the input textboxes"""
        grid_sizer = wx.FlexGridSizer(cols = 2, vgap = 10, hgap =10)
        sizer.Add(grid_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        ctrl = wx.StaticText(self, label = "Search for:")
        grid_sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        self.txt_to_replace = wx.TextCtrl(self, size = (150, -1))
        grid_sizer.Add(self.txt_to_replace, 0,
                       wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        self.ctrl_txt_exisiting = ctrl
        ctrl = wx.StaticText(self, label = "Replace with:")
        grid_sizer.Add(ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        self.txt_replace_with = wx.TextCtrl(self, size = (150, -1))
        grid_sizer.Add(self.txt_replace_with, 0,
                       wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        self.ctrl_txt_new = ctrl

    def _create_buttons(self, sizer):
        """Draws the event buttons"""
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box_sizer)
        box_sizer.AddSpacer((-1, 10))
        ctrl = wx.Button(self, label = "Find next")
        box_sizer.Add(ctrl, 0, wx.LEFT | wx.RIGHT, 10)
        self.btn_next = ctrl
        box_sizer.AddSpacer((-1, 5))
        ctrl = wx.Button(self, id = ID_FIND_REPLACE, label = "Replace")
        box_sizer.Add(ctrl, 0, wx.LEFT | wx.RIGHT, 10)
        self.btn_replace = ctrl
        box_sizer.AddSpacer((-1, 5))
        ctrl = wx.Button(self, id = ID_FIND_REPLACE_ALL, label = "Replace all")
        box_sizer.Add(ctrl, 0, wx.LEFT | wx.RIGHT, 10)
        self.btn_replace_all = ctrl
        box_sizer.AddSpacer((-1, 5))
        ctrl= wx.Button(self, id = ID_FIND_CANCEL, label = "Cancel")
        box_sizer.Add(ctrl, 0, wx.LEFT | wx.RIGHT, 10)
        self.btn_cancel = ctrl
        box_sizer.AddSpacer((-1, 10))

    def on_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.GetParent().Destroy()
        event.Skip()

    def set_binds(self):
        """Binds the events for the panel and the frame"""
        self.Bind(wx.EVT_BUTTON, self.GetParent().on_cancel, id=ID_FIND_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.on_replace, id = ID_FIND_REPLACE)
        self.Bind(wx.EVT_BUTTON, self.on_replace_all, id = ID_FIND_REPLACE_ALL)

    def _create_options(self, sizer):
        """Draws the checkboxes for options"""
        box_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(box_sizer)
        ctrl = wx.CheckBox(self, label = " Match whole word only")
        box_sizer.Add(ctrl, 0, wx.LEFT|wx.RIGHT, 10)
        self.check_whole_word = ctrl
        box_sizer.AddSpacer((-1, 10))
        self.case_check= wx.CheckBox(self, label = " Match case")
        box_sizer.Add(self.case_check, 0, wx.LEFT | wx.RIGHT, 10)
        self.check_match_case = ctrl

    def on_replace(self, event):
        """Replaces text on the current editor (self.active_editor)"""
        str_to_replace = self.txt_to_replace.GetValue()
        str_replace_with = self.txt_replace_with.GetValue()

        if str_to_replace or str_replace_with == "":
            return

        current_position = self.active_editor.GetCurrentPos()
        last_position = len(self.active_editor.GetText())

        active_text = self.active_editor.GetTextRange(current_position,
                                                      last_position)
        first_part_of_text = self.active_editor.GetTextRange(0,
                                                             current_position)

        new_text = self.replace(active_text, str_to_replace, str_replace_with)
        self.active_editor.SetText(first_part_of_text + new_text)

        self.GetParent().Destroy()

    def replace(self, text, to_replace, replace_width):
        """Replaces 'to_replace' by 'replace_width' on 'text'"""
        if self.case_check.GetValue(): #If case sensitive on
            return text.replace(to_replace, replace_width)
        else: #If case sensitive disabled
            return self.incase_replace(text, to_replace, replace_width)

    def on_replace_all(self, event):
        """Replaces on the whole document"""
        str_to_replace = self.txt_to_replace.GetValue()
        str_replace_with = self.txt_replace_with.GetValue()

        if str_to_replace or str_replace_with == "":
            return

        active_text = self.active_editor.GetText()

        new_text = self.replace(active_text, str_to_replace, str_replace_with)
        self.active_editor.SetText(new_text)

        self.GetParent().Destroy()

    def incase_replace(self, text, x, y):
        """Replaces x with y in an non case sensitive way"""
        x = x.lower()
        idx = text.lower().find(x)
        while idx != -1:
            text =  text[:idx] + y + text[idx+len(x):]
            idx = st.lower().find(x)
        return text
