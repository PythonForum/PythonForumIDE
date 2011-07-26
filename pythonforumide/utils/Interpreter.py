# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:05:42 2011

@author: jakob
"""
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import subprocess
import version

class Interpreter(object):
    def __init__(self):
        self.python = subprocess.Popen(version.get_python_exe(), 
                                       stdout = StringIO(),
                                        stderr = StringIO())        
        
    def write(self, data):
        print data
    

class IPythonInterpreter(Interpreter):
    """In the future we might be embedding IPython"""
    pass

class BPythonInterpreter(Interpreter):
    """In the future we might be embedding BPython"""
    pass

i = Interpreter()