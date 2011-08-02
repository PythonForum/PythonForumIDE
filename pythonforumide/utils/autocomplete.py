"""
@author: bunburya
"""


class CodeCompletion(object):
    """A backend class for code completion.
    This does more than it needs to for auto-complete in wx (which does
    most of the work), but the additional methods will be useful with
    different UI toolkits.
    """
    
    def __init__(self, *modules):
        self._suggestions = set()
        self._cache = set()
        for mod in modules:
            self.add_module(m)
    
    def add_module(self, module):
        """Adds the variable and method names from a module to the pool
        of potential suggestions.
        """
        self._suggestions.update(dir(module))
    
    def add_suggestion(self, *suggest):
        """Takes at least one string as an argument; adds each argument
        to the pool of potential suggestions.
        """
        self._suggestions.update(suggest)
    
    def suggest(self, key):
        """Return a set of possible completions based on the keyword
        provided. Stores the result in a cache so that future calls
        don't unnecessarily repeat searches.
        """
        pool = self._cache or self._suggestions
        suggs = {s for s in pool if s.startswith(key)}
        self._cache = set(suggs)
        return suggs
    
    def cache(self, c):
        self._cache = c
    
    def clear_cache(self):
        self._cache = set()
    
    @property
    def choices(self):
        """Return a set of all possible suggestions."""
        return self._suggestions()
