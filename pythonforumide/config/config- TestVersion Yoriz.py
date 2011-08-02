# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 21:01:15 2011
@author: Jakob, Somelauw
@reviewer: David, SomeLauw
"""

from __future__ import print_function
import os.path

try:
    import yaml #Pretty config file :D
    has_yaml = True
except ImportError:
    import ConfigParser #Ugly config file :(
    has_yaml = False

def config_file(profile):
    """Returns the name of the configuration file. It does not guarantee existence.
    Side effect: Tells the user if can't load the configuration file if it is not supported.
    """

    # We will need some fuzzy logic to accomplish this
    (profile, ext) = os.path.splitext(profile)
    yaml_exists = os.path.exists(profile + ".yaml")
    cfg_exists = os.path.exists(profile + ".cfg")

    # If no extension could be found, guess what configuration type is likely to be preferred
    if not ext:
        if yaml_exists or (has_yaml and not cfg_exists):
            ext = ".yaml"
        else:
            ext = ".cfg"

    # We can't load yaml if it doesn't exist
    if ext == ".yaml" and not has_yaml:
        print("yaml configuration could not be loaded because python-yaml is not installed.")
        ext = ".cfg"

    return profile + ext

def load_config(configfile):
    """Loads a config file"""
    (profile, ext) = os.path.splitext(configfile)
    if ext == ".yaml":
        return _BeautifulConfig(profile)
    else:
        return _UglyConfig(profile)

class _BeautifulConfig(object):
    """This is the config object if we can import yaml."""
    def __init__(self, profile):
        """Load the yaml config from file,
        if this fails write an empty new one."""
        filename = profile + ".yaml"

        try:
            self.config = yaml.load(open(filename))
        except IOError:
            #Raise a config warning error here?
            self.config = {}

        self.file = open(filename,'w')

    def __setitem__(self, option, value):
        """Set an option to a value inside the config, does not write."""
        self.config[option] = value

    def __getitem__(self, option):
        """Gets the option from the config, if the option is not there
        returns None"""
        return self.config.get(option, None)

    def set_default(self, option, value):
        self.config.set_default(option, value)

    def save(self):
        """Writes the config as yaml out to the config file."""
        yaml.dump(self.config, self.file)

class _UglyConfig(object):
    """This is the config object created if we can't use YAML and have to
    rely on ConfigParser."""
    def __init__(self, profile):
        filename = profile + ".cfg"
        filename= profile

        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read(filename)
        except IOError: # <<< Exception will never be trown (RTFM, noob!)
            pass #Raise a config warning error here?
            self.config.add_section('ide')

        if not self.config.has_section('ide'):
            self.config.add_section('ide')

        self.file = open(filename,'w')

    def __setitem__(self, option, value):
        """Set the value to the option inside the default section."""
        self.config.set('ide',option, value)

    def __getitem__(self, option):
        """Return the values to the option given, or return None"""
        try:
            return self.config.get('ide', option)
        except ConfigParser.NoOptionError:
            return None

    def set_default(self, option, value):
        if not self.config.has_option('ide', option):
            self[option] = value

    def save(self):
        """Write config to file."""
        self.config.write(self.file)


#If we have yaml then the ConfigObject will point to the cooler config object
if has_yaml:
    Config = _BeautifulConfig
else: # Otherwise we point to the ugly one
    Config = _UglyConfig
#This way the importers use the config the same way, same api but under the
#hood they are different.

class Ide_config(object):
    def __init__(self, filepath= "", filename= "Ide_Config"):
        if not filepath:
            filepath= os.path.dirname(__file__)
        self._filepath = filepath
        self._filename = filename
        self._fullpath= None
        self._data= {}
        self._get_file_fullpath()
        self.set_defaults()
        self.read_from_config_file()

    def _get_file_fullpath(self):
        """ Works out which config file type"""
        if has_yaml:
            ext= ".yaml"
        else:
            ext= ".cfg"
        self._fullpath= os.path.join(self._filepath, self._filename)+ext
        if not os.path.exists(self._fullpath):
             a= file(self._fullpath, "w")
             a.close()
        print ("Config useing filepath: %s" % (self._fullpath))

    def read_from_config_file(self):
        """ reads the config file and over writes defaults if theres as entry"""
        """ if theres a type flag it converts to the python type"""
        confile= Config(self._fullpath)
        for key, value in self._data.iteritems():
            config_value= confile[key]
            if config_value:
                try:
                    this_type, this_value= config_value.split("<")
                    print (this_type, this_value[:-1])
                    print (__builtins__[this_type](this_value[:-1]))
                    self._data[key]= __builtins__[this_type](this_value[:-1])
                except Exception, exception:
                    self._data[key]= config_value
        confile.file.close()

    def __setitem__(self, key, value):
        """ Sets the in memory value"""
        self._data[key]= value

    def __getitem__(self, key):
        """ Gets the in memory value"""
        return self._data[key]

    def update_configfile(self):
        """ Writes back the current values to the config file"""
        """ Adds a type flag to the entry"""
        confile= Config(self._fullpath)
        for key, value in self._data.iteritems():
            this_type= str(type(value))
            this_type= this_type[:-2].split("'")[1]
            if this_type not in ("int", "float", "bool"):
                this_type= "str"
            value= "%s<%s>" % (this_type, str(value))
            confile[key]= value
        confile.save()
        confile.file.close()

    def set_defaults(self):
        """ Sets default values"""
        self._data["indent"]= 4
        self._data["usetab"]= 0
        self._data["MainFrame.Height"] = 600
        self._data["MainFrame.Width"] = 600
        self._data["Test.bool"]= True
        self._data["Test.int"]= 25
        self._data["Test.float"]= 0.75
        self._data["Test.list"]= ["1", "2", "3"]
        self._data["Test.tuple"]= ("1", "2", "3")

""" This could be usefull not to have to worry about converting value to string
     to save them and then changing back toint, bool ect to use them"""

if __name__ == '__main__':
    ide_config= Ide_config()
    print (ide_config["indent"])
    ide_config["MainFrame.Height"]= 600
    print (type(ide_config["Test.bool"]))
    ide_config["indent"]= 4
    ide_config.update_configfile()
    ide_config= Ide_config()
    print (ide_config["Test.int"]*ide_config["Test.float"])
    print (type(ide_config["Test.list"]))
    print (type(ide_config["Test.tuple"]))
    print (ide_config["Test.list"])
    ide_config.update_configfile()


