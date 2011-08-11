"""
Created on 31 Jul 2011

@author: Main, David
"""

import wx

class MissingArt(object):
    """Sometimes wx doesn't have some attributes, this is caused with different
    wx versions, this decorator wraps each function call in a try/except and
    returns NullBitmap for everything that is not an attribute of wx."""
    def __init__(self, f):
        self.f = f
        
    def __call__(self):
        try:
            return self.f()
        except AttributeError:
            return wx.NullBitmap

@MissingArt
def get_icon_new():
    """Returns a new icon bmp"""
    return _get_art_bmp(wx.ART_NEW)

@MissingArt
def get_icon_open():
    """Returns a open icon bmp"""
    return _get_art_bmp(wx.ART_FILE_OPEN)

@MissingArt
def get_icon_save():
    """"Returns a save icon bmp"""
    return _get_art_bmp(wx.ART_FILE_SAVE)

@MissingArt
def get_icon_saveas():
    """Returns a saveas icon bmp"""
    return _get_art_bmp(wx.ART_FILE_SAVE_AS)

@MissingArt
def get_icon_cut():
    """Returns a cut icon bmp"""
    return _get_art_bmp(wx.ART_CUT)

@MissingArt
def get_icon_copy():
    """Returns a copy icon bmp"""
    return _get_art_bmp(wx.ART_COPY)

@MissingArt
def get_icon_paste():
    """Returns a paste icon bmp"""
    return _get_art_bmp(wx.ART_PASTE)

@MissingArt
def get_icon_undo():
    """Returns a undo icon bmp"""
    return _get_art_bmp(wx.ART_UNDO)

def get_icon_redo():
    """Returns a redo icon bmp"""
    return _get_art_bmp(wx.ART_REDO)

@MissingArt
def get_icon_close():
    """Returns a close icon bmp"""
    return _get_art_bmp(wx.ART_CLOSE)

@MissingArt
def get_icon_quit():
    """Returns a quit icon bmp"""
    return _get_art_bmp(wx.ART_QUIT)

@MissingArt
def get_icon_delete():
    """Returns a delete icon bmp"""
    return _get_art_bmp(wx.ART_DELETE)

@MissingArt
def get_find_and_replace():
    """Returns a find and replace icon bmp"""
    return _get_art_bmp(wx.ART_FIND_AND_REPLACE)

def _get_art_bmp(art_id):
    """Returns the passed in art_id as a icon bmp"""
    return wx.ArtProvider.GetBitmap(art_id, wx.ART_TOOLBAR, (16, 16))
