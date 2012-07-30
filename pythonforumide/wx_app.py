"""
Created on 31 Jul 2011

@author: D.W., David, confab, bunburya
@reviewer: David
"""

import os

import wx
import gui_lib.ide_mainframe as ide_mainframe
import gui_lib.ide_mainframe_events as ide_mainframe_events
from config.config import read_config, write_config

from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from utils.version import get_free_port

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
        self.config = read_config()

    def _create_port(self):
        """Creates a free port"""
        self._port = get_free_port()

    def get_port(self):
        return self._port

    def _set_up_reactor(self):
        """Set's up the reactor"""
        reactor.registerWxApp(self)
        reactor.listenTCP(self._port, ListenFactory())

    def start_reactor(self):
        """
        Starts the reactor, bind a reference to it locally."""
        print "Port: %s" % (self.get_port())
        self.this_reactor = reactor
        reactor.run()

    def _create_mainframe(self):
        """Creates the mainframe"""
        self.mainframe = ide_mainframe.MainFrame(None, title="PF-IDE - 0.1a")
        ide_mainframe_events.MainFrameEvents(self.mainframe)

    def OnExit(self):
        """Handles the event that closes the IDE"""
        print ("App closing")
        write_config(self.config)

class ListenProtocol(Protocol):
    """Handles connections"""
    def connectionMade(self):
        print "Got connection!!!!"

    def connectionLost(self, reason):
        print "Connection closed."

class ListenFactory(Factory):
    """Handles Twisted listen protocols"""
    protocol = ListenProtocol

if __name__ == '__main__':
    if os.name == 'nt':
        try:
            import win32api
        except ImportError:
            raise Exception("Pywin32 required.")
    wx_app = Wx_App(False)
    wx_app.start_reactor()
