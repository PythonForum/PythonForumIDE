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
        
    def outReceived(self, data):
        self.frame.WriteText(data)
        print "Got stdout."
    
    def errRecieved(self, data):
        print "Got stderr!"
