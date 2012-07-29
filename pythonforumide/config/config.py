# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 21:01:15 2011
@author: Jakob, Somelauw
@reviewer: David, Somelauw
"""

from __future__ import print_function
import os.path
import ConfigParser #Ugly config file :(

try:
    import yaml #Pretty config file :D
    has_yaml = True
except ImportError:
    has_yaml = False


def file_config(profile):
    """
    Returns the name of the configuration file.
    It does not guarantee existence.
    Side effect:
    Tells the user if can't load the configuration file if it is not supported.
    """

    # We will need some fuzzy logic to accomplish this
    profile, ext = os.path.splitext(profile)
    yaml_exists = os.path.exists(''.join((profile, ".yaml")))
    cfg_exists = os.path.exists(''.join((profile, ".cfg")))

    # If no extension could be found,
    # guess what configuration type is likely to be preferred.
    if not ext:
        if yaml_exists or (has_yaml and not cfg_exists):
            ext = ".yaml"
        else:
            ext = ".cfg"

    # We can't load yaml if it doesn't exist
    if ext == ".yaml" and not has_yaml:
        print("yaml configuration could not be loaded",
              "because python-yaml is not installed.")
        ext = ".cfg"

    return ''.join((profile, ext))

def load_config(configfile):
    """Loads a config file"""

    profile, ext = os.path.splitext(configfile)
    if ext == ".yaml":
        return _BeautifulConfig(profile)
    else:
        return _UglyConfig(profile)

class _BeautifulConfig(object):
    """This is the config object if we can import yaml."""

    def __init__(self, profile):
        """
        Load the yaml config from file, 
        if this fails write an empty new one.
        """

        filename = ''.join((profile, ".yaml"))

        try:
            self.config = yaml.load(open(filename))
        except IOError:
            self.config = None

        if self.config is None:
            self.config = {}

        self.file_config = open(filename, 'w')

    def __setitem__(self, option, value):
        """Set an option to a value inside the config, does not write."""

        self.config[option] = value

    def __getitem__(self, option):
        """
        Gets the option from the config.
        Return None, if the option is not there
        """

        return self.config.get(option, None)

    def set_default(self, option, value):

        self.config.set_default(option, value)

    def save(self):
        """Writes the config as yaml out to the config file."""

        yaml.dump(self.config, self.file_config)

class _UglyConfig(object):
    """
    This is the config object created if we can't use YAML and have to
    rely on ConfigParser.
    """

    def __init__(self, profile):

        filename = ''.join((profile, ".cfg"))
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

        if not self.config.has_section('ide'):
            self.config.add_section('ide')

        self.file_config = open(filename, 'w')

    def __setitem__(self, option, value):
        """Set the value to the option inside the default section."""

        self.config.set('ide', option, value)

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

        self.config.write(self.file_config)


#If we have yaml then the ConfigObject will point to the cooler config object
if has_yaml:
    Config = _BeautifulConfig
# Otherwise we point to the ugly one
else:
    Config = _UglyConfig
#This way the importers use the config the same way, same api but under the 
#hood they are different.


class IdeConfig(object):
    """ Store's config values in a dict, and to file
        converts to and from python type"""
    def __init__(self, filepath="", filename="Ide_Config"):
        """ Initialize"""
        if not filepath:
            filepath = os.path.dirname(__file__)
        self._fullpath = None
        self._data = {}
        self._get_file_fullpath(filepath, filename)
        self.set_defaults()
        self.read_from_config_file()

    def _get_file_fullpath(self, filepath, filename):
        """ Works out which config file type and creates if not exists"""
        _temp_path = os.path.join(filepath, filename)
        self._fullpath= file_config(_temp_path)
        with open(self._fullpath, "a") as _:
            # Opens file as append to ensure safe creation of the file.
            pass
        print ("Config using filepath: %s" % (self._fullpath))

    def read_from_config_file(self):
        """ reads the config file and over writes defaults if theres as entry"""
        """ if theres a type flag it converts to the python type"""
        confile = load_config(self._fullpath)
        for key, value in self._data.iteritems():
            config_value = confile[key]
            if config_value:
                self._data[key] = self.convert_to_pytype(config_value)
        confile.file_config.close()
        
    def convert_to_pytype(self, config_value):
        """ Converts the file stored string to a few python types"""
        try:
            get_type, get_value = config_value.split(">")
            if get_type == "int":
                return int(get_value)
            elif get_type == "float":
                return float(get_value)
            elif get_type == "bool" and get_value == "True":
                return True
            elif get_type == "bool" and get_value == "False":
                return False
            else:
                return str(get_value)
        except Exception, exception:
            print ("Exception when convert_to_pytype", exception.message)
            return str(config_value)
        
    def update_configfile(self):
        """ Writes back the current values to the config file"""
        confile = load_config(self._fullpath)
        for key, value in self._data.iteritems():
            confile[key] = self.convert_pytype_to_str(value)
        confile.save()
        confile.file_config.close()
        
    def convert_pytype_to_str(self, value):
        """ Adds a pytype flag to the entry"""
        get_type = str(type(value))
        get_type = get_type[:-2].split("'")[1]
        if get_type == "int":
            return "int>%s" % (value)
        elif get_type == "float":
                return "float>%s" % (value)
        elif get_type == "bool" and value == True:
            return "bool>%s" % (value)
        elif get_type == "bool" and value == False:
            return "bool>%s" % (value)
        else:
            return "str>%s" % (value)
        
    def __setitem__(self, key, value):
        """ Set the current config value"""
        self._data[key] = value

    def __getitem__(self, key):
        """ Get the current config value"""
        return self._data[key]

        
    def set_defaults(self):
        """ Sets default values"""
        self._data["indent"] = 4
        self._data["usetab"] = 0
        self._data["MainFrame.Height"] = 600
        self._data["MainFrame.Width"] = 600
        self._data["MainFrame.XPos"]= 0
        self._data["MainFrame.YPos"]= 0
        self._data["MainMenu.View.Toolbar.Show"]= True


if __name__ == '__main__':
    ide_config = IdeConfig()

    value = (ide_config["MainFrame.Width"])
    print (value)
    ide_config.update_configfile()


