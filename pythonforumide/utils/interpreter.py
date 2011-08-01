# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:05:42 2011

@author: jakob
"""
import sys
sys.path.append('..')

from twisted.internet.protocol import ProcessProtocol

class PythonProcessProtocol(ProcessProtocol):       
    def __init__(self, frame):
        self.frame = frame
        
    def connectionMade(self):
        print "subprocess open.!"

    def connectionLost(self, reason):
        self.frame.Newline()
        self.frame.WriteText("\n\nExited with code 0")
    
    def outReceived(self, data):
        self.frame.WriteText(data)
        print "Got stdout."
    
    def errReceived(self, data):
        print "Got stderr!"
        self.frame.Newline()
        self.frame.BeginTextColour("Red")
        self.frame.WriteText(data)                
        
    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
