"""
Created on 31 Jul 2011

@author: Main, David
"""

import wx

class MissingArt(object):
    """Handles missing icons"""
    def __init__(self, f):
        self.f = f
        
    def __call__(self):
        try:
            return self.f()
        except AttributeError:
            return wx.NullBitmap

def get_icon_new():
    """Returns a (24,24) new icon bmp"""
    return _get_art_bmp(wx.ART_NEW)

def get_icon_open():
    """Returns a (24,24) open icon bmp"""
    return _get_art_bmp(wx.ART_FILE_OPEN)

def get_icon_save():
    """"Returns a (24,24) save icon bmp"""
    return _get_art_bmp(wx.ART_FILE_SAVE)

def get_icon_saveas():
    """Returns a (24,24) saveas icon bmp"""
    return _get_art_bmp(wx.ART_FILE_SAVE_AS)

def get_icon_cut():
    """Returns a (24,24) cut icon bmp"""
    return _get_art_bmp(wx.ART_CUT)

def get_icon_copy():
    """Returns a (24,24) copy icon bmp"""
    return _get_art_bmp(wx.ART_COPY)

def get_icon_paste():
    """Returns a (24,24) paste icon bmp"""
    return _get_art_bmp(wx.ART_PASTE)

def get_icon_undo():
    """Returns a (24,24) undo icon bmp"""
    return _get_art_bmp(wx.ART_UNDO)

def get_icon_redo():
    """Returns a (24,24) redo icon bmp"""
    return _get_art_bmp(wx.ART_REDO)

@MissingArt
def get_icon_close():
    """Returns a (24,24) close icon bmp"""
    return _get_art_bmp(wx.ART_CLOSE)

def get_icon_quit():
    """Returns a (24,24) quit icon bmp"""
    return _get_art_bmp(wx.ART_QUIT)

def get_icon_delete():
    """Returns a (24,24) delete icon bmp"""
    return _get_art_bmp(wx.ART_DELETE)

def get_find_and_replace():
    """Returns a (24,24) find and replace icon bmp"""
    return _get_art_bmp(wx.ART_FIND_AND_REPLACE)

def _get_art_bmp(art_id):
    """Returns the passed in art_id as a (24,24) icon bmp"""
    return wx.ArtProvider.GetBitmap(art_id, wx.ART_TOOLBAR, (24,24))
