"""
@author: bunburya
"""

# TODO:
# - Find some way of inserting a hook in the class to be called when
#   AutoComplete is actually acted on.

class NoSuchNamespaceError(Exception): pass

# Nah leave them here.
keywords = set(['and ', 'elif ', 'is ', 'global ', 'pass', 'if ',
    'from ', 'raise ', 'for ', 'except ', 'finally', 'print ',
    'import ', 'return ', 'exec ', 'else', 'break', 'not ', 'class ',
    'assert ', 'in ', 'yield ', 'try', 'while ', 'continue', 'del ',
    'or ', 'def ', 'lambda '])
builtins = set(__builtins__.keys())

class CodeCompletion(object):
    """A backend class for code completion."""
    
    valid_ch = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    
    def __init__(self, *modules):
        self._suggestions = set()
        self._namespaces = {'': set()} # empty string represents global namespace
        self._current_ns = ''
        self._cache = set()
        self._key = []
        self._context_ns = ['']
        for mod in modules:
            self.add_module(mod)
    
    def add_builtins(self):
        self._namespaces['__builtins__'] = builtins
        self._namespaces[''].update(builtins)
    
    def add_keywords(self):
        self._namespaces[''].update(keywords)
    
    def add_module(self, module):
        """Adds the variable and method names from a module to the pool
        of potential suggestions.
        """
        print 'adding module %s' % module
        self._namespaces[module.__name__] = dir(module)
    
    def add_suggestions(self, suggest, ns=''):
        """Takes at least one string as an argument; adds each argument
        to the pool of potential suggestions.
        """
        if ns in self._namespaces:
            self._namespaces[ns].update(suggest)
        else:
            self._namespaces[ns] = suggest
    
    def add_suggestion(self, suggest, ns=''):
        if ns in self._namespaces:
            self._namespaces[ns].add(suggest)
        else:
            self._namespaces[ns] = set((suggest,))
    
    def suggest(self, key=None):
        """Return a set of possible completions based on the keyword
        provided. Stores the result in a cache so that future calls
        don't unnecessarily repeat searches.
        """
        if key is None:
            key = self.key
        if not key and len(self._context_ns) < 2:
            return set()
        pool = self._cache or self._namespaces[self._current_ns]
        suggs = set(s for s in pool if s.startswith(key))
        self._cache = set(suggs)
        return suggs
    
    def handle_point(self):
        """Called when the '.' char is fed to update_key."""
        key = self.key
        try:
            self.switch_ns(key)
        except NoSuchNamespaceError:
            return
        self._context_ns.append(key)
        print self._context_ns
        self.clear_key()
    
    def back_to_global(self):
        self._context_ns = ['']
        self.switch_ns('')
        
    def update_key(self, char):
        if char == '.':
            self.handle_point()
        elif not char in self.valid_ch:
            self.clear()
        else:
            self._key.append(char)
    
    def back(self):
        try:
            char = self._key.pop()
        except IndexError:
            if len(self._context_ns) > 1:
                self.key = self._context_ns.pop()
            else:
                self.clear_key()
            self.switch_ns(self._context_ns[-1])
    
    def cache(self, c):
        self._cache = c
    
    def clear_cache(self):
        self._cache = set()
    
    def clear_key(self):
        self._key = []
    
    def clear(self):
        self._cache = set()
        self._key = []
    
    def switch_ns(self, new):
        if new in self._namespaces:
            self._current_ns = new
            self.clear_cache()
        else:
            raise NoSuchNamespaceError(new)
    
    def parse_imports(x):
        """Parses an import in both formats. Returns the package and module
        Always returns in this format. (package, list_of_modules, as_mask)
        Some of those results can be None"""
        line = x.split(' ')
        if line[0] == 'import':
            if 'as' in line:
                las = line.index('as')
                return (None, line[1:las], line[las:])
            else:
                return (None, [item for item in line[1].split(',')], None)

        elif line[0] == 'from':
            if 'as' in line:
                #holy shit they used from x import y as z !
                pass
            else:
                if len(line[3].split(',')) > 1:
                    return (line[1], [item for item in line[3].split(',')], None)
                
    
    def on_complete(self):
        """This should be called when the user completes using the autocomp."""
        self.back_to_global()
    
    @property
    def choices(self):
        """Return a set of all possible suggestions."""
        return self._suggestions()
    
    @property
    def key(self):
        return ''.join(self._key)
    
    #@key.setter
    def key(self, new):
        self._key = list(new)
    
    @property
    def len_entered(self):
        return len(self._key)
