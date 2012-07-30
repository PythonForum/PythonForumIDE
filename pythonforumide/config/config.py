"""
Created on Mon Jul 16 2012
@author: bunburya, somelauw

Tested on:
    - Linux
"""

import os
import platform

from ConfigParser import ConfigParser

def get_config_filename():
    """
    Finds the location of the config file

    Uses environment variables to find the right location. 
    On unix platforms it follows the xdg_specification.
    """

    system = platform.system()
    if system == "Windows":
        configdir = (os.environ.get("%LOCALAPPDATA%") or
                     os.environ.get("%APPDATA%"))
    else:
        configdir = (os.environ.get("XDG_CONFIG_HOME") or
                     os.path.join(os.environ["HOME"], ".config"))

    return os.path.join(configdir, "pf_ide", "config.cfg")

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
    # Make sure the directory exists
    dirname = os.path.dirname(fname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(fname, 'w') as f:
        c.write(f)

def write_config(c):
    fname = get_config_filename()
    write_config_to(c, fname)

def write_default_config():
    write_config(get_default_config())
