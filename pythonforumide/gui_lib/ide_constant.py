"""
Created on 31 Jul 2011

@author: D.W.
"""

import wx
from collections import namedtuple as _nt

_id_text= _nt("id_text", "menu toolbar status menu_kind")

#===============================================================================
#  File ID
#===============================================================================
ID_NEW= wx.NewId()
id_text_new= _id_text("New\tCtrl+N", "New",
                      "Create a new file", wx.ITEM_NORMAL)

ID_OPEN= wx.NewId()
id_text_open= _id_text("Open\tCtrl+O", "Open",
                       "Open an existing file", wx.ITEM_NORMAL)

ID_SAVE= wx.NewId()
id_text_save= _id_text("Save\tCtrl+S", "Save",
                       "Save the current file", wx.ITEM_NORMAL)

ID_SAVEAS= wx.NewId()
id_text_saveas= _id_text("Save as", "Save as",
                         "Save as a new filename", wx.ITEM_NORMAL)

ID_CLOSETAB= wx.NewId()
id_text_closetab= _id_text("Close tab\tCtrl+W", "Close tab",
                           "Close current tab", wx.ITEM_NORMAL)

ID_EXITAPP= wx.NewId()
id_text_exitapp= _id_text("Exit\tCtrl+Q", "Exit",
                          "Exit the application", wx.ITEM_NORMAL)
#===============================================================================
#  Edit ID
#===============================================================================
ID_UNDO= wx.NewId()
id_text_undo= _id_text("Undo\tCtrl+Z", "Undo",
                       "Undo changes", wx.ITEM_NORMAL)

ID_REDO= wx.NewId()
id_text_redo= _id_text("Redo\tCtrl+Y", "Redo",
                       "Redo Changes", wx.ITEM_NORMAL)

ID_CUT= wx.NewId()
id_text_cut= _id_text("Cut\tCtrl+X", "Cut",
                      "Cut the selected text", wx.ITEM_NORMAL)

ID_COPY= wx.NewId()
id_text_copy= _id_text("Copy\tCtrl+C", "Copy",
                       "Copy the selected text", wx.ITEM_NORMAL)

ID_PASTE= wx.NewId()
id_text_paste= _id_text("Paste\tCtrl+V", "Paste",
                        "Paste from clipboard", wx.ITEM_NORMAL)

ID_DELETE= wx.NewId()
id_text_delete= _id_text("Delete", "Delete",
                         "Delete the selected text", wx.ITEM_NORMAL)

ID_SELECTALL= wx.NewId()
id_text_selectall= _id_text("Select All\tCtrl+A",
                            "Select all", "Select all", wx.ITEM_NORMAL)
#===============================================================================
#  View ID
#===============================================================================
ID_SHOW_TOOLBAR = wx.NewId()
id_show_toolbar = _id_text("Show Toolbar", "Show Toolbar", "Show Toolbar",
                           wx.ITEM_CHECK)
#===============================================================================
#  Search ID
#===============================================================================
ID_SEARCH= wx.NewId()
id_text_search= _id_text("Replace\tCtrl+H", "Replace",
                         "Find and replace in the active file", wx.ITEM_NORMAL)
#===============================================================================
#  Run ID
#===============================================================================
ID_RUNFILE=wx.NewId()
id_text_runfile= _id_text("Run file\tF5", "Run",
                          "Run the active file", wx.ITEM_NORMAL)
#===============================================================================
#  Find and Replace IDs
#===============================================================================
ID_FIND_CANCEL = wx.NewId()
ID_FIND_REPLACE_ALL = wx.NewId()
