"""
Created on Mon Jul 16 2012
@author: bunburya
"""

from os.path import join, dirname
from ConfigParser import ConfigParser

def get_config_filename():
    """This is just a placeholder for now."""
    return join(dirname(__file__), 'pf_ide.cfg')

def get_default_config():
    c = ConfigParser()
    c.add_section('interface')
    c.set('interface', 'y_pos', '17')
    c.set('interface', 'x_pos', '383')
    c.set('interface', 'height', '779')
    c.set('interface', 'width', '683')
    c.set('interface', 'show_toolbar', 'yes')
    c.add_section('editing')
    c.set('editing', 'indent', '4')
    c.set('editing', 'usetab', 'yes')
    return c

def read_config_from(fname):
    c = get_default_config()
    c.read(fname)
    return c

def read_config():
    fname = get_config_filename()
    return read_config_from(fname)

def write_config_to(c, fname):
    with open(fname, 'w') as f:
        c.write(f)

def write_config(c):
    fname = get_config_filename()
    write_config_to(c, fname)

def write_default_config():
    write_config(get_default_config())
