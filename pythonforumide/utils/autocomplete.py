"""
@author: bunburya
"""

class NoSuchNamespaceError(Exception): pass

# maybe move these to a separate file eventually
keywords = set(['and ', 'elif ', 'is ', 'global ', 'pass', 'if ',
    'from ', 'raise ', 'for ', 'except ', 'finally', 'print ',
    'import ', 'return ', 'exec ', 'else', 'break', 'not ', 'class ',
    'assert ', 'in ', 'yield ', 'try', 'while ', 'continue', 'del ',
    'or ', 'def ', 'lambda '])
builtins = set(__builtins__.keys())

class CodeCompletion(object):
    """A backend class for code completion.
    """
    
    valid_ch = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    
    def __init__(self, *modules):
        self._suggestions = set()
        self._namespaces = {'': set()} # empty string represents global namespace
        self._current_ns = ''
        self._cache = set()
        self._key = []
        self._context_ns = []
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
            key = ''.join(self._key)
        if not key:
            return set()
        pool = self._cache or self._namespaces[self._current_ns]
        suggs = set(s for s in pool if s.startswith(key))
        self._cache = set(suggs)
        return suggs
        
    def update_key(self, char):
        if char == '.':
            self.switch_ns(self.key)
            self._context_ns.append(self.key)
            print self._context_ns
            self.clear_key()
        elif not char in self.valid_ch:
            self.clear()
        else:
            self._key.append(char)
    
    def back(self):
        try:
            char = self._key.pop()
        except IndexError:
            if self._context_ns:
                self.key = self._context_ns.pop()
    
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
    
    @property
    def choices(self):
        """Return a set of all possible suggestions."""
        return self._suggestions()
    
    @property
    def key(self):
        return ''.join(self._key)
    
    @key.setter
    def key(self, new):
        self._key = list(new)
    
    @property
    def len_entered(self):
        return len(self._key)
