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
            #Raise a config warning error here?
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
        filename = profile
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

        if not self.config.has_section('ide'):
            self.config.add_section('ide')

        self.file_config = open(filename,'w')

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

    def __init__(self, filepath="", filename="Ide_Config"):

        if not filepath:
            filepath = os.path.dirname(__file__)
        self._filepath = filepath
        self._filename = filename
        self._fullpath = None
        self._data = {}
        self._get_file_fullpath()
        self._get_defaults()

    def _get_file_fullpath(self):

        if has_yaml:
            ext = ".yaml"
        else:
            ext = ".cfg"

        _temp_path = os.path.join(self._filepath, self._filename)
        self._fullpath = ''.join((_temp_path, ext))

        with open(self._fullpath, "a") as _:
            # Opens file as append to ensure safe creation of the file.
            pass

        print ("Config using filepath: %s" % (self._fullpath))

    def _get_defaults(self):

        confile = Config(self._fullpath)
        self._data["indent"] = confile["indent"] or 4
        self._data["usetab"] = confile["usetab"] or False
        self._data["MainFrame.Height"] = confile["MainFrame.Height"] or 600
        self._data["MainFrame.Width"] = confile["MainFrame.Width"] or 600
        confile.file_config.close()

    def __setitem__(self, key, value):

        self._data[key] = value

    def __getitem__(self, key):

        return self._data[key]

    def update_configfile(self):

        confile = Config(self._fullpath)
        for key, value in self._data.iteritems():
            confile[key] = value

        confile.save()
        confile.file_config.close()

if __name__ == '__main__':
    ide_config = IdeConfig(config_style=Config)
    print(ide_config["indent"])
    ide_config.update_configfile()

