"""
Created on 31 Jul 2011

@author: D.W., David
@reviewer: david
"""

import wx
import ide_constant as ide
from ide_images import menu_icons

class MenuBar(wx.MenuBar):
    """Creates a menubar"""
    def __init__(self, parent):
        super(MenuBar, self).__init__()
        self._parent = parent
        self._add_file_menu()
        self._add_edit_menu()
        self._add_search_menu()
        self._add_run_menu()
        
        #self._parent.SetMenuBar(self)
         
    def _add_file_menu(self):
        """Adds the file menu"""
        fileMenu = wx.Menu()
        self._add_menu_item(fileMenu, ide.ID_NEW,
                            ide.id_text_new, menu_icons.get_icon_new())
        
        fileMenu.AppendSeparator()
        
        self._add_menu_item(fileMenu, ide.ID_OPEN,
                            ide.id_text_open, menu_icons.get_icon_open())
        
        fileMenu.AppendSeparator()
        
        self._add_menu_item(fileMenu, ide.ID_SAVE,
                            ide.id_text_save, menu_icons.get_icon_save())

        self._add_menu_item(fileMenu, ide.ID_SAVEAS,
                            ide.id_text_saveas, menu_icons.get_icon_saveas())
        
        fileMenu.AppendSeparator()
        
        self._add_menu_item(fileMenu, ide.ID_CLOSETAB,
                            ide.id_text_closetab, menu_icons.get_icon_close())

        self._add_menu_item(fileMenu, ide.ID_EXITAPP, ide.id_text_exitapp, 
                            menu_icons.get_icon_quit())

        self.Append(fileMenu, "&File")
        
    def _add_edit_menu(self):
        """Adds the edit menu"""
        editMenu = wx.Menu()
        
        self._add_menu_item(editMenu, ide.ID_UNDO,
                            ide.id_text_undo, menu_icons.get_icon_undo())
        
        self._add_menu_item(editMenu, ide.ID_REDO,
                            ide.id_text_redo, menu_icons.get_icon_redo())

        editMenu.AppendSeparator()
        
        self._add_menu_item(editMenu, ide.ID_CUT,
                            ide.id_text_cut, menu_icons.get_icon_cut())
        
        self._add_menu_item(editMenu, ide.ID_COPY,
                            ide.id_text_copy, menu_icons.get_icon_copy())
        
        self._add_menu_item(editMenu, ide.ID_PASTE,
                            ide.id_text_paste, menu_icons.get_icon_paste())
        
        self._add_menu_item(editMenu, ide.ID_DELETE,
                            ide.id_text_delete, menu_icons.get_icon_delete())

        editMenu.AppendSeparator()
        
        self._add_menu_item(editMenu, ide.ID_SELECTALL, ide.id_text_selectall)
        
        self.Append(editMenu, "&Edit")
        
    def _add_search_menu(self):
        """Adds the search menu"""
        searchMenu = wx.Menu()
        
        self._add_menu_item(searchMenu, ide.ID_SEARCH,
                            ide.id_text_search, 
                            menu_icons.get_find_and_replace())
        
        self.Append(searchMenu, "&Search")
        
    def _add_run_menu(self):
        """Adds the run menu"""
        runMenu = wx.Menu()
        
        self._add_menu_item(runMenu, ide.ID_RUNFILE,
                            ide.id_text_runfile)
        
        self.Append(runMenu, "&Run")
        
    def _add_menu_item(self, parent_menu, id, id_text, icon_bmp= None):
        """Adds a menu item to the parent_menu"""
        item= wx.MenuItem(parent_menu, id, id_text.menu, id_text.status, 
                          id_text.menu_kind)
        if icon_bmp:
            item.SetBitmap(icon_bmp)
        parent_menu.AppendItem(item)
