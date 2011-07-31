'''
Created on 31 Jul 2011

@author: Main
'''

import wx
from pythonforumide.config.config import Ide_config

class Wx_App(wx.App):
    def __init__(self, *args, **kwargs):
        '''
        Creates a test wx App
        '''
        super(Wx_App, self).__init__(*args, **kwargs)
        self._create_config()
        
    def _create_config(self):
        '''
        Set up config
        '''
        self.config= Ide_config()
  
    def OnExit(self):
        print ("App closing")
        self.config.update_configfile()