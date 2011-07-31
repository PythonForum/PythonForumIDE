"""
Created on 31 Jul 2011

@author: D.W., david
@reviewer: david
"""

import wx
import gui_lib.ide_mainframe as ide_mainframe
import gui_lib.ide_mainframe_events as ide_mainframe_events
from config.config import Ide_config

#import config.config.Ide_config as Ide_config
from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from utils.version import get_free_port
from utils.interpreter import spawn_python

class Wx_App(wx.App):
    """Sets the editor up and the ports""" #Not sure if correct description
    def __init__(self, *args, **kwargs):
        """Creates a wx App"""
        super(Wx_App, self).__init__(*args, **kwargs)
        self._create_config()
        self._create_port()
        self._set_up_reactor()
        self._create_mainframe()
        
    def _create_config(self):
        """Set up config"""
        self.config = Ide_config()
        
    def _create_port(self):
        """Creates a free port"""
        self._port = get_free_port()
        
    def get_port(self):
        return self._port
    
    def _set_up_reactor(self):
        """Set's up the reactor"""
        reactor.registerWxApp(self)
        reactor.listenTCP(self._port, ListenFactory())
        reactor.spawnProcess(*spawn_python())
        #frame.Maximize() #Left commented to stop it getting on my nerves.
        
    def start_reactor(self):
        '''
        Sarts the reactor
        '''
        print "Port: %s" % (self.get_port())
        reactor.run()
        
    def _create_mainframe(self):
        """Creates the mainframe"""
        self.mainframe = ide_mainframe.MainFrame(None, title='PF-IDE - 0.1a')
        ide_mainframe_events.MainFrameEvents(self.mainframe)
        
    def OnExit(self):
        print ("App closing")
        self.config.update_configfile()
        
        
class ListenProtocol(Protocol):
    def connectionMade(self):
        print "Got connection!!!!"
        
    def connectionLost(self, reason):
        print "Connection closed."

class ListenFactory(Factory):
    protocol = ListenProtocol
    
if __name__ == '__main__':
    wx_app = Wx_App(False)
    wx_app.start_reactor()
